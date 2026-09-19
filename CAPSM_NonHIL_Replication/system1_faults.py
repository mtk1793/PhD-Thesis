from __future__ import annotations

import json
import time
from dataclasses import dataclass

import numpy as np
import torch
from sklearn.metrics import accuracy_score, confusion_matrix
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

from common import load_real_opsd, seed_everything, write_json

CLASSES = [
    "normal",
    "low_impedance",
    "high_impedance",
    "cyber_fdi",
    "voltage_sag",
    "frequency_deviation",
    "load_transient",
    "load_shedding",
]
FAULT_CLASSES = CLASSES[1:]


@dataclass
class FaultConfig:
    seq_len: int = 24
    sample_ms: float = 2.0
    onset: int = 8
    train_per_class: int = 260
    val_per_class: int = 70
    test_per_class: int = 110
    epochs: int = 18
    batch_size: int = 128


def _base_from_row(row, seq_len: int, rng: np.random.Generator) -> np.ndarray:
    # PMU-like channels grounded in a real hourly OPSD operating point.
    load = float(row.load_actual_mw)
    renew = float(row.renewable_mw)
    net = load - renew
    load_ref = 55000.0
    net_ref = 45000.0
    load_pu = np.clip(load / load_ref, 0.45, 1.45)
    renew_share = np.clip(renew / max(load, 1.0), 0.0, 1.2)
    net_pu = np.clip(net / net_ref, 0.2, 1.6)
    ferr = float(row.forecast_error_mw) / load_ref

    t = np.arange(seq_len, dtype=np.float32)
    # Slow pre-event micro-variation; this is not a fabricated daily profile,
    # only a millisecond measurement texture around the real operating point.
    phase = rng.uniform(0, 2 * np.pi)
    vm = 1.018 - 0.060 * (net_pu - 1.0) + 0.003 * np.sin(0.45 * t + phase)
    current = 0.82 * load_pu + 0.025 * np.sin(0.35 * t + phase / 2)
    freq = 60.0 - 0.04 * ferr + 0.008 * np.sin(0.2 * t + phase)
    rocof = np.gradient(freq) / 0.002
    load_ch = np.full(seq_len, load_pu)
    renew_ch = np.full(seq_len, renew_share)

    x = np.column_stack([vm, current, freq, rocof, load_ch, renew_ch]).astype(np.float32)
    x += rng.normal(0.0, [0.0030, 0.010, 0.008, 0.35, 0.004, 0.004], x.shape).astype(np.float32)
    return x


def _inject_event(x: np.ndarray, cls: int, cfg: FaultConfig, rng: np.random.Generator) -> np.ndarray:
    y = x.copy()
    o = cfg.onset
    n = len(y) - o
    if cls == 0:
        return y
    u = np.arange(n, dtype=np.float32)
    # Severity randomisation prevents a trivial template-matching classifier.
    s = rng.uniform(0.82, 1.18)
    if cls == 1:  # low impedance fault: fast deep sag + high current
        rise = 1.0 - np.exp(-u / 1.2)
        y[o:, 0] -= s * 0.255 * rise
        y[o:, 1] += s * 0.62 * rise
        y[o:, 2] -= s * 0.13 * (1.0 - np.exp(-u / 4.0))
        y[o:, 3] -= s * 6.0 * np.exp(-u / 4.5)
    elif cls == 2:  # high impedance: weak, slowly developing signature
        rise = 1.0 - np.exp(-u / 5.0)
        y[o:, 0] -= s * 0.058 * rise
        y[o:, 1] += s * 0.105 * rise
        y[o:, 3] += s * 1.2 * np.sin(1.5 * u) * rise
    elif cls == 3:  # cyber FDI: measurement-only offset, no current response
        step = (u >= rng.integers(1, 4)).astype(np.float32)
        y[o:, 0] += s * rng.choice([-1, 1]) * 0.085 * step
        y[o:, 2] += s * rng.choice([-1, 1]) * 0.22 * step
    elif cls == 4:  # voltage sag
        rise = 1.0 - np.exp(-u / 2.4)
        y[o:, 0] -= s * 0.135 * rise
        y[o:, 1] += s * 0.13 * rise
    elif cls == 5:  # frequency deviation
        rise = 1.0 - np.exp(-u / 3.0)
        y[o:, 2] -= s * 0.70 * rise
        y[o:, 3] -= s * 3.0 * np.exp(-u / 3.2)
        y[o:, 0] -= s * 0.022 * rise
    elif cls == 6:  # load transient
        impulse = np.exp(-u / 4.0)
        step = 1.0 - np.exp(-u / 2.0)
        y[o:, 1] += s * (0.32 * step + 0.12 * impulse)
        y[o:, 0] -= s * 0.072 * step
        y[o:, 2] -= s * 0.18 * impulse
    elif cls == 7:  # load shedding
        step = 1.0 - np.exp(-u / 2.0)
        y[o:, 1] -= s * 0.30 * step
        y[o:, 0] += s * 0.055 * step
        y[o:, 2] += s * 0.38 * step
        y[o:, 3] += s * 2.0 * np.exp(-u / 3.0)

    # Event-period sensor noise and location variation.
    y[o:] += rng.normal(0.0, [0.004, 0.012, 0.010, 0.45, 0.003, 0.003], y[o:].shape).astype(np.float32)
    return y


def make_dataset(df, days: list[int], n_per_class: int, cfg: FaultConfig, seed: int):
    rng = np.random.default_rng(seed)
    day = df["timestamp"].dt.day.to_numpy()
    idx = np.flatnonzero(np.isin(day, days))
    if len(idx) == 0:
        idx = np.arange(len(df))
    X, Y = [], []
    for cls in range(len(CLASSES)):
        for _ in range(n_per_class):
            i = int(rng.choice(idx))
            x = _base_from_row(df.iloc[i], cfg.seq_len, rng)
            x = _inject_event(x, cls, cfg, rng)
            X.append(x)
            Y.append(cls)
    order = rng.permutation(len(Y))
    return np.stack(X)[order].astype(np.float32), np.asarray(Y, dtype=np.int64)[order]


class FaultCNNLSTM(nn.Module):
    def __init__(self, n_features: int = 6, n_classes: int = 8):
        super().__init__()
        self.conv = nn.Sequential(
            nn.Conv1d(n_features, 32, 3, padding=1), nn.ReLU(),
            nn.Conv1d(32, 48, 3, padding=1), nn.ReLU(),
        )
        self.lstm = nn.LSTM(48, 64, batch_first=True)
        self.attn = nn.Sequential(nn.Linear(64, 32), nn.Tanh(), nn.Linear(32, 1))
        self.head = nn.Sequential(nn.Linear(64, 48), nn.ReLU(), nn.Dropout(0.08), nn.Linear(48, n_classes))

    def forward(self, x):
        z = self.conv(x.transpose(1, 2)).transpose(1, 2)
        h, _ = self.lstm(z)
        w = torch.softmax(self.attn(h), dim=1)
        c = (w * h).sum(1)
        return self.head(c)


def standardize(train, *others):
    mu = train.mean(axis=(0, 1), keepdims=True)
    sd = train.std(axis=(0, 1), keepdims=True) + 1e-6
    return (train - mu) / sd, [((x - mu) / sd).astype(np.float32) for x in others], mu, sd


def train_model(Xtr, ytr, Xv, yv, cfg: FaultConfig):
    model = FaultCNNLSTM()
    opt = torch.optim.AdamW(model.parameters(), lr=2e-3, weight_decay=1e-4)
    crit = nn.CrossEntropyLoss(label_smoothing=0.015)
    loader = DataLoader(TensorDataset(torch.from_numpy(Xtr), torch.from_numpy(ytr)),
                        batch_size=cfg.batch_size, shuffle=True)
    best_state, best_acc = None, -1.0
    history = []
    for ep in range(cfg.epochs):
        model.train()
        loss_sum = 0.0
        for xb, yb in loader:
            opt.zero_grad(set_to_none=True)
            logits = model(xb)
            loss = crit(logits, yb)
            loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            opt.step()
            loss_sum += loss.item() * len(xb)
        model.eval()
        with torch.no_grad():
            pred = model(torch.from_numpy(Xv)).argmax(1).numpy()
        acc = accuracy_score(yv, pred)
        history.append({"epoch": ep + 1, "loss": loss_sum / len(ytr), "val_accuracy": acc})
        if acc > best_acc:
            best_acc = acc
            best_state = {k: v.detach().clone() for k, v in model.state_dict().items()}
    model.load_state_dict(best_state)
    return model, history


def progressive_latency(model, Xraw, y, mu, sd, cfg: FaultConfig, conf_threshold=0.86):
    model.eval()
    latencies = {name: [] for name in FAULT_CLASSES}
    with torch.no_grad():
        fault_idx = np.flatnonzero(y > 0)
        # Cap progressive evaluation to keep the replication run compact.
        for ii in fault_idx[: min(len(fault_idx), 420)]:
            true_cls = int(y[ii])
            raw = Xraw[ii]
            detected = None
            for k in range(cfg.onset + 1, cfg.seq_len + 1):
                partial = raw.copy()
                if k < cfg.seq_len:
                    partial[k:] = partial[k - 1]
                z = ((partial[None] - mu) / sd).astype(np.float32)
                p = torch.softmax(model(torch.from_numpy(z)), dim=1)[0]
                cls = int(torch.argmax(p))
                if cls == true_cls and float(p[true_cls]) >= conf_threshold:
                    detected = (k - cfg.onset) * cfg.sample_ms
                    break
            if detected is None:
                detected = (cfg.seq_len - cfg.onset) * cfg.sample_ms
            latencies[CLASSES[true_cls]].append(float(detected))
    return {k: float(np.mean(v)) if v else float("nan") for k, v in latencies.items()}


def run(data_path=None, fast: bool = False):
    seed_everything()
    cfg = FaultConfig()
    if fast:
        cfg.train_per_class = 100
        cfg.val_per_class = 35
        cfg.test_per_class = 45
        cfg.epochs = 8
    df = load_real_opsd(data_path)
    # Chronological separation by real OPSD dates, no operating-point leakage.
    unique_days = sorted(df.timestamp.dt.day.unique().tolist())
    if len(unique_days) >= 7:
        train_days = unique_days[:5]
        val_days = [unique_days[5]]
        test_days = unique_days[6:]
    else:
        train_days, val_days, test_days = unique_days[: max(1, len(unique_days)-2)], unique_days[-2:-1], unique_days[-1:]
    Xtr_raw, ytr = make_dataset(df, train_days, cfg.train_per_class, cfg, 1)
    Xv_raw, yv = make_dataset(df, val_days, cfg.val_per_class, cfg, 2)
    Xte_raw, yte = make_dataset(df, test_days, cfg.test_per_class, cfg, 3)
    Xtr, [Xv, Xte], mu, sd = standardize(Xtr_raw, Xv_raw, Xte_raw)

    t0 = time.perf_counter()
    model, history = train_model(Xtr, ytr, Xv, yv, cfg)
    train_s = time.perf_counter() - t0
    model.eval()
    with torch.no_grad():
        logits = model(torch.from_numpy(Xte))
        pred = logits.argmax(1).numpy()
    overall = accuracy_score(yte, pred)
    cm = confusion_matrix(yte, pred, labels=np.arange(len(CLASSES)))
    per_class = {}
    for i, name in enumerate(CLASSES):
        den = cm[i].sum()
        per_class[name] = float(cm[i, i] / den) if den else float("nan")

    lat = progressive_latency(model, Xte_raw, yte, mu, sd, cfg)
    mean_fault_acc = float(np.mean([per_class[x] for x in FAULT_CLASSES]))
    mean_lat = float(np.mean(list(lat.values())))
    params = int(sum(p.numel() for p in model.parameters()))

    payload = {
        "data_source": df.attrs.get("source_path", ""),
        "full_opsd": bool(df.attrs.get("is_full_opsd", False)),
        "method": "real OPSD operating points + reproducible injected PMU fault signatures",
        "classes": CLASSES,
        "accuracy_all_8_classes": overall,
        "mean_fault_accuracy_7_classes": mean_fault_acc,
        "per_class_accuracy": per_class,
        "mean_detection_latency_ms": mean_lat,
        "per_fault_latency_ms": lat,
        "parameters": params,
        "train_seconds": train_s,
        "split_days": {"train": train_days, "validation": val_days, "test": test_days},
        "target_reference_pdf": {"mean_fault_accuracy": 0.9678, "mean_detection_latency_ms": 8.6},
        "history": history,
    }
    write_json("system1_faults.json", payload)
    torch.save({"state_dict": model.state_dict(), "mu": mu, "sd": sd, "classes": CLASSES},
               str(__import__('pathlib').Path(__file__).resolve().parent / "results/system1_faults.pt"))
    return payload


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, default=float))

"""Phase 4 (v2) — System 1 training and evaluation, leakage-free.

Rebuilt per master plan §7 (Phase D), §8 (Phase E), §15 (Phase L):

  Training:   RuleBasedVoltage demonstrations sampled from 2015-2017 only
  Validation: chronological windows inside the demonstration corpus +
              imitation metrics on 2018
  Test:       January 2019 (default) — strictly unseen during training

Outputs are versioned to ``results/phase4_v2/`` (historical results in
``results/phase4/`` are preserved untouched).

Usage:
  python scripts/phase4_system1.py [--epochs 100] [--seeds 42 43 44]
      [--episodes-per-year 8] [--test-start 2019-01-01 --test-end 2019-01-31]
      [--full-year-test]
"""

import argparse
import json
import time
from pathlib import Path

import numpy as np
import pandas as pd

from capsm.agents.baselines import (
    NoControl, PIDVoltage, RuleBasedVoltage, run_controller,
)
from capsm.agents.collector import collect_trajectory
from capsm.agents.system1 import StateEncoder, System1Controller
from capsm.agents.trainer import (
    TRAIN_YEARS, VAL_YEAR, TEST_YEARS,
    assert_no_test_leakage, build_window_dataset, collect_demos,
    sample_training_episodes, save_model, train_behavior_cloning,
)
from capsm.data.opsd import load_opsd
from capsm.grid.environment import QSTSEnvironment

RESULTS = Path("results/phase4_v2")
RESULTS.mkdir(parents=True, exist_ok=True)


def parse_args():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--epochs", type=int, default=100)
    p.add_argument("--seeds", type=int, nargs="+", default=[42, 43, 44])
    p.add_argument("--episodes-per-year", type=int, default=8)
    p.add_argument("--steps-per-episode", type=int, default=168)
    p.add_argument("--seq-len", type=int, default=12)
    p.add_argument("--test-start", type=str, default="2019-01-01")
    p.add_argument("--test-end", type=str, default="2019-01-31")
    p.add_argument("--full-year-test", action="store_true",
                   help="evaluate on the full 2019 held-out year")
    return p.parse_args()


def action_error_metrics(model, env, encoder, start: str, n_steps: int, seq_len: int) -> dict:
    """Per-output imitation MAE/RMSE against RuleBasedVoltage on held-out data."""
    rule = RuleBasedVoltage()
    obs = env.reset(start=start)
    states, actions = [], []
    for _ in range(n_steps):
        states.append(encoder.encode(obs))
        actions.append(np.asarray(_flatten(rule.act(obs, env)), dtype=np.float32))
        obs = env.step(rule.act(obs, env))
    states = np.stack(states)
    actions = np.stack(actions)
    # windows consistent with the window_reset convention
    X = np.stack([states[i - seq_len:i] for i in range(seq_len, len(states))])
    Y = actions[seq_len - 1:]
    import torch
    with torch.no_grad():
        pred, _ = model(torch.tensor(X, dtype=torch.float32), None)
    pred = pred.numpy()
    err = pred - Y[:, :pred.shape[1]]
    per_dim_mae = np.abs(err).mean(axis=0).round(5).tolist()
    return {
        "mae_mean": float(np.abs(err).mean()),
        "rmse_mean": float(np.sqrt((err ** 2).mean())),
        "mae_per_dim": per_dim_mae,
        "n_windows": int(len(X)),
    }


def _flatten(ctrl: dict) -> np.ndarray:
    facts = ctrl.get("facts", {})
    upfc = facts.get("UPFC_26", [0.0, 0.0])
    ev = ctrl.get("ev", {})
    return np.array([
        float(facts.get("SVC_14", 0.0)),
        float(facts.get("STATCOM_39", 0.0)),
        float(facts.get("TCSC_16_17", 0.0)),
        float(upfc[0]) if isinstance(upfc, (list, tuple)) else float(upfc),
        float(upfc[1]) if isinstance(upfc, (list, tuple)) and len(upfc) > 1 else 0.0,
        0.0,  # reserved UPFC series-Q — never a target
        float(ev.get("3", 0.0)), float(ev.get("8", 0.0)), float(ev.get("15", 0.0)),
    ], dtype=np.float32)


def main():
    args = parse_args()
    print("[phase4-v2] chronological split: "
          f"train={TRAIN_YEARS} val={VAL_YEAR} test={TEST_YEARS}")

    # ── load data by split (no test-year state reaches training) ─────
    print("[phase4-v2] loading OPSD profiles (train years) ...")
    train_profiles = load_opsd(start="2015-01-01", end="2017-12-31")
    val_profiles = load_opsd(start="2018-01-01", end="2018-12-31")
    test_start = "2019-01-01" if args.full_year_test else args.test_start
    test_end = "2019-12-31" if args.full_year_test else args.test_end
    test_profiles = load_opsd(start=test_start, end=test_end)

    # ── demonstrations from TRAINING years only ──────────────────────
    episodes = sample_training_episodes(
        train_profiles.index, years=TRAIN_YEARS,
        episodes_per_year=args.episodes_per_year,
        steps_per_episode=args.steps_per_episode, seed=42,
    )
    assert_no_test_leakage(episodes, TEST_YEARS)
    print(f"[phase4-v2] {len(episodes)} demonstration episodes sampled "
          f"from {TRAIN_YEARS} (leakage check passed)")
    trajectories, encoder = collect_demos("case39", train_profiles, episodes)
    dataset = build_window_dataset(trajectories, seq_len=args.seq_len)
    print(f"[phase4-v2] window dataset: train={dataset['X_train'].shape} "
          f"val={dataset['X_val'].shape}")

    # ── 2018 imitation metrics (held-out year for tuning) ────────────
    val_env = QSTSEnvironment("case39", val_profiles)

    # ── multi-seed training ──────────────────────────────────────────
    per_seed = []
    for seed in args.seeds:
        print(f"[phase4-v2] training seed {seed} ...")
        t0 = time.time()
        model, history = train_behavior_cloning(
            dataset, encoder.n_features, 9, seq_len=args.seq_len,
            epochs=args.epochs, batch_size=128, lr=1e-3, seed=seed,
            verbose=False,
        )
        train_time = time.time() - t0
        imitation_2018 = action_error_metrics(
            model, val_env, encoder, start="2018-01-01", n_steps=24 * 28,
            seq_len=args.seq_len,
        )
        save_model(model, RESULTS / f"system1_cnnlstm_seed{seed}.pt")

        # ── control performance on the UNSEEN test window ────────────
        env_t = QSTSEnvironment("case39", test_profiles)
        ctrl = System1Controller(model, encoder, temporal_mode="window_reset")
        t0 = time.time()
        df_s1 = run_controller(env_t, ctrl, start=test_start)
        s1_latency_ms = (time.time() - t0) / max(len(df_s1), 1) * 1000.0

        per_seed.append({
            "seed": seed,
            "train_loss_final": history["train_loss"][-1],
            "val_loss_final": history["val_loss"][-1],
            "val_mae": history["val_mae"],
            "val_rmse": history["val_rmse"],
            "trainable_parameters": history["trainable_parameters"],
            "imitation_2018": imitation_2018,
            "control_test": _summarise(df_s1),
            "s1_latency_ms_per_step": round(s1_latency_ms, 3),
            "train_time_s": round(train_time, 1),
        })
        c = per_seed[-1]["control_test"]
        print(f"[phase4-v2] seed {seed}: test dev={c['mean_voltage_dev_pu']} "
              f"viol={c['voltage_violation_hours']} h "
              f"losses={c['mean_losses_mw']} MW latency={s1_latency_ms:.2f} ms")

    # ── baselines on the same unseen window ──────────────────────────
    baselines = {}
    for label, cls in [("no_control", NoControl),
                       ("rule_based", RuleBasedVoltage),
                       ("pid", PIDVoltage)]:
        env_b = QSTSEnvironment("case39", test_profiles)
        df_b = run_controller(env_b, cls(), start=test_start)
        baselines[label] = _summarise(df_b)
        print(f"[phase4-v2] baseline {label}: dev={baselines[label]['mean_voltage_dev_pu']} "
              f"viol={baselines[label]['voltage_violation_hours']} h")

    # ── aggregate across seeds ───────────────────────────────────────
    def agg(key_path):
        vals = []
        for ps in per_seed:
            v = ps
            for k in key_path.split("."):
                v = v[k]
            vals.append(v)
        return {"mean": float(np.mean(vals)), "std": float(np.std(vals)),
                "n_seeds": len(vals)}

    summary = {
        "split": {"train": list(TRAIN_YEARS), "val": VAL_YEAR,
                  "test": list(TEST_YEARS),
                  "test_window": [test_start, test_end]},
        "temporal_mode": "window_reset",
        "seq_len": args.seq_len,
        "n_demo_episodes": len(episodes),
        "episode_starts": [e["start"] for e in episodes],
        "per_seed": per_seed,
        "aggregates": {
            "control_test.voltage_violation_hours": agg("control_test.voltage_violation_hours"),
            "control_test.mean_voltage_dev_pu": agg("control_test.mean_voltage_dev_pu"),
            "control_test.mean_losses_mw": agg("control_test.mean_losses_mw"),
            "val_mae": agg("val_mae"),
            "val_rmse": agg("val_rmse"),
        },
        "baselines_test": baselines,
        "note": "All results are E1 (offline measured) once produced by this script.",
    }
    with open(RESULTS / "phase4_v2_summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    print(f"[phase4-v2] summary written to {RESULTS / 'phase4_v2_summary.json'}")
    print("[phase4-v2] done.")


def _summarise(df) -> dict:
    return {
        "mean_losses_mw": round(float(df["losses_mw"].mean()), 2),
        "max_losses_mw": round(float(df["losses_mw"].max()), 2),
        "mean_voltage_dev_pu": round(float(df["voltage_deviation_pu"].mean()), 4),
        "p95_voltage_dev_pu": round(float(df["p95_voltage_dev_pu"].mean()), 4),
        "voltage_violation_hours": int(df["n_voltage_violations"].sum()),
        "violation_severity_pu2": round(float(df["violation_severity_pu2"].sum()), 5),
        "mean_vm_min": round(float(df["vm_min"].mean()), 4),
        "min_vm_min": round(float(df["vm_min"].min()), 4),
        "converged": int(df["converged"].sum()),
        "n_steps": len(df),
    }


if __name__ == "__main__":
    main()

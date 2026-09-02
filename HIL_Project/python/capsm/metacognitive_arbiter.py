"""
CAPSM Metacognitive Arbitration Layer

Executive function that arbitrates between System-1 (reflexive)
and System-2 (deliberative) control, determining which system
should control the grid at any given moment.

Decision is based on:
- Confidence (C): prediction certainty of System-1
- Novelty (N): how far current state is from familiar regimes
- Urgency (U): fault proximity / rate-of-change metrics

Arbitration logic:
  sigma = 1 (System-1) if C > threshold and U is low
  sigma = 2 (System-2) if N is high or optimality gap > epsilon
  sigma = Safe Mode if cyber-risk > security threshold

Author: CAPSM Thesis Project
"""

import numpy as np
from collections import deque
try:
    import torch
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False


class MetacognitiveArbiter:
    """
    Metacognitive arbitration layer for CAPSM framework.

    Determines when to rely on System-1 (fast reflexes)
    vs System-2 (deliberative optimization) vs Safe Mode
    (cyber-defense fallback).

    Also includes an autoencoder-based novelty detector
    for identifying unseen operating conditions and cyber-attacks.
    """

    def __init__(self, state_dim, confidence_threshold=0.7,
                 novelty_threshold=0.5, urgency_threshold=0.8,
                 cyber_risk_threshold=0.9,
                 autoencoder_hidden=32,
                 smoothing_window=10):
        """
        Parameters
        ----------
        state_dim : int
            Dimension of state vector
        confidence_threshold : float
            Threshold for trusting System-1 (above = trust)
        novelty_threshold : float
            Threshold for novelty detection (above = novel)
        urgency_threshold : float
            Threshold for urgent events (above = urgent)
        cyber_risk_threshold : float
            Threshold for cyber-risk (above = safe mode)
        autoencoder_hidden : int
            Hidden dimension for novelty autoencoder
        smoothing_window : int
            Window for smoothing arbitration decisions
        """
        self.state_dim = state_dim
        self.confidence_threshold = confidence_threshold
        self.novelty_threshold = novelty_threshold
        self.urgency_threshold = urgency_threshold
        self.cyber_risk_threshold = cyber_risk_threshold

        self.autoencoder = _NoveltyAutoencoder(
            state_dim, autoencoder_hidden
        ) if HAS_TORCH else None
        self.autoencoder_trained = False

        self.decision_history = deque(maxlen=1000)
        self.smoothing_window = smoothing_window
        self.recent_decisions = deque(maxlen=smoothing_window)

        self.mode_stats = {
            'SYSTEM_1_REFLEX': 0,
            'SYSTEM_2_PLANNING': 0,
            'SYSTEM_2_OVERRIDE': 0,
            'SAFE_MODE': 0,
            'BLENDED': 0,
        }

    def arbitrate(self, system1_proposal, system2_proposal,
                   current_state, system1_confidence,
                   urgency=0.0, cyber_risk=0.0):
        """
        Decide which control signal to send to the grid.

        Parameters
        ----------
        system1_proposal : dict
            Control actions from System-1
        system2_proposal : dict
            Control actions from System-2
        current_state : np.ndarray
            Current grid state vector
        system1_confidence : float
            Confidence score from System-1 [0, 1]
        urgency : float
            Urgency metric [0, 1] (1 = critical emergency)
        cyber_risk : float
            Cyber-risk indicator [0, 1]

        Returns
        -------
        mode : str
            'SYSTEM_1_REFLEX', 'SYSTEM_2_PLANNING',
            'SYSTEM_2_OVERRIDE', 'SAFE_MODE', or 'BLENDED'
        action : dict
            Selected control actions
        metadata : dict
            Decision metadata for logging and learning
        """
        novelty = self._detect_novelty(current_state)

        if cyber_risk > self.cyber_risk_threshold:
            mode = 'SAFE_MODE'
            action = self._safe_mode_action(current_state)
        elif urgency > self.urgency_threshold:
            mode = 'SYSTEM_1_REFLEX'
            action = system1_proposal
        elif novelty > self.novelty_threshold:
            mode = 'SYSTEM_2_OVERRIDE'
            action = system2_proposal
        elif system1_confidence > self.confidence_threshold:
            mode = 'SYSTEM_1_REFLEX'
            action = system1_proposal
        else:
            mode = 'SYSTEM_2_PLANNING'
            action = system2_proposal

        self.mode_stats[mode] = self.mode_stats.get(mode, 0) + 1
        self.recent_decisions.append(mode)

        metadata = {
            'mode': mode,
            'confidence': system1_confidence,
            'novelty': novelty,
            'urgency': urgency,
            'cyber_risk': cyber_risk,
            'smoothed_mode': self._get_smoothed_mode(),
        }
        self.decision_history.append(metadata)

        return mode, action, metadata

    def _detect_novelty(self, state):
        """
        Detect novelty using autoencoder reconstruction error.

        High reconstruction error = novel/unseen state.
        Falls back to distance-based metric if autoencoder not trained.
        """
        if self.autoencoder is None or not self.autoencoder_trained:
            return self._distance_novelty(state)

        state_tensor = torch.FloatTensor(state).unsqueeze(0)
        with torch.no_grad():
            reconstructed = self.autoencoder(state_tensor)
            error = torch.mean((state_tensor - reconstructed) ** 2).item()
        return min(error, 1.0)

    def _distance_novelty(self, state):
        """Fallback novelty detection based on state vector norm."""
        deviation = np.linalg.norm(state - np.mean(state))
        return min(deviation, 1.0)

    def _get_smoothed_mode(self):
        """Get the most common mode in the recent smoothing window."""
        if len(self.recent_decisions) == 0:
            return 'UNKNOWN'
        from collections import Counter
        counts = Counter(self.recent_decisions)
        return counts.most_common(1)[0][0]

    def _safe_mode_action(self, state):
        """
        Generate safe-mode control actions.

        When cyber-risk is high, the system:
        - Ignores System-2 optimization (potentially poisoned)
        - Maintains previous safe setpoints
        - Falls back to conservative voltage support
        """
        n = len(state) // 4 if len(state) >= 4 else 1
        vm = state[:n] if len(state) >= n else state

        action = {
            'gen_vg': np.clip(vm, 0.95, 1.05),
            'facts_q': {},
            'ev_p': {},
        }

        for i in range(min(3, n)):
            v_error = 1.0 - vm[i] if i < len(vm) else 0
            if abs(v_error) > 0.03:
                action['facts_q'][f'FACTS_{i+1}'] = 30 * np.sign(v_error)

        return action

    def train_autoencoder(self, training_data, epochs=50, lr=1e-3):
        """
        Train the novelty detection autoencoder on normal operation data.

        Parameters
        ----------
        training_data : np.ndarray
            Shape: (n_samples, state_dim) -- normal operation states
        epochs : int
        lr : float
        """
        if not HAS_TORCH or self.autoencoder is None:
            print("[Arbiter] PyTorch not available, using distance-based novelty")
            return

        optimizer = torch.optim.Adam(self.autoencoder.parameters(), lr=lr)
        criterion = torch.nn.MSELoss()

        self.autoencoder.train()
        for epoch in range(epochs):
            epoch_loss = 0.0
            for sample in training_data:
                x = torch.FloatTensor(sample).unsqueeze(0)
                reconstructed = self.autoencoder(x)
                loss = criterion(reconstructed, x)

                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
                epoch_loss += loss.item()

            if (epoch + 1) % 10 == 0:
                print(f"[Arbiter] AE Epoch {epoch+1}/{epochs}, Loss: {epoch_loss/len(training_data):.6f}")

        self.autoencoder_trained = True

    def get_statistics(self):
        """Return arbitration statistics."""
        total = sum(self.mode_stats.values())
        stats = {
            'total_decisions': total,
            'mode_distribution': {
                k: f"{v/total*100:.1f}%" if total > 0 else "0%"
                for k, v in self.mode_stats.items()
            },
            'current_smoothed_mode': self._get_smoothed_mode(),
        }
        return stats

    def save(self, path):
        """Save arbiter state."""
        if HAS_TORCH and self.autoencoder is not None:
            torch.save(self.autoencoder.state_dict(), path)
        print(f"[Arbiter] Saved to {path}")

    def load(self, path):
        """Load arbiter state."""
        if HAS_TORCH and self.autoencoder is not None:
            self.autoencoder.load_state_dict(torch.load(path, map_location='cpu'))
            self.autoencoder_trained = True
        print(f"[Arbiter] Loaded from {path}")


class _NoveltyAutoencoder(torch.nn.Module if HAS_TORCH else object):
    """Autoencoder for novelty/anomaly detection in grid states."""

    def __init__(self, input_dim, hidden_dim=32):
        if not HAS_TORCH:
            return
        super(_NoveltyAutoencoder, self).__init__()
        self.encoder = torch.nn.Sequential(
            torch.nn.Linear(input_dim, hidden_dim),
            torch.nn.ReLU(),
            torch.nn.Linear(hidden_dim, hidden_dim // 2),
            torch.nn.ReLU(),
            torch.nn.Linear(hidden_dim // 2, hidden_dim // 4),
        )
        self.decoder = torch.nn.Sequential(
            torch.nn.Linear(hidden_dim // 4, hidden_dim // 2),
            torch.nn.ReLU(),
            torch.nn.Linear(hidden_dim // 2, hidden_dim),
            torch.nn.ReLU(),
            torch.nn.Linear(hidden_dim, input_dim),
        )

    def forward(self, x):
        if not HAS_TORCH:
            return x
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded


if __name__ == '__main__':
    print("=" * 60)
    print("CAPSM Metacognitive Arbiter Test")
    print("=" * 60)

    state_dim = 39 * 4

    arbiter = MetacognitiveArbiter(
        state_dim=state_dim,
        confidence_threshold=0.7,
        novelty_threshold=0.5,
        urgency_threshold=0.8
    )

    n = 39
    s1_action = {
        'gen_vg': np.ones(n) * 1.03,
        'facts_q': {'FACTS_1': 50, 'FACTS_2': -30, 'FACTS_3': 20},
        'ev_p': {'EV_1': 20, 'EV_2': -15}
    }
    s2_action = {
        'gen_vg': np.ones(n) * 1.02,
        'facts_q': {'FACTS_1': 40, 'FACTS_2': -20, 'FACTS_3': 10},
        'ev_p': {'EV_1': 10, 'EV_2': -5}
    }
    state = np.random.uniform(0.95, 1.05, state_dim)

    print("\n--- Normal operation (low urgency, high confidence) ---")
    mode, action, meta = arbiter.arbitrate(
        s1_action, s2_action, state,
        system1_confidence=0.85, urgency=0.2, cyber_risk=0.1
    )
    print(f"Mode: {mode}")
    print(f"Metadata: confidence={meta['confidence']:.2f}, novelty={meta['novelty']:.4f}")

    print("\n--- Emergency (high urgency) ---")
    mode, action, meta = arbiter.arbitrate(
        s1_action, s2_action, state,
        system1_confidence=0.6, urgency=0.95, cyber_risk=0.1
    )
    print(f"Mode: {mode} (should be SYSTEM_1_REFLEX)")

    print("\n--- Novel situation (high novelty) ---")
    mode, action, meta = arbiter.arbitrate(
        s1_action, s2_action, state + 0.3,
        system1_confidence=0.3, urgency=0.3, cyber_risk=0.1
    )
    print(f"Mode: {mode} (should be SYSTEM_2_OVERRIDE)")

    print("\n--- Cyber-attack (high cyber-risk) ---")
    mode, action, meta = arbiter.arbitrate(
        s1_action, s2_action, state,
        system1_confidence=0.8, urgency=0.2, cyber_risk=0.95
    )
    print(f"Mode: {mode} (should be SAFE_MODE)")

    print("\n--- Statistics ---")
    stats = arbiter.get_statistics()
    print(f"Total decisions: {stats['total_decisions']}")
    print(f"Mode distribution: {stats['mode_distribution']}")

    print("\nOK")

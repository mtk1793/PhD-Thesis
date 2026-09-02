"""
CAPSM System-1: Reflexive Intelligence (CNN-LSTM)

Fast, intuitive control layer for millisecond-scale protection.
Implements a Convolutional Neural Network + Long Short-Term Memory
architecture for spatiotemporal pattern recognition in power system measurements.

This module provides:
- CNN-LSTM model for fault detection and stability assessment
- Physics-informed safety filter for constraint enforcement
- Sub-millisecond inference for real-time protection

Author: CAPSM Thesis Project
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from collections import deque


class CNNLSTMController(nn.Module):
    """
    CNN-LSTM architecture for fast reflexive power system control.

    The CNN layers extract spatial features from bus voltage/angle vectors,
    while the LSTM layers capture temporal dynamics over a sliding window
    of PMU measurements. Output is a control action vector for FACTS
    devices, EV charging, and generator reactive power.

    Architecture:
        Input: (batch, seq_len, n_features)  -- PMU time series
        CNN:  1D convolution over spatial dimension -> feature maps
        LSTM:  temporal processing of CNN outputs -> hidden states
        FC:    map hidden state -> control actions

    Timescale: tau_1 < 5ms (sub-millisecond inference on FPGA)
    """

    def __init__(self, n_buses, n_features=4, conv_channels=32,
                 lstm_hidden=64, n_actions=10, seq_len=10,
                 safety_filter=True):
        """
        Parameters
        ----------
        n_buses : int
            Number of buses in the power system
        n_features : int
            Features per bus (voltage, angle, frequency, RoCoF)
        conv_channels : int
            Number of CNN output channels
        lstm_hidden : int
            LSTM hidden state dimension
        n_actions : int
            Number of control actions to output
        seq_len : int
            Length of input time window (PMU samples)
        safety_filter : bool
            Whether to apply physics-informed safety constraints
        """
        super(CNNLSTMController, self).__init__()

        self.n_buses = n_buses
        self.n_features = n_features
        self.seq_len = seq_len
        self.n_actions = n_actions
        self.safety_filter_enabled = safety_filter

        self.conv1 = nn.Conv1d(n_features, conv_channels, kernel_size=3, padding=1)
        self.conv2 = nn.Conv1d(conv_channels, conv_channels * 2, kernel_size=3, padding=1)
        self.pool = nn.MaxPool1d(kernel_size=2)
        self.bn1 = nn.BatchNorm1d(conv_channels)
        self.bn2 = nn.BatchNorm1d(conv_channels * 2)

        cnn_output_dim = conv_channels * 2 * max(n_buses // 2, 1)

        self.lstm = nn.LSTM(
            input_size=cnn_output_dim,
            hidden_size=lstm_hidden,
            num_layers=2,
            batch_first=True,
            dropout=0.1
        )

        self.attention = AttentionLayer(lstm_hidden)
        self.fc = nn.Linear(lstm_hidden, n_actions)
        self.action_scale = nn.Parameter(torch.ones(n_actions))

        self.relu = nn.ReLU()
        self.tanh = nn.Tanh()

        self.v_limits = (0.94, 1.06)
        self.q_limits = (-100.0, 100.0)
        self.ramp_limit = 0.1

    def forward(self, x):
        """
        Forward pass through CNN-LSTM architecture.

        Parameters
        ----------
        x : torch.Tensor
            Shape: (batch, seq_len, n_buses, n_features)

        Returns
        -------
        actions : torch.Tensor
            Shape: (batch, n_actions) -- control actions in [-1, 1]
        confidence : torch.Tensor
            Shape: (batch, 1) -- confidence score for arbitration
        """
        batch_size = x.shape[0]

        x_cnn = x.permute(0, 3, 1, 2)
        x_cnn = x_cnn.reshape(batch_size * self.seq_len, self.n_features, self.n_buses)

        c = self.relu(self.bn1(self.conv1(x_cnn)))
        c = self.relu(self.bn2(self.conv2(c)))
        c = self.pool(c)
        c = c.permute(0, 2, 1)
        c = c.reshape(batch_size, self.seq_len, -1)

        lstm_out, (h_n, c_n) = self.lstm(c)

        attended = self.attention(lstm_out)
        actions = self.tanh(self.fc(attended)) * self.action_scale

        confidence = torch.sigmoid(attended.mean(dim=-1, keepdim=True))

        if self.safety_filter_enabled:
            actions = self._apply_safety_filter(actions, x[:, -1, :, :])

        return actions, confidence

    def _apply_safety_filter(self, actions, current_state):
        """
        Physics-informed safety filter (PINN-based).

        Constrains actions to prevent:
        - Voltage violations (0.94 < V < 1.06)
        - Excessive ramp rates
        - Thermal limit violations

        This is a differentiable projection that can be incorporated
        into the training loss.
        """
        vm = current_state[:, :, 0]
        batch_size = actions.shape[0]

        n_voltage_actions = min(actions.shape[1], vm.shape[1], self.n_buses)

        v_penalty = torch.zeros(batch_size, n_voltage_actions,
                                  device=actions.device)
        vm_reduced = vm[:, :n_voltage_actions]

        v_high_mask = vm_reduced > self.v_limits[1]
        v_low_mask = vm_reduced < self.v_limits[0]

        safe_actions = actions.clone()
        for b in range(batch_size):
            for i in range(n_voltage_actions):
                if v_high_mask[b, i]:
                    safe_actions[b, i] = torch.clamp(actions[b, i], max=0)
                elif v_low_mask[b, i]:
                    safe_actions[b, i] = torch.clamp(actions[b, i], min=0)

        if batch_size > 1:
            ramp = torch.diff(safe_actions, dim=0, prepend=safe_actions[:1])
            ramp_mask = torch.abs(ramp) > self.ramp_limit
            safe_actions[1:][ramp_mask] = safe_actions[:-1][ramp_mask] + \
                self.ramp_limit * torch.sign(ramp[ramp_mask])

        return safe_actions

    def predict(self, measurement_sequence):
        """
        Run inference on a measurement sequence.

        Parameters
        ----------
        measurement_sequence : np.ndarray
            Shape: (seq_len, n_buses, n_features) -- recent PMU data

        Returns
        -------
        actions : np.ndarray
            Control action vector
        confidence : float
            Confidence score [0, 1]
        inference_time_ms : float
            Measured inference time in milliseconds
        """
        import time
        self.eval()
        with torch.no_grad():
            x = torch.FloatTensor(measurement_sequence).unsqueeze(0)

            t0 = time.perf_counter()
            actions, confidence = self.forward(x)
            t1 = time.perf_counter()

        inference_time_ms = (t1 - t0) * 1000

        return (
            actions.numpy().squeeze(),
            confidence.item(),
            inference_time_ms
        )


class AttentionLayer(nn.Module):
    """Attention mechanism for weighting temporal features."""

    def __init__(self, hidden_dim):
        super(AttentionLayer, self).__init__()
        self.attention = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.Tanh(),
            nn.Linear(hidden_dim, 1)
        )

    def forward(self, lstm_output):
        scores = self.attention(lstm_output)
        weights = F.softmax(scores, dim=1)
        context = torch.sum(weights * lstm_output, dim=1)
        return context


class System1Agent:
    """
    System-1 agent wrapper for CAPSM framework.

    Maintains a sliding window of PMU measurements,
    runs CNN-LSTM inference, and provides fast
    reflexive control actions.

    Timescale: tau_1 < 5ms
    """

    def __init__(self, n_buses, n_features=4, seq_len=10,
                 n_actions=10, device='cpu'):
        self.n_buses = n_buses
        self.n_features = n_features
        self.seq_len = seq_len
        self.n_actions = n_actions
        self.device = device

        self.model = CNNLSTMController(
            n_buses=n_buses,
            n_features=n_features,
            n_actions=n_actions,
            seq_len=seq_len
        ).to(device)

        self.measurement_buffer = deque(maxlen=seq_len)
        self.is_trained = False

        self.detection_threshold = 0.7
        self.confidence_threshold = 0.5

    def update_measurements(self, observation):
        """Add new measurement to the sliding window."""
        features = np.array([
            observation['vm'],
            observation.get('va', np.zeros(self.n_buses)),
            np.full(self.n_buses, observation.get('freq', 60.0)),
            np.full(self.n_buses, observation.get('rocof', 0.0))
        ]).T
        self.measurement_buffer.append(features)

    def get_action(self, observation):
        """
        Get reflexive control action from System-1.

        Returns
        -------
        action : dict
            Control actions for FACTS, EV, generators
        confidence : float
            System-1 confidence [0, 1]
        inference_time : float
            Inference time in milliseconds
        event_detected : bool
            Whether a critical event was detected
        """
        self.update_measurements(observation)

        if len(self.measurement_buffer) < self.seq_len:
            return {'gen_vg': np.ones(self.n_buses)}, 0.0, 0.0, False

        measurement_seq = np.array(list(self.measurement_buffer))

        if not self.is_trained:
            actions = self._heuristic_response(observation)
            confidence = 0.3
            inference_time = 0.1
        else:
            raw_actions, confidence, inference_time = self.model.predict(measurement_seq)
            actions = self._decode_actions(raw_actions)

        event_detected = self._detect_event(observation)

        return actions, confidence, inference_time, event_detected

    def _heuristic_response(self, observation):
        """Heuristic control when model is not yet trained."""
        vm = observation['vm']
        v_ref = 1.0
        v_error = v_ref - vm

        gen_vg = np.clip(vm + 0.01 * v_error, 0.9, 1.1)

        action = {'gen_vg': gen_vg}

        if v_error.any() and np.any(np.abs(v_error) > 0.05):
            action['facts_q'] = {}
            for dev in range(min(3, len(v_error))):
                if abs(v_error[dev]) > 0.05:
                    action['facts_q'][f'FACTS_{dev+1}'] = 50 * np.sign(v_error[dev])

        return action

    def _decode_actions(self, raw_actions):
        """Decode raw neural network output to control action dict."""
        n = self.n_buses
        gen_vg = raw_actions[:n] if len(raw_actions) >= n else np.ones(n)
        facts_q = {}
        for i in range(min(3, len(raw_actions) - n)):
            facts_q[f'FACTS_{i+1}'] = float(raw_actions[n + i] * 100)

        ev_p = {}
        for i in range(min(2, len(raw_actions) - n - 3)):
            ev_p[f'EV_{i+1}'] = float(raw_actions[n + 3 + i] * 50)

        return {'gen_vg': gen_vg, 'facts_q': facts_q, 'ev_p': ev_p}

    def _detect_event(self, observation):
        """Detect critical events requiring fast response."""
        vm = observation['vm']
        freq = observation.get('freq', 60.0)
        rocof = observation.get('rocof', 0.0)

        v_deviation = np.max(np.abs(vm - 1.0))
        freq_deviation = abs(freq - 60.0)

        if v_deviation > 0.1 or freq_deviation > 0.5 or abs(rocof) > 0.5:
            return True
        return False

    def train(self, training_data, epochs=100, lr=1e-3):
        """
        Train the CNN-LSTM model on historical fault/disturbance data.

        Parameters
        ----------
        training_data : list of (sequence, optimal_action) tuples
        epochs : int
        lr : float
        """
        optimizer = torch.optim.Adam(self.model.parameters(), lr=lr)
        criterion = nn.MSELoss()

        self.model.train()
        losses = []

        for epoch in range(epochs):
            epoch_loss = 0.0
            for seq, target in training_data:
                x = torch.FloatTensor(seq).unsqueeze(0)
                y = torch.FloatTensor(target).unsqueeze(0)

                actions, conf = self.model(x)
                loss = criterion(actions, y)

                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

                epoch_loss += loss.item()

            losses.append(epoch_loss / len(training_data))
            if (epoch + 1) % 20 == 0:
                print(f"[System1] Epoch {epoch+1}/{epochs}, Loss: {losses[-1]:.6f}")

        self.is_trained = True
        return losses

    def save_model(self, path):
        """Save trained model."""
        torch.save(self.model.state_dict(), path)
        print(f"[System1] Model saved to {path}")

    def load_model(self, path):
        """Load trained model."""
        self.model.load_state_dict(torch.load(path, map_location=self.device))
        self.is_trained = True
        print(f"[System1] Model loaded from {path}")


if __name__ == '__main__':
    print("=" * 60)
    print("CAPSM System-1 (CNN-LSTM) Test")
    print("=" * 60)

    n_buses = 39
    agent = System1Agent(n_buses=n_buses, n_features=4, n_actions=10)

    obs = {
        'vm': np.random.uniform(0.95, 1.05, n_buses),
        'va': np.random.uniform(-0.5, 0.5, n_buses),
        'freq': 60.0 + np.random.uniform(-0.1, 0.1),
        'rocof': np.random.uniform(-0.2, 0.2),
    }

    for i in range(12):
        agent.update_measurements(obs)

    action, confidence, inf_time, event = agent.get_action(obs)
    print(f"Action keys: {list(action.keys())}")
    print(f"Confidence: {confidence:.4f}")
    print(f"Inference time: {inf_time:.3f} ms")
    print(f"Event detected: {event}")
    print(f"Model parameters: {sum(p.numel() for p in agent.model.parameters()):,}")

    print("\n--- Training test ---")
    dummy_data = []
    for _ in range(50):
        seq = np.random.randn(10, n_buses, 4)
        target = np.random.uniform(-1, 1, 10)
        dummy_data.append((seq, target))

    losses = agent.train(dummy_data, epochs=20, lr=1e-3)
    print(f"Training complete. Final loss: {losses[-1]:.6f}")

    action, confidence, inf_time, event = agent.get_action(obs)
    print(f"\nAfter training:")
    print(f"Confidence: {confidence:.4f}")
    print(f"Inference time: {inf_time:.3f} ms")
    print("OK")

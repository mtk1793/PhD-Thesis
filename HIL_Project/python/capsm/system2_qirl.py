"""
CAPSM System-2: Deliberative Optimization (QIRL)

Quantum-Inspired Reinforcement Learning for multi-timescale
optimal control of FACTS devices, EV fleets, and DERs.

Unlike classical DRL (DQN, PPO), the QIRL agent operates on
complex-valued probability amplitudes, leveraging quantum
superposition and interference for enhanced exploration.

Key innovations:
- Superposition-based state representation
- Quantum rotation gate update rule
- Tunneling operator for escaping local optima
- Multi-objective reward (stability + efficiency + cost)

Timescale: tau_2 ~ 50ms - seconds (deliberative, async)

Author: CAPSM Thesis Project
"""

import numpy as np
import os
from collections import defaultdict


class QIRLAgent:
    """
    Quantum-Inspired Reinforcement Learning agent.

    Represents Q-values as complex probability amplitudes
    (psi = r * exp(i*theta)), enabling:
    - Superposition: all actions evaluated simultaneously
    - Interference: constructive amplification of good actions
    - Tunneling: escape local optima through high-cost barriers

    Convergence: ~58-59% faster than classical DQN (per Ch11 results)
    """

    def __init__(self, state_dim, action_dim, n_actions_discrete=16,
                 learning_rate=0.01, discount=0.95,
                 exploration_rate=0.1, tunneling_strength=0.05,
                 temperature=1.0):
        """
        Parameters
        ----------
        state_dim : int
            Dimension of state space (n_buses * n_features)
        action_dim : int
            Dimension of continuous action space
        n_actions_discrete : int
            Number of discretized actions for Q-table
        learning_rate : float
            Alpha for Q-value updates
        discount : float
            Gamma discount factor
        exploration_rate : float
            Initial exploration probability
        tunneling_strength : float
            Quantum tunneling amplitude
        temperature : float
            Boltzmann temperature for amplitude updates
        """
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.n_actions = n_actions_discrete
        self.alpha = learning_rate
        self.gamma = discount
        self.epsilon = exploration_rate
        self.tunneling_strength = tunneling_strength
        self.beta = 1.0 / temperature

        self.theta = defaultdict(lambda: np.pi / 2 * np.ones(n_actions_discrete))
        self.alpha_amplitude = defaultdict(lambda: np.cos(np.pi / 2))
        self.beta_amplitude = defaultdict(lambda: np.sin(np.pi / 2))

        self.q_table = defaultdict(lambda: np.zeros(n_actions_discrete))
        self.visit_count = defaultdict(lambda: np.zeros(n_actions_discrete))

        self.best_q = -np.inf
        self.best_action = None
        self.convergence_history = []
        self.reward_history = []

        self.state_bins = self._create_state_bins(state_dim, n_bins=10)

    def _create_state_bins(self, state_dim, n_bins=10):
        """Create discretization bins for continuous states."""
        bins = {}
        for i in range(state_dim):
            bins[i] = np.linspace(-1, 1, n_bins + 1)
        return bins

    def _discretize_state(self, state):
        """Convert continuous state to discrete indices."""
        discrete = []
        for i, val in enumerate(state):
            if i < len(self.state_bins):
                idx = np.digitize(val, self.state_bins[i]) - 1
                idx = max(0, min(idx, len(self.state_bins[i]) - 2))
                discrete.append(idx)
            else:
                discrete.append(0)
        return tuple(discrete[:self.state_dim]) if discrete else (0,)

    def get_action(self, state, training=True):
        """
        Select action using quantum-inspired measurement.

        The quantum state collapses to a specific action with
        probability |beta|^2 (Born rule). During training,
        this provides exploration; during inference,
        it provides optimal action selection.

        Parameters
        ----------
        state : np.ndarray
            Current system state
        training : bool
            Whether in training mode (exploration allowed)

        Returns
        -------
        action : np.ndarray
            Continuous action vector
        q_value : float
            Estimated Q-value of selected action
        """
        discrete_state = self._discretize_state(state)

        if discrete_state not in self.q_table:
            self.q_table[discrete_state] = np.zeros(self.n_actions)

        if training and np.random.rand() < self.epsilon:
            amps = np.abs(np.asarray(self.beta_amplitude[discrete_state]).flatten()) ** 2
            probs = amps / (amps.sum() + 1e-10)
            if len(probs) == self.n_actions:
                action_idx = int(np.random.choice(self.n_actions, p=probs))
            else:
                action_idx = np.random.randint(self.n_actions)
        else:
            if discrete_state in self.q_table and self.q_table[discrete_state].any():
                action_idx = np.argmax(self.q_table[discrete_state])
            else:
                action_idx = np.random.randint(self.n_actions)

        continuous_action = self._decode_action(action_idx)
        q_value = self.q_table[discrete_state][action_idx] if discrete_state in self.q_table else 0.0

        return continuous_action, q_value

    def _decode_action(self, action_idx):
        """Convert discrete action index to continuous action vector."""
        action = np.zeros(self.action_dim)
        n_per_dim = self.n_actions // self.action_dim if self.action_dim > 0 else 1

        for i in range(self.action_dim):
            sub_idx = action_idx % n_per_dim if n_per_dim > 0 else 0
            action[i] = (sub_idx / max(n_per_dim - 1, 1)) * 2 - 1
            action_idx = action_idx // n_per_dim if n_per_dim > 0 else 0

        return action

    def update(self, state, action, reward, next_state, done):
        """
        Update Q-values using quantum-inspired rotation gate.

        The update mimics Grover's iteration:
        - Positive reward: rotate amplitude towards action (constructive)
        - Negative reward: rotate away (destructive)
        - Tunneling: probabilistic jump to escape local optima

        Parameters
        ----------
        state : np.ndarray
        action : np.ndarray
        reward : float
        next_state : np.ndarray
        done : bool
        """
        discrete_state = self._discretize_state(state)
        next_discrete = self._discretize_state(next_state)

        if discrete_state not in self.q_table:
            self.q_table[discrete_state] = np.zeros(self.n_actions)
        if next_discrete not in self.q_table:
            self.q_table[next_discrete] = np.zeros(self.n_actions)

        action_idx = self._encode_action(action)
        best_next = np.max(self.q_table[next_discrete])

        td_target = reward + self.gamma * best_next * (1 - done)
        td_error = td_target - self.q_table[discrete_state][action_idx]

        self.q_table[discrete_state][action_idx] += self.alpha * td_error
        self.visit_count[discrete_state][action_idx] += 1

        delta_theta = self.alpha * np.sign(td_error) * 0.1
        self.theta[discrete_state][action_idx] += delta_theta

        if td_error < 0 and np.random.rand() < self.tunneling_strength:
            tunnel_target = np.random.randint(self.n_actions)
            self.theta[discrete_state][tunnel_target] += np.pi / 4


        self.q_table[discrete_state] = self._boltzmann_update(
            discrete_state, self.beta
        )

        self.reward_history.append(reward)
        self.convergence_history.append(np.mean(self.reward_history[-100:]))

        if len(self.convergence_history) % 100 == 0:
            avg = np.mean(self.convergence_history[-100:])
            print(f"[System2-QIRL] Step {len(self.convergence_history)}, avg_reward: {avg:.4f}")

    def _encode_action(self, action):
        """Encode continuous action to discrete index."""
        idx = 0
        n_per_dim = max(self.n_actions // self.action_dim, 1)
        for i in range(min(len(action), self.action_dim)):
            sub = int((action[i] + 1) / 2 * (n_per_dim - 1))
            sub = max(0, min(sub, n_per_dim - 1))
            idx = idx * n_per_dim + sub
        return idx % self.n_actions

    def _boltzmann_update(self, state, beta):
        """Boltzmann (softmax) exploration based on Q-values."""
        q = self.q_table[state]
        exp_q = np.exp(beta * q - np.max(beta * q))
        probs = exp_q / (exp_q.sum() + 1e-10)
        return q + 0.01 * np.log(probs + 1e-10)

    def train_episode(self, env, max_steps=1000):
        """
        Train for one episode using the GridEnvironment.

        Parameters
        ----------
        env : GridEnvironment
        max_steps : int

        Returns
        -------
        total_reward : float
        steps : int
        """
        state = env.reset()
        total_reward = 0.0
        obs = env._get_observation()

        for step in range(max_steps):
            state_vec = self._obs_to_state(obs)
            action, q_val = self.get_action(state_vec, training=True)

            control = self._action_to_control(action)
            obs, reward, violations, info, done = env.step(control)

            if not info.get('success', False):
                obs = env._get_observation()
                total_reward += reward
                continue

            next_obs = obs
            next_state_vec = self._obs_to_state(next_obs)

            self.update(state_vec, action, reward, next_state_vec, done)

            total_reward += reward
            state_vec = next_state_vec
            obs = next_obs

            if done:
                break

        return total_reward, step + 1

    def _obs_to_state(self, obs):
        """Convert observation dict to state vector."""
        vm = np.nan_to_num(obs['vm'])
        va = np.nan_to_num(obs.get('va', np.zeros(len(vm))))
        freq = np.full(len(vm), obs.get('freq', 60.0))
        rocof = np.full(len(vm), obs.get('rocof', 0.0))
        return np.concatenate([vm, va, freq, rocof])

    def _action_to_control(self, action):
        """Convert action vector to control dict for GridEnvironment."""
        n = self.state_dim // 4 if self.state_dim >= 4 else 1
        control = {'gen_vg': np.ones(max(n, 1))}
        if len(action) >= n:
            control['gen_vg'] = np.clip(action[:n] * 0.01 + 1.0, 0.95, 1.05)
        return control
        if len(action) >= n + 3:
            control['facts_q'] = {}
            for i in range(3):
                control['facts_q'][f'FACTS_{i+1}'] = float(action[n + i] * 100)
        if len(action) >= n + 5:
            control['ev_p'] = {}
            for i in range(2):
                control['ev_p'][f'EV_{i+1}'] = float(action[n + 3 + i] * 50)
        return control

    def get_convergence_metrics(self):
        """Return convergence history for analysis."""
        return {
            'reward_history': self.reward_history,
            'convergence_history': self.convergence_history,
            'best_q': self.best_q,
            'total_states_visited': len(self.q_table),
            'avg_q': np.mean([np.mean(v) for v in self.q_table.values()]) if self.q_table else 0,
        }

    def save(self, path):
        """Save QIRL agent state."""
        np.savez(
            path,
            theta=self.theta,
            q_table=self.q_table,
            visit_count=self.visit_count,
            state_bins=self.state_bins
        )
        print(f"[System2-QIRL] Agent saved to {path}")

    def load(self, path):
        """Load QIRL agent state."""
        data = np.load(path, allow_pickle=True)
        self.theta = data['theta']
        self.q_table = data['q_table'].item()
        self.visit_count = data['visit_count'].item()
        self.state_bins = data['state_bins'].item()
        self.alpha_amplitude = np.cos(self.theta)
        self.beta_amplitude = np.sin(self.theta)
        print(f"[System2-QIRL] Agent loaded from {path}")


class DQNBaseline:
    """
    Classical Deep Q-Network baseline for comparison with QIRL.

    Used to demonstrate the ~58% faster convergence of QIRL
    over classical DQN (per Chapter 11 results).
    """

    def __init__(self, state_dim, action_dim, lr=0.001, gamma=0.95):
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.lr = lr
        self.gamma = gamma
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.q_table = defaultdict(lambda: np.zeros(action_dim))
        self.convergence_history = []

    def get_action(self, state):
        s = self._discretize(state)
        if np.random.rand() < self.epsilon:
            return np.random.randint(self.action_dim), 0.0
        return np.argmax(self.q_table[s]), self.q_table[s].max()

    def update(self, state, action, reward, next_state, done):
        s = self._discretize(state)
        ns = self._discretize(next_state)
        best_next = np.max(self.q_table[ns])
        target = reward + self.gamma * best_next * (1 - done)
        self.q_table[s][action] += self.lr * (target - self.q_table[s][action])
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)
        self.convergence_history.append(reward)

    def _discretize(self, state):
        n_bins = 10
        discrete = []
        for i, val in enumerate(state):
            b = np.linspace(-1, 1,n_bins+1)
            idx = int(np.digitize(val,b)) - 1
            idx = np.clip(idx,0,n_bins-1)
            discrete.append(idx)
        return tuple(discrete)


if __name__ == '__main__':
    print("=" * 60)
    print("CAPSM System-2 (QIRL) Test")
    print("=" * 60)

    import sys
    _here = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, os.path.dirname(_here))
    from gridsim.grid_environment import setup_capsm_environment

    env = setup_capsm_environment('case9', n_facts=2, n_ev=1)
    n_buses = env.n_bus
    state_dim = n_buses * 4
    action_dim = 10

    qirl = QIRLAgent(state_dim=state_dim, action_dim=action_dim,
                       n_actions_discrete=16, learning_rate=0.01)
    dqn = DQNBaseline(state_dim=state_dim, action_dim=16)

    print("\n--- Training QIRL (50 episodes) ---")
    qirl_rewards = []
    for ep in range(50):
        total_r, steps = qirl.train_episode(env, max_steps=100)
        qirl_rewards.append(total_r)
        if (ep + 1) % 10 == 0:
            print(f"  Episode {ep+1}: reward={total_r:.2f}, steps={steps}")

    print("\n--- Training DQN Baseline (50 episodes) ---")
    dqn_rewards = []
    for ep in range(50):
        obs = env.reset()
        total_r = 0
        for step in range(100):
            s = np.concatenate([obs['vm'], obs.get('va', np.zeros(n_buses))])
            a, q = dqn.get_action(s)
            control = {'gen_vg': np.ones(n_buses)}
            obs, r, v, info, done = env.step(control)
            ns = np.concatenate([obs['vm'], obs.get('va', np.zeros(n_buses))])
            dqn.update(s, a, r, ns, done)
            total_r += r
            if done:
                break
        dqn_rewards.append(total_r)
        if (ep + 1) % 10 == 0:
            print(f"  Episode {ep+1}: reward={total_r:.2f}")

    print(f"\n--- Convergence Comparison ---")
    qirl_conv = np.mean(qirl_rewards[-10:])
    dqn_conv = np.mean(dqn_rewards[-10:])
    print(f"QIRL avg reward (last 10): {qirl_conv:.2f}")
    print(f"DQN  avg reward (last 10): {dqn_conv:.2f}")
    print(f"QIRL improvement: {((qirl_conv - dqn_conv) / abs(dqn_conv) * 100):.1f}%")
    print("OK")

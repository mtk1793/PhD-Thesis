"""
CAPSM Integrated Controller - Main execution script

Integrates System-1 (CNN-LSTM), System-2 (QIRL), and the
Metacognitive Arbiter into a unified CAPSM controller.

This script runs the full offline simulation pipeline:
1. GridEnvironment with IEEE test system + FACTS + EV
2. System-1 provides fast reflexive control
3. System-2 provides deliberative optimization
4. Arbiter decides which system controls the grid
5. Results are collected for thesis Chapter 11

Author: CAPSM Thesis Project
"""

import sys
import os
import time
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gridsim.grid_environment import setup_capsm_environment
from capsm.system1_cnn_lstm import System1Agent
from capsm.system2_qirl import QIRLAgent, DQNBaseline
from capsm.metacognitive_arbiter import MetacognitiveArbiter


def run_capsm_offline(case_name='case39', n_facts=5, n_ev=3,
                      n_episodes=100, max_steps=200,
                      train_system1=True, train_system2=True,
                      verbose=True):
    """
    Run the full CAPSM offline simulation.

    Parameters
    ----------
    case_name : str
        IEEE test case ('case9', 'case14', 'case39', 'case118')
    n_facts : int
        Number of FACTS devices
    n_ev : int
        Number of EV fleets
    n_episodes : int
        Number of training episodes
    max_steps : int
        Steps per episode
    train_system1 : bool
        Whether to train System-1 CNN-LSTM
    train_system2 : bool
        Whether to train System-2 QIRL
    verbose : bool
        Print progress messages

    Returns
    -------
    results : dict
        Complete simulation results
    """
    if verbose:
        print("=" * 70)
        print(f"CAPSM Offline Simulation - {case_name}")
        print("=" * 70)

    env = setup_capsm_environment(case_name, n_facts=n_facts, n_ev=n_ev)
    info = env.get_system_info()
    if verbose:
        print(f"Environment: {info}")

    n_buses = env.n_bus
    state_dim = n_buses * 4
    action_dim = min(n_buses + n_facts + n_ev, 10)

    system1 = System1Agent(
        n_buses=n_buses,
        n_features=4,
        seq_len=10,
        n_actions=action_dim
    )

    system2_qirl = QIRLAgent(
        state_dim=state_dim,
        action_dim=action_dim,
        n_actions_discrete=16,
        learning_rate=0.01
    )

    system2_dqn = DQNBaseline(
        state_dim=state_dim,
        action_dim=16
    )

    arbiter = MetacognitiveArbiter(
        state_dim=state_dim,
        confidence_threshold=0.7,
        novelty_threshold=0.5
    )

    if train_system1:
        if verbose:
            print("\n--- Training System-1 (CNN-LSTM) ---")
        s1_training_data = _generate_system1_training_data(env, n_samples=100)
        losses = system1.train(s1_training_data, epochs=30, lr=1e-3)
        if verbose:
            print(f"System-1 training complete. Final loss: {losses[-1]:.6f}")

    if train_system2:
        if verbose:
            print("\n--- Training System-2 (QIRL vs DQN) ---")
        qirl_rewards = []
        dqn_rewards = []

        for ep in range(n_episodes):
            t0 = time.time()
            qirl_r, qirl_steps = system2_qirl.train_episode(env, max_steps=max_steps)
            qirl_rewards.append(qirl_r)
            t1 = time.time()

            obs = env.reset()
            dqn_r = 0
            for step in range(max_steps):
                s = np.concatenate([obs['vm'], obs.get('va', np.zeros(n_buses))])
                a, q = system2_dqn.get_action(s)
                control = {'gen_vg': np.ones(n_buses)}
                obs, r, v, i, done = env.step(control)
                ns = np.concatenate([obs['vm'], obs.get('va', np.zeros(n_buses))])
                system2_dqn.update(s, a, r, ns, done)
                dqn_r += r
                if done:
                    break
            dqn_rewards.append(dqn_r)

            if verbose and (ep + 1) % 20 == 0:
                print(f"  Episode {ep+1}/{n_episodes}: "
                      f"QIRL={qirl_r:.1f} ({t1-t0:.2f}s), DQN={dqn_r:.1f}")

    if verbose:
        print("\n--- Running CAPSM with Arbitration ---")
    eval_results = _evaluate_capsm(
        env, system1, system2_qirl, arbiter,
        n_scenarios=50, max_steps=max_steps, verbose=verbose
    )

    convergence_metrics = system2_qirl.get_convergence_metrics()
    arbiter_stats = arbiter.get_statistics()

    results = {
        'case_name': case_name,
        'system_info': info,
        'qirl_convergence': convergence_metrics,
        'dqn_comparison': {
            'qirl_final_reward': np.mean(qirl_rewards[-10:]) if qirl_rewards else 0,
            'dqn_final_reward': np.mean(dqn_rewards[-10:]) if dqn_rewards else 0,
        },
        'arbiter_stats': arbiter_stats,
        'eval_results': eval_results,
    }

    if verbose:
        print("\n" + "=" * 70)
        print("CAPSM Offline Simulation Complete")
        print("=" * 70)
        print(f"\nQIRL vs DQN convergence:")
        print(f"  QIRL avg reward (last 10): {results['dqn_comparison']['qirl_final_reward']:.2f}")
        print(f"  DQN  avg reward (last 10): {results['dqn_comparison']['dqn_final_reward']:.2f}")
        if results['dqn_comparison']['dqn_final_reward'] != 0:
            improvement = ((results['dqn_comparison']['qirl_final_reward'] -
                           results['dqn_comparison']['dqn_final_reward']) /
                          abs(results['dqn_comparison']['dqn_final_reward']) * 100)
            print(f"  QIRL improvement: {improvement:.1f}%")

        print(f"\nArbiter mode distribution:")
        for mode, pct in arbiter_stats['mode_distribution'].items():
            print(f"  {mode}: {pct}")

        print(f"\nEvaluation results:")
        for key, val in eval_results.items():
            print(f"  {key}: {val}")

    return results


def _generate_system1_training_data(env, n_samples=100):
    """Generate training data for System-1 CNN-LSTM."""
    training_data = []
    obs = env.reset()

    for _ in range(n_samples):
        vm = obs['vm']
        va = obs.get('va', np.zeros(env.n_bus))
        freq = np.full(env.n_bus, obs.get('freq', 60.0))
        rocof = np.full(env.n_bus, obs.get('rocof', 0.0))

        seq = np.random.randn(10, env.n_bus, 4) * 0.1 + np.stack([vm, va, freq, rocof], axis=1)

        v_error = 1.0 - vm
        target = np.zeros(env.n_bus)
        target[:len(vm)] = 0.1 * np.sign(v_error)
        target = target[:10] if len(target) >= 10 else np.pad(target, (0, 10 - len(target)))

        training_data.append((seq, target))

        obs, _, _, _, _ = env.step(None)

    return training_data


def _evaluate_capsm(env, system1, system2, arbiter, n_scenarios=50, max_steps=200, verbose=True):
    """Evaluate CAPSM across multiple scenarios."""
    results = {
        'total_scenarios': n_scenarios,
        'successful_pf': 0,
        'fault_response_time_ms': [],
        'voltage_violations': 0,
        'modes_used': {},
    }

    for scenario_idx in range(n_scenarios):
        obs = env.reset()
        scenario_violations = 0
        scenario_modes = []

        fault_injected = False
        fault_step = max_steps // 3
        cyber_injected = False
        cyber_step = (2 * max_steps) // 3

        for step in range(max_steps):
            state_vec = np.concatenate([
                obs['vm'],
                obs.get('va', np.zeros(env.n_bus)),
                np.full(env.n_bus, obs.get('freq', 60.0)),
                np.full(env.n_bus, obs.get('rocof', 0.0))
            ])

            if step == fault_step:
                fault_bus = min(env.n_bus // 2, env.n_bus)
                env.inject_fault(bus=fault_bus, fault_type='three_phase')
                fault_injected = True
                t_fault = time.time()

            if step == cyber_step:
                env.inject_cyber_attack(attack_type='fdi', magnitude=0.05)
                cyber_injected = True

            s1_action, s1_conf, s1_time, s1_event = system1.get_action(obs)

            s2_action, s2_q = system2.get_action(state_vec, training=False)
            s2_control = system2._action_to_control(s2_action)

            urgency = 0.9 if s1_event else 0.2
            cyber_risk = 0.85 if cyber_injected else 0.1

            mode, action, meta = arbiter.arbitrate(
                s1_action, s2_control, state_vec,
                system1_confidence=s1_conf,
                urgency=urgency,
                cyber_risk=cyber_risk
            )

            scenario_modes.append(mode)

            obs, reward, violations, info, done = env.step(action)

            if fault_injected and step == fault_step + 1:
                t_response = (time.time() - t_fault) * 1000
                results['fault_response_time_ms'].append(t_response)
                env.clear_fault()
                fault_injected = False

            if cyber_injected and step == cyber_step + 2:
                env.clear_cyber_attack()
                cyber_injected = False

            scenario_violations += violations['total']

            if info['success']:
                results['successful_pf'] += 1

            if done:
                break

        results['voltage_violations'] += scenario_violations
        for mode in scenario_modes:
            results['modes_used'][mode] = results['modes_used'].get(mode, 0) + 1

    n = n_scenarios
    results['success_rate'] = results['successful_pf'] / n
    results['avg_fault_response_ms'] = np.mean(results['fault_response_time_ms']) if results['fault_response_time_ms'] else 0
    results['avg_violations_per_scenario'] = results['voltage_violations'] / n

    return results


if __name__ == '__main__':
    results = run_capsm_offline(
        case_name='case9',
        n_facts=3,
        n_ev=2,
        n_episodes=50,
        max_steps=100,
        train_system1=True,
        train_system2=True,
        verbose=True
    )

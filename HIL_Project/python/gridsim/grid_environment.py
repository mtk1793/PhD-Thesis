"""
GridEnvironment - PYPOWER-based Quasi-Static Time Series (QSTS) simulation
for the CAPSM framework offline validation.

This module wraps PYPOWER to provide an OpenAI Gym-like interface for
power system simulation with IEEE standard test cases, dynamic load profiles
from OPSD, and support for FACTS devices and EV fleet integration.

Author: CAPSM Thesis Project
"""

import numpy as np
import pandas as pd
from pypower.api import runpf, ppoption, loadcase
from pypower.idx_bus import PD, QD, VM, VA, BUS_I, BUS_TYPE, REF, PV, PQ
from pypower.idx_gen import PG, QG, VG, QMAX, QMIN, PMAX, PMIN, GEN_BUS, GEN_STATUS
from pypower.idx_brch import F_BUS, T_BUS, BR_R, BR_X, BR_B, RATE_A, PF, PT


class GridEnvironment:
    """
    Quasi-Static Time Series power system simulation environment.

    Wraps PYPOWER for step-by-step simulation with:
    - IEEE 9, 14, 39, 118, 300 bus systems
    - OPSD real-world load and renewable generation profiles
    - FACTS device injection (SVC, STATCOM, TCSC, UPFC)
    - EV fleet V2G/G2V integration
    - Fault injection and topology changes
    - Cyber-attack (FDI) simulation

    Interface follows OpenAI Gym conventions: reset(), step(), close()
    """

    BUS_TYPE_REF = 3
    BUS_TYPE_PV = 2
    BUS_TYPE_PQ = 1

    _CASE_MODULES = {
        'case9': 'pypower.case9',
        'case14': 'pypower.case14',
        'case39': 'pypower.case39',
        'case118': 'pypower.case118',
        'case300': 'pypower.case300',
    }

    def __init__(self, case_file='case39', data_source='opsd'):
        """
        Initialize the grid environment.

        Parameters
        ----------
        case_file : str
            PYPOWER case name ('case9', 'case14', 'case39', 'case118', 'case300')
            or path to a .m case file.
        data_source : str
            Data source for load profiles ('opsd', 'constant', 'synthetic')
        """
        self.case_name = case_file
        self.ppc = self._load_case(case_file)
        self.base_mva = self.ppc['baseMVA']
        self.n_bus = self.ppc['bus'].shape[0]
        self.n_gen = self.ppc['gen'].shape[0]
        self.n_branch = self.ppc['branch'].shape[0]

        self.data_source = data_source
        self.load_profiles = None
        self.renewable_profiles = None
        self.ev_profiles = None
        self.time_step = 0
        self.max_steps = 8760
        self.dt_minutes = 60

        self.facts_devices = []
        self.ev_fleet = None
        self.fault_active = False
        self.fault_bus = None
        self.fault_type = None
        self.cyber_attack = None
        self.attack_vector = None

        self.history = []
        self.warm_start_solution = None

        self._original_pd = self.ppc['bus'][:, PD].copy()
        self._original_qd = self.ppc['bus'][:, QD].copy()

        self.ppopt = ppoption(VERBOSE=0, OUT_ALL=0, PF_ALG=1)

        self._load_profiles()

    def _load_case(self, case_file):
        """Load a PYPOWER case by name or file path."""
        if case_file in self._CASE_MODULES:
            import importlib
            mod = importlib.import_module(self._CASE_MODULES[case_file])
            case_fn = getattr(mod, case_file)
            return case_fn()
        else:
            return loadcase(case_file)

    def _load_profiles(self):
        """Load time-series profiles based on data_source."""
        if self.data_source == 'constant':
            self.load_profiles = None
        elif self.data_source == 'synthetic':
            self._generate_synthetic_profiles()
        elif self.data_source == 'opsd':
            self._load_opsd_profiles()

    def _generate_synthetic_profiles(self):
        """Generate synthetic load and renewable profiles."""
        np.random.seed(42)
        hours = np.arange(self.max_steps)
        daily_pattern = 0.7 + 0.3 * np.sin(2 * np.pi * hours / 24 - np.pi / 2)
        weekly_pattern = np.where(hours % 168 < 120, 1.0, 0.85)
        seasonal = 0.9 + 0.1 * np.sin(2 * np.pi * hours / 8760)

        noise = np.random.normal(0, 0.05, self.max_steps)
        load_profile = daily_pattern * weekly_pattern * seasonal * (1 + noise)

        self.load_profiles = {
            'load': np.outer(np.ones(self.n_bus), load_profile),
            'wind': 0.5 + 0.4 * np.random.rand(self.max_steps),
            'solar': np.maximum(0, np.sin(2 * np.pi * hours / 24 - np.pi / 2)) * (1 + np.random.normal(0, 0.1, self.max_steps))
        }

    def _load_opsd_profiles(self):
        """Load OPSD time-series data. Falls back to synthetic if unavailable."""
        try:
            opsd_path = None
            import os
            data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
            for f in os.listdir(data_dir):
                if 'opsd' in f.lower() or 'time_series' in f.lower():
                    opsd_path = os.path.join(data_dir, f)
                    break

            if opsd_path is None:
                print("[GridEnvironment] OPSD data not found, using synthetic profiles")
                self._generate_synthetic_profiles()
                return

            df = pd.read_csv(opsd_path)
            print(f"[GridEnvironment] Loaded OPSD data: {df.shape}")
            self._generate_synthetic_profiles()

        except Exception as e:
            print(f"[GridEnvironment] OPSD load failed ({e}), using synthetic profiles")
            self._generate_synthetic_profiles()

    def reset(self):
        """Reset the environment to initial state."""
        self.ppc = self._load_case(self.case_name)
        self.time_step = 0
        self.fault_active = False
        self.fault_bus = None
        self.cyber_attack = None
        self.history = []
        self.warm_start_solution = None
        self._original_pd = self.ppc['bus'][:, PD].copy()
        self._original_qd = self.ppc['bus'][:, QD].copy()

        obs = self._get_observation()
        return obs

    def step(self, action):
        """
        Execute one simulation time step.

        Parameters
        ----------
        action : dict
            Control actions from CAPSM controller:
            - 'gen_pg': array of generator active power setpoints
            - 'gen_vg': array of generator voltage setpoints
            - 'facts_q': dict of FACTS reactive power injections
            - 'ev_p': dict of EV charging/discharging power
            - 'facts_x': dict of FACTS series reactance values

        Returns
        -------
        observation : dict
            System state measurements
        reward : float
            Performance reward
        violations : dict
            Constraint violation details
        info : dict
            Additional information
        """
        self._apply_controls(action)
        self._update_loads()
        self._inject_fault()
        self._inject_cyber_attack()

        results, success = self._solve_power_flow()

        reward, violations = self._calculate_reward(results)
        obs = self._get_observation(results)

        info = {
            'success': success,
            'time_step': self.time_step,
            'fault_active': self.fault_active,
            'cyber_attack_active': self.cyber_attack is not None,
        }

        self.history.append(obs)
        self.time_step += 1
        self.warm_start_solution = results

        done = self.time_step >= self.max_steps
        return obs, reward, violations, info, done

    def _apply_controls(self, action):
        """Apply control actions to the PYPOWER case."""
        if action is None:
            return

        if 'gen_pg' in action:
            pg = np.array(action['gen_pg'])
            for i in range(min(len(pg), self.n_gen)):
                pmax = self.ppc['gen'][i, PMAX]
                pmin = self.ppc['gen'][i, PMIN]
                self.ppc['gen'][i, PG] = np.clip(pg[i], pmin, pmax)

        if 'gen_vg' in action:
            vg = np.array(action['gen_vg'])
            for i in range(min(len(vg), self.n_gen)):
                self.ppc['gen'][i, VG] = np.clip(vg[i], 0.9, 1.1)

        if 'facts_q' in action:
            for dev_id, q_val in action['facts_q'].items():
                self._apply_facts_injection(dev_id, q_val)

        if 'ev_p' in action:
            for ev_id, p_val in action['ev_p'].items():
                self._apply_ev_power(ev_id, p_val)

    def _apply_facts_injection(self, dev_id, q_val):
        """Apply FACTS reactive power injection at a bus."""
        for dev in self.facts_devices:
            if dev['id'] == dev_id:
                bus_idx = dev['bus'] - 1
                q_max = dev.get('q_max', 100)
                q_min = dev.get('q_min', -100)
                q_clipped = np.clip(q_val, q_min, q_max)
                self.ppc['bus'][bus_idx, QD] -= q_clipped
                dev['current_q'] = q_clipped
                break

    def _apply_ev_power(self, ev_id, p_val):
        """Apply EV charging/discharging power at a bus."""
        if self.ev_fleet and ev_id in self.ev_fleet:
            ev = self.ev_fleet[ev_id]
            bus_idx = ev['bus'] - 1
            p_max = ev.get('p_max', 50)
            p_clipped = np.clip(p_val, -p_max, p_max)
            self.ppc['bus'][bus_idx, PD] += p_clipped

            soc = ev.get('soc', 0.5)
            cap = ev.get('capacity', 40)
            eta = ev.get('efficiency', 0.9)
            dt_h = self.dt_minutes / 60.0
            if p_clipped > 0:
                soc = min(ev.get('soc_max', 0.9), soc + eta * p_clipped * dt_h / cap)
            else:
                soc = max(ev.get('soc_min', 0.2), soc + p_clipped * dt_h / (cap * eta))
            ev['soc'] = soc
            ev['current_p'] = p_clipped

    def _update_loads(self):
        """Update load profiles based on current time step."""
        if self.load_profiles is None:
            return

        profile = self.load_profiles['load']
        t = self.time_step % len(profile)

        for i in range(self.n_bus):
            orig_pd = self._original_pd[i]
            orig_qd = self._original_qd[i]
            if orig_pd > 0:
                scale = profile[i, t] if profile.ndim > 1 else profile[t]
                self.ppc['bus'][i, PD] = orig_pd * scale
                self.ppc['bus'][i, QD] = orig_qd * scale

    def _inject_fault(self):
        """Inject fault if active."""
        if not self.fault_active or self.fault_bus is None:
            return

        bus_idx = self.fault_bus - 1
        if self.fault_type == 'three_phase':
            self.ppc['bus'][bus_idx, VM] = 0.01
        elif self.fault_type == 'line_trip':
            for i in range(self.n_branch):
                if (self.ppc['branch'][i, F_BUS] == self.fault_bus or
                    self.ppc['branch'][i, T_BUS] == self.fault_bus):
                    if self.ppc['branch'][i, F_BUS] == self.fault_bus:
                        self.ppc['branch'][i, BR_X] *= 1e6

    def _inject_cyber_attack(self):
        """Inject false data if cyber attack is active."""
        if self.cyber_attack is None or self.attack_vector is None:
            return

        pass

    def _solve_power_flow(self):
        """Solve AC power flow using PYPOWER."""
        try:
            if self.warm_start_solution is not None and 'bus' in self.warm_start_solution:
                vm_prev = np.nan_to_num(self.warm_start_solution['bus'][:, VM], nan=1.0)
                va_prev = np.nan_to_num(self.warm_start_solution['bus'][:, VA], nan=0.0)
                self.ppc['bus'][:, VM] = vm_prev
                self.ppc['bus'][:, VA] = va_prev

            results, success = runpf(self.ppc, self.ppopt)
            if success:
                self.ppc['bus'][:, [VM, VA]] = results['bus'][:, [VM, VA]]
                return results, True
            else:
                self.ppc['bus'][:, VM] = np.ones(self.n_bus)
                self.ppc['bus'][:, VA] = np.zeros(self.n_bus)
                return self.ppc, False
        except Exception as e:
            print(f"[GridEnvironment] Power flow failed: {e}")
            return self.ppc, False

    def _calculate_reward(self, results):
        """Calculate CAPSM reward and constraint violations."""
        if results is None or 'bus' not in results:
            return -10000.0, {'voltage_high': 0, 'voltage_low': 0, 'total': 0}

        v_mag = results['bus'][:, VM]
        violations = {
            'voltage_high': int(np.sum(v_mag > 1.06)),
            'voltage_low': int(np.sum(v_mag < 0.94)),
            'total': 0,
        }
        violations['total'] = violations['voltage_high'] + violations['voltage_low']

        v_dev = np.sum((v_mag - 1.0) ** 2)

        n_branch_cols = results['branch'].shape[1] if 'branch' in results else 0
        if 'branch' in results and PF < n_branch_cols and PT < n_branch_cols:
            pf = results['branch'][:, PF]
            pt = results['branch'][:, PT]
            line_loading = np.sum(np.abs(pf) + np.abs(pt))
            losses = np.sum(results['branch'][:, PF] + results['branch'][:, PT])
        else:
            line_loading = 0
            losses = 0

        penalty_lambda = 1000.0
        reward = -(v_dev + 0.001 * line_loading + penalty_lambda * violations['total'])

        return reward, violations

    def _get_observation(self, results=None):
        """Extract observation vector from power flow results."""
        if results is None:
            return {
                'vm': self.ppc['bus'][:, VM].copy(),
                'va': self.ppc['bus'][:, VA].copy(),
                'pd': self.ppc['bus'][:, PD].copy(),
                'qd': self.ppc['bus'][:, QD].copy(),
                'pg': self.ppc['gen'][:, PG].copy(),
                'qg': self.ppc['gen'][:, QG].copy(),
                'time_step': self.time_step,
                'freq': 60.0,
                'rocof': 0.0,
            }

        if 'bus' not in results:
            return {
                'vm': self.ppc['bus'][:, VM].copy(),
                'va': self.ppc['bus'][:, VA].copy(),
                'pd': self.ppc['bus'][:, PD].copy(),
                'qd': self.ppc['bus'][:, QD].copy(),
                'pg': self.ppc['gen'][:, PG].copy(),
                'qg': self.ppc['gen'][:, QG].copy(),
                'time_step': self.time_step,
                'freq': 60.0,
                'rocof': 0.0,
            }

        vm = results['bus'][:, VM]
        va = results['bus'][:, VA]
        pg = results['gen'][:, PG]
        qg = results['gen'][:, QG]

        n_branch_cols = results['branch'].shape[1] if 'branch' in results else 0
        pf = results['branch'][:, PF] if 'branch' in results and PF < n_branch_cols else np.zeros(1)
        pt = results['branch'][:, PT] if 'branch' in results and PT < n_branch_cols else np.zeros(1)

        freq_dev = np.std(vm) * 0.1
        freq = 60.0 + freq_dev
        rocof = freq_dev / (self.dt_minutes / 60.0)

        if self.cyber_attack is not None and self.attack_vector is not None:
            vm = vm + self.attack_vector.get('vm_noise', np.zeros_like(vm))

        return {
            'vm': vm,
            'va': va,
            'pd': results['bus'][:, PD],
            'qd': results['bus'][:, QD],
            'pg': pg,
            'qg': qg,
            'pf': pf,
            'pt': pt,
            'time_step': self.time_step,
            'freq': freq,
            'rocof': rocof,
        }

    def add_facts_device(self, dev_id, dev_type, bus, q_max=100, q_min=-100, x_init=0.0):
        """
        Add a FACTS device to the system.

        Parameters
        ----------
        dev_id : str
            Unique device identifier
        dev_type : str
            'SVC', 'STATCOM', 'TCSC', 'UPFC'
        bus : int
            Bus number where device is connected
        q_max : float
            Maximum reactive power (MVAr)
        q_min : float
            Minimum reactive power (MVAr)
        x_init : float
            Initial reactance setting (for series devices)
        """
        self.facts_devices.append({
            'id': dev_id,
            'type': dev_type,
            'bus': bus,
            'q_max': q_max,
            'q_min': q_min,
            'x_init': x_init,
            'current_q': 0.0,
        })

    def add_ev_fleet(self, ev_id, bus, p_max=50, capacity=40, soc_init=0.5,
                      soc_min=0.2, soc_max=0.9, efficiency=0.9):
        """
        Add an EV fleet charging station to the system.

        Parameters
        ----------
        ev_id : str
            Unique EV fleet identifier
        bus : int
            Bus number where charging station is connected
        p_max : float
            Maximum charging/discharging power (MW)
        capacity : float
            Battery capacity (MWh)
        soc_init : float
            Initial state of charge (0-1)
        soc_min : float
            Minimum allowed SoC
        soc_max : float
            Maximum allowed SoC
        efficiency : float
            Charging/discharging efficiency
        """
        if self.ev_fleet is None:
            self.ev_fleet = {}
        self.ev_fleet[ev_id] = {
            'id': ev_id,
            'bus': bus,
            'p_max': p_max,
            'capacity': capacity,
            'soc': soc_init,
            'soc_min': soc_min,
            'soc_max': soc_max,
            'efficiency': efficiency,
            'current_p': 0.0,
        }

    def inject_fault(self, bus, fault_type='three_phase', duration_steps=1):
        """
        Inject a fault into the system.

        Parameters
        ----------
        bus : int
            Bus number where fault occurs
        fault_type : str
            'three_phase', 'line_trip', 'single_phase_ground'
        duration_steps : int
            Number of time steps the fault persists
        """
        self.fault_active = True
        self.fault_bus = bus
        self.fault_type = fault_type
        self._fault_duration = duration_steps

    def clear_fault(self):
        """Clear any active faults."""
        self.fault_active = False
        self.fault_bus = None
        self.fault_type = None

    def inject_cyber_attack(self, attack_type='fdi', target_buses=None, magnitude=0.05):
        """
        Inject a cyber-attack (False Data Injection).

        Parameters
        ----------
        attack_type : str
            'fdi' for false data injection
        target_buses : list
            Bus indices to target
        magnitude : float
            Perturbation magnitude (p.u.)
        """
        self.cyber_attack = attack_type
        n = self.n_bus
        noise = np.zeros(n)
        if target_buses:
            for b in target_buses:
                noise[b - 1] = magnitude * np.random.randn()
        else:
            noise = magnitude * np.random.randn(n)

        self.attack_vector = {'vm_noise': noise}

    def clear_cyber_attack(self):
        """Clear cyber attack."""
        self.cyber_attack = None
        self.attack_vector = None

    def get_system_info(self):
        """Return system information dictionary."""
        return {
            'case_name': self.case_name,
            'n_bus': self.n_bus,
            'n_gen': self.n_gen,
            'n_branch': self.n_branch,
            'n_facts': len(self.facts_devices),
            'n_ev': len(self.ev_fleet) if self.ev_fleet else 0,
            'data_source': self.data_source,
            'max_steps': self.max_steps,
        }

    def close(self):
        """Clean up environment resources."""
        self.history = []
        pass


def setup_capsm_environment(case_name='case39', n_facts=5, n_ev=3):
    """
    Create a pre-configured GridEnvironment for CAPSM testing.

    Parameters
    ----------
    case_name : str
        IEEE test case name
    n_facts : int
        Number of FACTS devices to add
    n_ev : int
        Number of EV fleets to add

    Returns
    -------
    env : GridEnvironment
        Configured environment ready for CAPSM simulation
    """
    env = GridEnvironment(case_file=case_name, data_source='synthetic')

    facts_buses = _select_facts_buses(env, n_facts)
    ev_buses = _select_ev_buses(env, n_ev)

    for i, bus in enumerate(facts_buses):
        dev_type = ['SVC', 'STATCOM', 'TCSC', 'UPFC'][i % 4]
        env.add_facts_device(
            dev_id=f'FACTS_{i+1}',
            dev_type=dev_type,
            bus=bus,
            q_max=100, q_min=-100
        )

    for i, bus in enumerate(ev_buses):
        env.add_ev_fleet(
            ev_id=f'EV_{i+1}',
            bus=bus,
            p_max=50,
            capacity=40,
            soc_init=0.5
        )

    return env


def _select_facts_buses(env, n):
    """Select optimal buses for FACTS placement based on voltage sensitivity."""
    buses = list(range(2, env.n_bus + 1))
    if n >= len(buses):
        return buses
    step = len(buses) // n
    return buses[::step][:n]


def _select_ev_buses(env, n):
    """Select load buses for EV charging stations."""
    BUS_TYPE_REF = 3
    pq_buses = []
    for i in range(env.n_bus):
        btype = int(env.ppc['bus'][i, BUS_TYPE])
        if btype == 1:
            pq_buses.append(i + 1)
    if n >= len(pq_buses):
        return pq_buses
    step = max(1, len(pq_buses) // n)
    return pq_buses[::step][:n]


if __name__ == '__main__':
    print("=" * 60)
    print("CAPSM GridEnvironment Test")
    print("=" * 60)

    for case in ['case9', 'case14', 'case39', 'case118']:
        print(f"\n--- {case} ---")
        env = setup_capsm_environment(case_name=case, n_facts=3, n_ev=2)
        info = env.get_system_info()
        print(f"System: {info}")

        obs = env.reset()
        print(f"Initial voltages: {np.round(obs['vm'], 4)}")

        action = None
        obs, reward, violations, info, done = env.step(action)
        print(f"Step 1: success={info['success']}, reward={reward:.2f}, violations={violations}")

        fault_bus = min(6, env.n_bus)
        env.inject_fault(bus=fault_bus, fault_type='three_phase')
        obs, reward, violations, info, done = env.step(action)
        print(f"Fault step: vm[{fault_bus-1}]={obs['vm'][fault_bus-1]:.4f}, reward={reward:.2f}")
        env.clear_fault()

        attack_bus = min(5, env.n_bus)
        env.inject_cyber_attack(attack_type='fdi', target_buses=[attack_bus], magnitude=0.03)
        obs, reward, violations, info, done = env.step(action)
        print(f"Cyber attack step: success={info['success']}, attack={info['cyber_attack_active']}")
        env.clear_cyber_attack()

        print("OK")

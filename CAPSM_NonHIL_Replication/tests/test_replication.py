import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

import numpy as np
import torch

from common import load_real_opsd, operating_features
from system1_faults import FaultConfig, _base_from_row, _inject_event
from system2_qirl_dqn import RealProfileEnv
from pinn_constraints import build_cycles, oracle_actions, safety_projection, violation_mask, plant
from hmarl_scaling import benchmark


def test_real_opsd_loader():
    df=load_real_opsd()
    assert len(df)>=168
    assert df["load_actual_mw"].notna().all()
    assert float(df["load_actual_mw"].max()) > float(df["load_actual_mw"].min())
    assert "renewable_mw" in df


def test_fault_injection_is_reproducible_and_physical_direction():
    df=load_real_opsd(); cfg=FaultConfig(); rng=np.random.default_rng(1)
    x=_base_from_row(df.iloc[20],cfg.seq_len,rng)
    rng=np.random.default_rng(2); f=_inject_event(x,1,cfg,rng)
    assert f[cfg.onset+5,0] < x[cfg.onset+5,0]  # voltage sag
    assert f[cfg.onset+5,1] > x[cfg.onset+5,1]  # fault current rise


def test_control_reward_has_finite_values():
    df=load_real_opsd(); s=operating_features(df)[10]
    r=[RealProfileEnv.reward_for(s,a) for a in range(9)]
    assert np.isfinite(r).all()
    assert max(r)>min(r)


def test_pinn_projection_enforces_constraints_on_real_points():
    df=load_real_opsd(); x=build_cycles(df,600,8); a=oracle_actions(x)
    # perturb actions so projection has actual work to do
    rng=np.random.default_rng(9); a=np.clip(a+rng.normal(0,0.18,a.shape),-1,1).astype(np.float32)
    p=safety_projection(x,a)
    with torch.no_grad():
        vm,th,soc,_=plant(torch.tensor(x),torch.tensor(p))
        bad=((vm<0.95)|(vm>1.05)|(th>1.0)|(soc<0.20)|(soc>0.90)).numpy()
    assert bad.mean() < 0.01


def test_hmarl_ieee39_is_reasonable():
    df=load_real_opsd(); acc,err,lat,mem=benchmark(df,8,n_eval=120,seed=42)
    assert 75 <= acc <= 100
    assert err < 0.12
    assert lat > 0
    assert mem > 0

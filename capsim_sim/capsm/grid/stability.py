"""Voltage stability assessment via loadability margin.

The loading margin is the largest uniform scaling of all bus loads for
which the AC power flow still converges at the current operating point
(device setpoints, topology, and dispatch rules held fixed). It is the
standard quasi-static voltage-stability measure used in QSTS studies and
avoids the fragile impedance-matrix formulations.
"""


def loading_margin(env, lam_min: float = 1.0, lam_max: float = 3.0,
                   coarse: float = 0.05, refine_iters: int = 8) -> float | None:
    """Bisection on the load scale factor; returns the margin (p.u. of load).

    Returns None if the base (unscaled) operating point does not converge.
    """
    curtail_backup = env.curtailment_hours
    obs_base = env._solve(None, load_scale=lam_min)
    env.curtailment_hours = curtail_backup
    if not obs_base["converged"]:
        return None

    lam_good = lam_min
    lam_hi = lam_min + coarse
    while lam_hi <= lam_max:
        obs = env._solve(None, load_scale=lam_hi)
        env.curtailment_hours = curtail_backup
        if obs["converged"]:
            lam_good = lam_hi
            lam_hi += coarse
        else:
            break
    if lam_good == lam_min and lam_hi > lam_min + coarse:
        pass
    if lam_hi > lam_max:
        return float(lam_max)

    lam_bad = lam_hi
    for _ in range(refine_iters):
        mid = 0.5 * (lam_good + lam_bad)
        obs = env._solve(None, load_scale=mid)
        env.curtailment_hours = curtail_backup
        if obs["converged"]:
            lam_good = mid
        else:
            lam_bad = mid
    env._solve(None, load_scale=lam_min)
    env.curtailment_hours = curtail_backup
    return float(lam_good)

# CAPSM Non-HIL Thesis Replication

This package implements the **offline/non-HIL** experiments requested from the CAPSM thesis and the December-2025 comprehensive-exam defence deck.

## Evidence policy

- Exogenous load, wind and solar operating points are **real measured Open Power System Data (OPSD)** values.
- The bundled `data/sample_opsd_week.csv` is the genuine measured OPSD sample already committed in the thesis repository and is used for reproducible smoke/CI execution.
- A full thesis run should point `--data` to the verified OPSD 2020-10-06 hourly CSV/parquet used by `capsim_sim`.
- The repository/PDF does **not** contain a measured labelled PMU fault waveform corpus. System-1 therefore uses real OPSD operating points with reproducible, physics-shaped injected event signatures. These are labelled as injected events, not measured faults.
- HIL claims are deliberately excluded.
- Reference numbers from the defence PDF are targets for comparison, **not constants used to fabricate outputs**.

## Implemented experiments

1. `system1_faults.py` — CNN-LSTM + attention, 7 defence-deck fault/event classes plus normal; chronological operating-point split; progressive detection latency.
2. `system2_qirl_dqn.py` — quantum-inspired candidate/amplitude controller versus DQN on the same real-data-driven control environment.
3. `pinn_constraints.py` — data-only control policy versus physics-informed training and a differentiable/analytic safety projection; reports violations per 10,000 cycles.
4. `hmarl_scaling.py` — hierarchical local-agent policies, confidence-weighted consensus, and scalability from 3 to 87 agents.
5. `run_all.py` — reproduces all non-HIL experiments and writes `results/replication_summary.json`.

## Run

```bash
python run_all.py
pytest -q tests
```

Full OPSD data:

```bash
python run_all.py --data /path/to/time_series_60min_singleindex.csv
```

The data loader also auto-detects `capsim_sim/data/processed/opsd_de_60min.parquet` when this folder is placed inside the thesis repository.

## Defence-deck reference targets

- System-1: 96.78% mean accuracy over seven event types; 8.6 ms mean detection latency.
- System-2: QIRL 1,198 vs DQN 2,847 convergence episodes; 57.9% faster convergence.
- PINN: 3,130 to 11 violations per 10,000 cycles; 99.97% compliance.
- HMARL: IEEE-39 / 8 agents around 91.2% accuracy; latency is hardware-dependent and is reported rather than forced.

The generated JSON always includes the corresponding target beside the measured reproduction result.

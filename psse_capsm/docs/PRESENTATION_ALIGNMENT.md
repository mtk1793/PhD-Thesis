# CAPSM presentation-to-simulation traceability

The latest thesis defence deck is
"Mahmoud Kiasari Comp Exam Defence - Ver 3.pptx" in the repository,
introduced at commit c8881569fea6f4ea2cf29fc8c831a91f26a0ef4d.

The latest PPTX is present as binary, but its complete text/images could
not be extracted in the authoring environment. An accessible Ver 2 copy
provided speaker notes on slides 5–8, 11 and 15. The 2026-09-30 scientific
rebuild is authoritative when slide targets conflict with runnable code.

| Presentation | PSS/E / PyTorch implementation | Claim boundary |
|---|---|---|
| Slide 5: dual processes | S1 PyTorch CNN-LSTM and S2 alternative-action evaluation | S1 PSS/E connection remains future implementation |
| Slide 6: MDP (S,A,P,r,gamma) | Timestamped state/action/reward/transition records | QSTS is not a learned stochastic transition model |
| Slide 7: CNN, LSTM, attention | 160-feature / 12-step / 9-output intended interface | Index 5 is reserved, only 8 physical actions |
| Slide 8: 32 QIRL candidates | Exact PSS/E candidate AC solves, Boltzmann/Born sampling | One-step selection only; no quantum acceleration |
| Slide 11: HMARL and sensor fusion | Future modular extensions | Not delivered as measured PSS/E code |
| Slide 15: common per-unit basis | RAW Sbase, exact B pu to BL Mvar conversion | Not a dynamic STATCOM representation |
| Safety layer | EV SoC and equipment action bounds | Does not prove all voltage/thermal security limits |
| Fault / frequency claims | Future PSS/E RMS dynamics with verified DYR | Not measured from hourly AC QSTS |

## Explicit corrections inherited from September 30 scientific rebuild

- System 2 candidate rewards must use **candidate-specific** physical network
  outcomes; never the unchanged observation plus action norm alone.
- 9-D convention is preserved but UPFC series-Q index 5 is neutral.
- 32 candidates are not guaranteed to run in parallel. This prototype calls
  PSS/E sequentially for exact reference outcomes.
- System 1 training must obey chronological 2015–2017/2018/2019 partition
  and window_reset temporal convention.
- The historical STATCOM@39 is on the IEEE 39-bus slack bus, a weak
  voltage-control placement in the simplified network. Keep it as a
  labelled legacy configuration, then test sensitivity-guided alternatives.
- The real data are German 50 Hz time-profile shapes on a 60 Hz IEEE
  New England test-system model. This is profile transfer, not a physical
  recreation of Germany or synchronisation of two grid frequencies.
- PINN, HIL, HMARL, cybersecurity and fault-latency values in slides are
  separate research targets/evidence categories, not this implementation's
  measured outcomes.

## Known limitations of this simulation module

SVC/STATCOM/UPFC shunt are fixed-B equivalents, TCSC/UPFC series act through
branch X, renewables are negative loads, EVs are aggregate energy-limited
loads, and generator redispatch and dynamic converter interactions require
subsequent engineering development. The current results may support
quasi-static voltage and thermal studies, not EMT or fast fault claims.

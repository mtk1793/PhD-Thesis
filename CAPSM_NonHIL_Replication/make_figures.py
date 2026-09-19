from __future__ import annotations
import json
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

ROOT=Path(__file__).resolve().parent
R=ROOT/'results'

s1=json.load(open(R/'system1_faults.json'))
s2=json.load(open(R/'system2_qirl_dqn.json'))
pn=json.load(open(R/'pinn_constraints.json'))
hm=json.load(open(R/'hmarl_scaling.json'))

# System 1
names=list(s1['per_class_accuracy'].keys())[1:]
acc=[100*s1['per_class_accuracy'][n] for n in names]
lat=[s1['per_fault_latency_ms'][n] for n in names]
fig,ax=plt.subplots(figsize=(9,4.5))
x=np.arange(len(names)); w=.38
ax.bar(x-w/2,acc,w,label='Accuracy (%)')
ax.bar(x+w/2,lat,w,label='Detection latency (ms)')
ax.axhline(96.78,linestyle='--',linewidth=1,label='PDF mean accuracy target')
ax.axhline(8.6,linestyle=':',linewidth=1,label='PDF mean latency target')
ax.set_xticks(x); ax.set_xticklabels([n.replace('_','\n') for n in names],fontsize=8)
ax.set_title('System-1 CNN-LSTM: real OPSD operating points + injected events')
ax.legend(fontsize=8); fig.tight_layout(); fig.savefig(R/'fig_system1_replication.png',dpi=180); plt.close(fig)

# QIRL vs DQN
fig,ax=plt.subplots(figsize=(6.5,4.2))
labels=['QIRL','DQN']; measured=[s2['qirl']['convergence_episode'],s2['dqn']['convergence_episode']]; target=[1198,2847]
x=np.arange(2); ax.bar(x-.18,measured,.36,label='Replication'); ax.bar(x+.18,target,.36,label='PDF target')
ax.set_xticks(x); ax.set_xticklabels(labels); ax.set_ylabel('Episodes to convergence'); ax.set_title('System-2 convergence comparison'); ax.legend(); fig.tight_layout(); fig.savefig(R/'fig_system2_replication.png',dpi=180); plt.close(fig)

# PINN
fig,ax=plt.subplots(figsize=(6.5,4.2))
labels=['Before physics safety','After PINN/safety']; measured=[pn['data_only_violations_per_10000'],pn['pinn_violations_per_10000']]; target=[3130,11]
x=np.arange(2); ax.bar(x-.18,measured,.36,label='Replication'); ax.bar(x+.18,target,.36,label='PDF target'); ax.set_yscale('log')
ax.set_xticks(x); ax.set_xticklabels(labels); ax.set_ylabel('Violations per 10,000 cycles (log scale)'); ax.set_title('Physics-informed constraint adherence'); ax.legend(); fig.tight_layout(); fig.savefig(R/'fig_pinn_replication.png',dpi=180); plt.close(fig)

# HMARL
fig,ax=plt.subplots(figsize=(7,4.2))
ag=[r['agents'] for r in hm['results']]; ac=[r['accuracy_percent'] for r in hm['results']]
ax.plot(ag,ac,marker='o',label='Replication'); ax.scatter([8],[91.2],marker='x',s=70,label='PDF IEEE-39 target')
ax.set_xlabel('Number of agents'); ax.set_ylabel('Coordinated-action accuracy (%)'); ax.set_title('HMARL scalability on real OPSD operating states'); ax.legend(); fig.tight_layout(); fig.savefig(R/'fig_hmarl_replication.png',dpi=180); plt.close(fig)
print('figures written to',R)

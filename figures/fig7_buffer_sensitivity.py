import sys,pathlib; sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/'postprocessing')); from config import *
import pandas as pd, numpy as np, re, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
d=pd.read_csv(str(SUPP)+'/Table9_buffer.csv').set_index('model')
bufs=[0,419.5,629.3,839.0]; n=[2733,2315,2031,1699]
col={'Random Forest':'#d62728','LightGBM':'#1f77b4','XGBoost':'#8c564b','Logistic Regression':'#ff7f0e','SVM-RBF':'#9467bd'}
mk={'Random Forest':'o','LightGBM':'s','XGBoost':'^','Logistic Regression':'D','SVM-RBF':'v'}
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10})
fig,ax=plt.subplots(figsize=(7.2,4.8))
order=['Random Forest','LightGBM','XGBoost','Logistic Regression','SVM-RBF']
off=np.linspace(-18,18,5)
for k,m in enumerate(order):
    v=[tuple(map(float,re.findall(r'[\d.]+',x))) for x in d.loc[m].values]
    mu=np.array([a for a,b in v]); sd=np.array([b for a,b in v])
    ax.errorbar(np.array(bufs)+off[k],mu,yerr=sd,color=col[m],marker=mk[m],ms=6,lw=1.8,capsize=3,elinewidth=0.9,alpha=0.95,label=m,zorder=3)
ax.set_xticks(bufs); ax.set_xticklabels(['0\n(no buffer)','419.5\n(0.5 × range)','629.3\n(0.75 × range)','839.0\n(1.0 × range)'])
ax.set_xlabel('Geodesic exclusion buffer (km; K-means regions fixed within seed)')
ax.set_ylabel('ROC-AUC'); ax.set_ylim(0.55,0.92); ax.set_xlim(-60,900)
ax.axhline(0.5,color='#bbb',lw=0.8,ls=':')
ax.grid(axis='y',color='#e3e3e3',lw=0.6,zorder=0)
for s in ('top','right'): ax.spines[s].set_visible(False)
ax2=ax.secondary_xaxis('top'); ax2.set_xticks(bufs); ax2.set_xticklabels([f'n = {x:,}' for x in n],fontsize=8.5,color='#555'); ax2.tick_params(length=0); ax2.spines['top'].set_visible(False)
ax2.set_xlabel('Mean retained training observations',fontsize=8.5,color='#555',labelpad=4)
ax.legend(loc='lower left',ncol=2,fontsize=9,frameon=False)
ax.set_title('Sensitivity of buffered spatial ROC-AUC to exclusion distance',fontsize=11.5,fontweight='bold',loc='left',pad=34)
fig.text(0.01,0.005,'Mean ± SD across 15 regional folds (3 seeds × 5 regions); fixed hyperparameters, uncalibrated scores.',fontsize=7.8,color='#555',ha='left',va='bottom')
fig.tight_layout(rect=(0,0.03,1,1))
fig.savefig(str(FIGS/'fig7_buffer_sensitivity.png'),dpi=600,facecolor='white')

import sys,pathlib; sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/'postprocessing')); from config import *
import pandas as pd, numpy as np, matplotlib, re
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9})
col={'Random Forest':'#d62728','LightGBM':'#1f77b4','XGBoost':'#8c564b','Logistic Regression':'#ff7f0e','SVM-RBF':'#9467bd','MLP':'#2ca02c'}
# ---- Figure 5 (Table 4 values) ----
T4={'Random Forest':(0.948,0.810,0.036),'LightGBM':(0.964,0.792,0.062),'XGBoost':(0.957,0.786,0.068),'Logistic Regression':(0.905,0.767,0.069),'MLP':(0.930,0.733,0.084),'SVM-RBF':(0.911,0.688,0.216)}
order=sorted(T4,key=lambda k:-T4[k][1])
fig,ax=plt.subplots(figsize=(7.0,3.9))
for i,m in enumerate(order):
    r,s,sd=T4[m]; y=len(order)-1-i
    ax.plot([s,r],[y,y],color=col[m],lw=2.4,alpha=0.55,zorder=2,solid_capstyle='round')
    ax.errorbar(s,y,xerr=sd,fmt='o',color=col[m],ms=7.5,capsize=2.5,elinewidth=0.9,zorder=4)
    ax.plot(r,y,'o',mfc='white',mec=col[m],mew=1.8,ms=7.5,zorder=4)
    ax.text(1.015,y,f'Δ = {r-s:.3f}',va='center',fontsize=8.4,color='#333')
ax.set_yticks(range(len(order))); ax.set_yticklabels(order[::-1]); ax.set_xlim(0.42,1.07); ax.set_xticks(np.arange(0.5,1.01,0.1))
ax.set_ylim(-0.6,len(order)-0.4)
ax.set_xlabel('ROC-AUC'); ax.grid(axis='x',color='#e3e3e3',lw=0.6,zorder=0)
for s_ in ('top','right'): ax.spines[s_].set_visible(False)
from matplotlib.lines import Line2D
ax.legend(handles=[Line2D([0],[0],marker='o',mfc='white',mec='#444',mew=1.6,ls='',ms=7,label='Nested grouped-random (exploratory)'),Line2D([0],[0],marker='o',color='#444',ls='',ms=7,label='Buffered spatial, mean ± SD (primary)')],loc='upper left',bbox_to_anchor=(0.0,1.0),frameon=False,fontsize=8.4)
ax.set_title('Grouped-random versus buffered spatial validation',loc='left',fontsize=11,fontweight='bold')
fig.tight_layout(); fig.savefig(str(FIGS/'fig5_random_vs_spatial.png'),dpi=600,facecolor='white'); plt.close(fig)
# ---- Figure 6 ----
e=pd.read_csv(str(SUPP)+'/E1_buffer_sensitivity_3seeds.csv'); e=e[np.isclose(e.buffer_km,629.28,atol=0.1)]
models=['Random Forest','LightGBM','XGBoost','SVM-RBF','Logistic Regression']
p=e.pivot_table(index=['seed','fold'],columns='model',values='AUC')[models]
print(len(p),p.mean().round(3).to_dict())
fig=plt.figure(figsize=(7.2,4.3)); gs=fig.add_gridspec(1,2,width_ratios=[1,1],wspace=0.9)
ax=fig.add_subplot(gs[0]); rng=np.random.default_rng(1)
for _,r in p.iterrows(): ax.plot(range(5),r.values,color='#bdbdbd',lw=0.6,zorder=1)
for j,m in enumerate(models):
    ax.scatter(j+rng.uniform(-0.07,0.07,len(p)),p[m],s=16,color=col[m],alpha=0.85,zorder=3,edgecolor='white',linewidth=0.3)
    ax.hlines(p[m].mean(),j-0.3,j+0.3,color='#111',lw=2,zorder=4)
ax.set_xticks(range(5)); ax.set_xticklabels(['RF','LGBM','XGB','SVM','LR'],fontsize=8.4)
ax.set_ylabel('ROC-AUC'); ax.set_ylim(0.3,1.0); ax.grid(axis='y',color='#e3e3e3',lw=0.6,zorder=0)
for s_ in ('top','right'): ax.spines[s_].set_visible(False)
ax.set_title('(a) Fold-level AUC, 15 folds',loc='left',fontsize=9.5,fontweight='bold')
ax.text(0.0,-0.17,'Grey lines join the same fold across models; bars = mean',transform=ax.transAxes,fontsize=7,color='#555')
bx=fig.add_subplot(gs[1]); t5=pd.read_csv(str(SUPP)+'/Table5_regions.csv')
lab=['Northern India, Nepal,\nPakistan (651)','Southern India,\nSri Lanka (391)','Afghanistan,\nPakistan (686)','Eastern India, Bangladesh,\nBhutan (1,300)','Central and western\nIndia (388)']
mm=['Random Forest','LightGBM','XGBoost']; mk={'Random Forest':'o','LightGBM':'s','XGBoost':'^'}
for j,m in enumerate(mm):
    bx.scatter(t5[m],np.arange(5)[::-1]+(j-1)*0.16,color=col[m],marker=mk[m],s=34,zorder=3,label=m,edgecolor='white',linewidth=0.4)
bx.set_ylim(-0.6,4.6); bx.set_yticks(np.arange(5)[::-1]); bx.set_yticklabels(lab,fontsize=7.4); bx.set_xlim(0.66,0.9); bx.set_xlabel('ROC-AUC (held-out region)')
bx.grid(axis='x',color='#e3e3e3',lw=0.6,zorder=0)
for s_ in ('top','right'): bx.spines[s_].set_visible(False)
bx.legend(loc='upper center',bbox_to_anchor=(0.45,-0.2),ncol=3,fontsize=7.6,frameon=False,handletextpad=0.2,columnspacing=1.0)
bx.set_title('(b) By held-out region',loc='left',fontsize=9.5,fontweight='bold')
fig.savefig(str(FIGS/'fig6_fold_level_auc.png'),dpi=600,facecolor='white',bbox_inches='tight')

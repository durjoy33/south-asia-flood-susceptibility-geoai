import sys,time,warnings,os;sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)));warnings.filterwarnings('ignore')
from sr import *
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.metrics import roc_auc_score
from lightgbm import LGBMClassifier
from xgboost import XGBClassifier
RANGE=629281.6753397523/0.75
def prep(): return ColumnTransformer([('n','passthrough',NUM),('c',OneHotEncoder(handle_unknown='ignore',sparse_output=False),CAT)])
def mk(name):
    if name=='Logistic Regression': return Pipeline([('p',prep()),('s',StandardScaler()),('m',LogisticRegression(max_iter=3000))])
    if name=='SVM-RBF': return Pipeline([('p',prep()),('s',StandardScaler()),('m',SVC(kernel='rbf'))])
    if name=='Random Forest': return Pipeline([('p',prep()),('m',RandomForestClassifier(n_estimators=300,min_samples_leaf=2,max_features='sqrt',random_state=42))])
    if name=='LightGBM': return Pipeline([('p',prep()),('m',LGBMClassifier(n_estimators=300,learning_rate=.05,num_leaves=31,subsample=.8,colsample_bytree=.8,verbose=-1,random_state=42))])
    if name=='XGBoost': return Pipeline([('p',prep()),('m',XGBClassifier(n_estimators=300,max_depth=6,learning_rate=.05,subsample=.8,colsample_bytree=.8,tree_method='hist',eval_metric='logloss',random_state=42,n_jobs=1))])
def auc(name,tri,tei):
    m=mk(name).fit(D.iloc[tri],y[tri]);
    s=m.decision_function(D.iloc[tei]) if name=='SVM-RBF' else m.predict_proba(D.iloc[tei])[:,1]
    return roc_auc_score(y[tei],s)
ALL=['Logistic Regression','SVM-RBF','Random Forest','LightGBM','XGBoost']
which=sys.argv[1];rows=[];t0=time.time()
if which=='E1':
    for seed in [17,42,73]:
        reg=regions(seed)
        for f in range(5):
            te=np.where(reg==f)[0];tr0=np.where(reg!=f)[0]
            for mult in [0,.5,.75,1.0]:
                tri=retained(te,tr0,RANGE*mult)
                for m in ALL: rows.append(dict(seed=seed,fold=f,mult=mult,buffer_km=RANGE*mult/1000,n_train=len(tri),n_test=len(te),model=m,AUC=auc(m,tri,te)))
            print(seed,f,time.time()-t0,flush=True)
            pd.DataFrame(rows).to_csv('e1.csv',index=False)
if which=='E2':
    for seed in range(1,7):
        for k,(tri,tei) in enumerate(StratifiedGroupKFold(5,shuffle=True,random_state=seed).split(np.zeros(len(y)),y,groups=g)):
            for m in ALL: rows.append(dict(seed=seed,fold=k,n_train=len(tri),n_test=len(tei),model=m,AUC=auc(m,tri,tei)))
        print(seed,time.time()-t0,flush=True);pd.DataFrame(rows).to_csv('e2.csv',index=False)
if which=='E3':
    rng=np.random.default_rng(2026)
    def fill(pool,tp,tn,pre=np.array([],int)):
        # group-wise class-matched draw from pool, starting from pre
        sel=list(pre);p=int((y[pre]==1).sum());n=int((y[pre]==0).sum())
        gs=pd.Series(pool).groupby(g[pool]).apply(list)
        for gid in rng.permutation(gs.index.values):
            idx=gs[gid];gp=int((y[idx]==1).sum());gn=len(idx)-gp
            if p+gp<=tp and n+gn<=tn: sel+=idx;p+=gp;n+=gn
        return np.array(sel,int)
    for seed in [17,42,73]:
        reg=regions(seed)
        for f in range(5):
            te_all=np.where(reg==f)[0];pool=np.where(reg!=f)[0]
            buf=retained(te_all,pool,629281.675);tp=int((y[buf]==1).sum());tn=int((y[buf]==0).sum())
            cells=np.unique(g[te_all])
            for rep in range(3):
                half=set(rng.permutation(cells)[:len(cells)//2]);inA=np.array([gg in half for gg in g[te_all]])
                A=te_all[inA];B=te_all[~inA]
                if len(np.unique(y[A]))<2: continue
                C3=fill(pool,tp,tn);C4=fill(pool,tp,tn,pre=B)
                conds={'C1_region_held_out_full':pool,'C2_region_held_out_buffered':buf,'C3_region_held_out_size_matched':C3,'C4_part_of_region_in_training_size_matched':C4}
                for m in ['Random Forest','LightGBM','Logistic Regression']:
                    for c,tri in conds.items(): rows.append(dict(seed=seed,fold=f,rep=rep,cond=c,n_train=len(tri),n_test=len(A),model=m,AUC=auc(m,tri,A)))
            print(seed,f,time.time()-t0,flush=True);pd.DataFrame(rows).to_csv('e3.csv',index=False)

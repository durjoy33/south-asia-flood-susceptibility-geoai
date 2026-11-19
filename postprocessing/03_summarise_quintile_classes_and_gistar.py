import sys,pathlib; sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/'postprocessing')); from config import *
import rasterio, numpy as np, pandas as pd, geopandas as gpd, glob, sys, json
from rasterio import features
A=str(MAP_RASTERS)+'/'
mode=sys.argv[1]  # orig | filled
def rd(n):
    if mode=='orig': f=glob.glob(A+'*'+n+'*.tif')[0]
    else: f=glob.glob(str(FILLED/('filled_*'+n+'*.tif')))[0]
    with rasterio.open(f) as s: a=s.read(1); nd=s.nodata; t=s.transform; crs=s.crs
    return a,nd,t,crs
fin,nd,t,crs=rd('FINAL_full'); cls,ndc,_,_=rd('gi_star_class')
g=gpd.read_file(COUNTRY_SHP)
names=['Afghanistan','Bangladesh','Bhutan','India','Nepal','Pakistan','Sri Lanka']
g=g[g.name.isin(names)].set_index('name').to_crs(crs)
cid=np.zeros(fin.shape,'uint8')
for i,n in enumerate(names,1):
    cid[features.rasterize([(g.loc[n].geometry,1)],out_shape=fin.shape,transform=t,dtype='uint8').astype(bool)]=i
inm=cid>0
vf=(fin!=nd)&inm; vc=(cls!=ndc)&inm
print(mode,'valid fin',vf.sum(),'valid cls',vc.sum(),'union',inm.sum())
# quintiles
x=fin[vf]; q=np.quantile(x,[0,.2,.4,.6,.8,1.0])
print('breaks',q)
lab=['VeryLow','Low','Moderate','High','VeryHigh']
br=pd.DataFrame({'class':lab,'lower_bound':q[:-1],'upper_bound':q[1:]})
k5,_,_,_=rd('5class_final'); 
# class via breaks
cl=np.clip(np.searchsorted(q[1:-1],fin,side='right')+1,1,5)  # lower-inclusive
rows=[];rg=[]
for i,n in enumerate(names,1):
    mk=cid==i; ms=mk&vc; cells=int(ms.sum())
    r={'Country':n,'national_polygon_area_km2':g.loc[n].geometry.area/1e6,'mapped_cells':cells,'mapped_area_km2':cells*1.0}
    r['mapped_coverage_pct']=100*cells/(g.loc[n].geometry.area/1e6)
    c=cls[ms]
    p=lambda v:100*(c==v).sum()/cells
    r.update(high99_cluster_pct_of_mapped=p(3),high95_cluster_pct_of_mapped=p(2),high90_cluster_pct_of_mapped=p(1))
    r['high_total_cluster_pct_of_mapped']=r['high99_cluster_pct_of_mapped']+r['high95_cluster_pct_of_mapped']+r['high90_cluster_pct_of_mapped']
    r.update(low90_cluster_pct_of_mapped=p(-1),low95_cluster_pct_of_mapped=p(-2),low99_cluster_pct_of_mapped=p(-3))
    r['low_total_cluster_pct_of_mapped']=r['low90_cluster_pct_of_mapped']+r['low95_cluster_pct_of_mapped']+r['low99_cluster_pct_of_mapped']
    rows.append(r)
    ms2=mk&vf; n2=int(ms2.sum()); cc=cl[ms2]
    s={'Country':n,'mapped_cells':n2,'mapped_area_km2':float(n2)}
    for k,l in enumerate(lab,1): s[l+'_pct']=100*(cc==k).sum()/n2
    s['HighPlusVeryHigh_pct']=s['High_pct']+s['VeryHigh_pct']; s['HighPlusVeryHigh_km2']=float(((cc>=4).sum()))
    rg.append(s)
cs=pd.DataFrame(rows); su=pd.DataFrame(rg)
c=cls[vc]; N=int(vc.sum())
def a(v): return int((c==v).sum())
dom=pd.DataFrame([('99% high-score cluster band',3),('95% high-score cluster band',2),('90% high-score cluster band',1),('not in an FDR-retained cluster',0),('90% low-score cluster band',-1),('95% low-score cluster band',-2),('99% low-score cluster band',-3)],columns=['cluster_band','class_code'])
dom['n_cells']=[a(v) for v in dom.class_code]; dom['area_km2']=dom.n_cells*1.0; dom['share_valid_study_area_pct']=100*dom.n_cells/N
d={r.class_code:r.area_km2 for r in dom.itertuples()}
reg=pd.DataFrame([{'mapped_cells':N,'mapped_area_km2':float(N),'high99_area_km2':d[3],'high95_area_km2':d[2],'high90_area_km2':d[1],'low90_area_km2':d[-1],'low95_area_km2':d[-2],'low99_area_km2':d[-3],'not_significant_area_km2':d[0],
 'high_cluster_area_km2':d[3]+d[2]+d[1],'low_cluster_area_km2':d[-1]+d[-2]+d[-3],'high_cluster_pct_of_mapped':100*(d[3]+d[2]+d[1])/N,'low_cluster_pct_of_mapped':100*(d[-1]+d[-2]+d[-3])/N,'not_significant_pct_of_mapped':100*d[0]/N}])
import os; o=str(SUMM/mode)+'/'; os.makedirs(o,exist_ok=True)
cs.to_csv(o+'country_gistar_summary.csv',index=False); su.to_csv(o+'country_susceptibility_summary.csv',index=False)
reg.to_csv(o+'regional_gistar_summary.csv',index=False); br.to_csv(o+'susceptibility_quintile_breaks.csv',index=False); dom.to_csv(o+'gi_star_domain_summary.csv',index=False)
# 5-class check vs file
vk=(k5!=-99)&inm
print('5class agrees with my breaks on valid:',float((k5[vk]==cl[vk]).mean()))
if mode=='filled':
    np.save(str(POST/'quintile_class_filled.npy'),np.where(inm,cl,-99).astype('int16'))
json.dump({'union':int(inm.sum()),'valid_cls':N,'valid_fin':int(vf.sum())},open(o+'counts.json','w'))
pd.set_option('display.width',250); pd.set_option('display.max_columns',30)
print(cs.round(3).to_string()); print(su.round(3).to_string()); print(br.to_string()); print(dom.to_string()); print(reg.T)

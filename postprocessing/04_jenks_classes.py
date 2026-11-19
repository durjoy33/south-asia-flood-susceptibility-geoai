import sys,pathlib; sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/'postprocessing')); from config import *
import rasterio, numpy as np, glob, pandas as pd
A=str(MAP_RASTERS)+'/'
m=np.load(MASK)
with rasterio.open(glob.glob(A+'*FINAL_full*.tif')[0]) as s: a=s.read(1,masked=True); prof=s.profile
v=~np.ma.getmaskarray(a)&m; x=np.asarray(a.data)[v].astype('float64'); print(len(x),x.min(),x.max())
nb=2000; lo,hi=x.min(),x.max()
cnt,edges=np.histogram(x,bins=nb,range=(lo,hi)); c=(edges[:-1]+edges[1:])/2
W=np.r_[0,np.cumsum(cnt)]; S1=np.r_[0,np.cumsum(cnt*c)]; S2=np.r_[0,np.cumsum(cnt*c*c)]
def cost(i,j):  # bins i..j-1
    w=W[j]-W[i]; return np.where(w>0,(S2[j]-S2[i])-(S1[j]-S1[i])**2/np.maximum(w,1),0.0)
K=5; INF=1e30
D=np.full((K+1,nb+1),INF); P=np.zeros((K+1,nb+1),int)
idx=np.arange(nb+1)
for j in range(1,nb+1): D[1,j]=cost(0,j)
for k in range(2,K+1):
    for j in range(k,nb+1):
        i=np.arange(k-1,j); t=D[k-1,i]+cost(i,j); b=t.argmin(); D[k,j]=t[b]; P[k,j]=i[b]
cuts=[]; j=nb
for k in range(K,1,-1): j=P[k,j]; cuts.append(j)
cuts=sorted(cuts); br=[lo]+[edges[i] for i in cuts]+[hi]
sst=((x-x.mean())**2).sum(); gvf=1-D[K,nb]/sst
print('breaks',np.round(br,4),'GVF',round(gvf,4))
cl=np.clip(np.searchsorted(br[1:-1],x,side='right')+1,1,5)
print('share %',np.round(100*np.bincount(cl)[1:]/len(x),2),'cells',np.bincount(cl)[1:])
np.save(str(JENKS)+'/breaks.npy',np.array(br))
pd.DataFrame({'class':['VeryLow','Low','Moderate','High','VeryHigh'],'lower_bound':br[:-1],'upper_bound':br[1:],'mapped_cells':np.bincount(cl)[1:],'share_of_mapped_pct':100*np.bincount(cl)[1:]/len(x)}).to_csv(str(JENKS)+'/susceptibility_jenks_breaks.csv',index=False)
# per-country shares
import geopandas as gpd, rasterio.features as F
with rasterio.open(glob.glob(A+'*FINAL_full*.tif')[0]) as s: tr=s.transform; crs=s.crs
g=gpd.read_file(COUNTRY_SHP).to_crs(crs).set_index('name')
rows=[]
full=np.where(v,np.clip(np.searchsorted(br[1:-1],np.asarray(a.data),side='right')+1,1,5),0)
for n in ['Afghanistan','Bangladesh','Bhutan','India','Nepal','Pakistan','Sri Lanka']:
    mk=F.rasterize([(g.loc[n].geometry,1)],out_shape=a.shape,transform=tr,dtype='uint8').astype(bool)&v
    b=np.bincount(full[mk],minlength=6)[1:]; rows.append([n,int(b.sum())]+list(np.round(100*b/b.sum(),2))+[round(100*(b[3]+b[4])/b.sum(),2)])
pd.DataFrame(rows,columns=['Country','mapped_cells','VeryLow_pct','Low_pct','Moderate_pct','High_pct','VeryHigh_pct','HighPlusVeryHigh_pct']).to_csv(str(JENKS)+'/country_susceptibility_jenks.csv',index=False)
print(pd.read_csv(str(JENKS)+'/country_susceptibility_jenks.csv').to_string())
# 5-class raster from FILLED surface using these breaks
with rasterio.open(glob.glob(str(FILLED/'filled_*FINAL_full*.tif'))[0]) as s: f=s.read(1); nd=s.nodata; p2=s.profile
out=np.where((f!=nd)&m,np.clip(np.searchsorted(br[1:-1],f,side='right')+1,1,5),-99).astype('int16')
p2.update(dtype='int16',nodata=-99,compress='deflate',predictor=2)
with rasterio.open(str(JENKS)+'/susceptibility_5class_jenks_filled.tif','w',**p2) as o: o.write(out,1)
np.save(str(JENKS)+'/cls_filled.npy',out)

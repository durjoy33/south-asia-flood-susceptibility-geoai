import numpy as np,pandas as pd
from sklearn.cluster import KMeans
from sklearn.neighbors import BallTree
from pyproj import CRS,Transformer
import os
D=pd.read_csv(os.environ.get('FLOOD_GEOAI_GROUPED_TABLE','SR_GEOAI_Flood_Master_Dataset_Grouped.csv'))
CRSW=CRS.from_proj4("+proj=aea +lat_0=23 +lon_0=80 +lat_1=8 +lat_2=38 +datum=WGS84 +units=m +no_defs")
tr=Transformer.from_crs(CRSW,"EPSG:4326",always_xy=True)
lon,lat=tr.transform(D.x.values,D.y.values)
D['lon'],D['lat']=lon,lat
RAD=np.radians(np.c_[lat,lon]);R=6371008.8
y=D.Label.values;g=D.sample_pixel_group_id.values
NUM=['Elevation','Slope','Aspect','Curvature','TWI','Soil_moist','NDVI','Dist_road','Dist_river','Dist_strm','Drain_dens','Flow_accu','Runoff','Total_rain','Rain_anom','Rain_days','Ext_rain_n','Pop_dens']
CAT=['Soil_type','Geology','LULC']
def regions(seed,k=5):
    u,inv=np.unique(g,return_inverse=True);cnt=np.bincount(inv)
    xy=D[['x','y']].values;c=np.zeros((len(u),2));np.add.at(c,inv,xy);c/=cnt[:,None]
    km=KMeans(k,random_state=seed,n_init=30,algorithm='lloyd').fit(c,sample_weight=cnt)
    return km.predict(c)[inv] if False else km.labels_[inv]
def retained(test_idx,train_idx,buf_m):
    if buf_m<=0: return train_idx
    bt=BallTree(RAD[test_idx],metric='haversine')
    d,_=bt.query(RAD[train_idx],k=1);d=d[:,0]*R
    gm=pd.Series(d).groupby(g[train_idx]).transform('min').values
    return train_idx[gm>=buf_m]

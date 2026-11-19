import sys,pathlib; sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/'postprocessing')); from config import *
import rasterio, glob, os, numpy as np
from scipy import ndimage as ndi
src=str(MAP_RASTERS)+'/'
m=np.load(MASK)
for f in sorted(glob.glob(src+'*.tif')):
    name=os.path.basename(f)
    with rasterio.open(f) as s:
        a=s.read(1); prof=s.profile; nd=s.nodata
    valid=(a!=nd)&m
    d,idx=ndi.distance_transform_edt(~valid,return_indices=True)
    out=a[idx[0],idx[1]]
    out[~m]=nd
    nfill=int((m&~valid).sum())
    prof.update(compress='deflate',predictor=3 if a.dtype.kind=='f' else 2,tiled=True,blockxsize=256,blockysize=256)
    with rasterio.open(str(FILLED/('filled_'+name)),'w',**prof) as o: o.write(out,1)
    print(name[:50],'filled',nfill,'maxdist_km',round(float(d[m&~valid].max()),1),'p99',round(float(np.percentile(d[m&~valid],99)),1),'left nodata in mask',int(((out==nd)&m).sum()))

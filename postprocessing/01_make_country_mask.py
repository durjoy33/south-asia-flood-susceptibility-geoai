"""Rasterize the seven study countries (cell-centre rule) onto the susceptibility-raster grid.
Writes country_union_mask.npy (True = cell centre falls inside one of the seven countries)."""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent)); from config import *
import glob, numpy as np, rasterio, geopandas as gpd
from rasterio import features
f = glob.glob(str(MAP_RASTERS / "*FINAL_full*.tif"))[0]
with rasterio.open(f) as s: shape, tr, crs = (s.height, s.width), s.transform, s.crs
g = gpd.read_file(COUNTRY_SHP)
g = g[g.name.isin(COUNTRIES)].to_crs(crs)
m = np.zeros(shape, bool)
for geom in g.geometry:
    m |= features.rasterize([(geom, 1)], out_shape=shape, transform=tr, dtype="uint8").astype(bool)
np.save(MASK, m)
print("union cells:", int(m.sum()))   # reference run: 5,058,381

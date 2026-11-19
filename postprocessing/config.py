"""Shared path configuration for post-processing and figure scripts.
Override any location with an environment variable; defaults are relative to the repository root."""
import os
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
def _p(var, default): return Path(os.environ.get(var, default))
# Map rasters written by the notebook (susceptibility_*, gi_star_* GeoTIFFs)
MAP_RASTERS = _p("FLOOD_GEOAI_MAP_RASTERS", ROOT / "outputs" / "sr_geoai_outputs_v3_2_2_pixel_grouped")
# Everything written by the post-processing scripts
POST = _p("FLOOD_GEOAI_POST_DIR", ROOT / "outputs" / "postprocessing")
FILLED = POST / "filled_tif"
SUMM = POST / "summaries"
JENKS = POST / "jenks"
MASK = POST / "country_union_mask.npy"
# Natural Earth 1:110m admin-0 countries (geopandas 0.14.x 'naturalearth_lowres' shapefile)
COUNTRY_SHP = _p("FLOOD_GEOAI_COUNTRY_VECTOR_PATH", ROOT / "data" / "raw" / "natural_earth" / "ne_110m_admin_0_countries.shp")
# Natural Earth 10 m physical vectors (rivers, lakes) for Figure 1
NE_VECTOR = _p("FLOOD_GEOAI_NE_VECTOR_DIR", ROOT / "data" / "raw" / "natural_earth")
SUPP = ROOT / "supplementary_analyses" / "results"
FIGS = _p("FLOOD_GEOAI_FIG_DIR", ROOT / "outputs" / "figures")
for d in (POST, FILLED, SUMM, JENKS, FIGS): d.mkdir(parents=True, exist_ok=True)
COUNTRIES = ["Afghanistan", "Bangladesh", "Bhutan", "India", "Nepal", "Pakistan", "Sri Lanka"]
# Official total surface area incl. inland water, km2 (World Bank indicator AG.SRF.TOTL.K2; FAO source; 2018)
TOTAL_AREA_KM2 = {"Afghanistan": 652860, "Bangladesh": 147570, "Bhutan": 38390, "India": 3287259, "Nepal": 147180, "Pakistan": 796100, "Sri Lanka": 65610}

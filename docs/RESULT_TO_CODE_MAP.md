# Which script produces which manuscript result

| Result | Script / source |
|---|---|
| Harmonized 1 km stack, inventory extraction, grouping, nested random and buffered spatial validation, calibration, final surfaces, Gi* (FDR) | `notebooks/south_asia_flood_pixel_grouped_spatial_validation.ipynb` |
| Tables 3, 5-9 (random vs spatial, regions, gap CI, levels, effects, buffer sensitivity) | `supplementary_analyses/exp.py` (E1-E3) and `supplementary_analyses/results/` |
| Country mask (5,058,381 cells) | `postprocessing/01_make_country_mask.py` |
| Nearest-valid-cell fill of nodata cells inside the country mask (used for the map figures only) | `postprocessing/02_fill_nodata_nearest.py` |
| Quintile class and Gi* summaries (Tables 12-15 percentages, computed on mapped cells only, `orig` mode) | `postprocessing/03_summarise_quintile_classes_and_gistar.py orig` |
| Fisher-Jenks five-class breaks and country shares | `postprocessing/04_jenks_classes.py` |
| Area estimates (country percentage x official national total area) | `postprocessing/05_area_estimates.py` |
| Figures 1, 3, 5, 6, 7 and the final susceptibility / Gi* map | `figures/` |

Run order for post-processing: 01 -> 02 -> 03 (`orig`, then `filled`) -> 04 -> 05, then the figures. Set `FLOOD_GEOAI_MAP_RASTERS` to the folder holding the notebook's GeoTIFFs and `FLOOD_GEOAI_COUNTRY_VECTOR_PATH` to the Natural Earth 1:110m admin-0 shapefile.

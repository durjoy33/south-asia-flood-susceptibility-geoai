# Supplementary analyses (manuscript Sections 4.3, 4.5, 4.6; Tables 3 and 5-9)

Scripts: `sr.py` (shared setup) and `exp.py`. Fixed hyperparameters, uncalibrated scores, five models (the MLP is not rerun). The geodesic buffer uses a haversine approximation; retained training sizes match the notebook to within 3 observations per fold.

Input: `SR_GEOAI_Flood_Master_Dataset_Grouped.csv`, written by the notebook (it adds `sample_pixel_group_id`, the 1-km raster-cell group). Point `FLOOD_GEOAI_GROUPED_TABLE` at it, then run from any folder:

```bash
python supplementary_analyses/exp.py E1   # buffer sensitivity, seeds 17/42/73, buffers 0 / 419.5 / 629.3 / 839.0 km  -> e1.csv
python supplementary_analyses/exp.py E2   # repeated grouped-random validation, 6 seeds x 5 folds                    -> e2.csv
python supplementary_analyses/exp.py E3   # four-condition decomposition C1-C4                                       -> e3.csv
```

`results/` holds the output tables used in the manuscript (E1-E3 raw outputs and Tables 3, 5-9). Table 5 country labels used geopandas with Natural Earth 1:50m admin-0 boundaries (`results/record_country_labels.csv`). Requires scikit-learn, lightgbm, xgboost and pyproj.


The precomputed result CSVs are included to document the tables reported in the manuscript. They are not evidence that the scripts were rerun during repository packaging. The six-seed grouped-random benchmark and E1–E3 experiments use fixed hyperparameters and are supplementary analyses, distinct from the main notebook's nested validation outputs.

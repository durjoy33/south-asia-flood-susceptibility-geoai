# Reproducibility scope

## Contents
- The v3.2.2 notebook (raster harmonization, inventory extraction, 1-km cell grouping, spatial dependence diagnostics, nested random and buffered spatial validation, calibration, size-matched reference, buffer sensitivity, map comparison, Gi*).
- `supplementary_analyses/`: the six-seed grouped-random benchmark, buffer sensitivity and the four-condition C1-C4 decomposition, with their output tables.
- `postprocessing/` and `figures/`: country mask, nearest-valid-cell fill for the map rasters, quintile and Jenks class summaries, area estimates and figure scripts.
- `data/processed/`: the modelling table and a data dictionary.

## Verified in packaging
`01_make_country_mask.py` reproduces the 5,058,381-cell country union exactly. Running `02`-`05` on the notebook's GeoTIFFs reproduced the quintile breaks (0.546 / 0.625 / 0.704 / 0.820 from mapped cells), the Jenks breaks (0.280 | 0.511 | 0.612 | 0.710 | 0.820 | 0.951; GVF 0.949) and the country high + very high area estimates. The notebook itself and `exp.py` were not re-run in packaging (they require the full raster stack and are computationally heavy).

## Random-holdout note
The notebook requests 15 nominal 80/20 grouped-random holdouts. Nominal seeds do not guarantee 15 distinct test partitions or full coverage; an earlier run gave seven distinct partitions and 78.5% unique prediction coverage. Read the actual coverage from the output of the run being reported and describe the repeats accordingly.

## Limitations
- The environment is not byte-for-byte pinned (the notebook was run in a Python 3.13 Kaggle kernel; no package lock was recorded). Record `pip freeze` after a verified run.
- One 1-km cell contains a presence and a background record; both are kept and grouped together.
- Event-level independence cannot be assessed without an event identifier; background points are not verified absences.
- Validation is internal (grouped random and buffered spatial), not independent external or design-based map-accuracy assessment.
- Area estimates in km2 scale mapped-cell percentages by official national total areas and assume unmapped cells resemble mapped cells.
- Nodata cells inside the country boundaries are filled with the nearest valid cell for the map figures; summary percentages use mapped cells only.
- Natural Earth boundaries (1:110m) should be supplied as a local, versioned file.

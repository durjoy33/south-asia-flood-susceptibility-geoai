# South Asia Flood Susceptibility — Pixel-Grouped Spatial Validation

**Research code for:** *Training support and geographic separation in flood-susceptibility modelling across South Asia: a 1-km pixel-grouped spatial validation study*  
**Author:** Naimur Rahman  
**Workflow version:** v3.2.2 pixel-grouped notebook plus supplementary, post-processing and figure scripts

## Overview

This repository contains the Jupyter workflow for constructing a harmonized 1-km predictor stack and evaluating flood-susceptibility classifiers under raster-cell-grouped random and buffered geographic validation. It is designed for a seven-country South Asian study domain: Afghanistan, Bangladesh, Bhutan, India, Nepal, Pakistan and Sri Lanka.

The notebook includes:

- Reprojection and harmonization of the supplied predictor rasters to a South Asia-centred Albers equal-area grid at 1,000 m;
- Extraction and quality-control of a binary flood-presence/background inventory using 21 retained modelling predictors (24 source raster layers are checked; three candidate layers are excluded from the final model matrix);
- Raster-cell grouping so observations sharing the same 1-km predictor support cannot cross the relevant train/test boundaries;
- Spatial dependence diagnostics, empirical variogram range estimation and geometry/support-based buffered spatial partition selection;
- Nested random and buffered spatial validation, probability calibration, model comparison and buffer sensitivity;
- Size-/class-matched reference experiments, spatial-block bootstrap summaries, raster map comparison and descriptive Gi* / country summaries;
- Output manifests, validation audits and a final package preflight.

See [`docs/RESULT_TO_CODE_MAP.md`](docs/RESULT_TO_CODE_MAP.md) for which script produces which manuscript table or figure, and [`docs/REPRODUCIBILITY_SCOPE.md`](docs/REPRODUCIBILITY_SCOPE.md) for what was verified and the known limitations.

## Repository structure

```text
.
├── README.md  CITATION.cff  LICENSE  requirements.txt  environment.yml  .gitignore  .env.example
├── notebooks/            v3.2.2 workflow notebook
├── supplementary_analyses/  exp.py, sr.py, results/ (E1-E3, Tables 3, 5-9)
├── postprocessing/       config.py, 01 mask, 02 fill, 03 summaries, 04 Jenks, 05 area estimates
├── figures/              figure scripts (Figures 1, 3, 5, 6, 7, final susceptibility / Gi* map)
├── data/processed/       SR_GEOAI_Flood_Master_Dataset.csv, DATA_DICTIONARY.csv
├── data/raw/             README only (rasters and points are on Zenodo / from providers)
├── config/               predictor manifest template
├── docs/                 code/data statement, result-to-code map, licensing, scope, publishing steps
└── scripts/              validate_notebook.py
```

## Data availability and input files

**The processed modelling table is included** (`data/processed/SR_GEOAI_Flood_Master_Dataset.csv`) together with its data dictionary. Before making this repository public, confirm that you have permission to redistribute this derived table because it contains georeferenced flood-presence/background records and values derived from third-party products. The original point inventory and the 24 predictor rasters are not included. Obtain them from the original providers or a project data archive only after its record has actually been published; do not cite a Zenodo DOI until one has been issued. See `docs/DATA_AND_LICENSING.md`.

The default directory layout is documented in [`data/raw/README.md`](data/raw/README.md). The notebook also supports environment-variable overrides. No personal access tokens or credentials are required by the analysis notebook.

Before a full run, check:

1. The point shapefile and all required sidecar files are present;
2. All 24 expected predictor raster files are present;
3. The point inventory CRS is correctly defined;
4. The predictor source metadata, effective temporal coverage, native resolution and licences are recorded;
5. A pinned local country-boundary file is configured for reproducible country-area summaries, rather than relying on the notebook's remote Natural Earth fallback.

## Environment setup

The notebook was authored/executed in a Python 3.13 Kaggle environment. The supplied notebook does not preserve a complete package-version lock. The manifests therefore list the imported dependencies, but they are not a byte-for-byte environment lockfile. The repository checks Python syntax and notebook structure; it does not claim that the full raster/model workflow has been rerun in a clean environment.

### Conda (recommended for geospatial dependencies)

```bash
conda env create -f environment.yml
conda activate south-asia-flood-geoai
jupyter lab
```

### pip alternative

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
jupyter lab
```

If a local environment differs from the original Kaggle kernel, record the resolved package versions (for example, `python -m pip freeze > requirements-lock.txt`) after verifying compatibility. Do not describe an untested environment as an exact reproduction.

## Configure data paths

By default, the notebook expects:

```text
data/raw/
└── flood-susceptibility-south-asia/
    ├── Flood Training/
    │   └── Flood Training/
    │       ├── Flood_Point.shp
    │       ├── Flood_Point.shx
    │       ├── Flood_Point.dbf
    │       └── Flood_Point.prj
    └── Flood_1km-20260503T054519Z-3-001/
        └── Flood_1km/
            ├── Elevation.tif
            ├── Slope.tif
            ├── Aspect.tif
            ├── Surface_roughness.tif
            ├── Curvature.tif
            ├── TWI.tif
            ├── Soil.tif
            ├── Geology.tif
            ├── Soil_moisture.tif
            ├── NDVI.tif
            ├── NDWI.tif
            ├── LULC.tif
            ├── Dist_from_road.tif
            ├── Dist_from_river.tif
            ├── Dist_from_stream.tif
            ├── Drainage_density.tif
            ├── Flow_accumulation.tif
            ├── Runoff.tif
            ├── Total_rainfall.tif
            ├── Rainfall_anomaly.tif
            ├── Rainfall_day.tif
            ├── 95p_day.tif
            ├── 95p_mm.tif
            └── Population_density.tif
```

To use a different input location, set environment variables before launching Jupyter, for example:

```bash
export FLOOD_GEOAI_DATA_ROOT="/path/to/data/raw"
export FLOOD_GEOAI_OUTPUT_DIR="/path/to/outputs/flood-validation"
export FLOOD_GEOAI_COUNTRY_VECTOR_PATH="/path/to/pinned/ne_110m_admin_0_countries.shp"
```

Optional overrides are `FLOOD_GEOAI_POINTS_PATH`, `FLOOD_GEOAI_RASTER_DIR`, and `FLOOD_GEOAI_MASTER_TABLE`. See `.env.example` for the variable names. The notebook reads environment variables directly; it does not automatically load a `.env` file.

## Run the analysis

1. Clone/download this repository.
2. Install the environment.
3. Obtain the raw point inventory and raster files and place them in the documented layout (or configure the path variables).
4. Open `notebooks/south_asia_flood_pixel_grouped_spatial_validation.ipynb`.
5. Run from the first code cell in a clean kernel. The first major processing stage harmonizes rasters and builds the complete-case modelling table.
6. Allow all validation, mapping and quality-control stages to complete. The workflow is computationally intensive and can require substantial memory and runtime.
7. Inspect the output manifests and audit files before using generated numbers in the manuscript.

The notebook writes to `outputs/sr_geoai_outputs_v3_2_2_pixel_grouped/` by default. Intermediate harmonized rasters and output tables should remain outside Git unless they are intentionally curated, small, redistributable research products.

**Checkpoint limitation:** checkpoint CSVs document completed model/fold rows; the notebook does not automatically resume an estimator fit after a runtime restart. A failed cell may need to be rerun.

## Important methodological qualifications

- The analysis groups by 1-km raster cell, not merely exact coordinate, to avoid placing records with identical raster-derived predictor support in both training and test partitions.
- The inventory includes one retained mixed-label raster cell (one presence and one background record); the notebook documents and controls its grouping but does not resolve the source-label ambiguity.
- Event-level independence cannot be assessed if a stable flood-event identifier is unavailable.
- Background observations are not assumed to be verified flood absences; model scores are relative susceptibility scores conditional on the sampled case/background design.
- The reported validation is repeated internal validation under specified designs, not independent external geographic validation or design-based map-accuracy assessment.
- Fold-level and seed-level standard deviations should not be interpreted as confidence intervals over independent regional populations.
- The selected mapping model is selected using the same spatial-CV evidence used to summarize its performance; this introduces model-selection optimism.
- Upsampling coarse climate or satellite products to 1 km does not create 1-km native information.
- The notebook's default country-boundary fallback is remote and unpinned. For reproducible country summaries, supply a locally archived, versioned boundary file.

## Post-processing and figures

After the notebook has written its GeoTIFFs, run `postprocessing/01`-`05` in order (see `docs/RESULT_TO_CODE_MAP.md`), then the scripts in `figures/`. Paths are set in `postprocessing/config.py` or by environment variables (`FLOOD_GEOAI_MAP_RASTERS`, `FLOOD_GEOAI_POST_DIR`, `FLOOD_GEOAI_COUNTRY_VECTOR_PATH`, `FLOOD_GEOAI_NE_VECTOR_DIR`, `FLOOD_GEOAI_FIG_DIR`). Nodata cells inside the country boundaries are filled with the nearest valid cell for the map figures (`02`); the tables use mapped cells only (`03 orig`).

## Data and code availability statement

See [`docs/CODE_AVAILABILITY_STATEMENT.md`](docs/CODE_AVAILABILITY_STATEMENT.md) and [`docs/PUBLISHING_STEPS.md`](docs/PUBLISHING_STEPS.md).

## License

The MIT License in this repository applies to original code files only. It does not grant rights to redistribute the processed modelling table, source flood inventory, predictor rasters, satellite products, boundary data or other third-party materials. Confirm redistribution rights for the processed table and each external dataset before making the repository public.

# Code and data availability statement
Nodata cells inside the country boundaries were assigned the value of the nearest valid cell for the map figures; class and cluster percentages in the tables were computed on mapped cells only.

## Manuscript wording before public release

The analysis code, including the main raster-harmonization and pixel-grouped validation notebook, supplementary experiments (E1–E3), post-processing scripts and figure-generation scripts, will be made publicly available at `https://github.com/[GITHUB_USERNAME]/south-asia-flood-susceptibility-geoai` upon repository publication. A versioned archival DOI will be added after a GitHub release has been archived and a DOI has actually been issued. The original flood-point inventory and predictor rasters are not bundled with the code repository and must be obtained from their respective providers or a separately released project data archive, subject to the providers’ terms and licences.

## Manuscript wording after GitHub publication

The analysis code, including the main raster-harmonization and pixel-grouped validation notebook, supplementary experiments (E1–E3), post-processing scripts and figure-generation scripts, is available at `https://github.com/[GITHUB_USERNAME]/south-asia-flood-susceptibility-geoai` (release `[RELEASE_TAG]`; archived code DOI: `[CODE_DOI]`). The original flood-point inventory and predictor rasters are available from their respective providers or the project data archive (`[DATA_DOI, if applicable]`), subject to the relevant terms and licences.

## Important data-distribution qualification

The repository package currently includes `data/processed/SR_GEOAI_Flood_Master_Dataset.csv`, a derived table containing georeferenced flood-presence/background records and predictor values. Confirm that its redistribution is permitted before publishing the repository. If permission is not established, remove that CSV from the public Git repository, retain the placeholder README in `data/processed/`, and distribute the data only through an approved access route. The MIT software licence does not apply to this dataset or third-party source data.

Do not replace any bracketed placeholder with an invented URL or DOI.

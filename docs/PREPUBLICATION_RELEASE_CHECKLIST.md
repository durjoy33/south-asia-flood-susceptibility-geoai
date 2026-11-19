# Pre-publication release checklist

- [ ] Confirm redistribution rights for the derived modelling CSV; remove it from the public repository if unclear.
- [ ] Confirm provider licences and attribution for every input layer.
- [ ] Fill every `TO CONFIRM` item in `data/processed/DATA_DICTIONARY.csv`.
- [ ] Verify source collection IDs, temporal start/end dates and aggregation windows against the original GEE scripts and raster metadata.
- [ ] Pin or archive a versioned country-boundary file; do not rely on an unpinned remote fallback for reproducible area summaries.
- [ ] Verify the notebook input directory structure and environment variables on a clean machine.
- [ ] Run `python scripts/validate_notebook.py` and compile all Python scripts. This is static validation only.
- [ ] If computational resources allow, execute the full workflow from a clean kernel and save actual package versions.
- [ ] Verify every manuscript table and figure against the included output CSVs and corresponding scripts.
- [ ] Check that the repository licence covers original code only and does not imply rights to third-party data.
- [ ] Publish the GitHub repository, create a tagged release, archive it on Zenodo if desired, and insert only verified URLs/DOIs into the manuscript.

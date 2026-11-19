# Raw input data (not included)

This repository does not redistribute the source inventory or raster files. Obtain them from the original data providers or from a project archive only after a public record and valid DOI have been created; verify the terms of use before downloading or redistributing any files. The notebook expects the following default layout beneath this directory.

## Point inventory

`flood-susceptibility-south-asia/Flood Training/Flood Training/Flood_Point.shp` and its shapefile sidecars (`.shx`, `.dbf`, `.prj`; include `.cpg` if supplied). The file must have a valid CRS and a binary `Label` field (or a documented `Id` field that can be mapped to `Label`).

## Predictor rasters

Place the 24 GeoTIFFs in `flood-susceptibility-south-asia/Flood_1km-20260503T054519Z-3-001/Flood_1km/`:

- `Elevation.tif`
- `Slope.tif`
- `Aspect.tif`
- `Surface_roughness.tif`
- `Curvature.tif`
- `TWI.tif`
- `Soil.tif`
- `Geology.tif`
- `Soil_moisture.tif`
- `NDVI.tif`
- `NDWI.tif`
- `LULC.tif`
- `Dist_from_road.tif`
- `Dist_from_river.tif`
- `Dist_from_stream.tif`
- `Drainage_density.tif`
- `Flow_accumulation.tif`
- `Runoff.tif`
- `Total_rainfall.tif`
- `Rainfall_anomaly.tif`
- `Rainfall_day.tif`
- `95p_day.tif`
- `95p_mm.tif`
- `Population_density.tif`

All files must have valid CRS metadata. The notebook verifies the raster stack and creates a common 1-km Albers equal-area grid. Twenty-one predictors are used in the final modelling matrix; `Surface_roughness.tif`, `NDWI.tif` and `95p_mm.tif` are source candidates retained for quality-control/manifest purposes but excluded from the 21-predictor model. Do not rename files without updating the `RASTERS` mapping in the notebook.

## Temporal metadata

Record the actual source collection/version, start/end date, effective observation count, aggregation method, native spatial resolution, resampling method and licence for each raster. A nominal reference interval in manuscript text must not be substituted for the true dates used to construct a raster.

## Natural Earth boundaries
Place the Natural Earth 1:110m admin-0 countries shapefile at `data/raw/natural_earth/ne_110m_admin_0_countries.shp` (or set `FLOOD_GEOAI_COUNTRY_VECTOR_PATH`) and the 10 m physical vectors (`ne_10m_rivers_lake_centerlines`, `ne_10m_lakes`) in the same folder for Figure 1. The reference run used the `naturalearth_lowres` shapefile bundled with geopandas 0.14.4.

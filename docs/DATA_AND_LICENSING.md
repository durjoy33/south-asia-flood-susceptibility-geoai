# Data provenance and licensing checklist

Before public release or journal submission, complete this inventory for every input layer:

| Input | Required metadata | Status in uploaded notebook |
|---|---|---|
| Flood point inventory | Provider, version/date, event linkage, point-generation rule, background-sampling method, CRS, licence | File path and field checks are coded; event/background provenance remains incomplete |
| Elevation / terrain derivatives | DEM product/version, acquisition/reference date, native resolution, derivative algorithms and neighbourhoods | Raster filenames are defined; detailed provenance must be supplied |
| HydroSHEDS / river and stream layers | Product/version, flow-accumulation/stream-order thresholds, extraction date, distance method | Filename-level input mapping only; thresholds need source metadata |
| Climate and hydrology | Product/collection ID, temporal window, units, aggregation and native resolution | Must be recovered from original raster metadata/GEE scripts |
| Soil and geology | Product version, depth/classification, scale and licence | Filenames are defined; source version/depth needs confirmation |
| NDVI / LULC | Collection/version, compositing, QA mask, dates, class legend | Filenames are defined; temporal processing must be documented |
| Population | Product/version, count-versus-density meaning, year, native grid and licence | Filename is defined; exact product and units need confirmation |
| Roads | OSM extract date, query/filter, geometry processing and licence/attribution | Filename is defined; extraction details need confirmation |
| Country boundaries | Boundary dataset/version, scale and name field | Remote Natural Earth fallback exists; pin a local release for reproducibility |

Do not commit data-provider files unless redistribution is permitted. The MIT code licence in this repository applies only to original code authored for this project; it does not override third-party dataset licences or attribution obligations.

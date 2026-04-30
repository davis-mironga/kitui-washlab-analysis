# Boundary Files

Kitui County administrative boundary shapefiles for use in GEE and GeoPandas.

## Source
GADM (Global Administrative Areas) — https://gadm.org  
Level 0: Kenya national boundary  
Level 1: County boundaries  
Level 2: Sub-county boundaries  
Level 3: Ward boundaries

## Download
```python
# In Colab — download Kitui boundaries directly
import requests, zipfile, io

# Kenya GADM Level 2 (sub-county level)
url = "https://geodata.ucdavis.edu/gadm/gadm4.1/shp/gadm41_KEN_shp.zip"
# Filter to Kitui County after loading

import geopandas as gpd
kenya = gpd.read_file('gadm41_KEN_2.shp')
kitui = kenya[kenya['NAME_1'] == 'Kitui'].copy()
kitui_wards = kenya_l3[kenya_l3['NAME_1'] == 'Kitui'].copy()  # Level 3 for wards
```

## Important: Ward name alignment
The GADM ward names do not always match the ward names in the borehole master dataset.
Before any spatial join, cross-check ward names using `docs/data_dictionary.md`.
Known mismatches are documented in the analysis plan.

## Files (add here when downloaded)
- `kitui_county.shp` — County boundary
- `kitui_subcounties.shp` — 7 sub-county boundaries  
- `kitui_wards.shp` — 40 ward boundaries

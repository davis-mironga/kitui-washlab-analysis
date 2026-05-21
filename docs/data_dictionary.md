# Data Dictionary — Kitui Borehole Dataset

**Format:** Excel (.xlsx) or CSV
**CRS:** WGS84 EPSG:4326
**Spatial CRS for analysis:** UTM Zone 37N (EPSG:32637)

The borehole dataset is provided by the Kitui County water authority. Place the file in `Kitui_WASHLAB/boreholes/` on Google Drive before running Notebook 04. The notebook auto-detects the file and prints available columns for verification before proceeding.

**Important:** The dataset has two distinct parts with different levels of detail. The main 34-ward sheet contains 632 individual borehole records with GPS coordinates and can be used directly in the spatial coverage gap analysis. The six additional wards sheet contains 98 boreholes as ward-level summaries only — no individual borehole locations — and can only be used for ward-level estimates.

| Part | Wards | Boreholes | Detail level | Spatial use |
|------|-------|-----------|--------------|-------------|
| Main dataset | 34 | 632 | Individual records with GPS | Full spatial analysis |
| Six additional wards | 6 | 98 | Ward-level totals only | Ward-level estimates only |
| **Total** | **40** | **730** | | |

---

## Loading in Python

```python
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# Load the borehole dataset
# Update sheet_name and header to match the actual file structure
# Print columns first to verify before proceeding
df = pd.read_excel('your_borehole_file.xlsx', sheet_name=0, header=0)
print(df.columns.tolist())

# Convert to GeoDataFrame (once column names are confirmed)
gdf = gpd.GeoDataFrame(
    df,
    geometry=[Point(xy) for xy in zip(df['Longitude'], df['Latitude'])],
    crs='EPSG:4326'
)

# Project to UTM Zone 37N for distance calculations in Kenya
gdf_utm = gdf.to_crs('EPSG:32637')
```

---

## Ward Name Reconciliation

Ward names in the borehole dataset may differ slightly from the WASI ward names used in Notebooks 01 to 03. Reconcile before any spatial join in Notebook 04. The table below documents the mismatches found in the April 2026 dataset — check against any updated file.

| Borehole dataset name | WASI ward name |
|-----------------------|----------------|
| Kanziko/Simisi | Kanziko |
| Kithumula/Kwa Mutonga | Kwa Mutonga/Kithumula |
| Mutitu/Kaliku | Mutito/Kaliku |
| Mutomo/Kibwea | Mutomo |
| Yatta/Kwa Vonza | Kwavonza/Yatta |

The six additional wards (Central, Kivou, Mui, Nguni, Nuu, Waita) are in a separate tab or sheet. Merge them into the main dataset before running Notebook 04, noting that they contain ward-level summaries only.

---

## Expected Column Reference

The columns below describe the expected dataset structure. Verify names against the actual file before use. Notebook 04 includes auto-detection for the most common column name variations.

| Column | Type | Description |
|--------|------|-------------|
| `Borehole_ID` | Text | Unique identifier per borehole. |
| `Sub_County` | Text | Sub-county name. One of 7 Kitui sub-counties. |
| `Ward` | Text | Ward name. 40 unique wards. See reconciliation table above. |
| `Borehole_Name` | Text | Official borehole name. |
| `Latitude` | Float | Decimal degrees. WGS84. Valid Kitui range: -3.1 to 0.0. |
| `Longitude` | Float | Decimal degrees. WGS84. Valid Kitui range: 37.5 to 39.2. |
| `Functionality_Status` | Text | See status vocabulary below. |
| `Is_Functional` | Boolean | `True` if borehole is operational. For quick filtering. |
| `Management_Type` | Text | See management vocabulary below. |
| `Population_Served_HHs` | Integer | Households served. Verify if >3,000. |
| `Yield_m3_hr` | Float | Borehole yield in m³/hr. Verify if >50 (may be scheme-level total). |
| `GPS_Quality` | Text | See GPS quality flags below. |
| `Data_Source` | Text | Origin of the record. |

---

## Controlled Vocabularies

### Functionality_Status
| Value | Meaning |
|-------|---------|
| `Functional` | Borehole operational with no known issues |
| `Functional - Needs Rehabilitation` | Operational but infrastructure deteriorating |
| `Functional - At Risk` | Operational but yield declining or seasonally unreliable |
| `Partially Functional` | Producing water but below design capacity |
| `Non-Functional` | Not producing water |
| `Non-Functional - Not Equipped` | Drilled but no pump installed |
| `Non-Functional - Capped` | Intentionally sealed |
| `Non-Functional - Abandoned` | No longer in use |
| `Non-Functional - Obsolete` | Superseded by alternative supply |
| `Under Construction` | Active construction or installation |
| `Unknown` | Status not recorded in source dataset |

### Management_Type
| Value | Meaning |
|-------|---------|
| `Community` | Community water committee or WUA |
| `Community / School` | Shared community and school management |
| `School / Institution` | School, hospital, or other institution |
| `Church / Faith-Based` | Religious organisation |
| `Kitwasco` | Kitui Water and Sewerage Company |
| `Kimwasco` | Kiambere-Mwingi Water and Sanitation Company |
| `Private` | Private operator or individual |
| `Other` | Does not fit above categories |
| `Unknown` | Not recorded |

### GPS_Quality
| Value | Use in analysis |
|-------|----------------|
| `Verified` | Safe to use in spatial analysis |
| `Needs Review` | Verify before spatial use |
| `Low Confidence` | Verify name and location before use |
| `No GPS` | No coordinates available — cannot be included in coverage gap map |

---

## Quick Filters (Python)

```python
# Functional boreholes — use for coverage gap buffer analysis
functional = df[df['Is_Functional'] == True]

# Non-functional boreholes — rehabilitation candidates
non_functional = df[df['Is_Functional'] == False]

# Validate coordinate ranges for Kitui County
valid_coords = df[
    (df['Longitude'] >= 37.5) & (df['Longitude'] <= 39.2) &
    (df['Latitude'] >= -3.1) & (df['Latitude'] <= 0.0)
]

# Boreholes with coordinates available
has_gps = df[df['Latitude'].notna() & df['Longitude'].notna()]

# Boreholes missing coordinates — cannot be used in spatial analysis
no_gps = df[df['Latitude'].isna() | df['Longitude'].isna()]
```

---

## Common Data Gaps

| Gap | Impact | Resolution |
|-----|--------|------------|
| Six additional wards available as ward totals only | Individual borehole locations not available for spatial analysis | Use for ward-level estimates only |
| Missing GPS coordinates | Cannot include in coverage gap map | Field GPS collection required |
| Missing population served | Cannot quantify population in gap | Field data collection |
| Missing yield data | Cannot assess reliable yield | Field data collection |
| Ward names not matching WASI wards | Spatial join will fail | See reconciliation table above |

---

## Walking Distance Threshold

The analysis uses **1km** as the primary threshold for coverage gap calculation, consistent with Kenya national water policy for rural basic access. A 2km secondary analysis is also run for comparison. Both outputs are saved by Notebook 04.

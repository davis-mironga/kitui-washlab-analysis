# Data Dictionary — Kitui Borehole Dataset

**File:** `28_04_2026_Borehole_Dashboard_Summary_40-Wards.xlsx`
**Records:** 632 boreholes across 34 wards (6 additional wards in separate tab)
**Wards:** 40 (34 in main sheet + 6 in additional tab)
**CRS:** WGS84 EPSG:4326
**Last updated:** April 2026

> **Note:** This data dictionary was written before the final borehole dataset was received. The column reference below reflects the planned dataset structure and may not exactly match the actual column names in the received file. Column names should be verified against the actual file before running Notebook 04. The Python loading code in Notebook 04 includes auto-detection for the most common column name variations.

---

## Loading in Python

```python
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# Load the borehole dataset
# Update sheet_name and header to match the actual file structure
df = pd.read_excel('28_04_2026_Borehole_Dashboard_Summary_40-Wards.xlsx',
                   sheet_name='1. Ward Status Summary', header=1)

# Print columns to verify before proceeding
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

Five ward names in the borehole dataset differ from the WASI ward names used in Notebooks 01–03. These must be reconciled before any spatial join in Notebook 04.

| Borehole dataset name | WASI ward name |
|-----------------------|----------------|
| Kanziko/Simisi | Kanziko |
| Kithumula/Kwa Mutonga | Kwa Mutonga/Kithumula |
| Mutitu/Kaliku | Mutito/Kaliku |
| Mutomo/Kibwea | Mutomo |
| Yatta/Kwa Vonza | Kwavonza/Yatta |

The six additional wards (Central, Kivou, Mui, Nguni, Nuu, Waita) are in a separate tab in the Excel file and must be merged into the main dataset before running Notebook 04.

---

## Column Reference

> The columns below reflect the planned dataset structure. Verify against the actual file before use.

| Column | Type | Description |
|--------|------|-------------|
| `Borehole_ID` | Text | Stable internal ID. Format: `KTI-NNNN`. Unique across all records. |
| `Sub_County` | Text | Sub-county name. Title Case. One of 7 Kitui sub-counties. |
| `Ward` | Text | Ward name. Title Case. 40 unique wards. See reconciliation table above. |
| `Borehole_Name` | Text | Official borehole name. |
| `Latitude` | Float | Decimal degrees. WGS84. Valid Kitui range: -2.2 to -0.2. |
| `Longitude` | Float | Decimal degrees. WGS84. Valid Kitui range: 37.6 to 39.1. |
| `Functionality_Status` | Text | See status vocabulary below. |
| `Is_Functional` | Boolean | `True` if borehole is operational. For quick filtering. |
| `Management_Type` | Text | See management vocabulary below. |
| `Population_Served_HHs` | Integer | Households served. Verify if >3,000. |
| `Yield_m3_hr` | Float | Borehole yield m³/hr. Verify if >50 (may be scheme-level total). |
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
| `No GPS` | No coordinates available — cannot be used in coverage gap map |

---

## Quick Filters (Python)

```python
# Functional boreholes — use for coverage gap buffer analysis
functional = df[df['Is_Functional'] == True]

# Non-functional boreholes — rehabilitation candidates
non_functional = df[df['Is_Functional'] == False]

# Boreholes with GPS available
has_gps = df[df['Latitude'].notna() & df['Longitude'].notna()]

# Validate coordinate ranges for Kitui
valid_coords = df[
    (df['Longitude'] >= 37.5) & (df['Longitude'] <= 39.2) &
    (df['Latitude'] >= -3.1) & (df['Latitude'] <= 0.0)
]
```

---

## Known Data Gaps

> Gap counts below are estimates based on the received dataset. Confirm exact counts after running Notebook 04.

| Gap | Impact | Resolution |
|-----|--------|------------|
| 6 additional wards in separate tab | Not included in main spatial join | Merge before running Notebook 04 |
| 5 ward name mismatches | Spatial join will fail without reconciliation | See reconciliation table above |
| Boreholes with no GPS coordinates | Cannot be included in coverage gap map | Field GPS collection required |
| Missing population served data | Cannot quantify population in gap for affected wards | Field collection |
| Missing yield data | Cannot assess reliable yield for affected boreholes | Field collection |

---

## Walking Distance Threshold

The analysis uses **1km** as the primary threshold for coverage gap calculation, consistent with Kenya national water policy for rural basic access. A 2km secondary analysis is also run for comparison. Both outputs are saved by Notebook 04.

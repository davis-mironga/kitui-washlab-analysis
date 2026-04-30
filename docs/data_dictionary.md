# Data Dictionary — Kitui Borehole Master Dataset

**File:** `Kitui_Boreholes_Master_Dataset.xlsx`  
**Records:** 706 boreholes (608 county inventory + 98 mWater 6-ward)  
**Wards:** 40 (34 county + 6 mWater-only)  
**CRS:** WGS84 EPSG:4326  
**Last updated:** April 2026

---

## Loading in Python

```python
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# Load spatial-ready sheet (GPS Verified only)
df = pd.read_excel('Kitui_Boreholes_Master_Dataset.xlsx',
                   sheet_name='B_Spatial_Analysis', header=2)

# Convert to GeoDataFrame
gdf = gpd.GeoDataFrame(
    df,
    geometry=[Point(xy) for xy in zip(df['Longitude'], df['Latitude'])],
    crs='EPSG:4326'
)

# Project to UTM Zone 37N for distance calculations in Kenya
gdf_utm = gdf.to_crs('EPSG:32637')
```

---

## Column Reference

| Column | Type | Description |
|--------|------|-------------|
| `Borehole_ID` | Text | Stable internal ID. Format: `KTI-NNNN`. Unique across all 706 records. |
| `Sub_County` | Text | Sub-county name. Title Case. One of 7 Kitui sub-counties. |
| `Ward` | Text | Ward name. Title Case. 40 unique wards. |
| `Borehole_Name` | Text | Official borehole name. Cleaned: no `?`, `*`, `"` characters. |
| `Latitude` | Float | Decimal degrees. WGS84. Valid Kitui range: -2.2 to -0.2. |
| `Longitude` | Float | Decimal degrees. WGS84. Valid Kitui range: 37.6 to 39.1. |
| `Coordinate_System` | Text | Always `WGS84 (EPSG:4326)`. Null where GPS not available. |
| `Functionality_Status` | Text | See status vocabulary below. |
| `Is_Functional` | Boolean | `True` if `Functionality_Status` starts with `Functional`. For quick filtering. |
| `Management_Type` | Text | See management vocabulary below. |
| `Population_Served_HHs` | Integer | Households served. County inventory only. Null for 6-ward mWater records. Verify if >3,000. |
| `Yield_m3_hr` | Float | Borehole yield m³/hr. County inventory only. Verify if >50 (may be scheme-level total). |
| `mWater_ID` | Integer | mWater platform unique identifier. Use to join future field survey data. |
| `Match_Method` | Text | How GPS was assigned. See match methods below. |
| `Match_Confidence` | Float | Similarity score 0.0–1.0. 1.0 = exact. Null for `no_match` and `mwater_only`. |
| `GPS_Available` | Boolean | `True` if Latitude/Longitude are populated. |
| `GPS_Quality` | Text | See GPS quality flags below. |
| `GPS_Shared_Flag` | Boolean | `True` if fuzzy-matched record shares GPS coordinates with another record. Needs manual review before spatial use. |
| `Is_Scheme_Entry` | Boolean | `True` if record represents a multi-ward piped scheme. Yield and population values reflect the scheme, not a single borehole. |
| `Data_Source` | Text | Origin of the record. See data sources below. |
| `Data_Date` | Text | Date of data compilation. Update when field data is added. |
| `Operationality_Status` | Text | **Original** status value before standardisation. Retained for audit trail. |
| `Management_Model` | Text | **Original** management model before standardisation. Retained for audit trail. |

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
| `Unknown` | Status not recorded in any source dataset |

### Management_Type
| Value | Meaning |
|-------|---------|
| `Community` | Community water committee / WUA |
| `Community / School` | Shared community and school management |
| `School / Institution` | School, hospital, or other institution |
| `Church / Faith-Based` | Religious organisation |
| `Kitwasco` | Kitui Water and Sewerage Company |
| `Kimwasco` | Kiambere-Mwingi Water and Sanitation Company |
| `Project Maji` | Project Maji NGO |
| `FundiFix` | FundiFix maintenance programme |
| `Private` | Private operator or individual |
| `Proposed - Professionalisation` | Currently community-managed, proposed for WSP |
| `Other` | Does not fit above categories |
| `Unknown` | Not recorded |

### GPS_Quality
| Value | Use in analysis |
|-------|----------------|
| `Verified` | Safe to use. Name matched exactly OR fuzzy match confirmed unique coordinates. |
| `Needs Review - Shared Coordinates` | Fuzzy-matched record shares GPS with another borehole. Review before spatial use. |
| `Low Confidence Match` | Match confidence below 0.90. Verify name and location before use. |
| `No GPS` | No GPS available. Use Sheet D (Field GPS Collection) for field data entry. |

### Match_Method
| Value | Meaning |
|-------|---------|
| `exact` | Borehole name matched exactly between county inventory and mWater |
| `fuzzy` | Name matched at ≥85% similarity. Match confidence score in `Match_Confidence` column. |
| `no_match` | No mWater record found. GPS from field collection required. |
| `mwater_only` | mWater record only — not in county 34-ward inventory. Applies to 6 extra wards. |

### Data_Source
| Value | Meaning |
|-------|---------|
| `County Inventory + mWater GPS` | Record from county inventory with GPS matched exactly from mWater |
| `County Inventory + mWater GPS (fuzzy match)` | County inventory record with GPS from fuzzy-matched mWater record |
| `County Inventory Only` | County inventory record with no GPS match found |
| `mWater Only` | mWater record from 6 extra wards — no county inventory counterpart |

---

## Quick Filters (Python)

```python
# Functional boreholes with verified GPS — use for coverage analysis
spatial_ready = df[(df['Is_Functional'] == True) & (df['GPS_Quality'] == 'Verified')]

# All GPS-verified boreholes — use for coverage gap buffers
all_gps = df[df['GPS_Quality'] == 'Verified']

# Boreholes needing field GPS collection
needs_gps = df[df['GPS_Quality'] == 'No GPS']

# Boreholes needing GPS review before spatial use
review_gps = df[df['GPS_Quality'].isin(['Needs Review - Shared Coordinates',
                                         'Low Confidence Match'])]

# County 34-ward boreholes only (scoreable on 100-point framework)
county_bh = df[df['Match_Method'].isin(['exact', 'fuzzy', 'no_match'])]

# 6 extra ward boreholes (GPS available, county scoring data pending)
extra_bh = df[df['Match_Method'] == 'mwater_only']

# Kitwasco/Kimwasco managed — IoT pilot priority candidates
wsp_managed = df[df['Management_Type'].isin(['Kitwasco', 'Kimwasco'])]
```

---

## Known Data Gaps

| Gap | Count | Impact | Resolution |
|-----|-------|--------|------------|
| No GPS | 199 | Absent from coverage gap map | Field GPS collection (Sheet D) |
| GPS needs review | 146 | Should not be used in spatial analysis until verified | Manual spot-check |
| No population data | ~133 county BH | Cannot score Population Served criterion (20 pts) | Field collection |
| No yield data | ~60 county BH | Cannot score Reliable Yield criterion (15 pts) | Field collection |
| No solarisation data | All 706 | Cannot score Energy Compliance criterion (20 pts) | Field verification |
| No water quality data | All 706 | Cannot score Safe-Water Potential criterion (10 pts) | Laboratory tests |
| 6-ward county data | 98 BH | Cannot score any of 9 criteria | Field assessment if scoped in |

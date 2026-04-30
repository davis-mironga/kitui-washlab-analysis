# Kitui County — WASHLAB Climate-Smart WASH Pilot
### Spatial Analysis: Water Access Stress & Borehole Coverage Gap Analysis

**Client:** Washlab Consult Limited  
**Analyst:** Davis Mironga — Environmental Data Analyst  
**County:** Kitui County, Kenya  
**Agreement date:** 17 April 2026  
**Status:** Phase 1 in progress

---

## Overview

This repository contains all code, methodology, and documentation for the WASHLAB Climate-Smart WASH Pilot spatial analysis for Kitui County. The analysis covers two phases:

- **Phase 1 — Water Access Stress Analysis:** Satellite-derived stress index, seasonal water availability, vegetation condition, and spatial hotspot mapping across all 40 wards.
- **Phase 2 — Coverage Gap Analysis and Site Prioritisation:** Borehole coverage mapping, underserved community identification, and IoT pilot site ranking using the county's 100-point scoring framework.

All code is written in Python and runs in Google Colab. Google Earth Engine is used for satellite data preprocessing. The web application is built in Streamlit and hosted publicly.

---

## Repository Structure

```
kitui-washlab-analysis/
│
├── notebooks/
│   ├── 01_GEE_Data_Preprocessing.ipynb       # Satellite data pull and export
│   ├── 02_Water_Stress_Index.ipynb            # WASI construction and mapping
│   ├── 03_Hotspot_Analysis.ipynb              # Gi* spatial autocorrelation
│   ├── 04_Coverage_Gap_Analysis.ipynb         # 2km buffer, population coverage
│   ├── 05_Site_Prioritisation.ipynb           # 100-point scoring and ranking
│   ├── 06_Validation_and_QA.ipynb             # GPS checks, outlier review
│   └── 07_Report_Figures.ipynb                # Final map and figure exports
│
├── app/
│   ├── app.py                                 # Streamlit web application
│   └── requirements.txt                       # Python dependencies (pinned)
│
├── data/
│   ├── boreholes/                             # Borehole master dataset (see note)
│   ├── boundaries/                            # Kitui county/ward shapefiles
│   └── satellite/                             # GEE-exported rasters (see note)
│
├── outputs/
│   ├── maps/                                  # PNG/PDF map exports
│   └/report/                                 # Final technical summary PDF
│
├── docs/
│   ├── analysis_plan.md                       # Full analysis plan
│   ├── data_dictionary.md                     # Column definitions and standards
│   └── scoring_framework.md                   # 100-point IoT site scoring criteria
│
├── .gitignore
└── README.md
```

---

## Data

### Borehole Dataset
- **706 boreholes** across **40 wards** and **7 sub-counties**
- 608 from the Kitui County 34-ward inventory
- 98 from 6 additional wards (Central, Kivou, Mui, Nguni, Nuu, Waita) sourced from mWater
- GPS quality flagged: 361 Verified | 146 Needs Review | 29 Low Confidence | 199 No GPS
- Full master dataset stored in Google Drive (not committed to this repo — contains county government data)

### Satellite Data
Large raster files exported from GEE are stored in Google Drive and loaded into Colab notebooks directly. File paths are documented in each notebook. Rasters are not committed to this repository.

### Boundaries
Kitui County, sub-county, and ward shapefiles sourced from GADM Level 2. Stored in `data/boundaries/`.

---

## Setup

### Requirements
- Google account with access to Google Earth Engine (sign up at earthengine.google.com)
- Google Colab (free tier sufficient for most notebooks)
- Python 3.10+

### Running notebooks
All notebooks are designed to run in Google Colab. Open directly from GitHub:

1. Go to [colab.research.google.com](https://colab.research.google.com)
2. File → Open notebook → GitHub tab
3. Enter this repository URL
4. Select the notebook you want to run

Each notebook has a setup cell at the top that installs all required packages.

### Running the web app locally
```bash
pip install -r app/requirements.txt
streamlit run app/app.py
```

---

## Deliverables

| Phase | Deliverable | Status |
|-------|-------------|--------|
| 1 | Water Access Stress Index map | In progress |
| 1 | Seasonal water availability map | In progress |
| 1 | Vegetation stress and land condition map | In progress |
| 1 | Spatial hotspot analysis | In progress |
| 1 | Interactive web app (Phase 1 layers) | In progress |
| 2 | Borehole coverage gap map | Pending Phase 1 completion |
| 2 | Priority site ranking (100-point framework) | Pending field assessment data |
| 2 | Updated web app (Phase 2 layers) | Pending |
| 2 | Final technical summary report | Pending |

---

## Satellite Data Sources

| Dataset | Source | Resolution | Use |
|---------|--------|------------|-----|
| NDVI | MODIS MOD13A3 | 1km monthly | Vegetation condition |
| Rainfall | CHIRPS v2.0 | 5km monthly | Seasonal water availability |
| Land Surface Temperature | MODIS MOD11A2 | 1km 8-day | Heat and aridity |
| Evapotranspiration | MODIS MOD16A2 | 500m 8-day | Water consumption |
| Terrain / DEM | SRTM 30m | 30m | Slope and accessibility |
| Population density | WorldPop 2020 | 100m | Exposure weighting |
| Soil moisture | ERA5-Land | ~9km monthly | Groundwater recharge proxy |
| Surface water | JRC Global Surface Water | 30m | Permanent vs seasonal water |

---

## Intellectual Property

All maps, the web application, code, and methodology produced under this project belong to Washlab Consult Limited on full payment, per the service agreement dated 17 April 2026. The code and methodology will be published openly so the analysis can be updated or replicated in other counties.

---

## Contact

**Davis Mironga**  
Environmental Data Analyst  
davismironga@gmail.com | +254 799 604 985

**Washlab Consult Limited**  
Marlon Odhiambo

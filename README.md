# Kitui County: WASHLAB Climate-Smart WASH Pilot

**Satellite analysis of water access stress and borehole coverage gaps across all 40 wards of Kitui County, Kenya.**

Client: Washlab Consult Limited  
Analyst: Davis Mironga, Environmental Data Analyst  
Agreement date: 17 April 2026

---

## What this is

This repository contains the full analysis pipeline for the WASHLAB Climate-Smart WASH Pilot site selection in Kitui County. The work covers two phases:

**Phase 1 (complete)** builds a Water Access Stress Index from four satellite datasets, rainfall variability, vegetation condition, population exposure, and terrain difficulty, across all 40 wards at 500m resolution. It also maps seasonal water availability and identifies spatial stress clusters using Getis-Ord Gi* analysis.

**Phase 2 (in progress)** maps borehole coverage gaps, identifies communities outside walking distance of a functional borehole, and ranks pilot sites using a 100-point scoring framework. Phase 2 notebooks are built and ready to run once field assessment data are incorporated.

All code runs in Google Colab. Satellite data is accessed through Google Earth Engine at no cost. The web application is live at the link below.

**Live app:** https://kitui-washlab-analysis-csx2cpc8rfvkrefgt342ue.streamlit.app

---

## Repository structure

```
kitui-washlab-analysis/
├── notebooks/
│   ├── 01_GEE_Data_Preprocessing.ipynb     # Satellite data export to GEE Assets
│   ├── 02_Water_Stress_Index.ipynb         # WASI construction and ward mapping
│   ├── 03_Hotspot_Analysis.ipynb           # Gi* spatial clustering analysis
│   ├── 04_Coverage_Gap_Analysis.ipynb      # Borehole coverage gap (Phase 2)
│   ├── 05_Site_Prioritisation.ipynb        # 100-point site ranking (Phase 2)
│   ├── 06_Validation_and_QA.ipynb          # GPS checks and outlier review (Phase 2)
│   └── 07_Report_Figures.ipynb             # Publication-ready figure exports
│
├── app/
│   └── app.py                              # Streamlit web application
│
├── data/
│   ├── kitui_wasi_ward.geojson             # Ward polygons with WASI scores
│   ├── kitui_wasi_ward_table.csv           # 40-ward WASI table with components
│   └── kitui_hotspot_ward.geojson          # Ward hotspot classification
│
├── docs/
│   ├── analysis_plan.md
│   ├── data_dictionary.md
│   └── scoring_framework.md
│
├── requirements.txt                        # Streamlit Cloud dependencies
└── README.md
```

---

## Phase 1 results

| Deliverable | Status | Output file |
|-------------|--------|-------------|
| Water Access Stress Index map | Complete | kitui_wasi_ward.geojson |
| Seasonal water availability map | Complete | fig01_seasonal_water_availability.png |
| Vegetation stress and land condition map | Complete | fig02_vegetation_stress.png |
| Spatial hotspot analysis | Complete | kitui_hotspot_ward.geojson |
| Interactive web application | Live | streamlit.app link above |
| Phase 1 report | Complete | Phase 1 report |

### Key findings

Kanziko is the highest-stress ward in the county (WASI = 0.559), the only ward to reach the High stress class. All four stress components are simultaneously elevated there. Township ranks second (WASI = 0.540) on the strength of its population exposure alone, it has the highest household density in the county. Kyangwithya East is the sole statistically significant hotspot ward, where high population density, steep terrain, and moderate rainfall variability converge in a small geographic area.

The hotspot analysis confirms significant spatial clustering (Moran's I = 0.332, p = 0.001). A strong pixel-level stress cluster was identified in the south of the county centred on Kanziko and Ikutha, with Gi* z-scores exceeding 7.5 at the most concentrated points. This cluster is not visible in the ward-level map alone.

---

## Phase 2 status

| Deliverable | Status |
|-------------|--------|
| Borehole coverage gap map | Notebooks built, borehole data received |
| Population in gap by ward | Ready to run |
| Priority site ranking | Ready to run after coverage gap |
| Updated web application | Pending Phase 2 outputs |
| Phase 2 report | Pending Phase 2 outputs |

The borehole dataset covers 632 boreholes across 34 wards with a county-wide functionality rate of 76.5%. Six additional wards are in a separate tab and will be merged before running Notebook 04. Five ward names require reconciliation between the borehole dataset and the WASI ward names before the spatial join.

---

## Satellite data sources

| Dataset | Source | Resolution | Used for |
|---------|--------|------------|----------|
| CHIRPS v2.0 | Climate Hazards Group, UC Santa Barbara | 5 km | Rainfall variability (C2) |
| MODIS MOD13A3 | NASA Land Processes DAAC | 500 m | Vegetation condition (C3) |
| WorldPop 2020 | WorldPop, University of Southampton | 100 m | Population exposure (C4) |
| SRTM | NASA/USGS | 30 m | Terrain difficulty (C5) |
| JRC Global Surface Water | Joint Research Centre, European Commission | 30 m | Surface water mapping |
| ERA5-Land | ECMWF | 9 km | Supporting reference |

All datasets accessed through Google Earth Engine. GEE project ID: `kitui-washlab-analysis`. Asset folder: `projects/kitui-washlab-analysis/assets/kitui/`.

Ward boundaries from the American Red Cross Kenya Wards dataset (HDX, 2019), derived from IEBC and National Land Commission data. This source was used instead of GADM because it reflects the post-2013 ward structure used by county governments.

---

## Running the notebooks

All notebooks run in Google Colab. Each has an Open in Colab badge at the top. The setup cell at the top of each notebook installs all required packages.

**Order of execution for Phase 1:**
1. Notebook 01 — run once to export satellite assets to GEE. Takes 20 to 30 minutes.
2. Notebook 02 — run after Notebook 01 completes. Produces WASI outputs to Google Drive.
3. Notebook 03 — run after Notebook 02. Produces hotspot outputs to Google Drive.
4. Notebook 07 — run after Notebook 03. Produces all report figures.

**For Phase 2**, place the borehole Excel file in `Kitui_WASHLAB/boreholes/` on Google Drive, then run Notebooks 04, 05, and 06 in order.

**Google Drive folder:** `MyDrive/Kitui_WASHLAB/`

---

## Running the web app locally

```bash
git clone https://github.com/davis-mironga/kitui-washlab-analysis
cd kitui-washlab-analysis
pip install -r requirements.txt
streamlit run app/app.py
```

---

## Intellectual property

All maps, the web application, code, and methodology produced under this project belong to Washlab Consult Limited per the service agreement dated 17 April 2026. The code and methodology are published openly so the analysis can be updated as new satellite data becomes available or replicated in other counties.

---

## Contact

Davis Mironga — davismironga@gmail.com  
Washlab Consult Limited

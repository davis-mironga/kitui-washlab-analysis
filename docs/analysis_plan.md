# Analysis Plan — Kitui WASHLAB Spatial Analysis

**Client:** Washlab Consult Limited  
**Analyst:** Davis Mironga  
**Agreement date:** 17 April 2026  
**Total budget:** KES 70,000 (Phase 1: 50K | Phase 2: 20K)

Full plan document: `Kitui_WASHLAB_Analysis_Plan_v2.docx` (shared via Google Drive)

---

## Phase 1 — Water Access Stress Analysis (Weeks 1–4, KES 50,000)

### Notebooks
| Notebook | Purpose | Status |
|----------|---------|--------|
| `01_GEE_Data_Preprocessing.ipynb` | Pull MODIS/CHIRPS/SRTM/WorldPop/JRC from GEE, export to Drive | In progress |
| `02_Water_Stress_Index.ipynb` | Build 5-component WASI, ward-level aggregation | Pending |
| `03_Hotspot_Analysis.ipynb` | Gi* spatial autocorrelation, stress cluster mapping | Pending |

### Deliverables
- Water Access Stress Index map (ward + 500m raster)
- Seasonal water availability map (JRC surface water seasonality)
- Vegetation stress map (NDVI anomaly vs 1995–2005 baseline)
- Spatial hotspot map (Gi* clusters)
- Phase 1 Streamlit web app

### WASI Components
| Component | Weight | Data source |
|-----------|--------|-------------|
| Distance to nearest functional borehole | 30% | GPS-verified boreholes |
| Rainfall deficit vs long-term mean | 25% | CHIRPS v2.0 |
| NDVI below baseline | 15% | MODIS MOD13A3 |
| Population density | 20% | WorldPop 2020 |
| Terrain / slope | 10% | SRTM 30m |

---

## Phase 2 — Coverage Gap Analysis & Site Prioritisation (Weeks 5–6, KES 20,000)

### Notebooks
| Notebook | Purpose | Status |
|----------|---------|--------|
| `04_Coverage_Gap_Analysis.ipynb` | 2km buffers, population in gap, ward-level table | Data ready |
| `05_Site_Prioritisation.ipynb` | 100-point scoring, interim 45-pt ranking, live update | Data ready |
| `06_Validation_and_QA.ipynb` | GPS review, fuzzy match check, outlier flags | Ready |
| `07_Report_Figures.ipynb` | Final map and figure exports | Last |

### Deliverables
- Coverage gap map (population outside 2km of functional borehole)
- Ward-level coverage table (total population, covered, in gap, % gap)
- IoT pilot site ranking (100-point framework, interim 45-pt available now)
- Updated Streamlit app (Phase 2 layers)
- Final technical summary report (PDF)

### Walking distance threshold
**2km** — confirm with Washlab before analysis. Some counties use 1km.

---

## Key data gaps to resolve

| Gap | Impact | Owner |
|-----|--------|-------|
| Solarisation status (all 706 BH) | Cannot score Energy Compliance (20 pts) | Washlab / field team |
| 55 field-assessed scoring points | Cannot produce final site rankings | Washlab / field team |
| 199 boreholes with no GPS | Absent from coverage gap map | Field team |
| 146 GPS-review records | Cannot use in spatial analysis until verified | Davis (Notebook 06) |
| Ward boundary alignment (GADM vs dataset) | Spatial join errors | Davis (pre-analysis) |
| Walking threshold confirmation | Coverage gap definition | Washlab decision |

---

## Inputs needed from Washlab

1. Confirm 40-ward scope (6 extra wards included)
2. Solarisation status list for existing boreholes
3. Confirm 2km walking threshold or advise alternative
4. Field assessment schedule (GPS for 199 no-GPS boreholes)
5. Feedback on deliverables within 5 working days (per agreement)

---

## Weekly update schedule

Davis to send a progress update to Marlon every Monday covering:
- Notebooks completed
- Blockers / inputs needed
- Estimated completion for next milestone

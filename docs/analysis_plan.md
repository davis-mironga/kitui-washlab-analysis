# Analysis Plan — Kitui WASHLAB Spatial Analysis

## Phase 1 — Water Access Stress Analysis (Complete)

### Notebooks

| Notebook | Purpose | Status |
|----------|---------|--------|
| `01_GEE_Data_Preprocessing.ipynb` | Pull MODIS, CHIRPS, SRTM, WorldPop, JRC from GEE and export to Drive as raster assets | Complete |
| `02_Water_Stress_Index.ipynb` | Build 4-component WASI, ward-level aggregation, diagnostic maps | Complete |
| `03_Hotspot_Analysis.ipynb` | Moran's I global autocorrelation, Gi* pixel-level cluster mapping | Complete |
| `07_Report_Figures.ipynb` | Publication-ready figure exports — seasonal water, vegetation, WASI, hotspot | Complete |

### Deliverables

- Water Access Stress Index map (40 wards, 500m raster)
- Seasonal water availability and water source loss map (JRC surface water)
- Vegetation stress and land condition map (NDVI anomaly vs 2000–2004 baseline)
- Spatial hotspot map (Gi* clusters, raster-level)
- Phase 1 Streamlit web application (live)
- Phase 1 report (WASHLAB_Kitui_Phase1_Report_v7.docx)

### WASI Components (Phase 1 — four components, C1 excluded)

| Component | Code | Weight | Data source |
|-----------|------|--------|-------------|
| Rainfall variability | C2 | 35.7% | CHIRPS v2.0 |
| Vegetation anomaly | C3 | 21.4% | MODIS MOD13A3 |
| Population exposure | C4 | 28.6% | WorldPop 2020 |
| Terrain difficulty | C5 | 14.3% | SRTM 30m |
| Distance to boreholes | C1 | 30.0% (Phase 2) | Pending |

C1 is excluded from Phase 1 because the borehole dataset was not available at the time of analysis. Weights above reflect four-component renormalisation to sum to 1.0. The C1 weight shown is its planned allocation in the five-component Phase 2 index.

### Key Phase 1 findings

| Ward | WASI | Class | Key signal |
|------|------|-------|------------|
| Kanziko | 0.559 | High | All four components elevated simultaneously |
| Township | 0.540 | Moderate | Highest population exposure in county (C4 = 0.970) |
| Ikutha | 0.528 | Moderate | High rainfall variability and vegetation decline |
| Kyangwithya East | 0.468 | Moderate | Sole hotspot ward — stress spatially concentrated |

Moran's I = 0.332 (p = 0.001). Spatial clustering confirmed. 15.1% of county in hotspot pixels at 99% confidence.

---

## Phase 2 — Coverage Gap Analysis and Site Prioritisation (In progress)

### Notebooks

| Notebook | Purpose | Status |
|----------|---------|--------|
| `04_Coverage_Gap_Analysis.ipynb` | 1km buffers, population in gap, ward-level coverage table | Ready to run |
| `05_Site_Prioritisation.ipynb` | Combined WASI and coverage gap ranking | Ready to run after NB04 |
| `06_Validation_and_QA.ipynb` | GPS review, outlier flags, quality checks | Ready to run after NB05 |

### Deliverables

- Coverage gap map (population outside 1km of functional borehole)
- Ward-level coverage table (total population, covered, in gap, percentage gap)
- Priority site ranking combining WASI scores and coverage gaps
- Updated Streamlit app with Phase 2 layers
- Phase 2 report

### Walking distance threshold

**1km** — Kenya national water policy standard for rural basic access. A 2km secondary analysis is also run for comparison.

---

## Borehole dataset

| Item | Detail |
|------|--------|
| Total boreholes | 730 across all 40 wards |
| Individual records (34 wards) | 632 — used directly in spatial coverage gap analysis |
| Ward-level summaries (6 wards) | 98 boreholes across Central, Kivou, Mui, Nguni, Nuu, Waita — ward-level estimates only |
| Source | Pending |

### Ward name reconciliation required before Phase 2 spatial join

| Borehole dataset name | WASI ward name |
|-----------------------|----------------|
| Kanziko/Simisi | Kanziko |
| Kithumula/Kwa Mutonga | Kwa Mutonga/Kithumula |
| Mutitu/Kaliku | Mutito/Kaliku |
| Mutomo/Kibwea | Mutomo |
| Yatta/Kwa Vonza | Kwavonza/Yatta |

---

## Data sources

| Dataset | Source | GEE collection | Used for |
|---------|--------|----------------|---------|
| CHIRPS v2.0 | Climate Hazards Group, UC Santa Barbara | UCSB-CHG/CHIRPS/PENTAD | C2 rainfall variability |
| MODIS MOD13A3 | NASA Land Processes DAAC | MODIS/061/MOD13A3 | C3 vegetation anomaly |
| WorldPop 2020 | WorldPop, University of Southampton | WorldPop/GP/100m/pop | C4 population exposure |
| SRTM 30m | NASA/USGS | USGS/SRTMGL1_003 | C5 terrain difficulty |
| JRC Global Surface Water | Joint Research Centre, European Commission | JRC/GSW1_4/GlobalSurfaceWater | Surface water mapping |
| Kenya Ward Boundaries | American Red Cross, derived from IEBC and NLC | HDX: administrative-wards-in-kenya-1450 | Spatial aggregation |

GEE project ID: `kitui-washlab-analysis`
Asset folder: `projects/kitui-washlab-analysis/assets/kitui/`

---

## Key links

| Resource | Link |
|----------|------|
| GitHub repository | github.com/davis-mironga/kitui-washlab-analysis |
| Streamlit app | kitui-washlab-analysis-csx2cpc8rfvkrefgt342ue.streamlit.app |
| Google Drive | MyDrive/Kitui_WASHLAB/ |

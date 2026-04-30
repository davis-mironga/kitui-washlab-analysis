"""
WASHLAB Climate-Smart WASH Pilot — Kitui County
Interactive Spatial Analysis Web Application

Author: Davis Mironga
Client: Washlab Consult Limited
"""

import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import st_folium
from shapely.geometry import Point

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Kitui County WASH Analysis",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Colour palette (matches project design) ───────────────────────────────────
COLOURS = {
    'Functional':               '#2E75B6',
    'Non-Functional':           '#C00000',
    'Unknown':                  '#FFC000',
    'Partially Functional':     '#ED7D31',
    'Under Construction':       '#70AD47',
    'verified_gps':             '#2E75B6',
    'review_gps':               '#FFC000',
    'no_gps':                   '#808080',
    'coverage_fill':            '#2E75B6',
    'hotspot_high':             '#C00000',
    'hotspot_low':              '#70AD47',
}

# ── Sidebar ───────────────────────────────────────────────────────────────────
st.sidebar.image(
    "https://via.placeholder.com/200x60/0B5394/FFFFFF?text=WASHLAB+Kitui",
    use_column_width=True,
)
st.sidebar.title("Kitui County WASH Analysis")
st.sidebar.markdown("*WASHLAB Climate-Smart WASH Pilot*")
st.sidebar.markdown("---")

phase = st.sidebar.radio(
    "Select phase",
    ["Phase 1 — Water Stress", "Phase 2 — Coverage & Priority Sites"],
    index=0,
)

# ── Data loading ──────────────────────────────────────────────────────────────
@st.cache_data
def load_boreholes():
    """Load GPS-verified boreholes from master dataset."""
    # TODO: Update path for deployment
    # Option 1: Load from Google Drive (local dev)
    # Option 2: Load from GitHub raw URL (deployment)
    # Option 3: Load from uploaded file
    try:
        df = pd.read_excel(
            'data/boreholes/Kitui_Boreholes_Master_Dataset.xlsx',
            sheet_name='B_Spatial_Analysis',
            header=2
        )
        gdf = gpd.GeoDataFrame(
            df,
            geometry=[Point(xy) for xy in zip(df['Longitude'], df['Latitude'])],
            crs='EPSG:4326'
        )
        return gdf
    except FileNotFoundError:
        st.warning("Borehole data file not found. Using sample data for demo.")
        return None

# ── Phase 1 view ─────────────────────────────────────────────────────────────
if "Phase 1" in phase:
    st.title("💧 Water Access Stress Analysis")
    st.markdown("Kitui County — Satellite-derived water stress mapping across 40 wards.")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Boreholes", "706")
    col2.metric("GPS Verified", "361")
    col3.metric("Functional", "531")
    col4.metric("Wards Covered", "40")

    st.markdown("---")

    # Map placeholder
    st.subheader("Water Access Stress Index")
    st.info(
        "🔄 Phase 1 satellite analysis in progress. "
        "The stress index map will appear here once GEE exports are complete."
    )

    # Borehole map (available now)
    st.subheader("Existing Borehole Network")
    layer_choice = st.sidebar.multiselect(
        "Show boreholes by status",
        ["Functional", "Non-Functional", "Unknown"],
        default=["Functional", "Non-Functional"],
    )

    gdf = load_boreholes()
    if gdf is not None:
        m = folium.Map(
            location=[-1.3, 38.0],
            zoom_start=8,
            tiles='CartoDB positron'
        )
        for status in layer_choice:
            subset = gdf[gdf['Functionality_Status'].str.contains(
                status.replace('Non-Functional', 'Non-Functional'), na=False)]
            colour = COLOURS.get(status, '#808080')
            for _, row in subset.iterrows():
                folium.CircleMarker(
                    location=[row['Latitude'], row['Longitude']],
                    radius=5,
                    color=colour,
                    fill=True,
                    fill_color=colour,
                    fill_opacity=0.7,
                    popup=folium.Popup(
                        f"<b>{row['Borehole_Name']}</b><br>"
                        f"Ward: {row['Ward']}<br>"
                        f"Status: {row['Functionality_Status']}<br>"
                        f"Management: {row['Management_Type']}",
                        max_width=250
                    )
                ).add_to(m)

        st_folium(m, width=None, height=500, returned_objects=[])
    else:
        st.map(pd.DataFrame({'lat': [-1.3], 'lon': [38.0]}))

# ── Phase 2 view ─────────────────────────────────────────────────────────────
elif "Phase 2" in phase:
    st.title("📍 Coverage Gap Analysis & Priority Sites")
    st.markdown("Identifying underserved communities and ranking IoT pilot sites.")

    st.info(
        "🔄 Phase 2 analysis will be available after Phase 1 is complete "
        "and field assessment data is received."
    )

    st.subheader("100-Point Scoring Framework")
    scoring_data = {
        'Criterion': [
            'Population Served', 'Reliable Yield', 'Borehole Ownership',
            'Additionality Strength', 'Safe-Water Potential', 'Rehabilitation Cost',
            'Viable Drinking Water Use', 'IoT Viability', 'Energy Compliance'
        ],
        'Max Points': [20, 15, 10, 20, 10, 10, 5, 5, 20],
        'Data Status': [
            'Available', 'Available', 'Available',
            'Field assessment required', 'Lab tests required', 'Engineering assessment required',
            'Field assessment required', 'Site survey required', 'Field verification required'
        ],
    }
    st.dataframe(
        pd.DataFrame(scoring_data),
        use_container_width=True,
        hide_index=True,
    )

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "*Analysis by Davis Mironga for Washlab Consult Limited | Kitui County, Kenya | April 2026*"
)

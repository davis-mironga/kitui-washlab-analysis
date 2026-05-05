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
import json

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Kitui WASH Analysis",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Brand colours ─────────────────────────────────────────────────────────────
C = {
    'blue':       '#0B5394',
    'light_blue': '#2E75B6',
    'red':        '#C00000',
    'orange':     '#ED7D31',
    'green':      '#70AD47',
    'yellow':     '#FFC000',
    'grey':       '#808080',
}

STATUS_COLOURS = {
    'Functional':                        C['light_blue'],
    'Functional - Needs Rehabilitation':  C['yellow'],
    'Functional - At Risk':               C['orange'],
    'Partially Functional':               '#FF9900',
    'Non-Functional':                     C['red'],
    'Non-Functional - Not Equipped':      '#FF6666',
    'Non-Functional - Abandoned':         '#AA0000',
    'Non-Functional - Capped':            '#880000',
    'Non-Functional - Obsolete':          '#660000',
    'Under Construction':                 C['green'],
    'Unknown':                            C['grey'],
}

HOTSPOT_COLOURS = {
    'Hotspot (99%)':   '#C00000',
    'Hotspot (95%)':   '#FF6666',
    'Hotspot (90%)':   '#FFAAAA',
    'Not significant': '#E0E0E0',
    'Coldspot (90%)':  '#AACCEE',
    'Coldspot (95%)':  '#2E75B6',
    'Coldspot (99%)':  '#0B5394',
}

WASI_CMAP = ['#1a9641', '#a6d96a', '#ffffbf', '#fdae61', '#d7191c']

# ── Data loading ──────────────────────────────────────────────────────────────
@st.cache_data
def load_boreholes():
    try:
        df = pd.read_excel(
            'data/boreholes/Kitui_Boreholes_Master_Dataset.xlsx',
            sheet_name='B_Spatial_Analysis',
            header=2
        )
        gps = df[df['GPS_Available'] == True].copy()
        gdf = gpd.GeoDataFrame(
            gps,
            geometry=[Point(xy) for xy in zip(gps['Longitude'], gps['Latitude'])],
            crs='EPSG:4326'
        )
        return df, gdf
    except FileNotFoundError:
        return None, None

@st.cache_data
def load_wasi_wards():
    try:
        return gpd.read_file('data/boundaries/kitui_wasi_ward.geojson')
    except Exception:
        return None

@st.cache_data
def load_hotspot_wards():
    try:
        return gpd.read_file('data/boundaries/kitui_hotspot_ward.geojson')
    except Exception:
        return None

@st.cache_data
def load_coverage():
    try:
        table = pd.read_csv('data/boundaries/kitui_coverage_gap_ward_table.csv')
        gap   = gpd.read_file('data/boundaries/kitui_coverage_gap.geojson')
        return table, gap
    except Exception:
        return None, None

@st.cache_data
def load_rankings():
    try:
        return pd.read_excel('data/boreholes/kitui_borehole_interim_rankings.xlsx')
    except Exception:
        return None

df_all, gdf_bh = load_boreholes()
wasi_wards      = load_wasi_wards()
hotspot_wards   = load_hotspot_wards()
coverage_table, coverage_gap = load_coverage()
rankings        = load_rankings()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        f"""
        <div style='background:{C["blue"]};padding:16px 12px;border-radius:8px;margin-bottom:12px'>
        <h3 style='color:white;margin:0;font-size:16px'>💧 WASHLAB Kitui</h3>
        <p style='color:#BDD7EE;margin:4px 0 0;font-size:12px'>Climate-Smart WASH Pilot</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    phase = st.radio(
        "Select view",
        ["Phase 1 — Water Stress", "Phase 2 — Coverage & Priority Sites"],
        index=0,
    )

    st.markdown("---")

    if "Phase 1" in phase:
        st.markdown("**Phase 1 layers**")
        show_boreholes = st.checkbox("Borehole network", value=True)
        show_wasi      = st.checkbox("WASI choropleth", value=bool(wasi_wards is not None))
        show_hotspots  = st.checkbox("Hotspot clusters", value=False)

        st.markdown("**Borehole filter**")
        status_opts = ['Functional', 'Non-Functional', 'Partially Functional',
                       'Unknown', 'Under Construction']
        selected_statuses = st.multiselect("Functionality status",
                                           status_opts, default=['Functional', 'Non-Functional'])
        gps_filter = st.selectbox("GPS quality", ["All", "Verified only",
                                                   "Verified + Needs Review"])
    else:
        walk_km = st.selectbox("Walking threshold (km)", [1.0, 2.0, 3.0], index=1)
        show_gap_map = st.checkbox("Coverage gap map", value=True)
        show_rankings_map = st.checkbox("IoT candidate sites", value=True)
        min_score = st.slider("Minimum interim score (of 45)", 0, 45, 25)

    st.markdown("---")
    st.caption("Analyst: Davis Mironga  \nWashlab Consult Limited  \nKitui County, Kenya — 2026")

# ── Helper: GPS filter ────────────────────────────────────────────────────────
def apply_gps_filter(gdf, gps_filter):
    if gdf is None:
        return None
    if gps_filter == "Verified only":
        return gdf[gdf['GPS_Quality'] == 'Verified']
    elif gps_filter == "Verified + Needs Review":
        return gdf[gdf['GPS_Quality'].isin(['Verified', 'Needs Review - Shared Coordinates'])]
    return gdf

# ── Helper: summary metrics ────────────────────────────────────────────────────
def metric_row(total, verified, functional, wards_covered):
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Boreholes", f"{total:,}")
    c2.metric("GPS Verified", f"{verified:,}")
    c3.metric("Functional", f"{functional:,}")
    c4.metric("Wards Covered", f"{wards_covered}/40")

# ── Phase 1 ───────────────────────────────────────────────────────────────────
if "Phase 1" in phase:
    st.title("💧 Water Access Stress Analysis")
    st.markdown("Kitui County, Kenya — satellite-derived water stress index across 40 wards.")

    if df_all is not None:
        metric_row(
            total=len(df_all),
            verified=int((df_all['GPS_Quality'] == 'Verified').sum()),
            functional=int(df_all['Is_Functional'].sum()),
            wards_covered=df_all['Ward'].nunique(),
        )
    else:
        metric_row(706, 361, 531, 40)

    st.markdown("---")

    # ── Map ───────────────────────────────────────────────────────────────────
    m = folium.Map(location=[-1.3, 38.0], zoom_start=8, tiles='CartoDB positron')

    # WASI choropleth layer
    if show_wasi and wasi_wards is not None:
        def wasi_style(feature):
            val = feature['properties'].get('WASI_mean', 0) or 0
            # Simple 5-step colour scale
            if val >= 0.70: colour = '#d7191c'
            elif val >= 0.55: colour = '#fdae61'
            elif val >= 0.40: colour = '#ffffbf'
            elif val >= 0.25: colour = '#a6d96a'
            else: colour = '#1a9641'
            return {'fillColor': colour, 'color': '#888888',
                    'weight': 0.6, 'fillOpacity': 0.55}

        folium.GeoJson(
            json.loads(wasi_wards.to_json()),
            name='WASI (ward)',
            style_function=wasi_style,
            tooltip=folium.GeoJsonTooltip(
                fields=['Ward', 'WASI_mean', 'Stress_Class', 'Functional_BH_Count'],
                aliases=['Ward', 'WASI score', 'Stress class', 'Functional BH'],
                localize=True,
            ),
        ).add_to(m)

        # WASI legend
        legend_html = """
        <div style='position:fixed;bottom:40px;left:40px;z-index:9999;background:white;
                    padding:10px;border-radius:6px;border:1px solid #ccc;font-size:11px'>
        <b>WASI (water stress)</b><br>
        <span style='background:#d7191c'>&nbsp;&nbsp;&nbsp;</span> Very High (≥0.70)<br>
        <span style='background:#fdae61'>&nbsp;&nbsp;&nbsp;</span> High (0.55–0.70)<br>
        <span style='background:#ffffbf'>&nbsp;&nbsp;&nbsp;</span> Moderate (0.40–0.55)<br>
        <span style='background:#a6d96a'>&nbsp;&nbsp;&nbsp;</span> Low (0.25–0.40)<br>
        <span style='background:#1a9641'>&nbsp;&nbsp;&nbsp;</span> Very Low (&lt;0.25)
        </div>
        """
        m.get_root().html.add_child(folium.Element(legend_html))

    elif show_wasi:
        st.info("WASI layer not available — run Notebook 02 and upload `kitui_wasi_ward.geojson` to `data/boundaries/`.")

    # Hotspot layer
    if show_hotspots and hotspot_wards is not None:
        def hotspot_style(feature):
            cls = feature['properties'].get('Hotspot_Class', 'Not significant')
            return {'fillColor': HOTSPOT_COLOURS.get(cls, '#E0E0E0'),
                    'color': '#888888', 'weight': 0.6, 'fillOpacity': 0.6}

        folium.GeoJson(
            json.loads(hotspot_wards.to_json()),
            name='Hotspot clusters',
            style_function=hotspot_style,
            tooltip=folium.GeoJsonTooltip(
                fields=['Ward', 'Hotspot_Class', 'Gi_Zs'],
                aliases=['Ward', 'Cluster type', 'Gi* Z-score'],
            ),
        ).add_to(m)

    elif show_hotspots:
        st.info("Hotspot layer not available — run Notebook 03 and upload `kitui_hotspot_ward.geojson` to `data/boundaries/`.")

    # Borehole layer
    if show_boreholes and gdf_bh is not None:
        filtered = apply_gps_filter(gdf_bh, gps_filter)

        # Apply status filter
        def matches_status(status_val, selected):
            for s in selected:
                if s == 'Non-Functional' and 'Non-Functional' in str(status_val):
                    return True
                if s != 'Non-Functional' and s in str(status_val):
                    return True
            return False

        filtered = filtered[filtered['Functionality_Status'].apply(
            lambda x: matches_status(x, selected_statuses)
        )]

        for _, row in filtered.iterrows():
            status = str(row.get('Functionality_Status', 'Unknown'))
            colour = next(
                (v for k, v in STATUS_COLOURS.items() if k in status),
                C['grey']
            )
            folium.CircleMarker(
                location=[row['Latitude'], row['Longitude']],
                radius=4,
                color=colour,
                fill=True,
                fill_color=colour,
                fill_opacity=0.8,
                popup=folium.Popup(
                    f"<b>{row.get('Borehole_Name', 'N/A')}</b><br>"
                    f"ID: {row.get('Borehole_ID', '')}<br>"
                    f"Ward: {row.get('Ward', '')}<br>"
                    f"Sub-county: {row.get('Sub_County', '')}<br>"
                    f"Status: {status}<br>"
                    f"Management: {row.get('Management_Type', '')}<br>"
                    f"GPS: {row.get('GPS_Quality', '')}<br>"
                    f"Yield: {row.get('Yield_m3_hr', 'N/A')} m³/hr<br>"
                    f"HH served: {row.get('Population_Served_HHs', 'N/A')}",
                    max_width=280
                )
            ).add_to(m)

    folium.LayerControl().add_to(m)
    st_folium(m, width=None, height=520, returned_objects=[])

    # ── WASI ward table ───────────────────────────────────────────────────────
    if wasi_wards is not None:
        st.markdown("---")
        st.subheader("Ward-Level WASI Summary")

        wasi_df = wasi_wards.drop(columns='geometry', errors='ignore')
        stress_filter = st.multiselect(
            "Filter by stress class",
            ['Very High', 'High', 'Moderate', 'Low', 'Very Low'],
            default=['Very High', 'High'],
        )
        if stress_filter:
            wasi_df = wasi_df[wasi_df['Stress_Class'].isin(stress_filter)]

        wasi_df = wasi_df.sort_values('WASI_mean', ascending=False).reset_index(drop=True)

        def colour_wasi(val):
            if isinstance(val, float):
                if val >= 0.70: return 'background-color: #FFCCCC'
                if val >= 0.55: return 'background-color: #FFE5CC'
                if val >= 0.40: return 'background-color: #FFFFCC'
                if val >= 0.25: return 'background-color: #E5FFCC'
                return 'background-color: #CCFFCC'
            return ''

        display_cols = [c for c in ['Ward', 'WASI_mean', 'Stress_Class', 'Functional_BH_Count']
                        if c in wasi_df.columns]
        st.dataframe(
            wasi_df[display_cols].style.applymap(colour_wasi, subset=['WASI_mean']),
            use_container_width=True,
            hide_index=True,
        )

        csv = wasi_df[display_cols].to_csv(index=False).encode()
        st.download_button("Download WASI ward table (CSV)", csv,
                           "kitui_wasi_ward.csv", "text/csv")

    # ── Borehole summary table ────────────────────────────────────────────────
    if df_all is not None:
        st.markdown("---")
        with st.expander("Borehole dataset summary", expanded=False):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Functionality status**")
                st.dataframe(
                    df_all['Functionality_Status'].value_counts().rename_axis('Status').reset_index(name='Count'),
                    use_container_width=True, hide_index=True
                )
            with col2:
                st.markdown("**GPS quality**")
                st.dataframe(
                    df_all['GPS_Quality'].value_counts().rename_axis('GPS Quality').reset_index(name='Count'),
                    use_container_width=True, hide_index=True
                )

            st.markdown("**Boreholes by sub-county**")
            ward_summary = (
                df_all.groupby('Sub_County')
                .agg(
                    Total=('Borehole_ID', 'count'),
                    Functional=('Is_Functional', 'sum'),
                    GPS_Verified=('GPS_Quality', lambda x: (x == 'Verified').sum()),
                    No_GPS=('GPS_Quality', lambda x: (x == 'No GPS').sum()),
                )
                .reset_index()
                .sort_values('Total', ascending=False)
            )
            ward_summary['Functional %'] = (ward_summary['Functional'] / ward_summary['Total'] * 100).round(1)
            st.dataframe(ward_summary, use_container_width=True, hide_index=True)

# ── Phase 2 ───────────────────────────────────────────────────────────────────
elif "Phase 2" in phase:
    st.title("📍 Coverage Gap Analysis & IoT Priority Sites")
    st.markdown("Identifying underserved communities and ranking boreholes for IoT pilot selection.")

    # Coverage metrics
    if coverage_table is not None:
        total_pop     = coverage_table['Total_Population'].sum()
        covered_pop   = coverage_table['Population_Covered'].sum()
        gap_pop       = coverage_table['Population_Gap'].sum()
        gap_pct       = gap_pop / total_pop * 100 if total_pop > 0 else 0
        wards_high    = (coverage_table['Pct_Pop_Gap'] > 50).sum()

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Population", f"{total_pop:,.0f}")
        c2.metric("Within 2km of BH", f"{covered_pop:,.0f}")
        c3.metric("Population in Gap", f"{gap_pop:,.0f}", f"{gap_pct:.1f}%")
        c4.metric("Wards >50% Gap", f"{wards_high}")
    else:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Walk threshold", f"{walk_km} km")
        c2.metric("GPS-verified BH", "361")
        c3.metric("Total boreholes", "706")
        c4.metric("Wards", "40")

    st.markdown("---")

    # ── Coverage map ──────────────────────────────────────────────────────────
    if show_gap_map:
        m2 = folium.Map(location=[-1.3, 38.0], zoom_start=8, tiles='CartoDB positron')

        if coverage_gap is not None:
            folium.GeoJson(
                json.loads(coverage_gap.to_json()),
                name=f'Coverage gap (>{walk_km}km from BH)',
                style_function=lambda x: {'fillColor': C['red'], 'color': '#880000',
                                           'weight': 0.5, 'fillOpacity': 0.35},
                tooltip=folium.GeoJsonTooltip(fields=['Ward'], aliases=['Ward']),
            ).add_to(m2)
        else:
            st.info("Coverage gap layer not available — run Notebook 04 and upload `kitui_coverage_gap.geojson` to `data/boundaries/`.")

        # IoT candidate sites
        if show_rankings_map and rankings is not None:
            top_candidates = rankings[
                (rankings['Score_45'] >= min_score) &
                (rankings['GPS_Quality'] == 'Verified') &
                (rankings['Latitude'].notna())
            ]
            for _, row in top_candidates.iterrows():
                score = row.get('Score_45', 0)
                colour = C['blue'] if score >= 35 else C['light_blue'] if score >= 25 else C['grey']
                folium.CircleMarker(
                    location=[row['Latitude'], row['Longitude']],
                    radius=6,
                    color=colour,
                    fill=True,
                    fill_color=colour,
                    fill_opacity=0.9,
                    popup=folium.Popup(
                        f"<b>{row.get('Borehole_Name', '')}</b><br>"
                        f"Ward: {row.get('Ward', '')}<br>"
                        f"Interim score: {score}/45<br>"
                        f"Management: {row.get('Management_Type', '')}<br>"
                        f"Status: {row.get('Functionality_Status', '')}<br>"
                        f"<i>55 field pts still pending</i>",
                        max_width=280
                    )
                ).add_to(m2)

        folium.LayerControl().add_to(m2)
        st_folium(m2, width=None, height=520, returned_objects=[])

    # ── Coverage table ────────────────────────────────────────────────────────
    if coverage_table is not None:
        st.markdown("---")
        st.subheader("Coverage Gap by Ward")
        ct = coverage_table.sort_values('Pct_Pop_Gap', ascending=False)
        st.dataframe(ct, use_container_width=True, hide_index=True)
        csv = ct.to_csv(index=False).encode()
        st.download_button("Download coverage table (CSV)", csv,
                           "kitui_coverage_gap.csv", "text/csv")

    # ── Rankings table ────────────────────────────────────────────────────────
    st.markdown("---")
    st.subheader("IoT Pilot Site Rankings")

    if rankings is not None:
        rank_cols = [c for c in [
            'Interim_Rank', 'Borehole_ID', 'Sub_County', 'Ward', 'Borehole_Name',
            'Score_45', 'Score_Pop', 'Score_Yield', 'Score_Ownership',
            'Field_Pts_Pending', 'GPS_Quality', 'Functionality_Status',
            'Management_Type', 'Population_Served_HHs', 'Yield_m3_hr'
        ] if c in rankings.columns]

        filtered_rankings = rankings[rankings['Score_45'] >= min_score][rank_cols]
        st.dataframe(filtered_rankings, use_container_width=True, hide_index=True)

        csv = filtered_rankings.to_csv(index=False).encode()
        st.download_button("Download interim rankings (CSV)", csv,
                           "kitui_interim_rankings.csv", "text/csv")

        st.warning(
            "**Interim rankings only** — these reflect 45 of 100 available points. "
            "The remaining 55 points require field assessment (additionality, water quality, "
            "rehabilitation cost, IoT viability, energy compliance). "
            "Do not use for final site selection until field data is collected."
        )
    else:
        st.info("Rankings not available — run Notebook 05 and upload `kitui_borehole_interim_rankings.xlsx` to `data/boreholes/`.")

    # ── Scoring framework ─────────────────────────────────────────────────────
    st.markdown("---")
    with st.expander("100-Point Scoring Framework", expanded=False):
        scoring_data = {
            'Criterion': [
                'Population Served', 'Reliable Yield', 'Borehole Ownership',
                'Additionality Strength', 'Safe-Water Potential', 'Rehabilitation Cost',
                'Viable Drinking Water Use', 'IoT Viability', 'Energy Compliance'
            ],
            'Max Points': [20, 15, 10, 20, 10, 10, 5, 5, 20],
            'Data Status': [
                'Available (scored)', 'Available (scored)', 'Available (scored)',
                'Field assessment required', 'Lab tests required', 'Engineering assessment required',
                'Field verification required', 'Site survey required', 'Field verification required'
            ],
            'Notes': [
                'HH served — 5 tiers', 'Yield m³/hr — threshold 2.5 m³/hr', 'Management type mapping',
                'Sustainability without project?', 'Microbial/chemical risk', 'Non-functional BH only',
                'Suitability for drinking', 'Casing, panel space, connectivity', 'Solar > grid > diesel'
            ]
        }
        st.dataframe(
            pd.DataFrame(scoring_data),
            use_container_width=True,
            hide_index=True,
        )

        st.markdown("""
        **Priority thresholds:**
        - **First Priority:** 80+ / 100 — recommended for IoT pilot
        - **Second Priority:** 65–79 / 100 — considered if first pool insufficient
        - **Conditional:** below 65 — requires significant justification
        """)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    f"<small>Analysis by Davis Mironga for Washlab Consult Limited | "
    f"Kitui County, Kenya | April 2026 | "
    f"<a href='mailto:davismironga@gmail.com'>davismironga@gmail.com</a></small>",
    unsafe_allow_html=True,
)

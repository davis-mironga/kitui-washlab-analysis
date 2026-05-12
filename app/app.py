import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px
import plotly.graph_objects as go
import json
import numpy as np

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title='WASHLAB Kitui — Water Access Stress Index',
    page_icon='💧',
    layout='wide',
    initial_sidebar_state='expanded'
)

# ── Data loading ──────────────────────────────────────────────────────────────
REPO = 'https://raw.githubusercontent.com/davis-mironga/kitui-washlab-analysis/main/data/'

@st.cache_data
def load_data():
    table    = pd.read_csv(REPO + 'kitui_wasi_ward_table.csv')
    wasi_geo = gpd.read_file(REPO + 'kitui_wasi_ward.geojson')
    hs_geo   = gpd.read_file(REPO + 'kitui_hotspot_ward.geojson')
    # Merge component scores into geo
    wasi_geo = wasi_geo.merge(
        table[['Ward','WASI_std','C2_Rainfall','C3_NDVI','C4_Population','C5_Slope']],
        on='Ward', how='left'
    )
    return table, wasi_geo, hs_geo

table, wasi_geo, hs_geo = load_data()

# ── Colour helpers ────────────────────────────────────────────────────────────
STRESS_COLOURS = {
    'Very High': '#C00000',
    'High':      '#E26B0A',
    'Moderate':  '#F6C344',
    'Low':       '#A9D18E',
    'Very Low':  '#375623',
}
HOTSPOT_COLOURS = {
    'Hotspot':         '#C00000',
    'Not significant': '#D9D9D9',
    'Coldspot':        '#2E75B6',
}

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image(
        'https://raw.githubusercontent.com/davis-mironga/kitui-washlab-analysis/main/app/assets/logo_placeholder.png',
        use_column_width=True
    ) if False else None  # placeholder — add logo later

    st.title('WASHLAB')
    st.caption('Climate-Smart WASH Pilot — Kitui County')
    st.markdown('---')

    st.subheader('Filters')
    stress_filter = st.multiselect(
        'Stress class',
        options=['Very High', 'High', 'Moderate', 'Low', 'Very Low'],
        default=['Very High', 'High', 'Moderate', 'Low', 'Very Low']
    )
    wasi_range = st.slider(
        'WASI score range',
        min_value=0.0, max_value=1.0,
        value=(0.0, 1.0), step=0.01
    )

    st.markdown('---')
    st.caption('Phase 1 — satellite analysis only')
    st.caption('C1 (boreholes) pending data receipt')
    st.caption('Source: CHIRPS, MODIS, WorldPop, SRTM')

# ── Filter data ───────────────────────────────────────────────────────────────
filtered = table[
    (table['Stress_Class'].isin(stress_filter)) &
    (table['WASI_mean'] >= wasi_range[0]) &
    (table['WASI_mean'] <= wasi_range[1])
].copy()

filtered_geo = wasi_geo[wasi_geo['Ward'].isin(filtered['Ward'])].copy()

# ── Header ────────────────────────────────────────────────────────────────────
st.title('Water Access Stress Index — Kitui County')
st.markdown(
    'Phase 1 satellite analysis combining rainfall variability, vegetation stress, '
    'population exposure, and terrain difficulty across all 40 wards.'
)

# ── KPI row ───────────────────────────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric('Total wards', 40)
k2.metric('High stress wards', int((table['Stress_Class'] == 'High').sum()))
k3.metric('Moderate stress', int((table['Stress_Class'] == 'Moderate').sum()))
k4.metric('Highest WASI ward', table.loc[table['WASI_mean'].idxmax(), 'Ward'])
k5.metric('County mean WASI', f"{table['WASI_mean'].mean():.3f}")

st.markdown('---')

# ── Tab layout ────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    'WASI Map', 'Component Analysis', 'Hotspot Analysis', 'Ward Data Table'
])

# ── TAB 1: WASI Map ───────────────────────────────────────────────────────────
with tab1:
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader('Water Access Stress Index by Ward')

        geojson_data = json.loads(filtered_geo.to_json())

        fig_map = px.choropleth_mapbox(
            filtered_geo,
            geojson=geojson_data,
            locations=filtered_geo.index,
            color='WASI_mean',
            color_continuous_scale=[
                [0.0,  '#375623'],
                [0.25, '#A9D18E'],
                [0.40, '#F6C344'],
                [0.55, '#E26B0A'],
                [0.70, '#C00000'],
                [1.0,  '#7B0000'],
            ],
            range_color=[0, 1],
            mapbox_style='carto-positron',
            zoom=7,
            center={'lat': -1.5, 'lon': 38.3},
            opacity=0.75,
            hover_data={
                'Ward':         True,
                'WASI_mean':    ':.3f',
                'Stress_Class': True,
                'C2_Rainfall':  ':.3f',
                'C3_NDVI':      ':.3f',
                'C4_Population':':.3f',
                'C5_Slope':     ':.3f',
            },
            labels={
                'WASI_mean':    'WASI Score',
                'Stress_Class': 'Stress Class',
                'C2_Rainfall':  'C2 Rainfall',
                'C3_NDVI':      'C3 NDVI',
                'C4_Population':'C4 Population',
                'C5_Slope':     'C5 Slope',
            }
        )
        fig_map.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),
            coloraxis_colorbar=dict(
                title='WASI Score',
                tickvals=[0, 0.25, 0.40, 0.55, 0.70, 1.0],
                ticktext=['0.00', '0.25 (Low)', '0.40 (Mod)', '0.55 (High)', '0.70 (V.High)', '1.00'],
            ),
            height=550
        )
        st.plotly_chart(fig_map, use_container_width=True)
        st.caption(
            'Hover over a ward to see its WASI score and component breakdown. '
            'C1 (distance to boreholes) not included — borehole dataset pending.'
        )

    with col2:
        st.subheader('Stress Class Distribution')
        class_counts = table['Stress_Class'].value_counts().reindex(
            ['Very High', 'High', 'Moderate', 'Low', 'Very Low'], fill_value=0
        ).reset_index()
        class_counts.columns = ['Class', 'Count']
        class_counts['Colour'] = class_counts['Class'].map(STRESS_COLOURS)

        fig_bar = px.bar(
            class_counts, x='Count', y='Class', orientation='h',
            color='Class',
            color_discrete_map=STRESS_COLOURS,
            text='Count'
        )
        fig_bar.update_layout(
            showlegend=False, height=250,
            margin=dict(l=0, r=0, t=10, b=0),
            xaxis_title='Number of wards',
            yaxis_title=''
        )
        fig_bar.update_traces(textposition='outside')
        st.plotly_chart(fig_bar, use_container_width=True)

        st.subheader('Top 10 Highest Stress Wards')
        top10 = table.nlargest(10, 'WASI_mean')[['Ward', 'WASI_mean', 'Stress_Class']].copy()
        top10['WASI_mean'] = top10['WASI_mean'].round(3)
        top10 = top10.reset_index(drop=True)
        top10.index += 1
        st.dataframe(top10, use_container_width=True)

# ── TAB 2: Component Analysis ─────────────────────────────────────────────────
with tab2:
    st.subheader('WASI Component Breakdown by Ward')
    st.caption(
        'Each bar shows the weighted contribution of the four components. '
        'The black dot shows the final WASI composite score.'
    )

    comp_sorted = table.sort_values('WASI_mean', ascending=True).copy()
    comp_cols   = ['C2_Rainfall', 'C3_NDVI', 'C4_Population', 'C5_Slope']
    weights     = [0.357, 0.214, 0.286, 0.143]
    colours     = ['#2E75B6', '#70AD47', '#ED7D31', '#FFC000']
    labels      = ['C2: Rainfall (35.7%)', 'C3: NDVI (21.4%)', 'C4: Population (28.6%)', 'C5: Slope (14.3%)']

    fig_comp = go.Figure()
    for col, w, colour, label in zip(comp_cols, weights, colours, labels):
        vals = comp_sorted[col].fillna(0) * w
        fig_comp.add_trace(go.Bar(
            y=comp_sorted['Ward'],
            x=vals,
            name=label,
            orientation='h',
            marker_color=colour,
            marker_opacity=0.85,
        ))

    fig_comp.add_trace(go.Scatter(
        y=comp_sorted['Ward'],
        x=comp_sorted['WASI_mean'],
        mode='markers',
        name='WASI composite',
        marker=dict(color='black', size=5, symbol='circle'),
    ))

    fig_comp.update_layout(
        barmode='stack',
        height=900,
        margin=dict(l=0, r=0, t=10, b=0),
        xaxis_title='Weighted stress contribution',
        yaxis_title='',
        legend=dict(orientation='h', yanchor='bottom', y=1.01, xanchor='left', x=0),
        xaxis=dict(range=[0, 0.75]),
    )
    fig_comp.add_vline(x=0.55, line_dash='dash', line_color='red', opacity=0.4,
                       annotation_text='High threshold', annotation_position='top right')
    st.plotly_chart(fig_comp, use_container_width=True)

    st.subheader('Select a ward for detailed breakdown')
    selected_ward = st.selectbox(
        'Ward', options=sorted(table['Ward'].tolist())
    )
    ward_row = table[table['Ward'] == selected_ward].iloc[0]

    wc1, wc2, wc3, wc4, wc5 = st.columns(5)
    wc1.metric('WASI Score', f"{ward_row['WASI_mean']:.3f}")
    wc2.metric('C2 Rainfall', f"{ward_row['C2_Rainfall']:.3f}")
    wc3.metric('C3 NDVI', f"{ward_row['C3_NDVI']:.3f}")
    wc4.metric('C4 Population', f"{ward_row['C4_Population']:.3f}")
    wc5.metric('C5 Slope', f"{ward_row['C5_Slope']:.3f}")

    fig_radar = go.Figure(go.Scatterpolar(
        r=[ward_row['C2_Rainfall'], ward_row['C3_NDVI'],
           ward_row['C4_Population'], ward_row['C5_Slope'],
           ward_row['C2_Rainfall']],
        theta=['C2 Rainfall', 'C3 NDVI', 'C4 Population', 'C5 Slope', 'C2 Rainfall'],
        fill='toself',
        fillcolor='rgba(46, 117, 182, 0.3)',
        line=dict(color='#2E75B6'),
        name=selected_ward
    ))
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        height=350,
        margin=dict(l=40, r=40, t=40, b=40),
        title=f'Component profile — {selected_ward}'
    )
    st.plotly_chart(fig_radar, use_container_width=True)

# ── TAB 3: Hotspot Analysis ───────────────────────────────────────────────────
with tab3:
    st.subheader('Spatial Water Stress Clustering — Getis-Ord Gi*')
    st.markdown(
        "**Moran's I = 0.332 (p = 0.001)** — water stress is significantly clustered spatially, "
        "not randomly distributed. The map shows which wards form statistically significant clusters."
    )

    hc1, hc2 = st.columns([2, 1])

    with hc1:
        hs_geojson = json.loads(hs_geo.to_json())
        hs_geo_plot = hs_geo.copy()
        hs_geo_plot['colour_val'] = hs_geo_plot['Ward_Class'].map(
            {'Hotspot': 1, 'Not significant': 0, 'Coldspot': -1}
        ).fillna(0)

        fig_hs = px.choropleth_mapbox(
            hs_geo_plot,
            geojson=hs_geojson,
            locations=hs_geo_plot.index,
            color='Ward_Class',
            color_discrete_map=HOTSPOT_COLOURS,
            mapbox_style='carto-positron',
            zoom=7,
            center={'lat': -1.5, 'lon': 38.3},
            opacity=0.75,
            hover_data={
                'Ward':        True,
                'Ward_Class':  True,
                'WASI_mean':   ':.3f',
                'Gi_Mean':     ':.3f',
                'Hotspot_Pct': ':.2f',
            },
            labels={
                'Ward_Class':  'Classification',
                'WASI_mean':   'WASI Score',
                'Gi_Mean':     'Mean Gi* Z-score',
                'Hotspot_Pct': 'Hotspot pixel %',
            }
        )
        fig_hs.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),
            height=500,
            legend=dict(title='Classification', orientation='v')
        )
        st.plotly_chart(fig_hs, use_container_width=True)
        st.caption(
            'Ward classified as hotspot if >=30% of pixels have Gi* z-score > 1.96 (p<0.05). '
            'Analysis run on 500m WASI raster with 1.5km neighbourhood window.'
        )

    with hc2:
        st.subheader('Classification summary')
        hs_counts = hs_geo['Ward_Class'].value_counts().reset_index()
        hs_counts.columns = ['Class', 'Wards']

        fig_hs_bar = px.bar(
            hs_counts, x='Wards', y='Class', orientation='h',
            color='Class',
            color_discrete_map=HOTSPOT_COLOURS,
            text='Wards'
        )
        fig_hs_bar.update_layout(
            showlegend=False, height=200,
            margin=dict(l=0, r=0, t=10, b=0),
            xaxis_title='Number of wards', yaxis_title=''
        )
        fig_hs_bar.update_traces(textposition='outside')
        st.plotly_chart(fig_hs_bar, use_container_width=True)

        st.subheader('Pixel-level results')
        st.markdown("""
        | Gi* Class | % of county |
        |-----------|-------------|
        | Hotspot 99% (z > 2.576) | 15.1% |
        | Hotspot 95% (z > 1.960) | 18.5% |
        | Not significant | 52.2% |
        | Coldspot 95% (z < -1.960) | 23.9% |
        | Coldspot 99% (z < -2.576) | 18.9% |
        """)

        st.subheader('Hotspot ward detail')
        hotspot_detail = hs_geo[hs_geo['Ward_Class'] == 'Hotspot'][
            ['Ward', 'WASI_mean', 'Gi_Mean', 'Hotspot_Pct']
        ].copy()
        hotspot_detail.columns = ['Ward', 'WASI', 'Gi* Mean', 'Hotspot %']
        hotspot_detail = hotspot_detail.round(3)
        st.dataframe(hotspot_detail, use_container_width=True, hide_index=True)

# ── TAB 4: Ward Data Table ────────────────────────────────────────────────────
with tab4:
    st.subheader('Full Ward Data Table')

    search = st.text_input('Search ward name', '')
    display = filtered.copy()
    if search:
        display = display[display['Ward'].str.contains(search, case=False)]

    display_cols = ['Ward', 'WASI_mean', 'Stress_Class',
                    'C2_Rainfall', 'C3_NDVI', 'C4_Population', 'C5_Slope']
    display = display[display_cols].sort_values('WASI_mean', ascending=False).reset_index(drop=True)
    display.index += 1

    display_rounded = display.copy()
    for col in ['WASI_mean', 'C2_Rainfall', 'C3_NDVI', 'C4_Population', 'C5_Slope']:
        display_rounded[col] = display_rounded[col].round(3)

    st.dataframe(
        display_rounded,
        use_container_width=True,
        height=600,
        column_config={
            'WASI_mean':     st.column_config.ProgressColumn('WASI Score', min_value=0, max_value=1, format='%.3f'),
            'C2_Rainfall':   st.column_config.ProgressColumn('C2 Rainfall', min_value=0, max_value=1, format='%.3f'),
            'C3_NDVI':       st.column_config.ProgressColumn('C3 NDVI', min_value=0, max_value=1, format='%.3f'),
            'C4_Population': st.column_config.ProgressColumn('C4 Population', min_value=0, max_value=1, format='%.3f'),
            'C5_Slope':      st.column_config.ProgressColumn('C5 Slope', min_value=0, max_value=1, format='%.3f'),
            'Stress_Class':  st.column_config.TextColumn('Stress Class'),
        }
    )

    tc1, tc2 = st.columns(2)
    tc1.download_button(
        'Download ward table (CSV)',
        data=table.to_csv(index=False),
        file_name='kitui_wasi_ward_table.csv',
        mime='text/csv'
    )
    tc2.metric('Showing', f'{len(display)} of 40 wards')

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown('---')
st.caption(
    'WASHLAB Climate-Smart WASH Pilot — Kitui County, Kenya | '
    'Phase 1 satellite analysis | '
    'Data: CHIRPS, MODIS MOD13A3, WorldPop 2020, SRTM, JRC Global Surface Water via Google Earth Engine | '
    'Analysis: Davis Mironga | '
    '[GitHub](https://github.com/davis-mironga/kitui-washlab-analysis)'
)

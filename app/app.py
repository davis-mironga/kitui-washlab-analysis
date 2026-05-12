import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import requests
st.set_page_config(page_title='WASHLAB Kitui',page_icon='💧',layout='wide',initial_sidebar_state='expanded')
REPO='https://raw.githubusercontent.com/davis-mironga/kitui-washlab-analysis/main/data/'
@st.cache_data
def load_data():
    table=pd.read_csv(REPO+'kitui_wasi_ward_table.csv')
    wasi_geo=requests.get(REPO+'kitui_wasi_ward.geojson').json()
    hs_geo=requests.get(REPO+'kitui_hotspot_ward.geojson').json()
    for f in wasi_geo['features']:
        ward=f['properties']['Ward']
        row=table[table['Ward']==ward]
        if not row.empty:
            f['properties'].update({'C2_Rainfall':float(row['C2_Rainfall'].iloc[0]),'C3_NDVI':float(row['C3_NDVI'].iloc[0]),'C4_Population':float(row['C4_Population'].iloc[0]),'C5_Slope':float(row['C5_Slope'].iloc[0])})
    return table,wasi_geo,hs_geo
table,wasi_geo,hs_geo=load_data()
wasi_df=pd.DataFrame([f['properties'] for f in wasi_geo['features']])
hs_df=pd.DataFrame([f['properties'] for f in hs_geo['features']])

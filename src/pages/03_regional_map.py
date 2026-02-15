import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(layout="wide")
st.title("Regional Overview")

parent_dir = Path.cwd().parent
full_df = pd.read_csv(f"{parent_dir}/outputs/data/categorical/Patient Characteristics Survey (Years 2013 - 2022) (categorical).csv")

# 3-digit zip code approximate center coordinates for NY
ZIP3_COORDS = {
    '100': {'lat': 40.71, 'lon': -74.00},   # Manhattan
    '101': {'lat': 40.71, 'lon': -73.99},   # Manhattan
    '102': {'lat': 40.71, 'lon': -73.98},   # Manhattan
    '103': {'lat': 40.58, 'lon': -74.15},   # Staten Island
    '104': {'lat': 40.85, 'lon': -73.87},   # Bronx
    '105': {'lat': 40.94, 'lon': -73.83},   # Westchester
    '106': {'lat': 41.03, 'lon': -73.76},   # Westchester
    '107': {'lat': 41.04, 'lon': -73.86},   # Westchester/Rockland
    '108': {'lat': 41.15, 'lon': -73.99},   # Rockland
    '109': {'lat': 41.10, 'lon': -73.72},   # Westchester
    '110': {'lat': 40.73, 'lon': -73.69},   # Queens
    '111': {'lat': 40.75, 'lon': -73.88},   # Queens
    '112': {'lat': 40.65, 'lon': -73.95},   # Brooklyn
    '113': {'lat': 40.71, 'lon': -73.95},   # Brooklyn
    '114': {'lat': 40.66, 'lon': -73.77},   # Queens
    '115': {'lat': 40.77, 'lon': -73.83},   # Queens
    '116': {'lat': 40.72, 'lon': -73.83},   # Queens
    '117': {'lat': 40.72, 'lon': -73.41},   # Long Island
    '118': {'lat': 40.77, 'lon': -73.20},   # Long Island
    '119': {'lat': 40.80, 'lon': -72.80},   # Long Island
    '120': {'lat': 42.65, 'lon': -73.75},   # Albany
    '121': {'lat': 42.80, 'lon': -73.68},   # Albany area
    '122': {'lat': 42.45, 'lon': -73.25},   # Hudson Valley
    '123': {'lat': 41.70, 'lon': -73.93},   # Hudson Valley
    '124': {'lat': 41.50, 'lon': -74.01},   # Newburgh
    '125': {'lat': 41.93, 'lon': -74.00},   # Kingston
    '126': {'lat': 41.67, 'lon': -74.68},   # Catskills
    '127': {'lat': 42.10, 'lon': -75.91},   # Binghamton
    '128': {'lat': 42.90, 'lon': -74.57},   # Gloversville
    '129': {'lat': 43.08, 'lon': -73.78},   # Saratoga
    '130': {'lat': 43.05, 'lon': -76.15},   # Syracuse
    '131': {'lat': 43.10, 'lon': -76.15},   # Syracuse
    '132': {'lat': 43.10, 'lon': -75.23},   # Utica
    '133': {'lat': 43.10, 'lon': -75.23},   # Utica area
    '134': {'lat': 43.97, 'lon': -75.91},   # Watertown
    '135': {'lat': 43.50, 'lon': -73.45},   # Glens Falls
    '136': {'lat': 44.70, 'lon': -73.45},   # Plattsburgh
    '137': {'lat': 42.45, 'lon': -76.50},   # Ithaca/Elmira
    '138': {'lat': 42.16, 'lon': -76.90},   # Elmira
    '140': {'lat': 42.88, 'lon': -78.87},   # Buffalo
    '141': {'lat': 42.88, 'lon': -78.87},   # Buffalo
    '142': {'lat': 42.88, 'lon': -78.87},   # Buffalo area
    '143': {'lat': 43.15, 'lon': -77.61},   # Rochester area
    '144': {'lat': 43.15, 'lon': -77.61},   # Rochester
    '145': {'lat': 43.15, 'lon': -77.61},   # Rochester area
    '146': {'lat': 43.15, 'lon': -77.61},   # Rochester
    '147': {'lat': 42.10, 'lon': -79.23},   # Jamestown
    '148': {'lat': 42.10, 'lon': -76.80},   # Elmira
    '149': {'lat': 42.50, 'lon': -78.00},   # Batavia
}

year = st.selectbox("Survey Year", sorted(full_df['Survey Year'].unique()))
metric = st.selectbox("Metric", ['Serious Mental Illness', 'Medicaid Insurance', 'SSI Cash Assistance'])

year_df = full_df[full_df['Survey Year'] == year]

# Aggregate by zip
zip_stats = year_df.groupby('Three Digit Residence Zip Code').agg(
    total=('Survey Year', 'count'),
    metric_count=(metric, lambda x: (x == 'YES').sum())
).reset_index()
zip_stats['rate'] = (zip_stats['metric_count'] / zip_stats['total'] * 100).round(1)
zip_stats['zip3'] = zip_stats['Three Digit Residence Zip Code'].astype(str)

# Add coordinates
zip_stats['lat'] = zip_stats['zip3'].map(lambda z: ZIP3_COORDS.get(z, {}).get('lat'))
zip_stats['lon'] = zip_stats['zip3'].map(lambda z: ZIP3_COORDS.get(z, {}).get('lon'))
zip_stats = zip_stats.dropna(subset=['lat', 'lon'])

# Density heat map
fig = px.density_mapbox(
    zip_stats,
    lat='lat',
    lon='lon',
    z='rate',
    radius=25,
    zoom=6,
    center={"lat": 42.0, "lon": -75.5},
    mapbox_style="carto-darkmatter",
    color_continuous_scale='YlOrRd',
    title=f'{metric} Rate by 3-Digit Zip Code ({year})',
    hover_data={'zip3': True, 'total': True, 'rate': True}
)
fig.update_layout(height=600)
st.plotly_chart(fig, use_container_width=True)
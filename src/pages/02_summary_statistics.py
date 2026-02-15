import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(layout="wide")
st.title("Summary Statistics")

parent_dir = Path.cwd().parent
full_df = pd.read_csv(f"{parent_dir}/outputs/data/categorical/Patient Characteristics Survey (Years 2013 - 2022) (categorical).csv")

col1, col2 = st.columns([1, 3])

with col1:
    year = st.selectbox("Survey Year", ["All Years"] + sorted(full_df['Survey Year'].unique().tolist()))
    metric = st.selectbox("Metric", [
        'Serious Mental Illness',
        'Employment Status', 
        'Program Category',
        'Age Group',
        'Sex'
    ])

with col2:
    if year != "All Years":
        filtered = full_df[full_df['Survey Year'] == year]
    else:
        filtered = full_df

    # Top-level metrics
    m1, m2, m3 = st.columns(3)
    m1.metric("Respondents", f"{len(filtered):,}")
    
    smi_rate = (filtered['Serious Mental Illness'] == 'YES').sum() / len(filtered) * 100
    m2.metric("SMI Rate", f"{smi_rate:.1f}%")
    
    medicaid_rate = (filtered['Medicaid Insurance'] == 'YES').sum() / len(filtered) * 100
    m3.metric("Medicaid Rate", f"{medicaid_rate:.1f}%")

    # Distribution chart
    counts = filtered[metric].value_counts()
    fig = px.bar(
        x=counts.index, y=counts.values,
        title=f'{metric} Distribution ({year})',
        labels={'x': metric, 'y': 'Count'},
        color=counts.values,
        color_continuous_scale='Blues'
    )
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
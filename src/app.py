import streamlit as st
from pathlib import Path

current_directory = Path.cwd()
parent_dir = current_directory.parent

st.set_page_config(page_title="PCS Explorer", layout="wide")

st.title("Medicaid & Serious Mental Illness in New York")
st.markdown("### Analyzing 750,000+ patient records from the NYS Patient Characteristics Survey (2013–2022)")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Records", "750,000+")
col2.metric("Survey Years", "5")
col3.metric("Patient Clusters", "11")
col4.metric("OMH Regions", "5")

st.divider()

st.markdown("""
### The Problem
Serious Mental Illness affects hundreds of thousands of New Yorkers receiving mental health services. 
Understanding how Medicaid enrollment, employment status, and regional differences impact this population 
is critical for effective policy — especially as continuous enrollment protections end.

### The Approach
This project combines traditional statistical analysis with modern NLP techniques to analyze 
the NYS Office of Mental Health Patient Characteristics Survey across five survey years.

**Data Pipeline** — Standardized schemas across 5 survey years with automated validation  
**NLP Clustering** — Embedded 10,000 patient records and clustered them into 11 clinically meaningful groups using HDBSCAN  
**LLM Summarization** — Generated clinical summaries for each cluster using GPT-4o-mini  
**Interactive Analysis** — Natural language query interface powered by LLM-generated Pandas code
""")

st.image(f'{parent_dir}/images/umap_clusters.png', caption="UMAP visualization of patient clusters")
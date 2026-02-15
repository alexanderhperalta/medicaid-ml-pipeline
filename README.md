# Medicaid Machine Learning Pipeline

## Project Overview
This project investigates the relationship between Medicaid coverage and Serious Mental Illness (SMI) in New York State. The final paper includes an analysis conducted on Patient Characteristics Survey (PCS) data for the years 2013, 2015, 2017, 2019, and 2022, exploring demographics, employment status, and insurance enrollment trends for individuals receiving mental health services. The primary research interest is identifying how Medicaid enrollment impacts health outcomes for beneficiaries with SMI, particularly in the context of the end of continuous enrollment laws.

## Repository Contents
- Medicaid and Serious Mental Illness.pdf: A comprehensive research paper detailing the history of Medicaid, the prevalence of SMI in New York, and the policy implications of current unwinding laws.
- 01_data_processing.ipynb: Handles data engineering and preparation. It includes custom Python classes to:
  - Automate directory and folder creation.
  - Map categorical values across multi-year datasets into a standardized numerical format.
- 02_HDBSCAN.ipynb: 
  - Embedded 10,000 patient records using OpenAI's text-embedding-3-small
  - Clustered patients using HDBSCAN into 11 meaningful groups
  - Generated clinical summaries for each cluster using GPT-4o-mini
  - Built an interactive Streamlit app that answers natural language questions about the dataset using LLM-generated Pandas code
- 03_analysis.ipynb: Performs the core statistical analysis. Key features include:
  - Generating summaries of respondent demographics (SMI prevalence, Medicaid enrollment, SSI assistance).
  - Analyzing employment status by program category (Emergency, Inpatient, Outpatient, etc.).
  - Implementing Instrumental Variable (IV) Regressions to assess the impact of Medicaid on mental health outcomes.

## Setup
1. Download PCS survey data from the links below into `data/`
2. Install dependencies: `pip install -r requirements.txt`
3. Run notebooks in order: `01_data_processing.ipynb` → `02_clustering.ipynb` → `03_analysis.ipynb`
4. Launch the app: `streamlit run src/app.py`

## Key Findings
- SMI Prevalence: Analysis shows a significant increase in adult respondents identified with SMI, rising from approximately 81.7% in 2013 to over 94.5% in 2022.
- Medicaid Enrollment: Enrollment among surveyed adults with SMI has remained relatively stable, hovering around 71–74% across the decade studied.
- Employment Disparities: There is a notable gap in employment for those with SMI; for example, in 2022, only ~33.6% of Outpatient program respondents with SMI were employed, compared to higher unemployment/NILF (Not in Labor Force) rates in other categories.

## Data Source
The data is sourced from the New York State Office of Mental Health (OMH) Patient Characteristics Survey.

Note: Due to the size of the datasets, raw CSV files are not included in this repository but can be found using the following links:

  - https://catalog.data.gov/dataset/patient-characteristics-survey-pcs-2013
  - https://catalog.data.gov/dataset/patient-characteristics-survey-pcs-2015
  - https://catalog.data.gov/dataset/patient-characteristics-survey-pcs-2017
  - https://catalog.data.gov/dataset/patient-characteristics-survey-pcs-2019
  - https://catalog.data.gov/dataset/patient-characteristics-survey-pcs-2022-persons-served-by-survey-year-region-of-provider-g

## Tech Stack
Python, Pandas, NumPy, OpenAI API, HDBSCAN, UMAP, scikit-learn, XGBoost, Streamlit, Plotly

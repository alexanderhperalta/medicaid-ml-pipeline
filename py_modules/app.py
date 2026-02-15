import streamlit as st
import pandas as pd
from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI
from pathlib import Path

client = OpenAI()

current_directory = Path.cwd()
parent_dir = current_directory.parent

@st.cache_data
def load_data():
    df = pd.read_csv(f"{parent_dir}/outputs/clusters/clustered_patients.csv")
    full_df = pd.read_csv(f"{parent_dir}/outputs/data/categorical/Patient Characteristics Survey (Years 2013 - 2022) (categorical).csv")
    data_dict = open(f"{parent_dir}/data/data_dictionary.txt").read()    
    return df, full_df, data_dict

df, full_df, data_dict = load_data()

st.title("Patient Characteristics Survey Explorer")

query = st.text_input("Ask a question about the PCS data")

if query:
    # Step 1: Ask LLM to write Pandas code
    code_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"""You are a data analyst. Write Python Pandas code to answer the user's question about a DataFrame called `full_df`.

Available columns: {list(full_df.columns)}

Data Dictionary:
{data_dict}

Sample data (first 3 rows):
{full_df.head(3).to_string()}

Value counts for key columns:
Sex: {full_df['Sex'].value_counts().to_dict()}
Serious Mental Illness: {full_df['Serious Mental Illness'].value_counts().to_dict()}
Survey Year: {full_df['Survey Year'].value_counts().to_dict()}

Rules:
- Write ONLY executable Python code, nothing else
- No markdown, no backticks, no explanations
- Store the final answer in a variable called `result`
- Use the variable `full_df` which is already loaded"""},
            {"role": "user", "content": query}
        ],
        temperature=0,
    )
    
    code = code_response.choices[0].message.content.strip()
    code = code.replace("```python", "").replace("```", "").strip()
    
    # Step 2: Execute the code
    try:
        local_vars = {"full_df": full_df, "pd": pd}
        exec(code, {}, local_vars)
        result = local_vars.get("result", "No result computed")
        
        # Step 3: Ask LLM to interpret the result
        answer_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert health economist. Interpret the following data result in plain English. Be specific with numbers."},
                {"role": "user", "content": f"Question: {query}\n\nResult: {result}"}
            ],
            temperature=0.3,
        )
        
        st.markdown("### Answer")
        st.write(answer_response.choices[0].message.content)
        
        with st.expander("View generated code"):
            st.code(code, language="python")
            
    except Exception as e:
        st.error(f"Error executing query: {e}")
        with st.expander("View failed code"):
            st.code(code, language="python")
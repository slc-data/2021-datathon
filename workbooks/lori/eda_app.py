# Streamlit EDA APP for COSA

# Imports
import pandas as pd
import numpy as np
import seaborn as sns
import streamlit as st
from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report

# Web App Title
st.markdown('''
# **Explore COSA Data App**
The **Explore COSA Data App** will take in csv's and output quick exploratory data analysis using Pandas Profiling Report.
''')

# Upload CSV data
with st.sidebar.header('1. Upload your CSV data'):
    uploaded_csv = st.sidebar.file_uploader("Upload your CSV file", type=["csv"])

# Pandas Profiling Report
if uploaded_csv is not None:
    @st.cache
    def load_csv():
        csv = pd.read_csv(uploaded_csv)
        return csv
    df = load_csv()
    pr = ProfileReport(df, explorative=True)
    st.header('**Checkout The Data!**')
    st.write(df)
    st.write('---')
    st.header('**Pandas Profiling Report**')
    st_profile_report(pr)
else:
    st.info('Upload a COSA dataset :) ')


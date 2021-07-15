# Streamlit CLEAN CODA DATA APP FOR DATATHON 2021

# Imports
import pandas as pd
import numpy as np
import seaborn as sns
import streamlit as st
from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report


# Web App Title
st.markdown('''
# **Clean COSA Data App**
The **Clean COSA Data App** will take in COSA csv's and perform cleaning for analysis.
''')



# Streamlit CLEAN COSA DATA APP for Datathon
####################################################################
#COSA CSV REFERENCES 8/18/2021
# Brooks air quality:  81661d35-a5c5-40d1-af16-92edd3946579.csv
# Brooks flood:  c0c546cd-fbfa-479c-b1ca-ac7a7244aa53.csv
# Brooks sound:  3cc6c00e-0874-423f-ac81-de6081c1b532.csv
# Brooks weather:  4dc78055-6ca6-4ce8-8a36-4c22804f6a9b.csv
# Downtown air quality:  12ebf68f-95b0-4d96-9a1b-9c4f4e25497e.csv
# Downtown flood:  346d33b7-0b74-4b92-aa22-452456954ed1.csv
# Downtown sound:  f21099d0-22d7-43e7-bf06-3dac304b6765.csv
# Downton weather:  f6038372-b38f-42bb-8cf5-5d6419a46cf1.csv
# Med center air quality:  0f16d9bc-fdf4-45fb-8198-dab84dc67ad7.csv
# med center flood:  aaf0e6a5-8df7-4f0c-bf22-7b2f6ad6943d.csv
# med center sound:  31f8a3f4-bc73-48c4-96bf-768388129f85.csv
# med center weather:  7c2649a6-bb5a-4579-ab86-fbaee4e7024a.csv  
#####################################################################
# Imports
import pandas as pd
import numpy as np
import seaborn as sns
import streamlit as st
import streamlit.components as stc
import clean_functions as cf

# Utils
import base64
import time
timestr = time.strftime("%Y%m%d-%H%M%S")

#csv downloader
def csv_downloader(data):
    csvfile = data.to_csv()
    b64 = base64.b64encode(csvfile.encode()).decode()
    new_filename = "new_text_file_{}_.csv".format(timestr)
    st.markdown("#### Download file ####")
    href = f'<a href="data:file/csv;base64,{b64}" download="{new_filename}">Click Here!!!</a>'
    st.markdown(href, unsafe_allow_html=True)


# Web App Title
st.markdown('''
# **Clean COSA Data App**
The **Clean COSA Data App** will take in SMARTSA Street Light Sensor csv and wrangle it into a form that can be easily explored for data analysis!
''')

#-----------------------------------------------------------------------------
# Upload CSV data
with st.sidebar.header('1. Upload your CSV data'):
    uploaded_csv = st.sidebar.file_uploader("Upload your CSV file", type=["csv"])

# Determine which cosa dataframe has been loaded
if uploaded_csv is not None:
    file_details = {"FileName":uploaded_csv.name,"FileType":uploaded_csv.type,"FileSize":uploaded_csv.size}
    st.write(file_details)
    @st.cache
    def load_csv():
        csv = pd.read_csv(uploaded_csv)
        return csv
    df = load_csv()
# Display unclean data
    st.header('**Checkout The Raw Data!**')
    st.dataframe(df)
#Which dataset
    def which_dataset():
        if uploaded_csv.name == 'c0c546cd-fbfa-479c-b1ca-ac7a7244aa53.csv':
            cf.clean_flood()
            st.header('Squeaky cleannn')
            st.dataframe(df)
        else:
            st.text('not flood')
#---------------------------------
    which_dataset()
else:
    st.info('Upload a SMARTSA Street Light Sensor dataset :) ')



#-----------------------------------------------------------------------------
#Print data types before clean


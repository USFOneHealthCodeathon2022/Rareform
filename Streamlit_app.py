import streamlit as st
import pandas as pd
import numpy as np

from PIL import Image
img = Image.open("images/Logo.png")

st.image(img)

st.title('classification of rare diseases')

##URL of orpha dataset
#url="https://raw.githubusercontent.com/Awtum/Topic3_TeamA/main/OrphaICD10.tsv"

df=pd.read_csv("Data/OrphaICD10.tsv", sep='\t')
list_of_codes = np.unique(df['Orpha_code'].to_list())

#set ophacode from selection box, should probably find a way to allow description searching
code=st.selectbox("orpha code", options=list_of_codes)

st.write('You selected:', code)
desc=df.loc[df['Orpha_code'] == orphacode]['Orphanet_disorder'] #find disorder description
st.write(desc.to_string(index=False))
#def load_data(nrows):
#    data=pd.read_csv(url, nrows=nrows, sep='\t')
#    lowercase = lambda x: str(x).lower()
#    data.rename(lowercase, axis='columns', inplace=True)
#    return data

def load_data(orphacode):
    data=df.loc[df['Orpha_code'] == orphacode]
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    return data

#col1, col2, col3 = st.columns(3)
#col1.metric("Description", "1.2 °F")
#col2.metric("ICD-10", "-8%")
#col3.metric("Orpha", "4%")


data_load_state = st.text('Loading data...')
data = load_data(code)
data
data_load_state  = st.text('Complete!')

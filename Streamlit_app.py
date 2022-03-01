import streamlit as st
import pandas as pd
import numpy as np

st.title('classification of rare diseases')

url="https://raw.githubusercontent.com/Awtum/Topic3_TeamA/main/OrphaICD10.tsv"

def load_data(nrows):
    data=pd.read_csv(url, nrows=nrows, sep='\t')
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    return data


data_load_state = st.text('Loading data...')
data = load_data(100)
data

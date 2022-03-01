
import streamlit as st
import pandas as pd
import numpy as np

st.title('classification of rare diseases')


def load_data(nrows):
    data=pd.read_csv("github.com/awtum/Topic3_TeamA/OrphaICD10.tsv", nrows=nrows, sep='\t')
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    return data


data_load_state = st.text('Loading data...')
data = load_data(100)
data

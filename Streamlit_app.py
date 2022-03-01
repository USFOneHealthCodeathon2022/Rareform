import streamlit as st
import pandas as pd
import numpy as np

backgroundColor = 'white'

from PIL import Image
img = Image.open("Logo2.png")

st.image(img)

st.title('classification of rare diseases')

url="https://raw.githubusercontent.com/Awtum/Topic3_TeamA/main/OrphaICD10.tsv"

st.selectbox("orpha code", options=('1','2','3','4','5'))

def load_data(nrows):
    data=pd.read_csv(url, nrows=nrows, sep='\t')
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    return data


data_load_state = st.text('Loading data...')
data = load_data(100)
data

import streamlit as st
import pandas as pd
import numpy as np
import gseapy as gp
import matplotlib.pyplot as plt
from PIL import Image

def load_data(orphacode):
    data=df.loc[df['Orpha_code'] == orphacode]
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    return data

def input_list(gene_list):
    if isinstance(gene_list, list):
        return gene_list
    else:
        gene_list = gene_list.split(',')
        return gene_list

def plot_enrichr(enrichr, color, k=10):
    fig, ax = plt.subplots()
    df = enrichr.results
    labels = df['Term'][:k].values
    values = df['Adjusted P-value'][:k].values
    values = [-np.log10(x) for x in values]
    ax.barh(labels, values, color=color)
    ax.invert_yaxis()
    ax.tick_params(axis='both', labelsize=15)
    plt.xlabel('-log10(P-value)')
    st.pyplot(fig)

img = Image.open("images/Logo.png")

st.image(img)

st.title('classification of rare diseases')

##URL of orpha dataset
#url="https://raw.githubusercontent.com/Awtum/Topic3_TeamA/Data/OrphaICD10.tsv"
new_choice = ['Disease', 'Gene']
choice = st.sidebar.radio('Types of analysis:',('Disease', 'Gene'))

if choice == 'Disease':

    df=pd.read_csv("Data/OrphaICD10.tsv", sep='\t')
    list_of_codes = [None]+list(np.unique(df['Orpha_code'].to_list()))  # added default None so the rest of the code won't run at start

    #set ophacode from selection box, should probably find a way to allow description searching
    code=st.selectbox("orpha code", options=list_of_codes)

    if code!=None:
        st.write('You selected:', code)
        desc=df.loc[df['Orpha_code'] == code]['Orphanet_disorder'] #find disorder description
        st.write(desc.to_string(index=False))
        #def load_data(nrows):
        #    data=pd.read_csv(url, nrows=nrows, sep='\t')
        #    lowercase = lambda x: str(x).lower()
        #    data.rename(lowercase, axis='columns', inplace=True)
        #    return data



        #col1, col2, col3 = st.columns(3)
        #col1.metric("Description", "1.2 °F")
        #col2.metric("ICD-10", "-8%")
        #col3.metric("Orpha", "4%")


        data_load_state = st.text('Loading data...')
        data = load_data(code)
        data
        data_load_state  = st.text('Complete!')

elif choice == 'Gene':
    with st.form(key='gene_list'):
        gene_list = st.text_input(label="Enter gene(s), separated by ',' :")
        submit_button = st.form_submit_button(label='Submit')

    if len(gene_list)!=0:


        enr_KEGG = gp.enrichr(gene_list=input_list(gene_list),
         gene_sets=['KEGG_2021_Human'],
         organism='Human', 
         outdir='.',
         cutoff=0.05
         )

        enr_AutoRIF = gp.enrichr(gene_list=input_list(gene_list),
         gene_sets=['Rare_Diseases_AutoRIF_Gene_Lists'],
         organism='Human', 
         outdir='.',
         cutoff=0.05
         )

        plot_enrichr(enr_KEGG, 'firebrick')
        plot_enrichr(enr_AutoRIF, 'sienna')



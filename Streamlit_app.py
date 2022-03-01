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
    
def load_disease(dis):
    data=df.loc[df['Orphanet_disorder'] == disease]
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
  
def gene_overlap(gene_list1, gene_list2):
                gene_list1 = gene_list1.split(';')
                gene_list2 = gene_list2.split(';')
                overlapped_gene = []
                for gene in gene_list1:
                    if gene in gene_list2:
                        overlapped_gene.append(gene)
                percent_gene_list1 = round(len(overlapped_gene)/len(gene_list1),4)*100
                percent_gene_list2 = round(len(overlapped_gene)/len(gene_list2),2)*100
                return overlapped_gene, percent_gene_list1, percent_gene_list2



img = Image.open("images/Logo.png")

st.image(img)

st.title('classification of rare diseases')

st.markdown( ####found some way around sidebar width
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        width: 150px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        width: 150px;
        margin-left: -150px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

##establish data type
new_choice = ['Disease', 'Gene']

choice = st.sidebar.radio('Types of analysis:',('Disease', 'Gene'))

###Disease
if choice == 'Disease':

    df=pd.read_csv("Data/OrphaICD10.tsv", sep='\t')
    list_of_codes = [None]+list(np.unique(df['Orpha_code'].to_list()))  # added default None so the rest of the code won't run at start

    #set ophacode from selection box, should probably find a way to allow description searching
    code=st.selectbox("orpha code", options=list_of_codes)

    if code!=None:
        st.write('You selected:', code)
        desc=df.loc[df['Orpha_code'] == code]['Orphanet_disorder'] #find disorder description
        st.write(desc.to_string(index=False))
        #col1, col2, col3 = st.columns(3)
        #col1.metric("Description", "1.2 °F")
        #col2.metric("ICD-10", "-8%")
        #col3.metric("Orpha", "4%")
        data_load_state = st.text('Loading data...')
        data = load_data(code)
        data
        data_load_state  = st.text('Complete!')
    
    st.write("OR")
    
    list_of_diseases = [None]+list(np.unique(df['Orphanet_disorder'].to_list()))  # added default None so the rest of the code won't run at start
    disease=st.selectbox("Disease name", options=list_of_diseases)
    if disease!=None:
        st.write('You selected:', disease)
        st.write(disease)
        data_load_state = st.text('Loading data...')
        data = load_disease(disease)
        data
        data_load_state  = st.text('Complete!')
    
    

elif choice == 'Gene':
    with st.form(key='gene_list'):
        gene_list = st.text_input(label="Enter gene(s), separated by ',' :")
        gene_anno=st.selectbox("Include gene annotation:", options=["No", "Minimal", "Full"])
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

        if enr_KEGG.results.empty and enr_AutoRIF.results.empty:
            st.write(f"No matching gene found in database for input '{gene_list}'!")
        else:
            plot_enrichr(enr_KEGG, 'firebrick')
            plot_enrichr(enr_AutoRIF, 'sienna')

        if gene_anno=='Minimal' or gene_anno=='Full':
            gene_list1 = enr_KEGG.results.iloc[0,-1]
            gene_list2 = enr_AutoRIF.results.iloc[0,-1]
            gene_db = pd.read_csv('Data/dbNSFP4.3a.Selected.csv')
            gene_db_orpha = pd.read_csv('Data/dbNSFP4.3a.Selected.Orpha.csv')

            cand_gene_list = gene_overlap(gene_list1, gene_list2)[0]

            orpha_list = []
            for count, gene in enumerate(cand_gene_list):
                count += 1
                idx1 = gene_db['Gene_name'] == gene
                idx2 = gene_db_orpha['Gene_name'] == gene
                orpha_list.append(idx2)
                if idx2.any():
                    st.write(f'Gene {count} ({gene}) can contribute to Orphanet disease.')
                    gene_annos_orpha = gene_db_orpha[idx2].iloc[0,-4:]
                    gene_annos = gene_db[idx1].iloc[0,-4:]
                    labels = ['Interactions', 'pLI', 'GDI', 'LoFtool']
                    X_axis = np.arange(len(labels))
                    fig, ax = plt.subplots()
                    plt.bar(X_axis-0.2, gene_annos_orpha.values.astype('float'), width=0.35, label='Orphanet genes', color='firebrick')
                    plt.bar(X_axis+0.2, gene_annos.values.astype('float'), width=0.35, label='All genes', color='paleturquoise')
                    plt.xticks([0,1,2,3], labels = labels,rotation=0)
                    plt.ylabel('Rankscore percentiles')
                    plt.legend()
                    st.pyplot(plt)

            if gene_anno=='Full':
                new_idx = gene_db_orpha['Gene_name'].isin(cand_gene_list)
                gene_db_orpha[new_idx].iloc[:,1:]



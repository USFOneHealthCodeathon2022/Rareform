import streamlit as st
import pandas as pd
import numpy as np
import gseapy as gp
import matplotlib.pyplot as plt
import networkx as nx
from PIL import Image


def load_data(orphacode):
    data=df.loc[df['Orpha_code'] == orphacode]
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    return data
    
def load_ICD(ICDcode):
    data=df.loc[df['ICD_10'] == ICDcode]
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


# st.title('classification of rare diseases')
st.markdown("<h1 style='text-align: Center; color: firebrick;'>classification of rare diseases</h1>", unsafe_allow_html=True)

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
    df=pd.read_csv("Data/OrphaICD10.tsv", sep='\t', index_col=False)
    sub=pd.read_csv("Data/disease-gene.tsv", sep='\t', index_col=False)
    df=df.loc[df['Orpha_code'].isin(list(np.unique(sub['OrphaCode'].to_list())))]
    
    list_of_codes = [None]+list(np.unique(df['Orpha_code'].to_list()))  # added default None so the rest of the code won't run at start

    #set ophacode from selection box, should probably find a way to allow description searching
    code=st.selectbox("orpha code", options=list_of_codes)

    if code!=None:
        st.write('You selected:', code)
        desc=df.loc[df['Orpha_code'] == code]['Orphanet_disorder']#find disorder description
        #desc=np.unique(desc) ###need to get syntax for reducing repetition. i.e. Hereditary pheochromocytoma-paraganglioma
        st.write(desc.to_string(index=False))
        genes=sub.loc[sub['OrphaCode'] == code]['Genes']
        st.write('genes:', genes.to_string(index=False))
        data = load_data(code)
        data
    
    st.write("OR")
    
    list_of_diseases = [None]+list(np.unique(df['Orphanet_disorder'].to_list()))  # added default None so the rest of the code won't run at start
    disease=st.selectbox("Disease name", options=list_of_diseases)
    if disease!=None:
        st.write('You selected:', disease)
        st.write(disease)
        code=df.loc[df['Orphanet_disorder'] == disease]['Orpha_code']
        code=int(code.values)
        genes=sub.loc[sub['OrphaCode'] == code]['Genes']
        st.write('genes:', genes.to_string(index=False))
        data = load_disease(disease)
        data
    
    st.write("OR")
        
    list_of_codes = [None]+list(np.unique(df['ICD_10'].to_list()))  # added default None so the rest of the code won't run at start

    #set ICD from selection box
    ICDcode=st.selectbox("ICD", options=list_of_codes)

    if ICDcode!=None:
        st.write('You selected:', ICDcode)
        desc=df.loc[df['ICD_10'] == ICDcode]['Orphanet_disorder'] #find disorder description
        st.write(desc.to_string(index=False))
        code=df.loc[df['ICD_10'] == ICDcode]['Orpha_code']
        code=int(code.values)
        genes=sub.loc[sub['OrphaCode'] == code]['Genes']
        st.write('genes:', genes.to_string(index=False))
        data = load_ICD(ICDcode)
        data

    if code == 144:
        #Hereditary Nonpolyposis Colorectal Cancer (HNPCC, Lynch syndrome)
        st.write('ICD-11: GB90.42')
        HPNCC = pd.DataFrame({'from':['HPNCC','HPNCC'], 'to':['Hereditary nonpolyposis colorectal cancer',' Familial nonpolyposis colorectal cancer']})
        G=nx.from_pandas_edgelist(HPNCC, 'from', 'to')
        nx.draw(G, pos=nx.spring_layout(G), with_labels=True, node_size=500, node_color="navy", alpha=0.8)
        plt.axis('off')
        axis = plt.gca()
        axis.set_xlim([2*x for x in axis.get_xlim()])
        axis.set_ylim([2*y for y in axis.get_ylim()])
        st.pyplot(plt)
        
    if code == 618:
    #Familial Melanoma (malignant melanoma)
        st.write('ICD-11: XH4846')
        Fanconi_anemia = pd.DataFrame({'from':['Fanconi anemia','Fanconi anemia','Fanconi anemia','Fanconi anemia','Fanconi anemia','Fanconi anemia'], 'to':['Congenital aplastic anaemia','DNA instability syndromes affecting the skin','Inherited cancer-predisposing syndromes', 'Fanconi-ichthyosis-dysmorphism syndrome','Fanconi hypoplastic anaemia','Fanconi familial refractory anaemia']})
        G=nx.from_pandas_edgelist(Fanconi_anemia, 'from', 'to')
        nx.draw(G, pos=nx.spring_layout(G), with_labels=True, node_size=500, node_color="navy", alpha=0.8)
        plt.axis('off')
        axis = plt.gca()
        axis.set_xlim([2*x for x in axis.get_xlim()])
        axis.set_ylim([2*y for y in axis.get_ylim()])
        st.pyplot(plt)
    
    if code == 97286:
    #Carney
        st.write('ICD-11: 5A70.Y')
        Malignant_Melanoma = pd.DataFrame({'from':['Carney Stratakis syndrome','Multiple polyglandular tumours','Neoplasms of uncertain behaviour withpluriglandular involvement'],'to':['Multiple polyglandular tumours','Neoplasms of uncertain behaviour withpluriglandular involvement','Neoplasms of uncertain behaviour of endocrineglands']})
        G=nx.from_pandas_edgelist(Malignant_Melanoma, 'from', 'to')
        nx.draw(G, pos=nx.spring_layout(G), with_labels=True, node_size=500, node_color="navy", alpha=0.8)
        plt.axis('off')
        axis = plt.gca()
        axis.set_xlim([2*x for x in axis.get_xlim()])
        axis.set_ylim([2*y for y in axis.get_ylim()])
        st.pyplot(plt)

elif choice == 'Gene':
    # st.markdown("<h2 style='text-align: left; color: black;'>Enter gene symbol(s), separated by ',':</h1>", unsafe_allow_html=True)

    with st.form(key='gene_list'):
        # gene_list = st.text_input(label='Gene input:',help="Enter gene symbol(s), separated by ',' :")
        st.markdown("<h2 style='text-align: left; color: black;'>Gene input:</h1>", unsafe_allow_html=True)

        gene_list = st.text_input(label='',help="Enter gene symbol(s), separated by ',' :")

        st.header('')

        st.markdown("<h2 style='text-align: left; color: black;'>Include gene annotation:</h1>", unsafe_allow_html=True)
        gene_anno=st.selectbox("", options=["No", "Minimal", "Full"],help='No: only display KEGG and AutoRIF enrichment analyses. \
                                                                                                   Minimal: display additional gene annotations.\n\
                                                                                                   Full: display annotations for prioritized genes that are responsible for the top disease-pathway pair.')
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
            st.markdown("<h2 style='text-align: left; color: black;'>Top KEGG pathways overrepresented by the gene set:</h1>", unsafe_allow_html=True)
            plot_enrichr(enr_KEGG, 'navy')
            st.markdown("<h2 style='text-align: left; color: black;'>Top diseases overrepresented by the gene set:</h1>", unsafe_allow_html=True)
            plot_enrichr(enr_AutoRIF, '#8F3900')

        if gene_anno=='Minimal' or gene_anno=='Full':
            gene_list1 = enr_KEGG.results.iloc[0,-1]
            gene_list2 = enr_AutoRIF.results.iloc[0,-1]
            gene_db = pd.read_csv('Data/dbNSFP4.3a.Selected.csv')
            gene_db_orpha = pd.read_csv('Data/dbNSFP4.3a.Selected.Orpha.csv')

            cand_gene_list = gene_overlap(gene_list1, gene_list2)[0]
            # cand_gene_list = gene_list
            orpha_list = []
            st.markdown("<h2 style='text-align: left; color: black;'>OrphaNet gene functional importance</h1>", unsafe_allow_html=True)
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
                    plt.bar(X_axis-0.2, gene_annos_orpha.values.astype('float'), width=0.35, label='Orphanet genes', color='#069C74')
                    plt.bar(X_axis+0.2, gene_annos.values.astype('float'), width=0.35, label='All genes', color='#3C30E3')
                    plt.xticks([0,1,2,3], labels = labels,rotation=0)
                    plt.ylabel('Rankscore percentiles')
                    plt.legend()
                    st.pyplot(plt)
            st.markdown("<h3 style='text-align: left; color: black;'>Notes:</h1>", unsafe_allow_html=True)
            st.write("Interactions: The number of other genes this gene interacting with(from ConsensusPathDB).")
            st.write("pLI: the probability of being loss-of-function intolerant (intolerant of both heterozygous and homozygous lof variants) based on gnomAD 2.1 data.")
            st.write("GDI: gene damage index score, a genome-wide, gene-level metric of the mutational damage that has accumulated in the general population from doi: 10.1073/pnas.1518646112. The higher the score the more likely the gene is to be responsible for monogenic diseases.")
            st.write("LoFtool_score: a percentile score for gene intolerance to functional change. The higher the score the higher gene intolerance to functional change. For details see doi: 10.1093/bioinformatics/btv602.")
                
            if gene_anno=='Full':
                st.markdown("<h2 style='text-align: left; color: black;'>Gene annotation table</h1>", unsafe_allow_html=True)
                new_idx = gene_db_orpha['Gene_name'].isin(cand_gene_list)
                st.table(gene_db_orpha[new_idx].iloc[:,2:].reset_index())


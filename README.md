![Our Logo](images/Logo.png)

## Team 3a: Developing classification systems to compare diseases to each other
### Team Members: Awtum Brashear, Deborah Cragun, David Enoma, Chang Li, Mirshokhid Okilbekov, Motahareh Pourebehzadi, Sara Stubben 


## Background

### Rare diseases are often neglected
Rare diseases are generally defined as those with a prevalence of less than 1 in 2,000 (Ayme et al., 2015). Because of this, rare diseases are underrepresented in clinical coding systems (Ayme et al., 2015). Hereditary cancer syndromes that result from monogenic inheritance, although not rare, are neglected and have also not been adequately represented in clinical coding systems. This lack of codes leads to a lack of research and understanding of their importance, true prevalence, and etiology (Ayme et al., 2015).

### Classification systems are of vital clinical importance
Rare diseases and hereditary cancer syndromes have significant clinical impacts and costs (Ayme et al., 2015). When diseases are incorrectly classified or have no codes to denote them in clinical billing, this leads to the potential for incorrect classification and can even have diagnostic and treatment consequences. For example, one patient who participated in a study conducted by one of our team members had her ovaries removed because she had a pathogenic variant in a gene that was categorized with other hereditary breast and ovarian cancer genes even though this particular gene does not confer increased risks for ovarian cancer. This highlights the critical importance of accurate disease classification systems and the need for codes that can differentiate hereditary cancer predisposition syndromes and sporadic cancers.

### Existing classification systems fall short for rare diseases
The International Classification of Diseases (ICD) is used worldwide to classify diseases and causes of mortality and morbidity (Fung et al., 2020). The ICD-11 was adopted in May 2019 and was available for use in January 2022 (Fung et al., 2020). However, many systems are still relying on ICD-10, which was adopted in 1992 and has significant gaps when it comes to rare diseases and hereditary cancer syndromes, most of which were not even identified until after the ICD-10 system was developed (Ayme et al., 2015; Fung et al., 2020).
 
Orphanet began in 1996 to help classify rare diseases (Ayme et al., 2015), and while it does have a wide array of rare disease information, this system's utility is decreased if it is not connected with other classification systems. In the creation of ICD-11 an expert rare disease group worked to increase the number of rare diseases included by a factor of over 10-fold (Ayme et al., 2015).
 
Other than adding a substantial number of codes to represent more rare diseases and hereditary cancer syndromes, other changes to the ICD-11 from ICD-10 include:
1. the foundation component is all electronic with a knowledge base that can be regularly updated  (Fung et al., 2020)
2. multi-hierarchical/parent system relationships are allowed along with a linearization process which allows for multiple ways to classify one disease
 
Rare diseases and hereditary cancer syndromes often go by several different names, which makes finding them in classification systems difficult and matching them even more challenging. For example our team discovered that the ICD11 coding system calls Lynch syndrome only by the name Hereditary Nonpolyposis Colorectal Cancer Syndrome (HNPCC). Furthermore, we identified multiple data sources that incorrectly classified a condition or linked it to an incorrect gene due to similarities in some disease names (e.g., Carney complex vs. Carney-Stratakis syndrome). When a disease is incorrectly classified or linked to an incorrect gene, these issues can be perpetuated as different systems are linked together and draw from each other. As our understanding of rare diseases changes, classifications need to be updated, verified for accuracy, and linked so that one can easily compare the various classification systems or translate and assess equivalency from one system to another. This is particularly important as the ICD system is updated because when codes change, if they are not aligned it can falsely appear that conditions are changing in prevalence. Indeed, this is one reason why we want to work to facilitate the implementation of ICD11 coding systems because we are unable to conduct medical records reviews for many rare diseases and hereditary cancer syndromes because until ICD11 they often lacked unique codes.

## Solution
We have developed the webapp "rareform" in order to navigate the relationship between different classification methods and find comparable diseases.


### The reform webapp
[Access the rareform WebApp](https://share.streamlit.io/awtum/topic3_teama/main/Streamlit_app.py)

#### Viewing disease attributes in reform
You can pull diseases up by Disease name, Orpha code or ICD10 code
![App Disease View](images/App2.png)

#### Characterizing genes in reform
You can search genes or gene lists within reform
![App Gene View](images/App1.png)


## Future Directions
We hope this design can be improved in the following ways: 
1. Comparisons between ICD 11 and ICD 10 
2. Incorporation of genetic information to improve medical coding and grouping 
3. Clinical significance - diagnostics
4. Clean up of existing classification systems and databases

## References
Ayme, S., Bellet, B., & Rath, A. (2015). Rare diseases in ICD11: Making rare diseases visible in health information systems through appropriate coding. *Orphanet Journal of Rare Diseases, 10*, 35. https://doi.org/10.1186/s13023-015-0251-8

Fung, K. W., Xu, J., & Bodenreider, O. (2020). The new International Classification of Diseases 11th edition: a comparative analysis with ICD-10 and ICD-10-CM. *Journal of the American Medical Informatics Association, 27*(5), 738-746. https://dx.doi.org/10.1093%2Fjamia%2Focaa030

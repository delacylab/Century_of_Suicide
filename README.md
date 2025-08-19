<div align="right">
  Last update: 2025 August 19, 16:46 (by Wayne Lam)
</div>
<hr>

# Code for "A century of suicide: New insights from long term data in the United States" by de Lacy et al.

This public repository stores the Python code used to compute the summary statistics reported in the paper. 

# Data Sources

The three data sources used to generate the Suicide Trends and Archival Comparative Knowledgebase (STACK) used in the paper are:

(1) U.S. cause-specific mortality rates from 1900-1968 were reported in the National Center for Health Statistics (NCHS) annual reports. See https://www.cdc.gov/nchs/products/vsus.htm. 

(2) U.S. data for county-level cause-specific mortality rates were obtained from NCHS for 1968-2021. These restricted data, also known as the Multiple Cause of Death (MCOD) data, stratified by age, sex, race, and year, were obtained by securing approval through a Data Use Agreement with NCHS. Investigators can apply for these data directly with NCHS (https://www.cdc.gov/nchs/nvss/nvss-restricted-data.htm ).

(3) Public-use population denominator counts for calendar year-sex-race-county-specific single-year age groups obtained from the Surveillance, Epidemiology, and End Results (SEER) Program that curates and distributes these US Census data. See https://seer.cancer.gov/popdata.

# Code

Code used to compute summary statistics is written in Python. The scripts, located in the directory `Python_Scripts`, include the following functions:

|Script name|Function name|Description|
|---|---|---|
|`Age_Standardization.py`|`compute_age_standardized_rates`|Compute age-standardized death rates from the MCOD data with the population denominator counts from the SEER data.|
|`Data_Indexing.py`|`indexing_data`|Compute indexed death rates from pre-computed crude or age-standardized death rates.|
|`Demographic_Sampling.py`|`extract_gender`|Sample individuals from the MCOD data with a specific gender.|
|`Demographic_Sampling.py`|`extract_3_race`|Sample individuals from the MCOD data with a specific race in the range of 'White', 'Black', and 'Others'.|
|`Demographic_Sampling.py`|`extract_4_race`|Sample individuals from the MCOD data with a specific race in the range of 'White', 'Black', and 'American Indian', and 'Asian or Pacific Islander'.|
|`Demographic_Sampling.py`|`extract_generation`|Sample individuals from the MCOD data with a specific generation in the range of 'Silent Generation', 'Baby Boomers', 'Generation X', 'Millennials', and 'Generation Z'.|

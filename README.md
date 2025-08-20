<div align="right">
  Last update: 2025 August 20, 09:39 MT (by Wayne Lam)
</div>
<hr>

# Code for "A century of suicide: New insights from long term data in the United States" by de Lacy et al.

This public repository stores the Python code used to compute the summary statistics reported in the paper. 

# Data Sources

The three data sources used to generate the Suicide Trends and Archival Comparative Knowledgebase (STACK) used in the paper are:

(1) U.S. cause-specific mortality rates from 1900 to 1968 were reported in the National Center for Health Statistics (NCHS) annual reports. See https://www.cdc.gov/nchs/products/vsus.htm. 

(2) U.S. data for county-level cause-specific mortality rates, also known as the Multiple Cause of Death (MCOD) data, were obtained from NCHS for 1968-2021. These restricted data, stratified by age, sex, race, and year, were obtained by securing approval through a Data Use Agreement with NCHS. Investigators can apply for these data directly with NCHS (https://www.cdc.gov/nchs/nvss/nvss-restricted-data.htm). The CDC Public Use Data File Documentation (https://www.cdc.gov/nchs/nvss/mortality_public_use_data.htm) provides instructions for parsing the raw MCOD data files.

(3) Public-use population denominator counts for calendar year-sex-race-county-specific single-year age groups obtained from the Surveillance, Epidemiology, and End Results (SEER) Program that curates and distributes these US Census data. See https://seer.cancer.gov/popdata.

# Code

The code used to compute summary statistics is written in Python (version 3.11 or later), requiring only the common `Numpy` (version 1.26.4 or later) and `Pandas` (version 2.2.3 or later) dependencies. The table below lists the functions defined in the scripts stored in the `Code` directory, which were used to extract the summary statistics reported in the paper.

|Script name|Function name|Description|
|---|---|---|
|`Age_Standardization.py`|`compute_age_standardized_rates`|Compute age-standardized rates from the MCOD and SEER data.|
|`Data_Indexing.py`|`indexing_data`|Compute indexed rates from pre-computed crude/age-standardized rates.|
|`Demographic_Sampling.py`|`extract_gender`|Sample individuals from the MCOD data with a specific gender.|
|`Demographic_Sampling.py`|`extract_3_race`|Sample individuals from the MCOD data with a specific race (i.e., 'White', 'Black', and 'others').|
|`Demographic_Sampling.py`|`extract_5_race`|Sample individuals from the MCOD data with a specific race (i.e., 'White', 'Black', 'American Indian', and 'Asian or Pacific Islander').|
|`Demographic_Sampling.py`|`extract_age_group`|Sample individuals from the MCOD data belonging to a specific age group.|
|`Demographic_Sampling.py`|`extract_generation`|Sample individuals from the MCOD data from a specific generation (i.e., 'Silent Generation', 'Baby Boomers', 'Generation X', 'Millennials', and 'Generation Z').|
|`Urbanicity_Sampling.py`|`extract_urbanicity`|Sample individuals from the MCOD data belonging to a specific urbanicity/rurality category (i.e., 'urban counties', 'metro counties', and 'rural counties').|
|`ICD_Classification.py`|`extract_suicide`|Sample individuals from the MCOD data with a suicide death.|
|`ICD_Classification.py`|`extract_suicide_specific`|Sample individuals from the MCOD data with a specific method of suicide death.|
|`ICD_Classification.py`|`extract_others`|Sample individuals from the MCOD data with a specific method of death (i.e., 'heart attack', 'homicide', 'motor vehicle accident', and 'overdose').|

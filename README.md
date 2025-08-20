<div align="right">
  Last update: 2025 August 19, 19:51 MT (by Wayne Lam)
</div>
<hr>

# Code for "A century of suicide: New insights from long term data in the United States" by de Lacy et al.

This public repository stores the Python code used to compute the summary statistics reported in the paper. 

# Data Sources

The three data sources used to generate the Suicide Trends and Archival Comparative Knowledgebase (STACK) used in the paper are:

(1) U.S. cause-specific mortality rates from 1900-1968 were reported in the National Center for Health Statistics (NCHS) annual reports. See https://www.cdc.gov/nchs/products/vsus.htm. 

(2) U.S. data for county-level cause-specific mortality rates, also known as the Multiple Cause of Death (MCOD) data, were obtained from NCHS for 1968-2021. These restricted data, stratified by age, sex, race, and year, were obtained by securing approval through a Data Use Agreement with NCHS. Investigators can apply for these data directly with NCHS (https://www.cdc.gov/nchs/nvss/nvss-restricted-data.htm ).

(3) Public-use population denominator counts for calendar year-sex-race-county-specific single-year age groups obtained from the Surveillance, Epidemiology, and End Results (SEER) Program that curates and distributes these US Census data. See https://seer.cancer.gov/popdata.

# Code

Code used to compute summary statistics is written in Python. See the following for the functions defined in the scripts stored in the `Code` directory.

|Script name|Function name|Description|
|---|---|---|
|`Age_Standardization.py`|`compute_age_standardized_rates`|Compute age-standardized rates from the MCOD and SEER data.|
|`Data_Indexing.py`|`indexing_data`|Compute indexed rates from pre-computed crude/age-standardized rates.|
|`Demographic_Sampling.py`|`extract_gender`|Sample individuals from the MCOD data with a specific gender in the list of 'female' and 'male'.|
|`Demographic_Sampling.py`|`extract_3_race`|Sample individuals from the MCOD data with a specific race in the list of 'White', 'Black', and 'others'.|
|`Demographic_Sampling.py`|`extract_5_race`|Sample individuals from the MCOD data with a specific race in the list of 'White', 'Black', 'American Indian', and 'Asian or Pacific Islander'.|
|`Demographic_Sampling.py`|`extract_generation`|Sample individuals from the MCOD data with a specific generation in the list of race in the list of 'Silent Generation', 'Baby boomers', 'Generation X', 'Millennials', and 'Generation Z'.|
|`Urbanicity_Sampling.py`|`extract_urbanicity`|Sample individuals from the MCOD data with a specific category in the list of 'urban counties', 'metro counties', and 'rural counties', defined by Rural-Urban Continuum Codes (RUCC).|
|`ICD_Classification.py`|`extract_suicide`|Sample individuals from the MCOD data recorded as death by suicide.|
|`ICD_Classification.py`|`extract_suicide_specific`|Sample individuals from the MCOD data recorded as death by suicide with a specific method of death in the list of 'firearms and explosives', 'poisoning', 'hanging, strangulation, and suffocation', and 'others'.|
|`ICD_Classification.py`|`extract_others`|Sample individuals from the MCOD data recorded as death by a specific method of death in the list of 'heart attack', 'homicide', 'motor vehicle accident', and 'overdose'.|

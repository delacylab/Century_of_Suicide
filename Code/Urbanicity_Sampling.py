########################################################################################################################
# Apache License 2.0
########################################################################################################################
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Copyright 2025 Nina de Lacy
########################################################################################################################

########################################################################################################################
# Overview: This script provides the function needed to sample the individuals whose residence belongs to a certain
# county with a corresponding Rural-Urban Continuum Code (RUCC) from the Multiple Cause of Death (MCOD) data.

# Remark 1: RUCC was developed in 1974. A standard geographical practice is to map FIPS codes to RUCC. However, MCOD
# data didn't incorporate FIPS codes until 1982. Before 1982, MCOD data used the Geographic Code Manual (GCM) to encode
# counties. Thus, a bridging from GCM codes to RUCC was manually performed in this script. See the following URL for
# GCM codes and RUCC.
# Reference for GCM codes: https://ntrl.ntis.gov/NTRL/dashboard/searchResults/titleDetail/PB81117046.xhtml
# Reference for RUCC: https://www.ers.usda.gov/data-products/rural-urban-continuum-codes

# Remark 2: This script assumes that the parsed MCOD data has the following two columns:
# 'Resident_State': The state that the individual resided, encoded by two-letter state code.
# 'Resident_County': The county that the individual resided, encoded as an integer, which stores the GCM code in
# 1974-1981 and FIPS code in 1982-2021.
########################################################################################################################

########################################################################################################################
# Import packages
########################################################################################################################
import pandas as pd
from typing import Literal

########################################################################################################################
# Define a function to extract records with individuals belong to a specific rurality/urbanicity group defined by RUCC.
########################################################################################################################


def extract_urbanicity(df: pd.DataFrame,
                       year: int,
                       urbanicity_int: Literal[0, 1, 2]):
    """
    :param df: A pandas.DataFrame.
           A dataset with each row representing an individual.
    :param year: Integer.
           The year of the MCOD data.
    :param urbanicity_int: An integer in [0, 1, 2].
           The urbanicity/rurality to be specified:
           0 for Urban counties (i.e., RUCC codes 0-3),
           1 for Metro counties (i.e., RUCC codes 4-7),
           2 for Rural counties (i.e., RUCC codes 8-9).
    :return:
    df_sub: A pandas.DataFrame.
    df with only individuals with the specified urbanicity/rurality (supplied with RUCC and Urbanicity columns)
    """

    # Type and value check
    assert isinstance(df, pd.DataFrame), 'df must be a pandas.DataFrame.'
    assert isinstance(year, int), 'year must be an integer.'
    assert year in range(1974, 2022), 'year must be within the range of [1974, 2021].'
    assert 'Resident_State' in df.columns, 'Resident_State must be a column in df.'
    assert 'Resident_County' in df.columns, 'Resident_County must be a column in df.'

    # Define the dictionary for state FIPS code
    state_codes: dict[str, str] = {
        'AK': '02', 'AL': '01', 'AR': '05', 'AZ': '04', 'CA': '06', 'CO': '08', 'CT': '09', 'DC': '11',
        'DE': '10', 'FL': '12', 'GA': '13', 'HI': '15', 'IA': '19', 'ID': '16', 'IL': '17', 'IN': '18',
        'KS': '20', 'KY': '21', 'LA': '22', 'MA': '25', 'MD': '24', 'ME': '23', 'MI': '26', 'MN': '27',
        'MO': '29', 'MS': '28', 'MT': '30', 'NC': '37', 'ND': '38', 'NE': '31', 'NH': '33', 'NJ': '34',
        'NM': '35', 'NV': '32', 'NY': '36', 'OH': '39', 'OK': '40', 'OR': '41', 'PA': '42', 'RI': '44',
        'SC': '45', 'SD': '46', 'TN': '47', 'TX': '48', 'UT': '49', 'VA': '51', 'VT': '50', 'WA': '53',
        'WI': '55', 'WV': '54', 'WY': '56'}

    # Consider the case in 1974-1981 where GCM is used to encode counties
    if year < 1982:

        # Map GCM codes to RUCC
        df_GCM: pd.DataFrame = pd.read_excel('Urbanicity_Encoding_Files/RUCC_1974_1982_GCM.xlsx',
                                             usecols=['State_Code', 'GCM', 'RUCC']).dropna(subset=['GCM'])
        df_GCM['GCM'] = df_GCM['GCM'].astype(int).astype(str)
        df_GCM['State_GCM'] = df_GCM['State_Code'] + df_GCM['GCM']
        df_GCM['RUCC'] = df_GCM['RUCC'].astype('Int32')
        df['Resident_County'] = df['Resident_County'].astype(int).astype(str)
        df['State_GCM'] = df['Resident_State'] + df['Resident_County']
        df = pd.merge(left=df, right=df_GCM.dropna(subset=['RUCC'])[['State_GCM', 'RUCC']], on='State_GCM', how='left')
        df = df.drop(columns=['State_GCM'])

    # Consider the case in 1982-2021 where FIPS codes became available in MCOD data
    else:

        # Specify the paths for the CSV files that map FIPS codes to RUCC codes
        FIPS_paths: list[str] = ['Urbanicity_Encoding_Files/RUCC_1983_1992.csv',
                                 'Urbanicity_Encoding_Files/RUCC_1993_2002.csv',
                                 'Urbanicity_Encoding_Files/RUCC_2003_2012.csv',
                                 'Urbanicity_Encoding_Files/RUCC_2013_2022.csv']
        if year in range(1983, 1993):
            FIPS_path: str = FIPS_paths[0]
        elif year in range(1993, 2003):
            FIPS_path: str = FIPS_paths[1]
        elif year in range(2003, 2013):
            FIPS_path: str = FIPS_paths[2]
        else:
            FIPS_path: str = FIPS_paths[3]

        # Load the CSV file and convert into a dictionary mapping FIPS codes to RUCC codes
        df_FIPS: pd.DataFrame = pd.read_csv(FIPS_path, usecols=['FIPS', 'RUCC'])
        df_FIPS['FIPS'] = df_FIPS['FIPS'].apply(lambda x: '0' * (5 - len(str(x))) + str(x))
        FIPS_RUCC_dict: dict[str, int] = dict(zip(df_FIPS["FIPS"], df_FIPS["RUCC"]))

        # Supply extra FIPS codes used in MCOD that were not listed in the CSV files
        extra_FIPS: dict[str, dict[int, int]] = {'02010': {y: 7 for y in range(1983, 1994)},
                                                 '02140': {y: 9 for y in range(1982, 1994)},
                                                 '02231': {1982: 7},
                                                 '02232': {y: 9 for y in range(1994, 2003)},
                                                 '02280': {2013: 7},
                                                 '51780': {1982: 6}}
        for k, v in extra_FIPS.items():
            if year in v.keys():
                FIPS_RUCC_dict[k] = v[year]

        # Map FIPS codes to RUCC
        df['State_FIPS'] = df['Resident_State'].map(state_codes)
        df['County_FIPS'] = df['Resident_County'].astype(str).apply(lambda x: '0' * (3 - len(x)) + x)
        df['FIPS'] = df['State_FIPS'] + df['County_FIPS']
        df['RUCC'] = df['FIPS'].map(FIPS_RUCC_dict)
        df = df.drop(columns=['State_FIPS', 'County_FIPS', 'FIPS'])

    # Map RUCC to urbanicity/rurality categorization
    urbanicity_map: dict[int, int] = {0: 0, 1: 0, 2: 0, 3: 0, 4: 1, 5: 1, 6: 1, 7: 1, 8: 2, 9: 2}
    df['Urbanicity'] = df['RUCC'].map(urbanicity_map)
    df_sub: pd.DataFrame = df[df['Urbanicity'] == urbanicity_int].reset_index(drop=True)
    return df_sub


########################################################################################################################
# Test run
########################################################################################################################


if __name__ == '__main__':

    # Example 1: Create a dummy dataframe to store individuals' residential record (at death) in 1974
    df_ = pd.DataFrame({'Subject_ID': ['A', 'B', 'C'],              # AK6: Lynn Canal-Icy, Alaska (RUCC=9)
                        'Resident_State': ['AK', 'UT', 'CA'],       # UT2: Box Elder County, Utah (RUCC=6)
                        'Resident_County': [6, 2, 34]})             # CA34: Sacramento County, California (RUCC=2)
    print(f'[Example 1] Filtered data frame:\n', extract_urbanicity(df=df_, year=1974, urbanicity_int=1), '\n')

    # Example 2: Create a dummy dataframe to store individuals' residential record (at death) in 1983
    df_ = pd.DataFrame({'Subject_ID': ['A', 'B', 'C'],              # AK185/02185: North Slope Borough (RUCC=9)
                        'Resident_State': ['AK', 'UT', 'CA'],       # UT005/49005: Cache County (RUCC=4)
                        'Resident_County': [185, 5, 81]})           # CA081/06081: San Mateo County (RUCC=1)
    print(f'[Example 1] Filtered data frame:\n', extract_urbanicity(df=df_, year=1983, urbanicity_int=1))

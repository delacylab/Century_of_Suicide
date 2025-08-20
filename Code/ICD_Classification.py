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
# Overview: This script provides the functions used to classify individuals by their method of death using the
# International Classification of Diseases (ICD) codes, in different revisions (i.e., ICD-8 in 1969-1978, ICD-9 in
# 1979-1998, and ICD-10 in 1999-2021).
########################################################################################################################

########################################################################################################################
# Remark 1: When filtering with the individuals who died by completing suicide, the 34 cause list titles in the Multiple
# Cause of Death (MCOD) data are used in 1969-1998. The cause list became unavailable since 1999, we used the
# corresponding ICD-10 codes for data in 1999-2021. In the following, we assume that ICD code used to determine the
# primary cause of death is stored in 'ICD8' and 'ICD34' in 1969-1978, 'ICD9' and 'ICD34' in 1979-1998, and 'ICD10' in
# 1999-2021.

# Remark 2: Since the Multiple Cause of Death (MCOD) data records various methods of death for each death record in
# its Record Axes (RAs), an individual is categorized as having a specific cause of death X if their RAs includes at
# least one of the ICD codes used to define X. In the following, we assume that the 20 RAs are stored as columns in the
# MCOD data as ['RA1', 'RA2', ..., 'RA20'].
########################################################################################################################

########################################################################################################################
# Import packages
########################################################################################################################
import numpy as np
import pandas as pd
from typing import Literal

pd.options.mode.chained_assignment = None


########################################################################################################################
# Define a function to extract the records with only the individuals who completed suicide.
########################################################################################################################


def extract_suicide(df: pd.DataFrame,
                    year: int):
    """
    :param df: A pandas.DataFrame.
           A dataset with each row representing an individual.
    :param year: Integer.
           The year of the MCOD data.
    :return:
    df_sub: A pandas.DataFrame.
    df with only individuals who completed suicide according to their death records.
    """

    # Type and value check
    assert isinstance(df, pd.DataFrame), 'df must be a pandas.DataFrame.'
    assert isinstance(year, int), 'year must be an integer.'
    assert year in range(1969, 2022), 'year must be within the range of [1969, 2021].'
    if year in range(1969, 1999):
        assert 'ICD34' in df.columns, 'ICD34 must be a column in df.'
    else:
        assert 'ICD10' in df.columns, 'ICD10 must be a column in df.'

    # Subset the death records by the corresponding year-specific ICD code(s)
    if year in range(1969, 1999):
        assert 'ICD34' in df.columns, 'ICD34 must be a column in df.'
        df_sub: pd.DataFrame = df[df['ICD34'].apply(lambda x: str(x) == 350)]
    else:
        U_codes = ['U03 ', 'U030', 'U039']
        X_codes = [f'X{i} ' for i in range(60, 85)]
        Y_codes = ['Y870']
        df_sub: pd.DataFrame = (df[df['ICD10'].apply(lambda x: str(x) in U_codes + X_codes + Y_codes)]
                                .reset_index(drop=True))
    return df_sub


########################################################################################################################
# Define a function to extract the records with only the individuals who completed suicide with a pre-specified method
# of death.
########################################################################################################################


def extract_suicide_specific(df: pd.DataFrame,
                             year: int,
                             method_int: Literal[0, 1, 2, 3]):
    """
    :param df: A pandas.DataFrame.
           A dataset with each row representing an individual.
    :param year: Integer.
           The year of the MCOD data.
    :param method_int: An integer in [0, 1, 2, 3].
           The integer encoding the suicide method: 0 for firearms and explosives, 1 for poisoning, 2 for hanging,
           strangulation, and suffocation, and 3 for others.
    :return:
    df_sub: A pandas.DataFrame.
    df with ony individuals who completed suicide by a pre-specified method according to their death records.
    """

    # Type and value check
    assert isinstance(df, pd.DataFrame), 'df must be a pandas.DataFrame.'
    assert isinstance(year, int), 'year must be an integer.'
    assert year in range(1969, 2022), 'year must be within the range of [1969, 2021].'
    if year in range(1969, 1979):
        assert 'ICD8' in df.columns, 'ICD8 must be a column in df.'
        icd_col = 'ICD8'
    elif year in range(1979, 1999):
        assert 'ICD9' in df.columns, 'ICD9 must be a column in df.'
        icd_col = 'ICD9'
    else:
        assert 'ICD10' in df.columns, 'ICD10 must be a column in df.'
        icd_col = 'ICD10'
    ra_cols = [f'RA{i}' for i in range(1, 21, 1)]
    assert all([col in df.columns for col in ra_cols]), 'RA1, ..., RA20 must be columns in df.'
    assert method_int in [0, 1, 2, 3], 'method_int must be an integer in [0, 1, 2, 3].'

    # Define the ICD codes for different methods of suicide death across different revisions
    ICD_dict: dict[int, dict[str, list]] = {
        0:  # 'Firearms and explosives'
            {'ICD8': [955],
             'ICD9': [9550, 9551, 9552, 9553, 9554, 9555, 9559],
             'ICD10': ['X72 ', 'X73 ', 'X74 ', 'X75 ']},
        1:  # 'Poisoning'
            {'ICD8': [9500, 9501, 9502, 9503, 9504, 9505, 9506, 9507, 9508, 9509, 951, 9520, 9521, 9529],
             'ICD9': [9500, 9501, 9502, 9503, 9504, 9505, 9506, 9507, 9508, 9509, 9510, 9511, 9518,
                      9520, 9521, 9528, 9529],
             'ICD10': ['X60 ', 'X61 ', 'X62 ', 'X63 ', 'X64 ', 'X65 ', 'X66 ', 'X67 ', 'X68 ', 'X69 ']},
        2:  # 'Hanging, strangulation, and suffocation'
            {'ICD8': [953],
             'ICD9': [9530, 9531, 9538, 9539],
             'ICD10': ['X70 ']},
        3:  # 'Others'
            {'ICD8': [954, 956, 957, 958, 959],
             'ICD9': [954, 956, 9570, 9571, 9572, 9579, 9580, 9581, 9582, 9583, 9584, 9585, 9586, 9587, 9588, 9589,
                      959],
             'ICD10': ['U030', 'X71 ', 'X76 ', 'X77 ', 'X78 ', 'X79 ', 'X80 ', 'X81 ', 'X82 ', 'X83 ', 'X84 ',
                       'Y870']}
    }

    # Extract the list of ICD codes to be used
    ICD_codes: list[str] = [str(code) for code in ICD_dict[method_int][icd_col]]

    # Determine whether each individual has a RA with an ICD code specified in ICD_codes
    ra_cols_caret: list[str] = []
    for ra_col in ra_cols:
        ra_col_caret: str = f'{ra_col}^'
        ra_cols_caret.append(ra_col_caret)
        df[ra_col_caret] = df[ra_col].apply(lambda x: int(pd.notna(x) and any(str(x) in code for code in ICD_codes)))
    df['Flag'] = df[ra_cols_caret].apply(lambda x: np.nanmax(x), axis=1).astype('Int32')

    # Filter with the individuals who has a positive value in the newly created 'Flag' column
    df_sub = df[df['Flag'] == 1]
    df_sub = df_sub.drop(columns=['Flag'] + ra_cols_caret).reset_index(drop=True)
    return df_sub


########################################################################################################################
# Define a function to extract the records with only the individuals who died by heart attack, homicide, motor
# vehicle accident, or overdose.
# Reference: https://www.mdch.state.mi.us/osr/fatal/icd10.asp
########################################################################################################################


def extract_others(df: pd.DataFrame,
                   year: int,
                   method_int: Literal[0, 1, 2, 3]):
    """
    :param df: A pandas.DataFrame.
           A dataset with each row representing an individual.
    :param year: Integer.
           The year of the MCOD data.
    :param method_int: An integer in [0, 1, 2, 3].
           The integer encoding the death method: 0 for heart attack, 1 for homicide, 2 for motor vehicle accident, and
           3 for overdose.
    :return:
    df_sub: A pandas.DataFrame.
    df with ony individuals who completed suicide according to their death records.
    """

    # Type and value check
    assert isinstance(df, pd.DataFrame), 'df must be a pandas.DataFrame.'
    assert isinstance(year, int), 'year must be an integer.'
    assert year in range(1969, 2022), 'year must be within the range of [1969, 2021].'
    if year in range(1969, 1979):
        assert 'ICD8' in df.columns, 'ICD8 must be a column in df.'
        icd_col = 'ICD8'
    elif year in range(1979, 1999):
        assert 'ICD9' in df.columns, 'ICD9 must be a column in df.'
        icd_col = 'ICD9'
    else:
        assert 'ICD10' in df.columns, 'ICD10 must be a column in df.'
        icd_col = 'ICD10'
    assert method_int in [0, 1, 2, 3], 'method_int must be an integer in [0, 1, 2, 3].'
    if method_int == 3:
        ra_cols = [f'RA{i}' for i in range(1, 21, 1)]
        assert all([col in df.columns for col in ra_cols]), 'RA1, ..., RA20 must be columns in df.'

    # Define the ICD codes for different methods of death across different revisions
    ICD_dict: dict[int, dict[str, list]] = {
        0:  # 'Heart attack'
            {'ICD8': [410],
             'ICD9': [410],
             'ICD10': ['I21 ', 'I22 ', ]},
        1:  # 'Homicide'
            {'ICD8': [960, 961, 962, 963, 964, 965, 966, 967, 968, 969],
             'ICD9': [960, 961, 962, 963, 964, 965, 966, 967, 968, 969],
             'ICD10': ['X85 ', 'X86 ', 'X87 ', 'X88 ', 'X89 ',
                       'X90 ', 'X91 ', 'X92 ', 'X93 ', 'X94 ', 'X95 ', 'X96 ', 'X97 ', 'X98 ', 'X99 ',
                       'Y00', 'Y01 ', 'Y02 ', 'Y03 ', 'Y04 ', 'Y05 ', 'Y06 ', 'Y07 ', 'Y08 ', 'Y09 ',
                       'Y871', 'U01 ', 'U02 ']},
        2:  # 'Motor vehicle accident'
            {'ICD8': [810, 811, 812, 813, 814, 815, 816, 817, 818, 819],
             'ICD9': [810, 811, 812, 813, 814, 815, 816, 817, 818, 819],
             'ICD10': ['V021', 'V029', 'V092',
                       'V122', 'V123', 'V124', 'V125',
                       'V132', 'V133', 'V134', 'V135',
                       'V142', 'V143', 'V144', 'V145',
                       'V194', 'V195', 'V196'] + \
                      [f'V{i}{j}' for i in range(20, 29) for j in [3, 4, 5, 9]] + \
                      [f'V{i}{j}' for i in range(29, 80) for j in range(4, 10)] + \
                      ['V803', 'V804', 'V805', 'V811', 'V821'] + \
                      [f'V{i}{j}' for i in range(83, 87) for j in range(4)] + \
                      [f'V87{i}' for i in range(9)] + \
                      ['V892']},
        3:  # 'Overdose'
            {'ICD8': [8500, 8501, 8502, 8503, 8504, 8505, 8506, 8507, 8508, 8509,
                      8510, 8511, 8512, 8513, 8514, 8515, 8516, 8517, 8518, 8519,
                      8520, 8521, 8522, 8523, 8524, 8525, 8526, 8627, 8528, 8529,
                      8530, 8531, 8532, 8533, 8534, 8535, 8539,
                      8540, 8541, 8542, 8543, 8548, 8549,
                      8550, 8551, 8552, 8553, 8554, 8555, 8556, 8559,
                      8560, 8561, 8562, 8563, 8564, 8568, 8569,
                      8570, 8571, 8572, 8573, 8574, 8575, 8576, 8579,
                      8580, 8581, 8582, 8583, 8584, 8585, 8586, 8589,
                      8590, 8591, 8592, 8593, 8594, 8595, 8596, 8597, 8598, 8599,
                      9500, 9501, 9502, 9503,
                      962,
                      9800, 9801, 9802, 9803],
             'ICD9': [8500, 8501, 8502, 8503, 8504, 8505, 8508, 8509,
                      851,
                      8520, 8521, 8522, 8523, 8524, 8525, 8528, 8529,
                      8530, 8531, 8532, 8538, 8539,
                      8540, 8541, 8542, 8543,
                      8550, 8551, 8552, 8553, 8554, 8555, 8556, 8558, 8559,
                      856,
                      857,
                      8580, 8581, 8582, 8583, 8584, 8585, 8586, 8587, 8588, 8589,
                      9500, 9501, 9502, 9503, 9504, 9505,
                      9620,
                      9800, 9801, 9802, 9803, 9804, 9805],
             'ICD10': ['X40 ', 'X41 ', 'X42 ', 'X43 ', 'X44 ',
                       'X60 ', 'X61 ', 'X62 ', 'X63 ', 'X64 ',
                       'X85 ',
                       'Y10 ', 'Y11 ', 'Y12 ', 'Y13 ', 'Y14 ']}
    }
    ICD_codes: list[str] = [str(code) for code in ICD_dict[method_int][icd_col]]

    # Subset the death records by the corresponding year-specific ICD code(s)
    df_sub: pd.DataFrame = df[df[icd_col].apply(lambda x: str(x) in ICD_codes)]
    if method_int == 3:
        T_codes: list[str] = ['T360 ', 'T361 ', 'T362 ', 'T363 ', 'T364 ', 'T365 ', 'T366 ', 'T367 ', 'T368 ', 'T369 ',
                              'T370 ', 'T371 ', 'T372 ', 'T373 ', 'T374 ', 'T375 ', 'T378 ', 'T379 ',
                              'T380 ', 'T381 ', 'T382 ', 'T383 ', 'T384 ', 'T385 ', 'T386 ', 'T387 ', 'T388 ', 'T389 ',
                              'T390 ', 'T391 ', 'T392 ', 'T393 ', 'T394 ', 'T398 ', 'T399 ',
                              'T400 ', 'T401 ', 'T402 ', 'T403 ', 'T404 ', 'T405 ', 'T406 ', 'T407 ', 'T408 ', 'T409 ',
                              'T410 ', 'T411 ', 'T412 ', 'T413 ', 'T414 ', 'T415 ',
                              'T420 ', 'T421 ', 'T422 ', 'T423 ', 'T424 ', 'T425 ', 'T426 ', 'T427 ', 'T428 ',
                              'T430 ', 'T431 ', 'T432 ', 'T433 ', 'T434 ', 'T435 ', 'T436 ', 'T438 ', 'T439 ',
                              'T440 ', 'T441 ', 'T442 ', 'T443 ', 'T444 ', 'T445 ', 'T446 ', 'T447 ', 'T448 ', 'T449 ',
                              'T450 ', 'T451 ', 'T452 ', 'T453 ', 'T454 ', 'T455 ', 'T456 ', 'T457 ', 'T458 ', 'T459 ',
                              'T460 ', 'T461 ', 'T462 ', 'T463 ', 'T464 ', 'T465 ', 'T466 ', 'T467 ', 'T468 ', 'T469 ',
                              'T470 ', 'T471 ', 'T472 ', 'T473 ', 'T474 ', 'T475 ', 'T476 ', 'T477 ', 'T478 ', 'T479 ',
                              'T480 ', 'T481 ', 'T482 ', 'T483 ', 'T484 ', 'T485 ', 'T486 ', 'T487 ',
                              'T490 ', 'T491 ', 'T492 ', 'T493 ', 'T494 ', 'T495 ', 'T496 ', 'T497 ', 'T498 ', 'T499 ',
                              'T500 ', 'T501 ', 'T502 ', 'T503 ', 'T504 ', 'T505 ', 'T506 ', 'T507 ', 'T508 ', 'T509 ']

        ra_cols = [f'RA{i}' for i in range(1, 21, 1)]
        ra_cols_caret: list[str] = [f'{ra_col}^' for ra_col in ra_cols]
        for ra_col in ra_cols:
            ra_col_caret: str = f'{ra_col}^'
            df_sub[ra_col_caret] = df_sub[ra_col].apply(
                lambda x: int(pd.notna(x) and any(str(x) in code for code in T_codes)))
        df_sub['Flag'] = df_sub[ra_cols_caret].apply(lambda x: np.nanmax(x), axis=1).astype('Int32')
        df_sub = df_sub[df_sub['Flag'] == 1]
        df_sub = df_sub.drop(columns=['Flag'] + ra_cols_caret).reset_index(drop=True)
    return df_sub


########################################################################################################################
# Test run
########################################################################################################################


if __name__ == '__main__':

    # Specify the year of the death records
    year_ = 2000

    # Create a dummy dataframe to store the death records of the individuals
    df_ = pd.DataFrame({'Subject_ID': ['A', 'B', 'C'],
                        'ICD10': ['X64 ', 'Y870', 'X88 '],  # X64 and Y870 are codes for suicide, X88 is not.
                        'RA1': ['X64 ', 'Y870', 'X88 '],  # Each RA can repeat the codes in the ICD10 column
                        })
    for k in range(2, 21):
        df_[f'RA{k}'] = np.nan  # RAs other than the 1st one can be missing

    # Filter df_ with individuals who completed suicide
    df_sub_ = extract_suicide(df_, year_)
    print(f'Data filtered with only individuals who completed suicide:\n', df_sub_)

    # Filter df_sub_ further by individuals who completed suicide by poisoning
    df_sub_poisoning_ = extract_suicide_specific(df_sub_, year=year_, method_int=1)
    print(f'Data filtered with only individuals who completed suicide by poisoning:\n', df_sub_poisoning_)

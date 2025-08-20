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
# Overview: This script provides the functions needed to sample the individuals of a certain demographic group (by
# gender, race, and generation) from the Multiple Cause of Death (MCOD) data.
########################################################################################################################

########################################################################################################################
# Import packages
########################################################################################################################
import numpy as np
import pandas as pd
from typing import Literal

########################################################################################################################
# Define a function to extract the records with only the individuals with a specific gender.
# Remark: Assume that 'Gender' exists in the MCOD data as a column to encode gender.
########################################################################################################################


def extract_gender(df: pd.DataFrame,
                   gender: Literal['M', 'F']):
    """
    :param df: A pandas.DataFrame.
           A dataset with each row representing an individual.
    :param gender: A string in ['M', 'F'].
           The gender to be specified: 'M' for male and 'F' for female.
    :return:
    df_sub: A pandas.DataFrame.
    df with only individuals with the specified gender.
    """

    # Type and value check
    assert isinstance(df, pd.DataFrame), 'df must be a pandas.DataFrame.'
    assert gender in ['M', 'F'], 'gender must be an string in ["M", "F"].'
    assert 'Gender' in df.columns, 'Gender must be a column in df.'

    # Subset the records by the specific gender
    df_sub: pd.DataFrame = df[df['Gender'] == gender].reset_index(drop=True)
    return df_sub

########################################################################################################################
# Define a function to extract records with only the individuals with a specific race in White (1), Others (2), and
# Black (3).
# Remark: Assume that 'Race_Recode_3' exists in the MCOD data as a column to encode race as a 3-valued variable for
# years in 1969-2020. In 2021, we bridge the 40 races to 3 races accordingly, with individuals reporting multiple races
# considered as Others.
########################################################################################################################


def extract_3_race(df: pd.DataFrame,
                   year: int,
                   race_int: Literal[1, 2, 3]):
    """
    :param df: A pandas.DataFrame.
           A dataset with each row representing an individual.
    :param year: Integer.
           The year of the MCOD data.
    :param race_int: An integer in [1, 2, 3].
           The race to be specified: 1 for White, 2 for Others, and 3 for Black.
    :return:
    df_sub: A pandas.DataFrame.
    df with only individuals with the specified race.
    """

    # Type and value check
    assert isinstance(df, pd.DataFrame), 'df must be a pandas.DataFrame.'
    assert isinstance(year, int), 'year must be an integer.'
    assert year in range(1969, 2022), 'year must be within the range of [1969, 2021].'
    if year in range(1969, 2021):
        assert 'Race_Recode_3' in df.columns, 'Race_Recode_3 must be a column in df.'
    else:
        assert 'Race_Recode_40' in df.columns, 'Race_Recode_40 must be a column in df.'
    assert race_int in [1, 2, 3], 'race_int must be an integer in [1, 2, 3].'

    # For 2021, create a mapping to bridge 40 races to 3 races
    def race_40_to_3(x):
        if pd.isna(x):
            return np.nan
        elif x == 1:
            return 1
        elif x == 2:        # Black is encoded as 2 (instead of 3) in 2021
            return 3
        else:
            return 2
    if year == 2021:
        df['Race_Recode_3'] = df['Race_Recode_40'].apply(race_40_to_3)

    # Subset the records by the specific race
    df_sub: pd.DataFrame = df[df['Race_Recode_3'] == race_int].reset_index(drop=True)
    return df_sub

########################################################################################################################
# Define a function to extract records with only the individuals with a specific race in White (1), Black (2),
# 'American Indian' (3), and 'Asian / Pacific Islander' (4).
# Remark: Assume that 'Race_Recode_5' exists in the MCOD data as a column to encode race as a 4-valued variable for
# years in 2003-2021. In 2021, we bridge the 40 races to 4 races accordingly, with individuals reporting multiple races
# being ignored.
########################################################################################################################


def extract_5_race(df: pd.DataFrame,
                   year: int,
                   race_int: Literal[1, 2, 3, 4]):
    """
    :param df: A pandas.DataFrame.
           A dataset with each row representing an individual.
    :param year: Integer.
           The year of the MCOD data.
    :param race_int: An integer in [1, 2, 3, 4].
           The race to be specified: 1 for White, 2 for Black, 3 for American Indian, and 4 for Asian/Pacific Islander.
    :return:
    df_sub: A pandas.DataFrame.
    df with only individuals with the specified race.
    """

    # Type and value check
    assert isinstance(df, pd.DataFrame), 'df must be a pandas.DataFrame.'
    assert isinstance(year, int), 'year must be an integer.'
    assert year in range(2003, 2022), 'year must be within the range of [2003, 2021].'
    if year in range(2003, 2021):
        assert 'Race_Recode_5' in df.columns, 'Race_Recode_5 must be a column in df.'
    else:
        assert 'Race_Recode_40' in df.columns, 'Race_Recode_40 must be a column in df.'
    assert race_int in [1, 2, 3, 4], 'race_int must be an integer in [1, 2, 3, 4].'

    # For 2021, create a mapping to bridge 40 races to 4 races
    def race_40_to_4(x):
        if x in [1, 2, 3]:
            return x
        elif x in [4, 5, 6, 7, 8, 9, 10]:        # Codes for 'Asian/Pacific Islander' in 2021
            return 4
        else:
            return np.nan
    if year == 2021:
        df['Race_Recode_3'] = df['Race_Recode_40'].apply(race_40_to_4)

    # Subset the records by the specific race
    df_sub: pd.DataFrame = df[df['Race_Recode_5'] == race_int].reset_index(drop=True)
    return df_sub

########################################################################################################################
# Define a function to extract records with only the individuals with a specific generation: 'Silent Generation' (0),
# 'Baby Boomers' (1), 'Generation X' (2), 'Millennials' (3), and 'Generation Z' (4).
# Remark: Assume that 'Age_Number' exists in the MCOD data as a column to encode individuals' age in years. In some
# uncommon occasions, the 'Age_Type' column is used to encode a certain unit used in encoding age. For example,
# 'Age_Type' as 1 means the individual has an age above 100 such that his actual age should be defined by 'Age_Type' +
# 'Age_Number'. Users should clean the MCOD data accordingly before using this function.
# Reference: https://www.pewresearch.org/short-reads/2019/01/17/where-millennials-end-and-generation-z-begins/
########################################################################################################################


def extract_generation(df: pd.DataFrame,
                       year: int,
                       generation_int: Literal[0, 1, 2, 3, 4]):
    """
    :param df: A pandas.DataFrame.
           A dataset with each row representing an individual.
    :param year: Integer.
           The year of the MCOD data.
    :param generation_int: An integer in [0, 1, 2, 3, 4].
           The race to be specified: 0 for Silent Generation, 1 for Baby Boomers, 2 for Generation X, 3 for Millennials,
           and 4 for Generation Z.
    :return:
    df_sub: A pandas.DataFrame.
    df with only individuals with the specified generation.
    """

    # Type and value check
    assert isinstance(df, pd.DataFrame), 'df must be a pandas.DataFrame.'
    assert 'Age_Number' in df.columns, 'Age_Number must be a column in df.'
    assert isinstance(year, int), 'year must be an integer.'
    assert year in range(1969, 2022), 'year must be within the range of [1969, 2021].'
    assert generation_int in [0, 1, 2, 3, 4], 'generation_int must be an integer in [0, 1, 2, 3, 4].'

    # Define a dictionary to map birth year to generation code
    generation_dict: dict[int, int] = {}
    for birth_year in range(1928, 2022):
        if birth_year in range(1928, 1945 + 1):
            generation_dict[birth_year] = 0          # class 0: Silent Generation
        elif birth_year in range(1946, 1964 + 1):
            generation_dict[birth_year] = 1          # class 1: Baby Boomers
        elif birth_year in range(1965, 1980 + 1):
            generation_dict[birth_year] = 2          # class 2: Generation X
        elif birth_year in range(1981, 1996 + 1):
            generation_dict[birth_year] = 3          # class 3: Millennials
        elif birth_year in range(1997, 2012 + 1):
            generation_dict[birth_year] = 4          # class 4: Generation Z
        else:
            generation_dict[birth_year] = np.nan     # Not categorized

    df['Birth_Year'] = year - df['Age_Number']
    df['Generation'] = df['Birth_Year'].map(generation_dict)

    # Subset the records by the specific generation
    df_sub: pd.DataFrame = df[df['Generation'] == generation_int].reset_index(drop=True)
    return df_sub

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
# Overview: This script provides the function needed to compute age-standardized rates from raw rates.
########################################################################################################################

########################################################################################################################
# Import packages
########################################################################################################################
import numpy as np
import pandas as pd
########################################################################################################################

########################################################################################################################
# Define the function to match an age (in years) to an age group in [0, 1, ..., 10]
# Reference: https://www.cdc.gov/nchs/hus/sources-definitions/age-adjustment.htm (AgeAdj-Table II.)
########################################################################################################################


def create_age_group_dict():
    """
    :return: A dictionary mapping age (in integers) to codes for age group in [0, 1, ..., 10]
    """
    age_group_dict: dict[int, int] = {}
    for age in range(200):
        if age == 0:
            age_group_dict[age] = 0
        elif age in range(1, 5):
            age_group_dict[age] = 1
        elif age in range(5, 15):
            age_group_dict[age] = 2
        elif age in range(15, 25):
            age_group_dict[age] = 3
        elif age in range(25, 35):
            age_group_dict[age] = 4
        elif age in range(35, 45):
            age_group_dict[age] = 5
        elif age in range(45, 55):
            age_group_dict[age] = 6
        elif age in range(55, 65):
            age_group_dict[age] = 7
        elif age in range(65, 75):
            age_group_dict[age] = 8
        elif age in range(75, 85):
            age_group_dict[age] = 9
        elif age in range(85, 200):
            age_group_dict[age] = 10
        else:
            age_group_dict[age] = np.nan
    return age_group_dict

########################################################################################################################
# Define a function to assign proportion distribution (weight) to each age group using the 2000 U.S. standard population
# Reference: https://www.cdc.gov/nchs/hus/sources-definitions/age-adjustment.htm (AgeAdj-Table II.)
########################################################################################################################


def create_age_group_weight_dict():
    """
    :return: A dictionary mapping age group codes in [0, 1, ..., 10] to the age-group-specific weights (floats)
    """
    age_weight_dict: dict[int, float] = {0: 0.013818,
                                         1: 0.055317,
                                         2: 0.145565,
                                         3: 0.138646,
                                         4: 0.135573,
                                         5: 0.162613,
                                         6: 0.134834,
                                         7: 0.087247,
                                         8: 0.066037,
                                         9: 0.044842,
                                         10: 0.015508,
                                         np.nan: np.nan}
    return age_weight_dict

########################################################################################################################
# Define a function to compute age-standardized rates from a raw dataset with rows storing the individuals' age
########################################################################################################################


def compute_age_standardized_rates(df: pd.DataFrame,
                                   df_pop: pd.DataFrame,
                                   age_col: str,
                                   age_group_col: str,
                                   pop_col: str):
    """
    :param df: A pandas.DataFrame.
           A dataset with each row representing an individual.
    :param df_pop: A pandas.DataFrame.
           A dataset with each row storing the population count for each encoded age group.
    :param age_col: A string.
           The column name in df that encodes the individuals' age.
    :param age_group_col: A string.
           The column name in df_pop that encodes the encoded age groups.
    :param pop_col: A string.
           The column name in df_pop that encodes the age-group-specific population counts.
    :return:
    (a) raw_rate: A float.
        The raw rate.
    (b) standardized_rate: A float.
        The age-standardized rate.
    """

    # Type and value check
    assert isinstance(df, pd.DataFrame), 'df must be a pandas.DataFrame.'
    assert isinstance(df_pop, pd.DataFrame), 'df_pop must be a pandas.DataFrame.'
    assert isinstance(age_col, str), 'age_col must be a string.'
    assert isinstance(age_group_col, str), 'age_group_col must be a string.'
    assert isinstance(pop_col, str), 'pop_col must be a string.'
    assert age_col in df.columns, 'age_col must be a column in df.'
    assert age_group_col in df_pop.columns, 'age_group_col must be a column in df_pop.'
    assert pop_col in df_pop.columns, 'pop_col must be a column in df_pop.'

    # Compute the count per age group from each individual's age
    df[age_group_col]: pd.Series = df[age_col].map(create_age_group_dict())
    df_age_group: pd.DataFrame = df.groupby(by=age_group_col).agg(count=(age_group_col, 'count')).reset_index()

    # Merge with df_pop on the age_group_col columns
    df_age_group = pd.merge(left=df_age_group, right=df_pop[[age_group_col, pop_col]], on=age_group_col, how='left')

    # Compute the raw rate (per 100,000 persons) for each age group
    df_age_group['Raw_Rate_Per_100k']: pd.Series = df_age_group['count'] / (df_age_group['Population'] / 100000)

    # Compute the proportional rate (per 100,000 persons) for each age group
    df_age_group['Weight']: pd.Series = df_age_group['Age_Group'].map(create_age_group_weight_dict())
    df_age_group['Standardized_Rate_Per_100k']: pd.Series = df_age_group['Raw_Rate_Per_100k'] * df_age_group['Weight']

    # Compute and return the raw rate and age-standardized rates (per 100,000 persons)
    raw_rate: float = df_age_group['Raw_Rate_Per_100k'].sum()
    standardized_rate: float = df_age_group['Standardized_Rate_Per_100k'].sum()
    return raw_rate, standardized_rate

########################################################################################################################
# Test run
########################################################################################################################


if __name__ == '__main__':

    # Create a dummy dataframe to store the individuals' ages
    df_ = pd.DataFrame({'Age': [15, 22, 25, 32, 45, 38, 39, 51, 77, 102, 57]})

    # Create a dummy population dataframe to store the population information for each age group
    df_pop_ = pd.DataFrame({'Age_Group': range(11),
                            'Population': range(1000000, 11000001, 1000000)})

    # Compute the raw rates and age-standardized rates
    raw_rate_, standardized_rate_ = compute_age_standardized_rates(df=df_,
                                                                   df_pop=df_pop_,
                                                                   age_col='Age',
                                                                   age_group_col='Age_Group',
                                                                   pop_col='Population')
    print(f'Raw rate (per 100,000 persons): {raw_rate_:.2f}')
    print(f'Age-standardized rate (per 100,000 persons): {standardized_rate_:.2f}')

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
# Overview: This script provides the function needed to perform data-indexing.
########################################################################################################################

########################################################################################################################
# Import packages
########################################################################################################################
import pandas as pd
########################################################################################################################


def indexing_data(df: pd.DataFrame,
                  rate_col: str,
                  year_col: str):
    """
    :param df: A pandas.DataFrame.
           A dataset with each row representing annual death rate.
    :param rate_col: A string.
           The column name in df that encodes the annual death rates.
    :param year_col: A string.
           The column name in df that encodes the years.
    :return:
    df_copy: A pandas.DataFrame.
    df with an extra column '{rate_col}_indexed' that encodes the indexed rate_col.
    """

    # Type and value check
    assert isinstance(df, pd.DataFrame), 'df must be a pandas.DataFrame.'
    assert rate_col in df.columns, 'rate_col must be a column in df.'
    assert year_col in df.columns, 'year_col must be a column in df.'
    try:
        df[rate_col] = df[rate_col].astype(float)
    except TypeError:
        raise TypeError('rate_col must have a data type of float.')
    try:
        df[year_col] = df[year_col].astype('Int32')
    except TypeError:
        raise TypeError('year_col must have a data type of Int32.')

    # Sort df by years in ascending order
    df = df.sort_values(by=year_col, ascending=True)

    # Compute the base rate
    rate_base: float = df.loc[df[year_col] == df[year_col].min(), rate_col].values[0]

    # Compute the annual indexed rate as an extra column
    df[f'{rate_col}_indexed'] = df[rate_col] * (100 / rate_base)
    df_copy = df.copy(deep=True)
    return df_copy

########################################################################################################################
# Test run
########################################################################################################################


if __name__ == '__main__':

    # Create a dummy dataframe to store the annual raw rates
    df_ = pd.DataFrame({'Year': range(2010, 2016),
                        'Rate': [11.1, 12.2, 9.3, 12.5, 13.1, 10.7]})
    df_copy_ = indexing_data(df=df_, rate_col='Rate', year_col='Year')
    print(f'Updated data frame with an extra column for indexed rates:\n', df_copy_)

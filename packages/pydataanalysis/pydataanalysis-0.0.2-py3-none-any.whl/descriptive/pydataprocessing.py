import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler, Normalizer, KBinsDiscretizer, MinMaxScaler, RobustScaler
from sklearn.preprocessing import PowerTransformer, QuantileTransformer
from scipy.stats import boxcox
from collections import Counter

"""

     Data Preprocessing 

            -  Data Preprocessing - Functions 


"""


#                 ----------------  DATA PREPROCESSING  ----------------


def unique_values(data, categorical_column: str):
    """
    Print out all the unique values in a categorical column
    :param data:variable
    :param categorical_column:string with column name
    :return:unique values in dataset
    """
    cat_col = data[categorical_column].unique()
    cat_col.sort()
    return cat_col


def columns_with_missing_values(data) -> list:
    """
    PRINT COLUMNS WITH MISSING VALUES
    :param data:variable
    :return:a list of columns with missing values
    """
    cols_with_missing = [col for col in data.columns if data[col].isnull().any()]
    return cols_with_missing


def fill_missing_value(data, column_name: str, filling_with: str):
    """
    Handle missing values
    filling_with string replace "NAN" rows, with one of the chosen string name :
    median
    mode
    mean
    :param data:variable
    :param column_name:a string with column name
    :param filling_with:filling with
    :return: updated filled column
    """
    if filling_with.lower() == "median":
        return data[column_name].fillna(data[column_name].median(), inplace=True)
    elif filling_with.lower() == "mean":
        return data[column_name].fillna(data[column_name].mean(), inplace=True)
    elif filling_with.lower() == "mode":
        return data[column_name].fillna(data[column_name].mode(), inplace=True)
    else:
        print("Enter mean, median or mode to fill in the missing values")


def drop_missing_rows(data):
    """
    Remove all the rows that contain a missing value
    :param data:variable
    :return:dataframe without missing rows
    """
    dataframe_without_missing_rows = data.copy()
    dataframe_without_missing_rows.dropna(inplace=True)
    return dataframe_without_missing_rows


def replace_missing_values_with_zero(data):
    """
    Replace all NaN values with 0
    :param data:variable
    :return:dataframe filled row with 0
    """
    data_filled_with_zero = data.copy()
    data_filled_with_zero.fillna(0, inplace=True)
    return data_filled_with_zero


def replace_missing_values_with_what_comes_after_it(data):
    """
    Replace missing values that comes directly after it in the same column,
    :param data:variable
    :return:filled dataframe
    """
    bfill_data = data.copy()
    bfill_data.fillna(method="bfill", axis=0, inplace=True)
    return bfill_data


def replace_missing_values_with_string(data, column: str, my_string: str):
    """
     replace missing values with a string
    :param data: variable
    :param column: categorical column name as a string
    :param my_string: fill missing values with a string
    :return: filled dataframe
    """

    data[column].fillna(my_string, axis=0, inplace=True)
    return data


def remove_duplicated_columns(data):
    """
    Removes duplicated columns(based on column names)
    :param data: variable
    :return: data without duplicate columns
    """
    data_without_duplicates = data.loc[:, ~data.columns.duplicated()]
    return data_without_duplicates


def one_hot_encoding(data, categorical_col: list):
    """
    encode categorical variables using one-hot encoding
    :param data:variable
    :param categorical_col:list with categorical columns name
    :return: one hot encoded  dataframe
    """
    try:
        one_hot_encoded_data = pd.get_dummies(data, columns=categorical_col)

    except TypeError:
        print("categorical column Input must be a list")
    except KeyError:
        print("None of type ='object' are in the [columns]")
    else:
        return one_hot_encoded_data


def label_encoding(data, categorical_col: list):
    """
    encode categorical variables using label encoder
    :param data:variable
    :param categorical_col:list of categorical column names
    :return: encoded categorical dataframe
    """
    try:
        label_encoder = LabelEncoder()
        data[categorical_col] = data[categorical_col].apply(label_encoder.fit_transform)
    except ValueError:
        print("categorical column Input must be a list")
    except KeyError:
        print("None of type ='object' are in the [columns]")
    else:
        return data


def standardization_numerical_columns(data, numerical_column: list):
    """
    scale the values of a numeric column so that they have zero mean and unit variance
    :param data: variable
    :param numerical_column:String with numerical column name
    :return: scale dataframe
    """
    std_scaler = StandardScaler()
    df_scaled = std_scaler.fit_transform(data[numerical_column])
    df_scaled = pd.DataFrame(df_scaled, columns=numerical_column)
    return df_scaled


def normalize_numerical_column(data, numerical_column: str):
    """
    scale the values of a numeric column so that they have a minimum value of 0
    and a maximum value of 1
    :param data:
    :param numerical_column:
    :return:
    """
    normalizer = Normalizer()
    data[numerical_column] = normalizer.fit_transform(data[[numerical_column]])
    return data


def divide_num_col_into_cat_col_using_bins(data, numerical_col: str, number_bins: int):
    """
    Divide the values of a continuous numeric column into categorical column using bins
    :param data: variable
    :param numerical_col: string with numerical column name
    :param number_bins: integer of numbers of bins
    :return: dataframe
    """
    discretizer = KBinsDiscretizer(n_bins=number_bins, encode="ordinal")
    data[numerical_col] = discretizer.fit_transform(data[[numerical_col]])
    return data


def min_max_scaler_to_numerical_column(data, numerical_column: list):
    """
    scale the values of a numeric column so that they have a minimum value of 0
    and a maximum value of 1
    :param data: variable
    :param numerical_column:string with numerical column name
    :return:dataframe
    """
    scaler = MinMaxScaler()
    df_scaled = scaler.fit_transform(data.to_numpy())
    df_scaled = pd.DataFrame(df_scaled, columns=numerical_column)
    return df_scaled


def robust_scaling_to_numerical_column(data, numerical_column: str):
    """
    scale the values of a numeric column using the median and interquartile range.
    it's useful when the data contains outliers.
    :param data:variable
    :param numerical_column:string with numerical column name
    :return:dataframe
    """
    scaler = RobustScaler()
    data[numerical_column] = scaler.fit_transform(data[[numerical_column]])
    return data


def power_transformation_to_numerical_column(data, numerical_column: str):
    """
    power transformer are a class of functions that can be used to transform the values of a numeric column in order to
    stabilize or improve the assumptions of certain statistical models. it can be useful
    for correcting the skewness of a distribution
    :param data:variable
    :param numerical_column:string with numerical column name
    :return:dataframe
    """
    transformer = PowerTransformer()
    data[numerical_column] = transformer.fit_transform(data[[numerical_column]])
    return data


def quantile_transformation_to_numerical_column(data, numerical_column: str):
    """
    Transform the values of a numeric columns so that they have a uniform or normal distribution
    :param data:variable
    :param numerical_column:string of numerical column name
    :return:dataframe
    """
    transformer = QuantileTransformer()
    data[numerical_column] = transformer.fit_transform(data[[numerical_column]])
    return data


def box_cox_transformation_to_numerical_column(data, numerical_column: str):
    """
    Transform the values of a numeric columns so that they are approximately normally distributed
    :param data:variable
    :param numerical_column:string with numerical column name
    :return:dataframe
    """
    data[numerical_column], lambda_ = boxcox(data[numerical_column])
    return data


def cumulatively_categories(data, variable_column, threshold: float):
    """
    summing overall column of a random variables less than or equal to a specified threshold percentage
    :param data: data variable
    :param variable_column: string with column name
    :param threshold: float of percentage values to detect
    :return: dataframe with new cumulative column
    """
    threshold_value = int(threshold * len(data[variable_column]))
    categories_list = []
    s = 0
    counts = Counter(data[variable_column])
    for i, j in counts.most_common():
        s += dict(counts)[i]
        categories_list.append(i)
        if s >= threshold_value:
            break
    categories_list.append("Other")
    data[variable_column] = data[variable_column].apply(lambda x: x if x in categories_list else "Other")
    return data


def detect_outliers(data):
    """
    Detect outliers in a data frame
    :param data: variable
    :return: dataframe of columns with outliers percentage
    """
    outlier_percents = {}
    for column in data.columns:
        if data[column].dtype != object:
            q1 = np.quantile(data[column], 0.25)
            q3 = np.quantile(data[column], 0.75)
            iqr = q3 - q1
            upper_bound = q3 + (1.5 * iqr)
            lower_bound = q1 - (1.5 * iqr)
            outliers = data[(data[column] > upper_bound) | (data[column] < lower_bound)][column]
            outlier_percentage = len(outliers) / len(data[column]) * 100
            outlier_percents[column] = outlier_percentage
    outlier_dataframe = pd.DataFrame(data=outlier_percents.values(), index=list(outlier_percents.keys()),
                                     columns=['Outlier_percentage'])
    return outlier_dataframe.sort_values(by='Outlier_percentage', ascending=False)


def handle_outliers(data, column_name: str):
    tenth = np.percentile(data[column_name], 10)
    ninetieth = np.percentile(data[column_name], 90)
    data[column_name] = np.where(data[column_name] > ninetieth, ninetieth, data[column_name])
    return data[column_name]


def age_range(df, age_col: str):
    bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    labels = ["0-18", "18-29", "30-41", "42-53", "54-65", "66-77", "77-88", "88-100"]
    result = pd.cut(df[age_col], bins=bins, labels=labels, right=False)
    return result
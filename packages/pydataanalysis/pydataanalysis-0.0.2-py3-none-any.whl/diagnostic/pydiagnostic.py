from scipy.stats import ttest_ind, chi2_contingency, wilcoxon
from scipy import stats
from math import ceil
import pandas as pd

"""

                Diagnostic Analysis - Answer the question (Why did it happen?)

     Functions in the module : 
     -  test_p_value: Takes a p_value parameter and print out if the null hypothesis is rejected or not
           alpha is set to 0.05. 
     -  chi2_test : Test about two categorical variables and return the p-value, the return value can be passed to 
           the test_p_value 
     -  test_one_categorical_and_one_numeric: Test about one numerical and one categorical variable (two-sided test)
           and return the p-value, the return value can be passed to the test_p_value 
           if you divide the two-sided p-value by two , this will give the one sided one. 
     -  analysis_of_variance_test : Test about one categorical with more than two unique values and one numeric 
        variable, return the p-value, the return value can be passed to the test_p_value    
     -  wilcoxon_rank_test: Test about one numerical variable before and one numeric variable after,
           return the p-value, the return value can be passed to the test_p_value                  
     -  test_relationship_between_two_numeric_variables: Test about two numeric variables , the function print out
           Pearson Correlation Coefficient and a P-value. moreover, it returns the p-value which can be passed 
           to the test_p_value function. 
     -  compare_the_means_of_two_numerical_columns: perform a t_test to compare the means of two numeric columns 
           and return the p-value, the return value can be passed to the test_p_value function 

"""


def test_p_value(p_value: float):
    """
    The function test the p-value with significance level of  0.05
    :param p_value: float p-value
    :return: print out the test
    """
    alpha = 0.05
    p_value = ceil(p_value)
    if p_value < alpha:
        print("Reject the null hypothesis")
    else:
        print("Accept the null hypothesis")


def chi2_test(data, categorical_column_one: str, categorical_column_two: str) -> float:
    """
    Test about two categorical variables
    Sample question: Does the proportion of male and female differ across age groups
    :param data:variable
    :param categorical_column_one:string with categorical column name
    :param categorical_column_two:string with categorical column name
    :return: p-value
    """

    df_cont = pd.crosstab(data[categorical_column_one], data[categorical_column_two])
    observed_values = df_cont.values
    val = chi2_contingency(df_cont)
    expected_values = val[3]
    no_of_rows = df_cont.shape[0]
    no_of_columns = df_cont.shape[1]
    degree_of_freedom = (no_of_rows-1) * (no_of_columns - 1)
    chi_square = sum([(o-e)**2/e for o, e in zip(observed_values, expected_values)])
    chi_square_statistic = chi_square[0] + chi_square[1]
    # critical_value = stats.chi2.ppf(q=1 -alpha, df=ddof)
    p_value = 1 - stats.chi2.cdf(x=chi_square_statistic, df=degree_of_freedom)
    print("p_value", p_value)
    print("Degree of freedom", degree_of_freedom)
    return p_value


def test_one_categorical_and_one_numeric(data, numerical_column: str, categorical_column: str) -> float:
    """
    Test about one categorical and one numeric Variable
    Sample question:  Is there a difference in height between men and women
    :param data:variable
    :param numerical_column:string with numerical column name
    :param categorical_column:string with categorical column name
    :return: p_value
    """
    category_group_list = data.groupby(categorical_column)[numerical_column].apply(list)
    fvalue, p_value = stats.ttest_ind(*category_group_list)
    print(f"P-value of: {p_value}")
    return p_value


def analysis_of_variance_test(data, numerical_column: str, categorical_group_column: str) -> float:
    """
    Function takes the  group as input and returns ANOVA f and p value
    Sample question:  Is there a difference in height between age groups
    :param data:variable
    :param numerical_column:string with numerical column name
    :param categorical_group_column:string with categorical column name
    :return: float p_value
    """
    category_group_list = data.groupby(categorical_group_column)[numerical_column].apply(list)
    fvalue, p_value = stats.f_oneway(*category_group_list)
    print(f"P-value of: {p_value}")
    return p_value


def wilcoxon_rank_test(data, numerical_colum_before: str, numerical_column_after: str) -> float:
    """
    example hypotheses test:
            H0: Sample distribution are equal
            H1: Sample distribution are not equal
    :param data:variable
    :param numerical_colum_before:string with numerical column name
    :param numerical_column_after:string with numerical column name
    :return:float p_value
    """
    w, p_value = wilcoxon(data[numerical_colum_before], data[numerical_column_after])
    print(f"P-value of: {p_value}")
    return p_value


def test_relationship_between_two_numeric_variables(data, numeric_column_one: str, numeric_column_two: str) -> float:
    """
    Test about two numeric variables
    Sample question: Is there a relationship between height and weight
    :param data:variable
    :param numeric_column_one:string with numerical column name
    :param numeric_column_two:string with numerical column name
    :return:float p_value
    """
    pearson_coef, p_value = stats.pearsonr(data[numeric_column_one], data[numeric_column_two])
    print(f"Pearson Correlation Coefficient {pearson_coef}, and a P-value of{p_value}")
    return p_value


def compare_the_means_of_two_numerical_columns(data, numerical_col_one: str, numerical_col_two: str) -> float:
    """
    perform a t_test to compare the means of two numeric columns
    :param data:variable
    :param numerical_col_one:string with numerical column name
    :param numerical_col_two:string with numerical column name
    :return: float p-value
    """
    t, p_value = ttest_ind(data[numerical_col_one], data[numerical_col_two])
    print(t, p_value)
    return p_value
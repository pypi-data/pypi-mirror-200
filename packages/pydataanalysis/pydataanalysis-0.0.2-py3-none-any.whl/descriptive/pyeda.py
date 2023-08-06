import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.plotting import lag_plot, autocorrelation_plot, scatter_matrix
import statsmodels.graphics.gofplots as sm


pd.set_option("display.max_columns", None)

"""

     Descriptive Analysis - Answer the question (What Happen? )

        It is divided to two parts:
            -    part_one. EDA - Functions 
            -    part_two. Analysis Functions 


"""


#             ----------------  EDA Methods  ---------------


def read_dataset(file_name: str):
    """
    read cvs data file
    :param file_name: a string contain the csv file name
    :return: pandas dataframe
    """
    try:
        df = pd.read_csv(file_name, parse_dates=True)
        return df
    except FileNotFoundError:
        print("No such File, upload your dataset CSV file to the project")


def display_summary_data(dataframe):
    """
    The function prints out a summary table of columns
        - number of unique
        - Null values
        - Null Percentage
        - DataType
    :param dataframe: variable
    :return: Summarize columns dataframe
    """
    summary_tabel = pd.DataFrame({"Unique": dataframe.nunique(),
                                  "Null": dataframe.isna().sum(),
                                  "NullPercent": dataframe.isna().sum() / len(dataframe),
                                  "Types": dataframe.dtypes.values})
    print(summary_tabel)


def display_seperation_list_of_columns(data):
    """
    Separate numerical features and categorical features
    and print out a list of variables name
    :param data: variable
    :return: list of numerical and categorical features
    """
    numeric_variable_lst = data.select_dtypes(include=["int64", "float64"]).columns.tolist()
    categorical_variable_lst = data.select_dtypes(include=["object"]).columns.tolist()

    print(f"Numerical Columns: {numeric_variable_lst}\nCategorical Columns: {categorical_variable_lst}")


def select_numeric_variables(data_frame):
    """
    Selecting numerical variables
    :param data_frame: variable
    :return: all numeric features in a dataset
    """
    numeric_variable_lst = data_frame.select_dtypes(exclude="object")
    return numeric_variable_lst


def select_categorical_variables(data):
    """
    Selecting categorical variables
    :param data: variable
    :return: all categorical features in a dataset
    """
    categorical_variable_lst = data.select_dtypes(include="object")
    return categorical_variable_lst


def visualize_different_plots_of_numeric_col(data_frame, column_name: str):
    """
    Plot numerical variable in different charts
    :param data_frame: variable
    :param column_name: string with column name
    :return: collections of charts
    """
    if data_frame[column_name].dtype != object:
        fig, ax = plt.subplots(1, 5, figsize=(24, 4))
        sns.histplot(data_frame[column_name], bins=30, kde=True, ax=ax[0])
        sns.kdeplot(data_frame[column_name], ax=ax[1])
        sns.countplot(x=data_frame[column_name], ax=ax[2])
        sns.boxplot(y=data_frame[column_name], ax=ax[3])
        sns.scatterplot(x=data_frame.index, y=data_frame[column_name], ax=ax[4])
        plt.tight_layout()
        plt.show()
    else:
        print("Provide a numerical column to visualize")


def visualize_categorical_col(data_frame, column_name: str):
    """
    Plot Categorical Variable
    :param data_frame: variable
    :param column_name: string with column name
    :return: bar chart of the categorical column
    """
    data_frame[column_name].value_counts().plot(kind="bar")
    plt.ylabel("Count")
    plt.xlabel(column_name)
    plt.show()


def display_statistics_for_individual_col(data, column_name: str) -> None:
    """
    Print out basic statistics
    :param data: variable
    :param column_name: string with column name
    :return: print out basic statistics
    """
    print(data[column_name].describe())


def correlation_between_two_numerical_columns(data, column_one: str, column_two: str) -> float:
    """
    Calculate correlation between two numerical columns
    :param data: variable
    :param column_one: string with column name
    :param column_two: string with column name
    :return: correlation value between two numerical columns
    """
    return data[column_one].corr(data[column_two])


def calculate_statistics_for_cat_by_num_col(data, cat_column: list, num_column: list):
    """
    Group the data by a categorical column and numerical column and calculate statistics
    :param data: variable
    :param cat_column: List with categorical column name
    :param num_column: List with numerical column name
    :return: new index dataframe
    """
    grouped_data = data.groupby(by=cat_column)[num_column].describe(percentiles=[])
    return grouped_data


def scatter_plot(data, numeric_column_one: str, numeric_column_two: str):
    """
    create a scatter plot to visualize the relationship. between two numeric columns
    :param data:
    :param numeric_column_one: string with numerical column name
    :param numeric_column_two: string with numerical column name
    :return: scatter plot
    """
    plt.scatter(data[numeric_column_one], data[numeric_column_two])
    plt.xlabel(numeric_column_one)
    plt.ylabel(numeric_column_two)
    plt.show()


def box_plot_distribution(data, numeric_column: str):
    """
    Create a box plot to visualize the distribution of a numeric column
    :param data: variable
    :param numeric_column: string with numerical column name
    :return: boxplot chart
    """
    plt.boxplot(data[numeric_column])
    plt.ylabel(numeric_column)
    plt.show()


def visualize_bar_plot_for_each_category_of_categorical_column(data, cat_column: str, num_column: str):
    """
    Create a bar plot to visualize the mean of a numeric column for each category of
    a categorical column
    :param data: variable
    :param cat_column:string with categorical column name
    :param num_column:string with numerical column name
    :return: bar chart
    """
    data.groupby(cat_column)[num_column].mean().plot(kind="bar")
    plt.ylabel(f"Average {num_column}")
    plt.show()


def pivot_tabel(data, index_col: list, columns: list, values: list, agg: str):
    """
    Create a pivot table to summarize the data
    :param data:variable
    :param index_col:list of columns names
    :param columns:list of columns name
    :param values:list of columns name
    :param agg:string of aggfunction
    :return: pivot table
    """

    pivot_table = pd.pivot_table(data, index=index_col, columns=columns, values=values, aggfunc=agg, margins=True)
    return pivot_table


def visualize_pivot_table(pivot_table):
    """
    Create a heatmap to visualize the pivot table
    :param pivot_table:
    :return: heatmap
    """
    try:
        plt.pcolor(pivot_table, cmap="Reds")
        plt.colorbar()
        plt.show()
    except ValueError:
        print("Not enough values to unpack ")


def visualize_relationship_between_multiple_numeric_columns(data, numerical_columns: list):
    """
    Create a pair plot to visualize the relationship between multiple numeric columns
    :param data:variable
    :param numerical_columns:list of numerical column names
    :return:pair-plot chart
    """
    sns.pairplot(data, vars=numerical_columns)
    plt.title("Relationship Between Columns")
    plt.show()


def visualize_the_mean_by_categories_of_categorical_column(data, numerical_col: str, categorical_col: str):
    """
    create a point plot to visualize the mean of a numerical column
    by the categories of a categorical column
    :param data:variable
    :param numerical_col:string with numerical column name
    :param categorical_col:string with categorical column name
    :return: point plot chart
    """
    sns.pointplot(data, x=categorical_col, y=numerical_col)
    plt.ylabel(f"Average {numerical_col}")
    plt.show()


def visualize_the_count_of_cat_col_by_categories_cat_col(data, cat_col_one: str, by_cat_col_two: str):
    """
    create a count plot to visualize the count of a categorical column
    by the categories of another categorical column
    :param data:variable
    :param cat_col_one:string with categorical column name
    :param by_cat_col_two:string with categorical column name
    :return:count plot chart
    """
    sns.countplot(x=cat_col_one, hue=by_cat_col_two, data=data)
    plt.show()


def visualize_boxplot_of_numeric_column_by_categorical_col(data, categorical_col: str, numerical_col: str):
    """
    Create a box plot to visualize the distribution of a numeric column
    by the categories of a categorical column
    :param data:variable
    :param categorical_col:string with categorical column name
    :param numerical_col:string with numerical column name
    :return: boxplot chart
    """
    sns.boxplot(data=data, x=categorical_col, y=numerical_col)
    plt.ylabel(f"{numerical_col}")
    plt.show()


def visualize_numeric_column_by_the_categories_of_cat_col(data, categorical_colum: str, numerical_column: str):
    """
    Create a faceting grid to visualize the distribution of multiple numeric
    columns by the categories of a categorical column
    :param data:variable
    :param categorical_colum:string with categorical column name
    :param numerical_column:string with numerical column name
    :return: visualize chart
    """
    g = sns.FacetGrid(data, col=categorical_colum)
    g.map(plt.hist, numerical_column)
    plt.show()


def relationship_matrix_between_multiple_numeric_columns(data, numerical_columns: list):
    """
    Create a scatter plot matrix to visualize the relationship between
    multiple numeric columns
    :param data:variable
    :param numerical_columns:string with numerical column name
    :return: scatter plot matrix
    """
    scatter_matrix(data[numerical_columns], alpha=0.2, figsize=(6, 6))
    plt.show()


def visualize_heatmap(data):
    """
    Create a heatmap to visualize the correlation between multiple numeric columns
    :param data:variable
    :return: Heatmap chart
    """
    numeric_features = select_numeric_variables(data)
    plt.figure(figsize=(12, 8))
    sns.heatmap(numeric_features.corr(), cmap="RdYlGn", annot=True)
    plt.show()


def visualize_check_of_auto_correlation_in_numerical_col(data, numerical_colum: str):
    """

    :param data:
    :param numerical_colum:
    :return: auto correlation chart
    """
    lag_plot(data[numerical_colum])
    plt.show()


def visualize_auto_correlation_in_numerical_column(data, numerical_colum: str):
    """

    :param data:
    :param numerical_colum:
    :return: auto correlation chart
    """
    autocorrelation_plot(data[numerical_colum])
    plt.show()


def regression_plot_between_two_numerical_col(data, numerical_col_one: str, numerical_col_two: str):
    """
    Create a regression plot to visualize the relationship between two numeric columns
    :param data:variable
    :param numerical_col_one:string with numerical column name
    :param numerical_col_two:string with numerical column name
    :return:regression chart
    """
    sns.regplot(x=numerical_col_one, y=numerical_col_two, data=data)
    plt.show()


def mean_confidence_interval_of_numeric_by_categories_col(data, categorical_col: str, numerical_col: str):
    """
    Create a point plot to visualize the mean and confidence interval of a
    numerical column by the categories of a categorical column
    :param data:variable
    :param categorical_col:string with categorical column name
    :param numerical_col:string with numerical column name
    :return: point plot chart
    """
    sns.pointplot(x=categorical_col, y=numerical_col, data=data, errorbar=("ci", 95))
    plt.ylabel(f"Average {numerical_col}")
    plt.show()


def visualize_relationship_by_two_numeric_and_categories_col(data, num_col_one: str, num_col_two: str, cat_col: str):
    """
    Create a line plot to visualize the relationship between two numeric columns and the
    categories of a categorical column
    :param data:variable
    :param num_col_one:string with numerical column name
    :param num_col_two:string with numerical column name
    :param cat_col:string with categorical column name
    :return: line plot chart
    """
    sns.lmplot(data=data, x=num_col_one, y=num_col_two, hue=cat_col)
    plt.show()


def boxen_plot_distribution_of_numeric_and_categories_col(data, num_col: str, cat_col: str):
    """
    Create a boxen plot to visualize the distribution of a numerical column
    by the categories of a categorical column
    :param data:variable
    :param num_col:string with numerical column name
    :param cat_col:string with categorical column name
    :return: boxen plot chart
    """
    sns.boxenplot(data=data, x=cat_col, y=num_col)
    plt.ylabel(f"{num_col}")
    plt.show()


def visualize_distribution_of_numerical_column(data, numerical_col: str):
    """
    Create a distplot to visualize the distribution of numerical column
    :param data:variable
    :param numerical_col:string with numerical column name
    :return:distribution chart
    """
    sns.histplot(data[numerical_col])
    plt.show()


def kernel_density_estimate(data, numerical_col: str):
    """
    Create a kdeplot to visualize the kernel density estimate ofa numerical column
    :param data:variable
    :param numerical_col:string with numerical column name
    :return:visualize kernel density estimate
    """
    sns.kdeplot(data[numerical_col])
    plt.show()


def rugplot(data, numerical_col: str):
    """
    Create a rugplot to visualize the distribution of numerical column
    :param data:variable
    :param numerical_col:string with numerical column name
    :return:visualize rugplot distribution
    """
    sns.rugplot(data[numerical_col])
    plt.show()


def joint_plot(data, numerical_col_one: str, numerical_col_two: str):
    """
    Create a joint plot to visualize the relationship between two numerical columns
    and their distributions
    :param data:variable
    :param numerical_col_one:string with numerical column name
    :param numerical_col_two:string with numerical column name
    :return:relationship distribution plot
    """
    sns.jointplot(data=data, x=numerical_col_one, y=numerical_col_two)
    plt.show()


def pie_chart_by_numerical_col(data, cat_column: str, num_col: str):
    """
    Pie chart a categorical column by numerical column
    :param data: variable
    :param cat_column: categorical column as string
    :param num_col: numerical column as string
    :return: pie chart
    """
    data.groupby([cat_column]).sum().plot(kind="pie", y=num_col, colors=sns.color_palette("dark"),
                                          startangle=90, autopct="%1.0f%%")
    plt.show()


def pie_chart_cate_column(data, cat_column: str):
    """
    Pie chart a categorical column
    :param data: variable
    :param cat_column: column name as string
    :return: pie chart
    """
    data[cat_column].value_counts().plot(kind="pie", colors=sns.color_palette("dark"), autopct="%1.0f%%")
    plt.show()


def contingency_table(data, cat_column: str, cat_colum_two: str):
    """
    Create contingency table
    :param data: variable
    :param cat_column: first column name as a string
    :param cat_colum_two: second column name as a string
    :return: dataframe
    """
    cross_tab_data = pd.crosstab(index=data[cat_column], columns=data[cat_colum_two], margins=True)
    return cross_tab_data

#                 ----------------  Analysis Functions  ----------------


def calculate_the_skewness(data, numerical_colum: str) -> float:
    """
    Calculate Kurtosis of a numerical variable
    :param data:variable
    :param numerical_colum:string with numerical column name
    :return:skewness value
    """
    skew = data[numerical_colum].skew()
    if skew == 0:
        print("Symmetric Column")
    elif skew > 0:
        print("Right Skewed ---> most values on the left")
    elif skew < 0:
        print("Left Skewed ---> most values on the right")
    return skew


def calculate_the_kurtosis(data, numerical_colum: str) -> float:
    """
    Calculate Kurtosis of a numerical variable
    :param data:variable
    :param numerical_colum:
    :return:kurtosis value
    """
    kurt = data[numerical_colum].kurtosis()
    if kurt == 0:
        print("Mesokurtic ---> (Normal)")
    elif kurt > 0:
        print("Leptokurtic ---> (Thin)")
    elif kurt < 0:
        print("PlatyKurtic ---> (Flat)")
    return kurt


def visualize_normal_probability_plot(data, numerical_column: str):
    """
    To find the deviation from the normal process
    :param data:variable
    :param numerical_column:string with numerical column name
    :return: chart
    """
    fig, ax = plt.subplots(1, 2, figsize=(12, 7))
    sns.histplot(data[numerical_column], kde=True, color="blue", ax=ax[0])
    sm.ProbPlot(data[numerical_column]).qqplot(line="s", ax=ax[1])
    plt.show()


def column_summary_statistics(data, column_name: str):
    """
    Statistical report of a variable
    :param data:variable
    :param column_name:string with column name
    :return: print out statistical summary
    """
    print(data[column_name].describe())


def save_data_to_csv_file(data, filename: str):
    """
    Save the data to a csv file
    :param data: variable
    :param filename: string with file name and csv extension
    :return: updated csv data file
    """
    new_data = data.to_csv(filename, index=False)
    return new_data
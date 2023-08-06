from scipy.stats import chi2
import statsmodels.api as sm
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_selection import chi2, mutual_info_regression
import numpy as np
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split
from scipy.signal import periodogram
from sklearn.cluster import KMeans

"""

     Predictive Analysis - Answer the question (What is likely to Happen? )

     The module is divided to three parts:
     1. Regression  
     2. Forcasting 
     3. Classification  
     4. Clustering 
     Regression vs Classification
     regression algorithms are used to predict the continuous values and classification algorithms are used to
     predict/ classify the discrete values 
     *      Types of Classification Algorithms                           *     Types of Regression Algorithms 
            Logistic Regression                                                Simple Linear Regression              
            K_Nearest Neighbours                                               Multiple Linear Regression   
            Support Vector Machine                                             Polynomial Regression  
            Kernel SVM                                                         Support Vector Regression   
            Decision Tree Classification                                       Decision Tree Regression   
            Random Forest Classification and more ...                          Random Forest Regression           


"""
#                   ---------------  REGRESSION     ---------------


def calculate_slope(data, independent_column: str, predicted_column: str) -> float:
    """
    calculate slope
    :param data:variable
    :param independent_column:string
    :param predicted_column:string
    :return: slope value
    """
    if len(data[independent_column]) != len(data[predicted_column]):
        raise ValueError(f"length of {data[independent_column]} is not equal to length of{data[predicted_column]}")
    data[independent_column] = np.array(data[independent_column])
    data[predicted_column] = np.array(data[predicted_column])
    n = len(data[independent_column])
    n_sum_x_y = n * np.sum(data[independent_column] * data[predicted_column])
    sum_x_sum_y = data[independent_column].sum() * data[predicted_column].sum()
    n_sum_x_exp2 = n * np.sum(data[independent_column] ** 2)
    sum_x_exp2 = data[independent_column].sum() ** 2
    slope = (n_sum_x_y - sum_x_sum_y) / (n_sum_x_exp2 - sum_x_exp2)
    # print(f"slope : {np.round(slope, 4)}")
    return np.round(slope, 4)


def calculate_intercept_of_y(data, independent_column: str, predicted_column: str) -> float:
    """
    calculate y - intercept
    :param data:variable
    :param independent_column:string
    :param predicted_column:string
    :return: y_intercept value
    """
    if len(data[independent_column]) != len(data[predicted_column]):
        raise ValueError(f"length of {data[independent_column]} is not equal to length of{data[predicted_column]}")

    n, slope = len(data[independent_column]), calculate_slope(data, independent_column, predicted_column)
    sum_y = data[predicted_column].sum()
    m_sum_x = slope * data[independent_column].sum()
    y_intercept = (sum_y - m_sum_x) / n
    # print(f"y intercept: {np.round(y_intercept, 4)}")
    return np.round(y_intercept, 4)


def plot_linear_equation(data, independent_column: str, predicted_column: str):
    """
    Plot a linear equation
    :param data:variable
    :param independent_column:string
    :param predicted_column:string
    :return: scatter plot
    """
    slope = calculate_slope(data, independent_column, predicted_column)
    y_intercept = calculate_intercept_of_y(data, independent_column, predicted_column)
    data["predicted"] = data[independent_column].map(lambda x: slope * x + y_intercept)
    sns.scatterplot(x=independent_column, y=predicted_column, data=data)
    sns.lineplot(x=independent_column, y=data["predicted"], color="orange", lw=4, data=data)
    plt.show()


def split_data_into_training_and_test(data, independent_colum: list, dependent_column: str):
    """
    Split data to training and test 80 % train and 20 % test
    :param data:variable
    :param independent_colum:list
    :param dependent_column:string
    :return: x_train, x_test, y_train, y_test
    """
    x = data[independent_colum]
    y = data[dependent_column]
    x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.80, test_size=0.20, random_state=0)
    return x_train, x_test, y_train, y_test


def plot_polynomial_regression(data, independent_colum, dependent_column, degree: int):
    """
    implementing polynomial regression, transforming the inputs to include nonlinear terms such as X2
    depending on the case choose the right optimal degree by taking in consideration under fitting and over fitting
    for small data
    :param data:variable
    :param independent_colum:string
    :param dependent_column:list
    :param degree:integer
    :return: Polynomial Regression Plot & printing out the intercept_, coef_, R2(coefficient of determination)
    """
    series = pd.Series(data[independent_colum])
    arr = series.values
    x = arr.reshape((-1, 1))
    y = data[dependent_column]
    x_ = PolynomialFeatures(degree=degree, include_bias=False).fit_transform(x)
    model = LinearRegression().fit(x_, y)
    r_sq = model.score(x_, y)
    print(f"coefficient of determination: {r_sq}\nintercept: {model.intercept_}\ncoefficients: {model.coef_}")
    plt.scatter(x=data[independent_colum], y=data[dependent_column], color="blue")
    plt.plot(x, model.predict(x_), color="red")
    plt.title("Polynomial Regression")
    plt.xlabel(f"{independent_colum}")
    plt.ylabel(f"{dependent_column}")
    plt.show()
    return model


def multi_linear_regression(data, independent_colum: list, dependent_column: str):
    """
    implementing MLR, implement independent column as a list
    :param data:
    :param independent_colum:list
    :param dependent_column:string
    :return: MLR & printing out the intercept_, coef_, R2(coefficient of determination)
    """
    x = data[independent_colum]
    y = data[dependent_column]
    model = LinearRegression().fit(x, y)
    r_sq = model.score(x, y)
    print(f"coefficient of determination: {r_sq}\nintercept: {model.intercept_}\ncoefficients: {model.coef_}")
    return model


def print_linear_regression_summary(data, x_input: list, y_output: str):
    """

    :param data:
    :param x_input: list
    :param y_output: string
    :return:
    """
    x = sm.add_constant(data[x_input])
    model = sm.OLS(data[y_output], x)
    results = model.fit()
    print(results.summary())
    # print(f"coefficient of determination: {results.rsquared}\nadjust coefficient of determination: "
    #       f"{results.rsquared_adj}\nregression coefficients: {results.params}")


def make_mi_score(x, y):
    """
    mutual information
    :param x:
    :param y:
    :return:
    """
    for colname in x.select_dtypes(["object", "category"]):
        x[colname], _ = x[colname].factorize()
    discrete_features = [pd.api.types.is_integer_dtype(t) for t in x.dtypes]
    mi_scores = mutual_info_regression(x, y, discrete_features=discrete_features, random_state=0)
    mi_scores = pd.Series(mi_scores, name="MI Scores", index=x.columns)
    mi_scores = mi_scores.sort_values(ascending=False)
    return mi_scores


def plot_mi_scores(scores):
    """
    plot out sorted mutual score
    :param scores: variable
    :return: bar chart
    """
    scores = scores.sort_values(ascending=True)
    width = pd.Series(scores)
    ticks = scores.index
    plt.barh(width, scores)
    plt.yticks((width, ticks))
    plt.title("Mutual Information Scores")
    plt.show()

#                   ---------------  FORCASTING     ---------------


def set_index_to_date(data, date_column: str):
    data = data.set_index(date_column)
    set_index_data = pd.to_datetime(data.index, infer_datetime_format=True)
    return set_index_data


def create_date_range(start_date: str, end_date: str):
    data_sequence = pd.date_range(start=start_date, end=end_date)
    return data_sequence


def create_date_features(data, date_column: str):
    """
    create date features
    :param data: data variable
    :param date_column: string with date  column name
    :return: dataframe with date features
    """
    df = data.set_index[date_column]
    df[date_column] = pd.to_datetime(df[date_column], format="%Y-%m-%d", errors="coerce", infer_datetime_format=True)
    df["dayOfWeek"] = df.index.dayofweek
    df["Quarter"] = df.index.quarter
    df["Month"] = df.index.month
    df["Year"] = df.index.year
    df["dayOfYear"] = df.index.dayofyear
    return df


def create_hourly_feature(data, date_column: str):
    """
    create hourly features
    :param data: data variable
    :param date_column: string with date  column name
    :return: dataframe with hourly features
    """
    df = data.set_index[date_column]
    df[date_column] = pd.to_datetime(df[date_column], format="%Y-%m-%d %H:%M:%S", errors="coerce",
                                     infer_datetime_format=True)
    df["hour"] = df.index.hour
    return df


def seasonal_plot(x, y, period, freq, ax=None):
    """
    X = tunnel.copy()

    # days within a week
    X["day"] = X.index.dayofweek  # the x-axis (freq)
    X["week"] = X.index.week  # the seasonal period (period)

    # days within a year
    X["dayofyear"] = X.index.dayofyear
    X["year"] = X.index.year
    fig, (ax0, ax1) = plt.subplots(2, 1, figsize=(11, 6))
    seasonal_plot(X, y="NumVehicles", period="week", freq="day", ax=ax0)
    seasonal_plot(X, y="NumVehicles", period="year", freq="dayofyear", ax=ax1);
    """
    if ax is None:
        _, ax = plt.subplots()
    palette = sns.color_palette("husl", n_colors=x[period].nunique(), )
    ax = sns.lineplot(
        x=freq,
        y=y,
        hue=period,
        data=x,
        ci=False,
        ax=ax,
        palette=palette,
        legend=False,
    )
    ax.set_title(f"Seasonal Plot ({period}/{freq})")
    for line, name in zip(ax.lines, x[period].unique()):
        y_ = line.get_ydata()[-1]
        ax.annotate(
            name,
            xy=(1, y_),
            xytext=(6, 0),
            color=line.get_color(),
            xycoords=ax.get_yaxis_transform(),
            textcoords="offset points",
            size=14,
            va="center",
        )
    return ax


def plot_periodogram(ts, detrend='linear', ax=None):
    """
    plot_periodogram(tunnel.NumVehicles);
    """
    fs = pd.Timedelta("1Y") / pd.Timedelta("1D")
    freqencies, spectrum = periodogram(
        ts,
        fs=fs,
        detrend=detrend,
        window="boxcar",
        scaling='spectrum',
    )
    if ax is None:
        _, ax = plt.subplots()
    ax.step(freqencies, spectrum, color="purple")
    ax.set_xscale("log")
    ax.set_xticks([1, 2, 4, 6, 12, 26, 52, 104])
    ax.set_xticklabels(
        [
            "Annual (1)",
            "Semiannual (2)",
            "Quarterly (4)",
            "Bimonthly (6)",
            "Monthly (12)",
            "Biweekly (26)",
            "Weekly (52)",
            "Semiweekly (104)",
        ],
        rotation=30,
    )
    ax.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
    ax.set_ylabel("Variance")
    ax.set_title("Periodogram")
    return ax


#                   ---------------  Classification     ---------------
def chi_value_plot(data):
    """
    plot the variable importance by ch2 for binary classification
    Higher the chi value , higher the importance
    :param data:
    :return: bar chart
    """
    for col in data:
        le = LabelEncoder()
        data[col] = le.fit_transform(data[col])
    x = data.iloc[:, : -1]
    y = data.iloc[:, -1]
    # Higher the chi value , higher the importance
    chi_scores = chi2(x, y)
    chi_values = pd.Series(chi_scores[0], index=x.columns)
    chi_values.sort_values(ascending=False, inplace=True)
    chi_values.plot.bar()
    plt.show()


def p_value_plot(data):
    """
    plot the variable importance by ch2 for binary classification
    if p-value > 0.5, lower the importance
    :param data: variable
    :return: bar chart
    """
    for col in data:
        le = LabelEncoder()
        data[col] = le.fit_transform(data[col])
    x = data.iloc[:, : -1]
    y = data.iloc[:, -1]
    # if p-value > 0.5, lower the importance
    chi_scores = chi2(x, y)
    chi_values = pd.Series(chi_scores[1], index=x.columns)
    chi_values.sort_values(ascending=False, inplace=True)
    chi_values.plot.bar()
    plt.show()


#                   ---------------  Clustering     ---------------

def number_of_cluster(scaled_features):
    """
    After scaling the features, the function choose the appropriate number of clusters
    :param scaled_features: variable
    :return: plot chart
    """
    kmean_kwargs = {
        "init": "random",
        "n_init": 10,
        "max_iter": 300,
        "random_state": 42
    }
    sse = []
    for k in range(1, 11):
        kmeans = KMeans(n_clusters=k, **kmean_kwargs)
        kmeans.fit(scaled_features)
        sse.append(kmeans.inertia_)
    plt.style.use("fivethirtyeight")
    plt.plot(range(1, 11), sse)
    plt.xticks(range(1, 11))
    plt.xlabel("Number of Clusters")
    plt.ylabel("SSE")
    plt.show()
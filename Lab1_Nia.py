import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder


# For reading database datatypes:
# file_path = 'texas.csv'
# df = pd.read_csv(file_path)
# print(df.info())

def data_wakixtva(filename):
    mylist = []
    with open(filename, newline='', encoding='utf-8') as chemi_dataset:
        my_dataset_data = csv.reader(chemi_dataset, delimiter=',')
        headers = next(my_dataset_data) 
        for row in my_dataset_data:
            mylist.append(row)
        return headers, mylist

# Task2---------------------------------
def statisticis_gamotvla(data, headers):
    df = pd.DataFrame(data, columns=headers)

    numerical_columns = ["statefip", "year", "bmprison", "wmprison", "alcohol", 
                         "income", "ur", "poverty", "black", "perc1519", "aidscapita"]
    categorical_column = "state"

    for col in numerical_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    stats_shedegi = {}

    for column in numerical_columns:
        if column in df.columns:
            stats_shedegi[column] = {
                'Total Values': df[column].count(),
                'Missing Percentage': 100 * df[column].isna().mean(),
                'Cardinality': df[column].nunique(),
                'Min': df[column].min(),
                'Max': df[column].max(),
                '1st Quartile': df[column].quantile(0.25),
                '3rd Quartile': df[column].quantile(0.75),
                'Average': df[column].mean(),
                'Median': df[column].median(),
                'Standard Deviation': df[column].std()
            }

    # Task3---------------------------------
    if categorical_column in df.columns:
        total_values = df[categorical_column].count()
        missing_percentage = 100 * df[categorical_column].isna().mean()
        cardinality = df[categorical_column].nunique()

        mode_value = df[categorical_column].mode()[0] if not df[categorical_column].mode().empty else None
        mode_frequency = df[categorical_column].value_counts().iloc[0] if not df[categorical_column].value_counts().empty else 0
        mode_percentage = 100 * mode_frequency / total_values if total_values > 0 else 0

        second_mode_value, second_mode_frequency, second_mode_percentage = None, None, None
        if df[categorical_column].nunique() > 1:
            second_mode_value = df[categorical_column].value_counts().index[1]
            second_mode_frequency = df[categorical_column].value_counts().iloc[1]
            second_mode_percentage = 100 * second_mode_frequency / total_values

        stats_shedegi[categorical_column] = {
            'Total Values': total_values,
            'Missing Percentage': missing_percentage,
            'Cardinality': cardinality,
            'Mode': mode_value,
            'Mode Frequency': mode_frequency,
            'Mode Percentage': mode_percentage,
            'Second Mode': second_mode_value,
            'Second Mode Frequency': second_mode_frequency,
            'Second Mode Percentage': second_mode_percentage
        }

    return stats_shedegi

# Task4---------------------------------
def plot_histograms_and_categorical(df):
    n = df.shape[0]
    bins = int(1 + 3.22 * np.log10(n))

    for column in df.select_dtypes(include=[np.number]).columns:
        plt.figure(figsize=(8, 6))
        plt.hist(df[column].dropna(), bins=bins, color='skyblue', edgecolor='black')
        plt.title(f"Histogram for {column}")
        plt.xlabel(column)
        plt.ylabel("Frequency")
        plt.show()

    # Task4 Bar chart for "state"---------------------------------
    categorical_column = "state"
    if categorical_column in df.columns and df[categorical_column].dtype == 'object':
        plt.figure(figsize=(12, 6))
        df[categorical_column].value_counts().plot(kind='bar', color='skyblue', edgecolor='black')
        plt.xlabel(categorical_column)
        plt.ylabel("Count")
        plt.title(f"Distribution of {categorical_column}")
        plt.xticks(rotation=45)
        plt.show()

    #Task6 - Creating box plots and histograms for numeric and categorical variables -------
    plt.figure(figsize=(12, 6))
    sns.boxplot(x=df["state"], y=df["income"], palette="coolwarm")
    plt.xlabel("State")
    plt.ylabel("Income")
    plt.title("Income Distribution by State")
    plt.xticks(rotation=90)
    plt.show()

    plt.figure(figsize=(10, 6))
    sns.histplot(df, x="poverty", hue="state", multiple="stack", bins=30, palette="viridis")
    plt.xlabel("Poverty Rate")
    plt.ylabel("Count")
    plt.title("Poverty Rate Across Different States")
    plt.legend(title="State", bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.show()

    plt.figure(figsize=(12, 6))
    sns.boxplot(x=df["state"], y=df["ur"], palette="Set2")
    plt.xlabel("State")
    plt.ylabel("Unemployment Rate")
    plt.title("Unemployment Rate by State")
    plt.xticks(rotation=90)
    plt.show()

# Task5 - Cleaning missing percentages ----------------------
def wmprison_gawmenda(df):
    column = "wmprison"

    df[column] = pd.to_numeric(df[column], errors='coerce')

    median_value = df[column].median()
    df.fillna({column: median_value}, inplace=True)

    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    df = df[(df[column] >= lower_bound) & (df[column] <= upper_bound)].copy()
    
    return df

# Task6 ---------------------------
def plot_scatter_plots(df):
    strong_pairs = [("income", "poverty"), ("bmprison", "poverty"), ("wmprison", "income")]
    weak_pairs = [("aidscapita", "statefip"), ("ur", "black"), ("year", "poverty")]

    for x, y in strong_pairs:
        plt.figure(figsize=(6, 4))
        sns.scatterplot(x=df[x], y=df[y], alpha=0.5)
        plt.title(f"Scatter Plot: {x} vs {y}")
        plt.xlabel(x)
        plt.ylabel(y)
        plt.show()

    for x, y in weak_pairs:
        plt.figure(figsize=(6, 4))
        sns.scatterplot(x=df[x], y=df[y], alpha=0.5)
        plt.title(f"Scatter Plot: {x} vs {y}")
        plt.xlabel(x)
        plt.ylabel(y)
        plt.show()

def splom_plot(df):
    selected_columns = ["income", "poverty", "bmprison", "wmprison", "ur", "aidscapita"]
    sns.pairplot(df[selected_columns])
    plt.show()


#task7------------------------------
def calculate_covariance_correlation(df):
    numeric_df = df.select_dtypes(include=[np.number])
    covariance_matrix = numeric_df.cov()
    correlation_matrix = numeric_df.corr()
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
    plt.title("Correlation Matrix")
    plt.show()
    
    return covariance_matrix, correlation_matrix


#Task8 -------------------------------
def normalize_data(df, numerical_columns):
    for col in numerical_columns:
        if col in df.columns:
            min_val = df[col].min()
            max_val = df[col].max()
            df[col] = (df[col] - min_val) / (max_val - min_val)
    return df

#Task9------------------------------------
def encode_categorical(df):
    encoder = LabelEncoder()
    df['state_encoded'] = encoder.fit_transform(df['state'])
    return df


headers, new_list = data_wakixtva('texas.csv')
df = pd.DataFrame(new_list, columns=headers)

numerical_columns = ["statefip", "year", "bmprison", "wmprison", "alcohol", 
                     "income", "ur", "poverty", "black", "perc1519", "aidscapita"]

for col in numerical_columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')

df = wmprison_gawmenda(df)
df = normalize_data(df, numerical_columns)
df = encode_categorical(df)

statistics = statisticis_gamotvla(df.values.tolist(), df.columns)

# for column, stats in statistics.items():
#     print(f"Statistics for {column}:")
#     for stat, value in stats.items():
#         print(f"  {stat}: {value}")
#     print()

# plot_histograms_and_categorical(df) ---------- for showing plot histograms and categorical 
# plot_scatter_plots(df)   ------------ for showing scatter plots
# splom_plot(df)   -------- for showing plot splom

# covariance, correlation = calculate_covariance_correlation(df)   -- for showing covariance correlation

# print(df[numerical_columns].head())


states = ['Texas', 'California', 'New York', 'Texas', 'Florida', 'California']

encoder = LabelEncoder()

encoded_states = encoder.fit_transform(states)
print("Original States:", states)
print("Encoded States:", encoded_states)

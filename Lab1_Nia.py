import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# For reading database datatypes:
# file_path = 'texas.csv'
# df = pd.read_csv(file_path)
# print(df.info())

def load_data(filename):
    mylist = []
    with open(filename, newline='', encoding='utf-8') as my_dataset:
        my_dataset_data = csv.reader(my_dataset, delimiter=',')
        headers = next(my_dataset_data) 
        for row in my_dataset_data:
            mylist.append(row)
        return headers, mylist

# Task2---------------------------------
def calculate_statistics(data, headers):
    df = pd.DataFrame(data, columns=headers)

    numerical_columns = ["statefip", "year", "bmprison", "wmprison", "alcohol", 
                         "income", "ur", "poverty", "black", "perc1519", "aidscapita"]
    categorical_column = "state"

    for col in numerical_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    stats_result = {}

    for column in numerical_columns:
        if column in df.columns:
            stats_result[column] = {
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

        stats_result[categorical_column] = {
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

    return stats_result

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

    # Task4 Bar chart for state---------------------------------
    categorical_column = "state"
    if categorical_column in df.columns and df[categorical_column].dtype == 'object':
        plt.figure(figsize=(12, 6))
        df[categorical_column].value_counts().plot(kind='bar', color='skyblue', edgecolor='black')
        plt.xlabel(categorical_column)
        plt.ylabel("Count")
        plt.title(f"Distribution of {categorical_column}")
        plt.xticks(rotation=45)
        plt.show()

#Task5 - Cleaning missing percentages ----------------------
def clean_wmprison(df):
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

headers, new_list = load_data('texas.csv')
df = pd.DataFrame(new_list, columns=headers)

numerical_columns = ["statefip", "year", "bmprison", "wmprison", "alcohol", 
                     "income", "ur", "poverty", "black", "perc1519", "aidscapita"]

for col in numerical_columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')

df = clean_wmprison(df)

statistics = calculate_statistics(df.values.tolist(), df.columns)

for column, stats in statistics.items():
    print(f"Statistics for {column}:")
    for stat, value in stats.items():
        print(f"  {stat}: {value}")
    print()

# plot_histograms_and_categorical(df)

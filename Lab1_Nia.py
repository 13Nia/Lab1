import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#For reading database datatypes:
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

#Task2------------------------------------

def calculate_statistics(data, headers):
    df = pd.DataFrame(data, columns=headers)
    
    numerical_columns = ["rowname", "statefip", "year", "bmprison", "wmprison", "alcohol", "income", "ur", "poverty", "black", "perc1519", "aidscapita"]
    
    for col in numerical_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    categorical_column = "state"
    
    stats_result = {}
    
    for column in numerical_columns:
        if column in df.columns:
            total_values = df[column].count()
            missing_percentage = 100 * df[column].isna().mean()
            cardinality = df[column].nunique()
            min_value = df[column].min()
            max_value = df[column].max()
            first_quantile = df[column].quantile(0.25)
            third_quantile = df[column].quantile(0.75)
            mean = df[column].mean()
            median = df[column].median()
            std_dev = df[column].std()

            stats_result[column] = {
                'Total Values': total_values,
                'Missing Percentage': missing_percentage,
                'Cardinality': cardinality,
                'Min': min_value,
                'Max': max_value,
                '1st Quartile': first_quantile,
                '3rd Quartile': third_quantile,
                'Average': mean,
                'Median': median,
                'Standard Deviation': std_dev
            }
    
    #Task3-------------------------------------------------

    if categorical_column in df.columns:
        total_values = df[categorical_column].count()
        missing_percentage = 100 * df[categorical_column].isna().mean()
        cardinality = df[categorical_column].nunique()
        
        mode_value = df[categorical_column].mode()[0] if not df[categorical_column].mode().empty else None
        mode_frequency = df[categorical_column].value_counts().iloc[0] if not df[categorical_column].value_counts().empty else 0
        mode_percentage = 100 * mode_frequency / total_values if total_values > 0 else 0

        second_mode_value = None
        second_mode_frequency = None
        second_mode_percentage = None

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

#Task4-----------------------------------
def plot_histograms(df):
    n = df.shape[0]
    bins = int(1 + 3.22 * np.log10(n))

    for column in df.columns:
        if df[column].dtype in [np.float64, np.int64]:
            plt.figure(figsize=(8, 6))
            plt.hist(df[column].dropna(), bins=bins, color='skyblue', edgecolor='black')
            plt.title(f"Histogram for {column}")
            plt.xlabel(column)
            plt.ylabel("Frequency")
            plt.show()


headers, new_list = load_data('texas.csv')

df = pd.DataFrame(new_list, columns=headers)

for col in df.columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')

statistics = calculate_statistics(new_list, headers)

# for column, stats in statistics.items():
#     print(f"Statistics for {column}:")
#     for stat, value in stats.items():
#         print(f"  {stat}: {value}")
#     print()

plot_histograms(df)

\

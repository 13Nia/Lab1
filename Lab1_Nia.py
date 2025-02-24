import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def load_data(filename):
    mylist = []
    with open(filename) as my_dataset:
        my_dataset_data = csv.reader(my_dataset, delimiter=',')
        headers = next(my_dataset_data)
        for row in my_dataset_data:
            mylist.append(row)
        return headers, mylist

new_list = load_data('texas.csv')

for row in new_list:
    print(row)

#Task2/3------------------------------------------------------------

def calculate_statistics(data, headers):
    df = pd.DataFrame(data, columns=headers)
    df = df.apply(pd.to_numeric, errors='coerce')

    df = df.dropna(axis=1, how='all')

    stats_task2 = {}
    for column in df.columns:
        if df[column].dtype in [np.float64, np.int64]:
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

            stats_task2[column] = {
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

    for column in df.columns:
        if df[column].dtype == object:
            total_values = df[column].count()
            missing_percentage = 100 * df[column].isna().mean()
            cdardinality = df[column].nunique()

            mode_value = df[column].mode().iloc[0]
            mode_frequency = df[column].value_counts().iloc[0]
            mode_percentage = 100 * mode_frequency / total_values

            if df[column].nunique() > 1:
                    second_mode_value = df[column].mode().iloc[1]
                    second_mode_frequency = df[column].value_counts().iloc[1]
                    second_mode_percentage = 100 * second_mode_frequency / total_values
            else:
                    second_mode_value = None
                    second_mode_frequency = None
                    second_mode_percentage = None

            stats_task2[column] = {
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
    return stats_task2

    
#Task4---------------------------------------------------------
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

statistics = calculate_statistics(new_list, headers)

plot_histograms(df)


for column, stats in statistics.items():
    print(f"Statistics for {column}:")
    for stat, value in stats.items():
        print(f"  {stat}: {value}")
    print()

#---------------------------------------------------------


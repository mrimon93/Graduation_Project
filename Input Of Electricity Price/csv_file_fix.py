#Second Code, Harmonize the CSV file and Create a new one with the Harmonized Data

import pandas as pd

# read the CSV file into a pandas dataframe
importing_name = input('Import the name of your CSV-file: ')
df = pd.read_csv(f"{importing_name}.csv", delimiter=";", header=None, names=['Index', 'Timestamp', 'PriceArea', 'SpotPriceEUR'], skiprows=[0])

# drop the 'Index' column
df = df.drop('Index', axis=1)

# Sort the DataFrame in descending order based on a specific column
df.sort_values(by='Timestamp', ascending=True, inplace=True)

# save the sorted dataframe to a new CSV file
new_user = input('Enter the name for the new file: ')
df.to_csv(f'{new_user}.csv', index=False)

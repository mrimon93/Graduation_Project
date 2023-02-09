#%%
import os
import pandas as pd

cwd = os.getcwd()
# print(cwd)
target_folder = os.path.join(cwd, 'data_w/target/')
# print(target_folder)
targets = os.listdir(target_folder)
wind_targets = [x for x in targets if x.endswith('4.csv')]
temp_targets = [x for x in targets if x.endswith('1.csv')]
# print(targets)

# stations = [63510, # 63510
#             66110, # 66110
#             62260, # 62260
#             52240] # 52240

#%%
## OK
def average_wind(stations:list):
    '''Search in 'data_el/target/ folder'   \n
    Adds prefix: 'average_'                 \n
    Saves into 'data_w/final_avg/' folder.'''
    
    stations.sort()

    df1 = pd.read_csv(target_folder + stations[0], low_memory=False)
    df2 = pd.read_csv(target_folder + stations[1])
    df3 = pd.read_csv(target_folder + stations[2])
    df4 = pd.read_csv(target_folder + stations[3])

    # #merge dataframes using the average of the wind speed of each station
    df5 = pd.merge(df1, df2, on='Timestamp', how='inner')
    df6 = pd.merge(df3, df4, on='Timestamp', how='inner')
    df7 = pd.merge(df5, df6, on='Timestamp', how='inner')

    df7['Vindhastighet AVG'] = df7[['Vindhastighet_x_x', 'Vindhastighet_y_x', 'Vindhastighet_x_y', 'Vindhastighet_y_y']].mean(axis=1)
    df7 = df7.drop(['Vindhastighet_x_x', 'Vindhastighet_y_x', 'Vindhastighet_x_y', 'Vindhastighet_y_y'], axis=1)
    
    df7.to_csv('data_w/final_avg/average_wind.csv', sep=';', index=False)
    # print(df7)

average_wind(wind_targets)

#%%
## OK
def average_temp(stations:list):
    '''Search in 'data_el/target/ folder'   \n
    Adds prefix: 'average_'                 \n
    Saves into 'data_w/final_avg/' folder.'''
    stations.sort()

    df1 = pd.read_csv(target_folder + stations[0], low_memory=False)
    df2 = pd.read_csv(target_folder + stations[1])
    df3 = pd.read_csv(target_folder + stations[2])
    df4 = pd.read_csv(target_folder + stations[3])

    #First merge the dataframe on the timestamp. Then calculate the average temperature across all dataframes, and keep only one row per timestamp
    df5 = pd.merge(df1, df2, on='Timestamp', how='inner')
    df6 = pd.merge(df3, df4, on='Timestamp', how='inner')
    df7 = pd.merge(df5, df6, on='Timestamp', how='inner')

    df7['Lufttemperatur AVG'] = df7[['Lufttemperatur_x_x', 'Lufttemperatur_y_x', 'Lufttemperatur_x_y', 'Lufttemperatur_y_y']].mean(axis=1)
    df7 = df7.drop(['Lufttemperatur_x_x', 'Lufttemperatur_y_x', 'Lufttemperatur_x_y', 'Lufttemperatur_y_y'], axis=1)

    df7.to_csv('data_w/final_avg/average_temp.csv', sep=';', index=False)

average_temp(temp_targets)

#%%
## OK
def merge_weather_and_prices(wind_file, temp_file, price_file):
    '''Searches in 'data_el/harmonized' folder for 'price_file'             \n
    Searches in 'data_w/final_avg' folder for 'wind_file' and 'temp_file'   \n
    Saves into: 'data_el/'
    '''

    df1 = pd.read_csv('data_w/final_avg/' + wind_file, sep=';')      #WIND
    df2 = pd.read_csv('data_w/final_avg/' + temp_file, sep=';')      #TEMP
    df3 = pd.read_csv('data_el/harmonized/' + price_file, sep=';')   #PRICES

    #merge dataframes on timestamp using df3 as base
    df1['Timestamp'] = pd.to_datetime(df1['Timestamp'], format='%Y-%m-%d %H:%M')
    df2['Timestamp'] = pd.to_datetime(df2['Timestamp'], format='%Y-%m-%d %H:%M')
    df3['Timestamp'] = pd.to_datetime(df3['Timestamp'], format='%Y-%m-%d %H:%M')

    df = pd.merge(df3, df1, on='Timestamp', how='inner')
    df = pd.merge(df, df2, on='Timestamp', how='inner')
    
    df.to_csv('elpriser_och_vader.csv', sep=';', index=False)

merge_weather_and_prices(
    'average_wind.csv',
    'average_temp.csv',
    'harmonized_el_prices.csv')

#%%
## OK
def find_and_fill_missing_data():

    df = pd.read_csv('elpriser_och_vader.csv', sep=';', low_memory=False)
    
    #fill missing data
    mean_wind = df['Vindhastighet AVG'].mean()
    mean_temp = df['Lufttemperatur AVG'].mean()
    
    df['Lufttemperatur AVG'] = df['Lufttemperatur AVG'].fillna(mean_temp)
    df['Vindhastighet AVG'] = df['Vindhastighet AVG'].fillna(mean_wind)

    df.to_csv('nonull_elpriser_och_vader.csv', sep=';', index=False)

find_and_fill_missing_data()

#%%
## Might not be needed, find_and_fill_missing_data(): should handel missing values.
def find_duplicates(File):
    df = pd.read_csv(File, sep=';', low_memory=False)
    print(df)
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%Y-%m-%d %H:%M')
    df = df.set_index('Timestamp')
    df = df[df.index.duplicated()]
    print(df)

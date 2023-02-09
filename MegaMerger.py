#%%
import os
import pandas as pd

cwd = os.getcwd()
# print(cwd)
trgt_folder = os.path.join(cwd, 'data_w/target/')
# print(target_folder)
targets = os.listdir(trgt_folder)
wind_targets = [x for x in targets if x.endswith('4.csv')]
temp_targets = [x for x in targets if x.endswith('1.csv')]


#%%
## OK
def calculate_averages(stations:list):
    '''Calculates average on both wind and temperature. \n
    Search in 'data_w/target/ folder'                   \n
    Adds suffix: '_AVG'                                 \n
    Saves into 'data_w/final_avg/' folder.              \n
    Parameter:
    ----------
        sations : list
    ----------
    '''

    target_folder = os.path.join(cwd, 'data_w/target/')
    dfs = []

    stations.sort()
    for i in range(len(stations)):
        df = pd.read_csv(target_folder + stations[i], low_memory=False)
        dfs.append(df)

    # df1 = pd.read_csv(target_folder + stations[0], low_memory=False)
    # df2 = pd.read_csv(target_folder + stations[1])
    # df3 = pd.read_csv(target_folder + stations[2])
    # df4 = pd.read_csv(target_folder + stations[3])

    dfs_merged = []
    for i in range(len(dfs)):
        if i in range(0, 100, 4):
            if i > len(dfs)-3:
                pass

            else:
                dfm1 = pd.merge(dfs[i], dfs[i+2], on='Timestamp', how='inner')
                dfm2 = pd.merge(dfs[i+1], dfs[i+3], on='Timestamp', how='inner')

                dfs_merged.append(dfm1)
                dfs_merged.append(dfm2)

    df_temp = pd.merge(dfs_merged[0], dfs_merged[2], on='Timestamp', how='inner')
    df_wind = pd.merge(dfs_merged[1], dfs_merged[3], on='Timestamp', how='inner')
   
    # # #merge dataframes using the average of the wind speed of each station
    # df5 = pd.merge(df1, df2, on='Timestamp', how='inner')
    # df6 = pd.merge(df3, df4, on='Timestamp', how='inner')
    # df7 = pd.merge(df5, df6, on='Timestamp', how='inner')
    
    df_temp[f'{df_temp.columns[1][:-4]} AVG'] = df_temp[df_temp.columns[1:]].mean(axis=1)
    df_wind[f'{df_wind.columns[1][:-4]} AVG'] = df_wind[df_wind.columns[1:]].mean(axis=1)

    # df7['Vindhastighet AVG'] = df7[df7.columns[1:]].mean(axis=1)
    # print(df7.columns[1:-1])
    
    dfc_temp = df_temp.drop(df_temp.columns[1:-1], axis=1).copy()
    dfc_wind = df_wind.drop(df_wind.columns[1:-1], axis=1).copy()
    # df8 = df7.drop(df7.columns[1:-1], axis=1)
    # print(df8)
    print(dfc_temp)
    print(dfc_wind)
    # df8.to_csv('data_w/final_avg/average_wind.csv', sep=';', index=False)
    # print(df7)
    dfc_temp.to_csv(f'data_w/final_avg/{df_temp.columns[1][:-4]}_AVG.csv', sep=';', index=False)
    dfc_wind.to_csv(f'data_w/final_avg/{dfc_wind.columns[1][:-4]}_AVG.csv', sep=';', index=False)

# average_wind(wind_targets)
calculate_averages(targets)

#%%
## OK but nod needed
def average_temp(stations:list):
    '''Search in 'data_el/target/ folder'   \n
    Adds prefix: 'average_'                 \n
    Saves into 'data_w/final_avg/' folder.'''
    target_folder = os.path.join(cwd, 'data_w/target/')
    stations.sort()

    df1 = pd.read_csv(target_folder + stations[0], low_memory=False)
    df2 = pd.read_csv(target_folder + stations[1])
    df3 = pd.read_csv(target_folder + stations[2])
    df4 = pd.read_csv(target_folder + stations[3])

    #First merge the dataframe on the timestamp. Then calculate the average temperature across all dataframes, and keep only one row per timestamp
    df5 = pd.merge(df1, df2, on='Timestamp', how='inner')
    df6 = pd.merge(df3, df4, on='Timestamp', how='inner')
    df7 = pd.merge(df5, df6, on='Timestamp', how='inner')
    print(df7.columns[1:])
    df7['Lufttemperatur AVG'] = df7[['Lufttemperatur_x_x', 'Lufttemperatur_y_x', 'Lufttemperatur_x_y', 'Lufttemperatur_y_y']].mean(axis=1)
    df7 = df7.drop(['Lufttemperatur_x_x', 'Lufttemperatur_y_x', 'Lufttemperatur_x_y', 'Lufttemperatur_y_y'], axis=1)

    df7.to_csv('data_w/final_avg/average_temp.csv', sep=';', index=False)

# average_temp(temp_targets)

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
    'Vindhastighet_AVG.csv',
    'Lufttemperatur_AVG.csv',
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

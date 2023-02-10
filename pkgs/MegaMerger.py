import os
import pandas as pd


class MegaMerger:
    '''Methods:
    ----------
        calculate_averages(stations : list)                         \n
        merge_weather_and_prices(wind_file, temp_file, price_file)  \n
        find_and_fill_missing_data()
        '''

    def __init__(self):
        pass

    def calculate_averages(self, stations:list):
        '''Calculates average on both wind and temperature. \n
        Search in 'data_w/target/ folder'                   \n
        Adds suffix: '_AVG'                                 \n
        Saves into 'data_w/final_avg/' folder.              \n
        Parameter:
        ----------
            stations : list
        ----------
        '''
        cwd           = os.getcwd()
        target_folder = os.path.join(cwd, 'data_w/target/')
        dfs = []

        stations.sort()
        for i in range(len(stations)):
            df = pd.read_csv(target_folder + stations[i], low_memory=False)
            dfs.append(df)

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

        df_temp[f'{df_temp.columns[1][:-4]} AVG'] = df_temp[df_temp.columns[1:]].mean(axis=1)
        df_wind[f'{df_wind.columns[1][:-4]} AVG'] = df_wind[df_wind.columns[1:]].mean(axis=1)

        dfc_temp = df_temp.drop(df_temp.columns[1:-1], axis=1).copy()
        dfc_wind = df_wind.drop(df_wind.columns[1:-1], axis=1).copy()

        dfc_temp.to_csv(f'data_w/final_avg/{df_temp.columns[1][:-4]}_AVG.csv', sep=';', index=False)
        dfc_wind.to_csv(f'data_w/final_avg/{dfc_wind.columns[1][:-4]}_AVG.csv', sep=';', index=False)


    def merge_weather_and_prices(self, wind_file, temp_file, price_file):
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

        df.to_csv('data_el/merged/elpriser_och_vader.csv', sep=';', index=False)


    def find_and_fill_missing_data(self):

        df = pd.read_csv('data_el/merged/elpriser_och_vader.csv', sep=';', low_memory=False)

        #fill missing data
        mean_wind = df['Vindhastighet AVG'].mean()
        mean_temp = df['Lufttemperatur AVG'].mean()

        df['Lufttemperatur AVG'] = df['Lufttemperatur AVG'].fillna(mean_temp)
        df['Vindhastighet AVG'] = df['Vindhastighet AVG'].fillna(mean_wind)

        df.to_csv('data_el/merged/nonull_elpriser_och_vader.csv', sep=';', index=False)
        print('Done @: data_el/merged/nonull_elpriser_och_vader.csv')


if __name__ == '__main__':
    cwd         = os.getcwd()
    trgt_folder = os.path.join(cwd, 'data_w/target/')
    targets     = os.listdir(trgt_folder)

    mm = MegaMerger()
    mm.calculate_averages(targets)
    mm.merge_weather_and_prices(
        'Vindhastighet_AVG.csv',
        'Lufttemperatur_AVG.csv',
        'harmonized_el_prices.csv')

    mm.find_and_fill_missing_data()
    pass

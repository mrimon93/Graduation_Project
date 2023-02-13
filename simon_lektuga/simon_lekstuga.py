import requests
import pandas as pd
import datetime as dt
import functools as ft


Start_date = "2021-10-31 00:00"####FIXA DATUM, IDIOT
end_date = "2022-11-01 00:00"


SE_Area = "SE4"
params = ["1", "4"]

stations = [63510,
            66110,
            62260,
            52240]

station1 = 63510
station2 = 66110
station3 = 62260
station4 = 52240


files = ['weather52240param1.csv',
         'weather52240param4.csv',
         'weather62260param1.csv',
         'weather62260param4.csv',
         'weather63510param1.csv',
         'weather63510param4.csv',
         'weather66110param1.csv',
         'weather66110param4.csv']


# url2 = f"https://opendata-download-metobs.smhi.se/api/version/1.0/parameter/{params}/station/{stations}/period/corrected-archive/data.csv"

# url1 = f"https://api.energidataservice.dk/dataset/Elspotprices/download?format=json?offset=0&start={Start_date}T00:00&end={end_date}T00:00&filter=%7B%22PriceArea%22:[%22{SE_Area}%22]%7D&sort=HourUTC%20DESC&timezone=dk"


def get_data_prices(Start_date, end_date, SE_Area):
    url1 = f"https://api.energidataservice.dk/dataset/Elspotprices/download?format=json?offset=0&start={Start_date[:10]}T00:00&end={end_date[:10]}T00:00&filter=%7B%22PriceArea%22:[%22{SE_Area}%22]%7D&sort=HourUTC%20DESC&timezone=dk"
    response = requests.get(url1)
    if response.status_code == 200:
        new_one = requests.get(url1)
        data = new_one.json()
        df = pd.DataFrame(data)
        df.to_json("elpriser_raw.json", index=True, orient='records')
    else:
        print("Error")

def get_data_weather(station, param):
    url2 = f"https://opendata-download-metobs.smhi.se/api/version/1.0/parameter/{param}/station/{station}/period/corrected-archive/data.csv"
    response = requests.get(url2)
    if response.status_code == 200:
        df = pd.read_csv(url2,skiprows=9, sep=';', low_memory=False)
        df.to_csv(f"weather{station}param{param}.csv", sep= ';',index=False)

def clean_elpriser(File_elpriser):
    df = pd.read_json(File_elpriser)
    df = df.drop(['HourUTC', 'SpotPriceDKK'], axis=1)
    df['HourDK'] = df['HourDK'].str[:16]
    df['HourDK'] = df['HourDK'].str.replace('T', ' ')
    df = df.rename(columns={'HourDK': 'Timestamp'})
    #sort by timestamp ascending
    #drop duplicates
    df = df.drop_duplicates(subset=['Timestamp'], keep='first')
    df = df.sort_values(by=['Timestamp'])
    df.to_csv('elpriser_harmoniserade.csv', sep=';', index=False)

def clean_weather(File_weather_raw, Start_date, end_date):
    df = pd.read_csv(File_weather_raw, sep=';', low_memory=False)
    df['Timestamp'] = df['Datum'] + ' ' + df['Tid (UTC)'].str[:5]
    df = df.drop(['Datum', 'Tid (UTC)'], axis=1)
    if "param1" in File_weather_raw:
        df = df[['Timestamp', 'Lufttemperatur',  'Kvalitet', 'Tidsutsnitt:']]
    elif "param4" in File_weather_raw:
        df = df[['Timestamp', 'Vindhastighet',  'Kvalitet', 'Tidsutsnitt:']]
    df = df.drop(['Kvalitet', 'Tidsutsnitt:'], axis=1)
    #change below to keep only a one year period between specified dates
    df = df[(df['Timestamp'] >= Start_date) & (df['Timestamp'] <= end_date)]
    df.to_csv( 'harmonised' +File_weather_raw, sep=';', index=False)



def join_vader_prices(wind, temp, prices):
    df1 = pd.read_csv(wind, sep=';') #WIND
    df2 = pd.read_csv(temp, sep=';') #TEMP
    df3 = pd.read_csv(prices, sep=';')#PRICES
    #merge dataframes on timestamp using df3 as base
    df1['Timestamp'] = pd.to_datetime(df1['Timestamp'], format='%Y-%m-%d %H:%M')
    df2['Timestamp'] = pd.to_datetime(df2['Timestamp'], format='%Y-%m-%d %H:%M')
    df3['Timestamp'] = pd.to_datetime(df3['Timestamp'], format='%Y-%m-%d %H:%M')
    df = pd.merge(df3, df1, on='Timestamp', how='inner')
    df = pd.merge(df, df2, on='Timestamp', how='inner')
    
    df.to_csv('elpriser_och_vader.csv', sep=';', index=False)

def average_wind(station1, station2, station3, station4):
    df1 = pd.read_csv(f'harmonisedweather{station1}param4.csv', sep=';', low_memory=False)
    df2 = pd.read_csv(f'harmonisedweather{station2}param4.csv', sep=';')
    df3 = pd.read_csv(f'harmonisedweather{station3}param4.csv', sep=';')
    df4 = pd.read_csv(f'harmonisedweather{station4}param4.csv', sep=';')
    #merge dataframes using the average of the wind speed of each station
    df5 = pd.merge(df1, df2, on='Timestamp', how='inner')
    df6 = pd.merge(df3, df4, on='Timestamp', how='inner')
    df7 = pd.merge(df5, df6, on='Timestamp', how='inner')
    df7['Vindhastighet AVG'] = df7[['Vindhastighet_x_x', 'Vindhastighet_y_x', 'Vindhastighet_x_y', 'Vindhastighet_y_y']].mean(axis=1)
    df7 = df7.drop(['Vindhastighet_x_x', 'Vindhastighet_y_x', 'Vindhastighet_x_y', 'Vindhastighet_y_y'], axis=1)
    df7.to_csv('average_wind.csv', sep=';', index=False)

def average_temp(station1, station2, station3, station4):
    df1 = pd.read_csv(f'harmonisedweather{station1}param1.csv', sep=';', low_memory=False)
    df2 = pd.read_csv(f'harmonisedweather{station2}param1.csv', sep=';')
    df3 = pd.read_csv(f'harmonisedweather{station3}param1.csv', sep=';')
    df4 = pd.read_csv(f'harmonisedweather{station4}param1.csv', sep=';')
    #First merge the dataframe on the timestamp. Then calculate the average temperature across all dataframes, and keep only one row per timestamp
    df5 = pd.merge(df1, df2, on='Timestamp', how='inner')
    df6 = pd.merge(df3, df4, on='Timestamp', how='inner')
    df7 = pd.merge(df5, df6, on='Timestamp', how='inner')
    df7['Lufttemperatur AVG'] = df7[['Lufttemperatur_x_x', 'Lufttemperatur_y_x', 'Lufttemperatur_x_y', 'Lufttemperatur_y_y']].mean(axis=1)
    df7 = df7.drop(['Lufttemperatur_x_x', 'Lufttemperatur_y_x', 'Lufttemperatur_x_y', 'Lufttemperatur_y_y'], axis=1)
    #drop duplicates

    df7.to_csv('average_temp.csv', sep=';', index=False)



def find_and_fill_missing_data():
    df = pd.read_csv('elpriser_och_vader.csv', sep=';', low_memory=False)
    #fill missing data
    mean_wind = df['Vindhastighet AVG'].mean()
    mean_temp = df['Lufttemperatur AVG'].mean()
    df['Lufttemperatur AVG'] = df['Lufttemperatur AVG'].fillna(mean_temp)
    df['Vindhastighet AVG'] = df['Vindhastighet AVG'].fillna(mean_wind)
    df.to_csv('elpriser_och_vader.csv', sep=';', index=False)







def find_duplicates(File):
    df = pd.read_csv(File, sep=';', low_memory=False)
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%Y-%m-%d %H:%M')
    df = df.set_index('Timestamp')
    df = df[df.index.duplicated()]
    print(df)


get_data_prices(Start_date, end_date, SE_Area)


for station in stations:
    for param in params:
        get_data_weather(station, param)

clean_elpriser('elpriser_raw.json')

for file in files:
    clean_weather(file, Start_date, end_date)

average_wind(station1, station2, station3, station4)

average_temp(station1, station2, station3, station4)

join_vader_prices('average_temp.csv', 'average_wind.csv', 'elpriser_harmoniserade.csv')


find_and_fill_missing_data()
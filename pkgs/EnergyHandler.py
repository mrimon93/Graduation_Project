import requests
import pandas as pd


class EnergyHandler:
    '''Get, Save raw data. Then Clean the data'''

    def __init__(self):
        pass

    def get_data(self, start_date, end_date, se_area):
        '''Get data from:   start date, end date, se_area       \n
        se_area examples: SE1, SE2, SE3, SE4. (For now only SE4)\n 
        https://api.energidataservice.dk/dataset/Elspotprices   \n
        Saves into 'data_el/raw/' folder as 'raw_el_prices.json' '''

        url = f'https://api.energidataservice.dk/dataset/Elspotprices' + \
            f'/download?format=json?offset=0&start={start_date[:10]}' + \
                f'T00:00&end={end_date[:10]}T00:00&filter=%7B%22PriceArea%22:' + \
                    f'[%22{se_area}%22]%7D&sort=HourUTC%20DESC&timezone=dk'

        response = requests.get(url)

        if response.status_code == 200:
            new_one = requests.get(url)
            data    = new_one.json()
            df      = pd.DataFrame(data)

            df.to_json("data_el/raw/raw_el_prices.json", index = True, orient='records')
        
        else:
            print("Error: get_data_prices()")


    def clean_price_data(self, raw_file):
        '''Searches in 'data_el/raw/' folder.      \n
        Saves into 'data_el/harmonized/ folder.'   '''

        df = pd.read_json('data_el/raw/' + raw_file)
        df = df.drop(['HourUTC', 'SpotPriceDKK'], axis=1)

        df['HourDK'] = df['HourDK'].str[:16]
        df['HourDK'] = df['HourDK'].str.replace('T', ' ')

        df = df.rename(columns={'HourDK': 'Timestamp'})
        df = df.drop_duplicates(subset=['Timestamp'], keep='first')
        df = df.sort_values(by=['Timestamp'])

        name_harmonized = \
            f'{raw_file}'.replace('raw', 'harmonized').replace('.json', '.csv')

        df.to_csv(f'data_el/harmonized/{name_harmonized}', sep = ';', index = False)


if __name__ == '__main__':
    start_date = '2021-11-01 00:00'
    end_date   = '2022-11-01 00:00'

    SE_AREA = "SE4"
    params  = ["1", "4"]

    stations = [63510,
                66110,
                62260,
                52240]
    
    EnergyHandler().get_data(start_date, end_date, SE_AREA)
    EnergyHandler().clean_price_data('raw_el_prices.json')
    
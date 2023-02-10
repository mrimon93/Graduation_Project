import requests
import pandas as pd

class HandleSMHI:
    '''Handle .csv files from SMHI.                 \n
    Download, clean and filter by dates.            \n
    --------                                        
    Methods:                                        
    --------                                        
        get_raw_csv(name, station_id, parameter)    \n
        clean_csv(filename)                         \n
        get_data_between(start_date, end_date, filename)
    '''

    def __init__(self):
        pass

    def get_raw_csv(self, name:str, station_id:int, parameter:int):
        ''''Save to "data_w/raw" folder.                \n
        Endpoint entry at:                              \n
        https://opendata-download-metobs.smhi.se/api/   \n
        Parameters:                           
        ----------
            name : str
            station_id : int
            parameter : int
        '''

        endpoint_entry = \
            'https://opendata-download-metobs.smhi.se/api/'
    
        download_url = endpoint_entry + \
            f'version/1.0/parameter/{parameter}/' + \
            f'station/{station_id}/period/corrected-archive/data.csv'
        
        re = requests.get(download_url)
        
        try:
            with open(f'data_w/raw/{name}_{station_id}_{parameter}.csv',
                'w', encoding='utf-8-sig') as out:
                    out.write(re.text)
                    return 1
                    
        except:
            return 0

    def clean_csv(self, filename:str):
        '''Clear all unwanted columns and rows  \n
        saves to "data_w/clean" folder          \n
        ----------
        Parameters:
        ----------
            filename : str
        '''

        df = pd.read_csv('data_w/raw/' + 
            f'{ filename }',
            delimiter  = ';',
            skiprows   = 9,
            index_col  = False,
            low_memory = False)
    
        dfc = df[df.columns[:3]].copy()
        dfc['Timestamp'] = df['Datum'] + ' ' + df['Tid (UTC)'].str[:5]

        dfc = dfc.drop(['Datum', 'Tid (UTC)'], axis = 1)
        dfcc = dfc[[dfc.columns[1], dfc.columns[0]]]

        return dfcc.to_csv('data_w/clean/' + f'clean_{ filename }', index = False)


    def get_data_between(self, start_date:str, end_date:str, filename:str):
        '''Searches in 'data_w/clean/' folder.                      \n
        Save data between two dates into "data_w/target" folder.    \n
        Valid date format: '2021-11-01'                             \n
        ----------
        Parameters:
        ----------
            start_date : str
            end_date : str
            filename : str
        '''

        df  = pd.read_csv('data_w/clean/' + filename, index_col = 'Timestamp')
        dfc = df.loc[start_date:end_date]

        try:
            dfc.to_csv('data_w/target/' + \
                filename.replace('clean', f'{ start_date }_{ end_date }'))
            return 1
        
        except:
            return 0


if __name__ == '__main__':
    a = HandleSMHI()
    # a.get_raw_csv('Falsterbo_A', 52240, 1)
    # a.clean_csv('Falsterbo_a_52240_1.csv')
    # a.get_data_between('2021-11-01', '2022-10-31', 'clean_Falsterbo_a_52240_1.csv')
import os
from pkgs.HandleSMHI import HandleSMHI
# from MergerSMHI import MergerSMHI

class MainSMHI:
    def __init__(self):
        pass

    def get_raw(self, parameter = 'temperature'):
        '''Works only with "temperature" and "wind" parameter   \n
        Iterates over 'data_w/station_keys.csv' '''
        
        handler       = HandleSMHI()
        weather_value = 0

        if parameter == 'wind':
            weather_value = 4

        elif parameter == 'temperature':
            weather_value = 1

        with open('pkgs/station_keys.csv', 'r', encoding = 'utf-8-sig') as station_keys:

            for line in station_keys.readlines()[1:]:
                city    = line.split(',')[0].capitalize().replace(' ', '_')
                city_id = line.split(',')[1].replace('\n', '')

                print(f"Getting .csv for:\n{ city }\nID: { city_id }")

                handler.get_raw_csv(name = city, station_id = city_id, parameter = weather_value)


    def clean_raw(self):
        '''Searches in 'data_w/raw/' folder. \n
        Saves to 'data_w/clean/' folder. '''
        
        raw_list = os.listdir('data_w/raw')
        handler  = HandleSMHI()

        for file in raw_list:
            print(f'Cleaning:', '\ndata_w/raw/' + file)
            handler.clean_csv(file)


    def save_samples(self, start_date, end_date):
        '''Searches in 'data_w/clean' folder.   \n
        Saves into "data_w/target" folder.
        '''
        clean_list = os.listdir('data_w/clean')
        handler    = HandleSMHI()

        for file in clean_list:
            handler.get_data_between(start_date, end_date, file)


if __name__ == '__main__':
    smhi = MainSMHI()
    smhi.get_raw()
    smhi.get_raw('wind')
    smhi.clean_raw()
    smhi.save_samples('2021-11-01', '2022-10-31')
    smhi.merge_samples()
    pass

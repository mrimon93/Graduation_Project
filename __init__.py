import os
from EnergyHandler import EnergyHandler
from MainSMHI import MainSMHI
from MegaMerger import MegaMerger

start_date = '2021-11-01 00:00'
end_date   = '2022-11-01 00:00'
SE_AREA = "SE4"
params  = ["1", "4"]

# Prices 
e_handle = EnergyHandler()
e_handle.get_data(start_date, end_date, SE_AREA)
e_handle.clean_price_data('raw_el_prices.json')

## Weather
smhi = MainSMHI()
smhi.get_raw()
smhi.get_raw('wind')
smhi.clean_raw()
smhi.save_samples('2021-11-01', '2022-11-01')
# smhi.merge_samples() # Not yet done


# Merger
targets = os.listdir('data_w/target/')

mm = MegaMerger()
mm.calculate_averages(targets)
mm.merge_weather_and_prices(
    'Vindhastighet_AVG.csv', 'Lufttemperatur_AVG.csv', 'harmonized_el_prices.csv')
mm.find_and_fill_missing_data()

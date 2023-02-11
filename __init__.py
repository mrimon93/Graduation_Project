import os
from tkinter import messagebox
from pkgs.EnergyHandler import EnergyHandler
from pkgs.MainSMHI import MainSMHI
from pkgs.MegaMerger import MegaMerger

start_date = '2021-11-01 00:00'
end_date   = '2022-11-01 00:00'
SE_AREA = "SE4"
params  = ["1", "4"]

start_now = messagebox.askquestion(
    'askquestion', 
    'Will fetch data from remote servers.\n'+ \
        '~100MB\nProceed anyway?')

if start_now == 'no':
    print('Exiting...')
    exit()

else:
    
    ## Make directory tree if not present
    os.system('./pkgs/make_tree.sh')

    ## Prices 
    e_handle = EnergyHandler()
    e_handle.get_data(start_date, end_date, SE_AREA)
    e_handle.clean_price_data('raw_el_prices.json')

    ## Weather
    smhi = MainSMHI()
    smhi.get_raw()
    smhi.get_raw('wind')
    smhi.clean_raw()
    smhi.save_samples('2021-11-01', '2022-11-01')

    ## Merger
    targets = os.listdir('data_w/target/')

    mm = MegaMerger()
    mm.calculate_averages(targets)
    mm.merge_weather_and_prices(
        'Vindhastighet_AVG.csv', 'Lufttemperatur_AVG.csv', 'harmonized_el_prices.csv')
    mm.find_and_fill_missing_data()

messagebox.showinfo('showinfo', 'Done!\nFile saved in:\n' + \
    'data_el/merged/\nas:\nnonull_elpriser_och_vader.csv')

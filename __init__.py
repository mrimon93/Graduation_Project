import os
from tkinter import messagebox
import pandas as pd
from pkgs import mkdirs_win
from pkgs.EnergyHandler import EnergyHandler
from pkgs.MainSMHI import MainSMHI
from pkgs.MegaMerger import MegaMerger
from Database_queries.DBWorker import DBWorker

start_date = '2021-11-01 00:00'
end_date   = '2022-11-01 00:00'
params     = ['1', '4']

SE_AREA    = 'SE4'
CURR_DIR_PATH = os.path.dirname(os.path.realpath('__file__'))

start_now = messagebox.askquestion(
    'Are you sure?', 
    'Will fetch data from remote servers.\n'+ \
        '~100MB\nProceed anyway?')

if start_now == 'no':
    print('Exiting...')
    exit()

else:

    ## Make directory tree if not present
    mkdirs_win.make_directory_tree(CURR_DIR_PATH)

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

    ## Preload data before database
    fact_df = pd.read_csv(CURR_DIR_PATH + "/data_el/merged/nonull_elpriser_och_vader.csv", sep=';')
    fact_data = ""

    for index, row in fact_df.iterrows():
        row_text = "('" + row[0] + "'," + str(row[4]) + "," + str(row[3]) + ",'" + row[1] + "'," + str(row[2]) + "),"
        fact_data = fact_data + "\n" + row_text
    fact_data = fact_data[:-1]
   
    ## Connect and do db work
    db_worker = DBWorker()
    conn = db_worker.connect_to_db()
    db_worker.write_to_fact(conn, fact_data)

messagebox.showinfo('Done!', 'File saved in:\n' + \
    'data_el/merged/\nas:\nnonull_elpriser_och_vader.csv')

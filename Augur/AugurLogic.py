import os
import calendar
from time import time
import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import StandardScaler
import currency_converter as cc
#load the model from a file

class AugurLogic:
    def __init__(self):
        pass

    
    def get_input_and_predict(self, wind, temp, month_int, hour, day_int, predict_var):
        filename = os.getcwd() + '/Augur/ML/finalized_model_weekdays.sav'
        # '/simon_lektuga/finalized_model_weekdays.sav'
        
        vindhastighet  = float(wind.get())
        lufttemperatur = float(temp.get())
        month     = int(month_int.get())
        timeofday = int(hour.get())
        weekday   = int(day_int.get())

        loaded_model = pickle.load(open(filename, 'rb'))

        #put the input into a dataframe
        df = pd.DataFrame(
            {'Vindhastighet AVG': [vindhastighet],
            'Lufttemperatur AVG': [lufttemperatur],
            'Month': [month],
            'TimeOfDay': [timeofday],
            'DayOfWeek': [weekday]})
        
        #scale the data
        X = df[['Vindhastighet AVG', 'Lufttemperatur AVG', 'Month', 'TimeOfDay', 'DayOfWeek']]
        scaler = StandardScaler()
        scaler.fit(X).transform(X)

        #make a prediction
        y_pred = loaded_model.predict(X)

        #convert from EUR per Mwh to SEK per Kwh
        c = cc.CurrencyConverter()
        y_pred = y_pred / 1000
        y_pred = y_pred * c.convert(1, 'EUR', 'SEK')
        print("The price of electricity in the future is: " + str(y_pred[0].round(2)) + " SEK per Kwh")
        
        result = 'A {} at {}:00,\n'.format(calendar.day_name[weekday], hour.get()) + \
            'in the month of\n{},\n'.format(calendar.month_name[month]) + \
                'with wind average of\n{} m / s\nand '.format(wind.get()) + \
                    'average temperature of\n{}°C\n'.format(temp.get()) + \
                        'the price should be:\n{} SEK / KWh'.format(str(y_pred.round(2)[0])) # some str var...

        # Set 'Predict: result' 
        predict_var.set(result) 

        return y_pred[0].round(2)

if __name__ == '__main__':
    au = AugurLogic()
    runnum = 0
    start_t = time()

    for i in range(0,10):
        runnum += 1
        wind  = np.random.randint(0, 14)
        temp  = np.random.randint(-10, 24)
        month = np.random.randint(1, 12)
        hour  = np.random.randint(0, 23)
        day   = np.random.randint(1, 8)
        
        print('\nTest:', runnum)
        print(f'Hour: {hour}, Temp: {temp}, Wind: {wind}, Month: {month}')

        au.get_input_and_predict(wind = wind, temp = temp, month_int = month, hour = hour, day_int = day)

    end_t = time()
    print('Executed in:', (end_t - start_t), 'seconds')

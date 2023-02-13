#Create a script that takes input from the user and uses it to predict the price of electricity in the future.
#  Load a trained model from a file and use it to make predictions. The script should take the following input from the user:
#  Vindhastighet AVG, Lufttemperatur AVG, Month, TimeOfDay. The script should then use the model to make a prediction of the price of electricity in the future.
#  The script should then print the prediction to the user.
import os
from time import time
import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import StandardScaler
import currency_converter as cc
#load the model from a file

class NewLogic:
    def __init__(self):
        pass

    
    def get_input_and_predict(self, wind:float, temp:float, month_int:int, hour:int, day_int:int):
        filename = os.getcwd() + '/Augur/ML/finalized_model_weekdays.sav'
        # '/simon_lektuga/finalized_model_weekdays.sav'
        
        vindhastighet  = float(wind)
        lufttemperatur = float(temp)
        month     = int(month_int)
        timeofday = int(hour)
        weekday   = int(day_int)

        loaded_model = pickle.load(open(filename, 'rb'))

        #put the input into a dataframe
        df = pd.DataFrame({'Vindhastighet AVG': [vindhastighet], 'Lufttemperatur AVG': [lufttemperatur], 'Month': [month], 'TimeOfDay': [timeofday], 'DayOfWeek': [weekday]})
        
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
        return y_pred[0].round(2)

if __name__ == '__main__':
    au = NewLogic()
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

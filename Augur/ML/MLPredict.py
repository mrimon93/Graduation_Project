#Create a script that takes input from the user and uses it to predict the price of electricity in the future.
#  Load a trained model from a file and use it to make predictions. The script should take the following input from the user:
#  Vindhastighet AVG, Lufttemperatur AVG, Month, TimeOfDay. The script should then use the model to make a prediction of the price of electricity in the future.
#  The script should then print the prediction to the user.

import pandas as pd
# import numpy as np
import pickle
from sklearn.preprocessing import StandardScaler
import currency_converter as cc
#load the model from a file

def get_input_and_predict(wind:float, temp:float, month:int, hour:int):
    filename = 'finalized_model.sav'
    vindhastighet = float(wind)
    lufttemperatur = float(temp)
    month_in  = int(month)
    timeofday = int(hour)

    loaded_model = pickle.load(open(filename, 'rb'))

    #put the input into a dataframe
    df = pd.DataFrame(
        {'Vindhastighet AVG': [vindhastighet],
        'Lufttemperatur AVG': [lufttemperatur],
        'Month':      [month_in],
        'TimeOfDay': [timeofday]}
    )

    #scale the data
    X = df[['Vindhastighet AVG', 'Lufttemperatur AVG', 'Month', 'TimeOfDay']]
    scaler = StandardScaler()
    scaler.fit(X).transform(X)

    #make a prediction
    y_pred = loaded_model.predict(X)

    #convert from EUR per Mwh to SEK per Kwh
    c = cc.CurrencyConverter()
    y_pred = y_pred / 1000
    y_pred = y_pred * c.convert(1, 'EUR', 'SEK')

    print("The price of electricity in the future is: " + str(y_pred.round(1)[0]) + " SEK per Kwh")

    return float(y_pred.round(1)[0]) # y_pred

if __name__ == '__main__':
    get_input_and_predict(wind = 2, temp = 12, month = 4, hour = 4)
    get_input_and_predict(wind = 2, temp = 12, month = 6, hour = 4)
    get_input_and_predict(wind = 2, temp = 12, month = 8, hour = 4)

#Create a script that takes input from the user and uses it to predict the price of electricity in the future.
#  Load a trained model from a file and use it to make predictions. The script should take the following input from the user:
#  Vindhastighet AVG, Lufttemperatur AVG, Month, TimeOfDay. The script should then use the model to make a prediction of the price of electricity in the future.
#  The script should then print the prediction to the user.

import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import StandardScaler
import currency_converter as cc
#load the model from a file

filename = 'finalized_model_weekdays.sav'



def get_input_and_predict():
    print("Enter the following information to predict the price of electricity in the future:")
    print("Vindhastighet AVG in meters per second:")
    vindhastighet = float(input())
    print("Lufttemperatur AVG:")
    lufttemperatur = float(input())
    print("Month:")
    month = int(input())
    print("TimeOfDay:")
    timeofday = int(input())
    print("DayOfWeek:")
    weekday = int(input())
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
    print("The price of electricity in the future is: " + str(y_pred) + " SEK per Kwh")
    return y_pred


get_input_and_predict()

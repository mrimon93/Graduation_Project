#%%
import calendar
import pandas as pd
import pickle
from sklearn.preprocessing import StandardScaler
import currency_converter as cc
#load the model from a file

class AugurLogic:
    def __init__(self):
        pass

    def get_input_and_predict(self, wind, temp, month, hour, predict_var):
        filename = 'finalized_model.sav'

        vindhastighet = float(wind.get())
        lufttemperatur = float(temp.get())
        month_in  = int(month.get())
        timeofday = int(hour.get())

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

        print("The price of electricity in the future is: " + str(y_pred.round(2)[0]) + " SEK per Kwh")

        
    
        result = 'At {}:00,\n'.format(hour.get()) + \
            'with wind average of\n{} m/s\nand '.format(wind.get()) + \
                'average temperature of\n{}°C\n'.format(temp.get()) + \
                    'in the month of\n{},\n'.format(calendar.month_name[month_in]) + \
                        'the price should be:\n{} SEK'.format(str(y_pred.round(2)[0])) # some str var...

        # Set 'Predict: result' 
        predict_var.set(result) 
        # args[3].set(result)

        return float(y_pred.round(2)[0]) # y_pred

    # def return_str(self, *args):
    #     month = 1
    #     if len(args) <= 0:
    #         month = int(args[2].get())
    
    #     result = 'With wind average of\n{} m/s\nand '.format(args[0].get()) + \
    #         'average temperature of\n{}°C\n'.format(args[1].get()) + \
    #             'in the month of\n{},\n'.format(calendar.month_name[month]) + \
    #                 'the price should be:\n{}'.format(args[4].get()) # some str var...

    #     # Set 'Predict: result'  
    #     args[3].set(result)

    #     return result

        
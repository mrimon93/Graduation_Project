#make a regression model of the multidemensional data from elpriser_vader.csv to make predictions of the SpotPriceEUR using Vindhastighet AVG and Lufttemperatur AVG as features.
#Test the model with the test data and evaluate the model. Plot the model in a 3d graph.

import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from scipy.stats import spearmanr
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

df = pd.read_csv('C:\code\EXJOBB\elpriser_och_vader.csv', sep=';')

#scale the data


scaler = StandardScaler()

#make to new columns with a repersentation between of month and time of day using the timestamp column

df['Month'] = pd.DatetimeIndex(df['Timestamp']).month
df['TimeOfDay'] = pd.DatetimeIndex(df['Timestamp']).hour

#Make a column with the day of the week represented as a number

df['DayOfWeek'] = pd.DatetimeIndex(df['Timestamp']).dayofweek



print(df['TimeOfDay'])
#plit the data into train and test data

X = df[['Vindhastighet AVG', 'Lufttemperatur AVG', 'Month', 'TimeOfDay', 'DayOfWeek']]
y = df['SpotPriceEUR']
scaler.fit(X).transform(X)


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)



# from sklearn.neural_network import MLPRegressor

regressor = MLPRegressor(random_state=1, max_iter=10000, hidden_layer_sizes= 500, solver="lbfgs", verbose=True, ).fit(X_train, y_train)

y_pred = regressor.predict(X_test)

print('Mean squared error: %.2f'

        % mean_squared_error(y_test, y_pred))

print('Coefficient of determination: %.2f'

        % r2_score(y_test, y_pred))




#save the model to a file



filename = 'finalized_model_weekdays.sav'

pickle.dump(regressor, open(filename, 'wb'))

#load the model from a file





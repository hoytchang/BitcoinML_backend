from sklearn.linear_model import LinearRegression
import pandas as pd
import json
import os
import numpy as np

class Model():
    def __init__(self, settings):
        self.settings = settings

    def print(self):
        print('settings = '+str(self.settings))

    def build_model(self):
        names = ['market-price', 'hash-rate', 'n-unique-addresses', 'n-transactions']

        # Read in json files
        def read_json(name):
            filename = os.path.join(os.getcwd(),'ML')
            filename = os.path.join(filename,'data')
            filename = os.path.join(filename,name+'.json')
            with open(filename, 'r') as openfile:
                json_object = json.load(openfile)
            return json_object
        data = [read_json(n) for n in names]

        # Store json data into data frame
        df = pd.DataFrame(columns = ['Time'])
        for dictionary in data:
            values = dictionary['values']
            timeList = []
            valueList = []
            for val in values:
                timeList.append(val['x'])
                valueList.append(val['y'])
            name = dictionary['name']
            data_dictionary = {'Time': timeList,
                            name: valueList}
            df_i = pd.DataFrame(data_dictionary)
            df = pd.merge(df, df_i, on='Time', how='outer')

        # Sort and impute missing data
        df = df.sort_values(by=['Time'])
        df = df.fillna(method='pad')

        # Get factor names
        columnNames = df.columns.values
        index = np.where(columnNames == "Time")
        columnNames = np.delete(columnNames, index)
        index = np.where(columnNames == 'Market Price (USD)')
        factors = np.delete(columnNames, index)
        print("factors = "+str(factors))

        # Remove NaN, and 0.0 price
        df = df.dropna()
        df = df[df['Market Price (USD)'] != 0.0]
        print('len(df) = ' + str(len(df)))

        # Build a linear regression (full data set)
        X = df[factors]
        y = df['Market Price (USD)']
        reg = LinearRegression()
        reg.fit(X,y)
        print('coef = '+str(reg.coef_))
        y_pred_linreg = reg.predict(X)

        # Build a linear regression, splitting training and test data
        df = df.reset_index()
        training_length = (len(df) * 0.9)
        df_train = df.loc[0:training_length]
        df_test = df.loc[training_length+1:len(df)]
        x_train = df_train[factors]
        y_train = df_train['Market Price (USD)']
        reg = LinearRegression()
        reg.fit(x_train,y_train)
        print('coef = '+str(reg.coef_))
        x_test = df_test[factors]
        y_pred_linreg_test = reg.predict(x_test)

        # Store predictions
        self.regression_full_data_set_x = df['Time']
        self.regression_full_data_set_y = y_pred_linreg
        self.regression_oos_x = df_test['Time']
        self.regression_oos_y = y_pred_linreg_test
        self.actual_x = df['Time']
        self.actual_y = df['Market Price (USD)']

    def predict(self):
        pred = {}
        pred['regression_full_data_set_x'] = self.regression_full_data_set_x
        pred['regression_full_data_set_y'] = self.regression_full_data_set_y
        pred['regression_oss_x'] = self.regression_oos_x
        pred['regression_oss_y'] = self.regression_oos_y
        pred['actual_x'] = self.actual_x
        pred['actual_y'] = self.actual_y
        return pred

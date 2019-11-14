import pickle
from ds import *
import pandas as pd
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn import metrics
from sklearn import ensemble
import numpy as np
import xgboost as xgb
from sklearn.impute import SimpleImputer
import csv

data_as_list = []

with open('data/out.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for idx,row in enumerate(readCSV):
        if idx==0: continue
        try:
            title_len = len(row[0])
            story_len = len(row[1])
            goal = int(row[4])
            category = row[5]
            amt_raised = int(row[3])
            data_as_list.append([title_len, story_len, goal, category, amt_raised])
        except Exception:
            continue

df = pd.DataFrame(data_as_list, columns = ["title_len", "story_len", "goal", "category", "amt_raised"])
df['category'] = pd.Categorical(df['category'])
dfDummies = pd.get_dummies(df['category'], prefix='category')
df = pd.concat([df, dfDummies], axis=1)

predictor_variable_indexes = [i for i in range(0,2+1)]
predictor_variable_indexes.extend([i for i in range(5, 23+1)])

response_variable_index = 4

X = df.iloc[:, predictor_variable_indexes].values
y = df.iloc[:, response_variable_index].values


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

#regressor = RandomForestRegressor(n_estimators=300, random_state=0, n_jobs=10, verbose=1)
regressor = LinearRegression()
print("Started training")
regressor.fit(X_train, y_train)
print("Finished training")
y_pred = regressor.predict(X_test)

pickle.dump( regressor, open("data/regressor.pkl", "wb" ) )
pickle.dump( X_train, open("data/X_train.pkl", "wb" ) )
pickle.dump( X_test, open("data/X_test.pkl", "wb" ) )
pickle.dump( y_train, open("data/y_train.pkl", "wb" ) )
pickle.dump( y_test, open("data/y_test.pkl", "wb" ) )
pickle.dump( y_pred, open("data/y_pred.pkl", "wb" ) )

print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred))
print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred))
print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred)))

print("Done")



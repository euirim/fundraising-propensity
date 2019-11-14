import pickle
from ds import *
import pandas as pd
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn import metrics
import numpy as np
from sklearn.impute import SimpleImputer

data_as_list = []

pickle_files = ['data/dataset_0_10000.pkl', 'data/dataset_10000_20000.pkl', 'data/dataset_20000_30000.pkl', 'data/dataset_30000_40000.pkl']

for pickle_file in pickle_files:
    pickle_off = open(pickle_file, "rb")
    emp = pickle.load(pickle_off)

    title_vec_len = emp[0].features.title.vector.shape[0]
    story_vec_len = emp[0].features.story.vector.shape[0]
    for dataobject in emp:
        category = dataobject.features.category
        goal = dataobject.features.goal
        created = dataobject.features.created
        title_vec = dataobject.features.title.vector
        story_vec = dataobject.features.story.vector
        amt_raised = dataobject.result
        feature_vec = [category, goal, created]
        feature_vec.extend(title_vec)
        feature_vec.extend(story_vec)
        feature_vec.append(amt_raised)

        data_as_list.append(feature_vec)

headings = ["category", "goal", "created"]
headings.extend(["title_{}".format(i) for i in range(0, title_vec_len)])
headings.extend(["story_{}".format(i) for i in range(0, story_vec_len)])
headings.append("amt_raised")

df = pd.DataFrame(data_as_list, columns = headings)
df['category'] = pd.Categorical(df['category'])
dfDummies = pd.get_dummies(df['category'], prefix='category')
df = pd.concat([df, dfDummies], axis=1)
df.to_pickle("data/output_df.pkl")

print(len(df))
df.dropna(axis=0, how='any', thresh=None, subset=None, inplace=True)
print(len(df))


predictor_variable_indexes = [i for i in range(1,194+1)]
predictor_variable_indexes.extend([i for i in range(196, 214+1)])
response_variable_index = 195

X = df.iloc[:, predictor_variable_indexes].values
y = df.iloc[:, response_variable_index].values


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

#regressor = RandomForestRegressor(n_estimators=300, random_state=0, n_jobs=10, verbose=1)
regressor = MLPRegressor(hidden_layer_sizes=(100,), max_iter=100000, verbose=True)
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



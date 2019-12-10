import pickle
import sys
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn import metrics
import numpy as np
from sklearn.impute import SimpleImputer
import pandas as pd
# data_as_list = []
# 
# pickle_files = ['data/dataset_0_10000.pkl', 'data/dataset_10000_20000.pkl', 'data/dataset_20000_30000.pkl', 'data/dataset_30000_40000.pkl']
# 
# for pickle_file in pickle_files:
#     pickle_off = open(pickle_file, "rb")
#     emp = pickle.load(pickle_off)
# 
#     title_vec_len = emp[0].features.title.vector.shape[0]
#     story_vec_len = emp[0].features.story.vector.shape[0]
#     for dataobject in emp:
#         category = dataobject.features.category
#         goal = dataobject.features.goal
#         created = dataobject.features.created
#         title_vec = dataobject.features.title.vector
#         story_vec = dataobject.features.story.vector
#         amt_raised = dataobject.result
#         feature_vec = [category, goal, created]
#         feature_vec.extend(title_vec)
#         feature_vec.extend(story_vec)
#         feature_vec.append(amt_raised)
# 
#         data_as_list.append(feature_vec)
# 
# headings = ["category", "goal", "created"]
# headings.extend(["title_{}".format(i) for i in range(0, title_vec_len)])
# headings.extend(["story_{}".format(i) for i in range(0, story_vec_len)])
# headings.append("amt_raised")
# 
# df = pd.DataFrame(data_as_list, columns = headings)
# df['category'] = pd.Categorical(df['category'])
# dfDummies = pd.get_dummies(df['category'], prefix='category')
# df = pd.concat([df, dfDummies], axis=1)
# df.to_pickle("data/output_df.pkl")
# 
# print(len(df))
# df.dropna(axis=0, how='any', thresh=None, subset=None, inplace=True)
# print(len(df))
# 
# 
# predictor_variable_indexes = [i for i in range(1,194+1)]
# predictor_variable_indexes.extend([i for i in range(196, 214+1)])
# response_variable_index = 195
# 
# X = df.iloc[:, predictor_variable_indexes].values
# y = df.iloc[:, response_variable_index].values
# 
# 
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# X_train = pickle.load(open("data/X_train.pkl", "rb"))
# X_test = pickle.load(open("data/X_test.pkl", "rb"))
# y_train = pickle.load(open("data/y_train.pkl", "rb"))
# y_test = pickle.load(open("data/y_test.pkl", "rb"))
# y_pred = pickle.load(open("data/y_pred.pkl", "rb"))

# sc = StandardScaler()
# X_train = sc.fit_transform(X_train)
# X_test = sc.transform(X_test)

model_type = sys.argv[1]

if model_type == 'svr':
    regressor = SVR(degree=3, gamma='scale', epsilon=0.2, verbose=True)
elif model_type == 'random_forest':
    regressor = RandomForestRegressor(n_estimators=100, random_state=0, n_jobs=10, verbose=1)
elif model_type == 'mlp':
    regressor = MLPRegressor(hidden_layer_sizes=(300, 200, 200, 100,), max_iter=1000, verbose=True)
elif model_type == 'linear_regression':
    regressor = LinearRegression()
else:
    raise RuntimeError ('Unkown model type: {}'.format(model_type))

#X_train, X_test, y_train, y_test = read_csv()
df = pd.read_csv(sys.argv[2])
df['category'] = pd.Categorical(df['category'])
dfDummies = pd.get_dummies(df['category'], prefix='category')
df = pd.concat([df, dfDummies], axis=1)
df.dropna(axis=0, how='any', thresh=None, subset=None, inplace=True)

col_names = []
predictor_variable_indexes = []
response_variable_index = None

for col in df.columns:
    col_names.append(str(col))

for idx, col_name in enumerate(col_names):
    if "vec" in col_name or "category_" in col_name or col_name == "goal" or col_name == "created":
        predictor_variable_indexes.append(idx)
    if col_name == "raised":
        response_variable_index = idx


X = df.iloc[:, predictor_variable_indexes].values
y = df.iloc[:, response_variable_index].values


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)
print("Started training")
regressor.fit(X_train, y_train)
print("Finished training")
y_pred = regressor.predict(X_test)

pickle.dump( regressor, open("{}_regressor.pkl".format(model_type), "wb" ) )
# pickle.dump( X_train, open("data/X_train.pkl", "wb" ) )
pickle.dump( X_test, open("{}_X_test.pkl".format(model_type), "wb" ) )
# pickle.dump( y_train, open("data/y_train.pkl", "wb" ) )
pickle.dump( y_test, open("{}_y_test.pkl".format(model_type), "wb" ) )
pickle.dump( y_pred, open("{}_y_pred.pkl".format(model_type), "wb" ) )

print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred))
print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred))
print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred)))

print("Done")



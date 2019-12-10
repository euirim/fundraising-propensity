import numpy as np
from sklearn import metrics
import pickle
import sys

y_pred = pickle.load(open(sys.argv[1], 'rb'))
y_pred[y_pred < 0] = 0
y_test = pickle.load(open(sys.argv[2], 'rb'))

mae = metrics.mean_absolute_error(y_test, y_pred)
mse = metrics.mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)

print('Mean Absolute Error: {}'.format(mae))
print('Mean Squared Error: {}'.format(mse))
print('Root Mean Squared Error: {}'.format(rmse))
print('Done')

import pickle

pickle_off = open('data/y_pred.pkl', "rb")
y_pred = pickle.load(pickle_off)

pickle_off = open('data/y_test.pkl', "rb")
y_test = pickle.load(pickle_off)

print("Done")
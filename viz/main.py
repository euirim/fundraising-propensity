import os
import sys
import pickle

import matplotlib.pyplot as plt
import numpy as np


def create_hist(y_pred_fn, y_test_fn, title, num_bins, subplot, add_axes):
    """
    y_pred_fn: pickle filename
    y_test_fn: pickle filename
    num_bins: int
    """
    # load numpy arrays from pickled files
    y_pred = None
    y_test = None

    try:
        with open(y_pred_fn, 'rb') as f:
            y_pred = pickle.load(f)
    except Exception as err:
        print(f'Unable to load y_pred pickle file. Reason: {err}.')
        return

    try:
        with open(y_test_fn, 'rb') as f:
            y_test = pickle.load(f)
    except Exception as err:
        print(f'Unable to load y_pred pickle file. Reason: {err}.')
        return

    # threshold to zero for negative predicted values
    y_pred[y_pred < 0] = 0

    # subtract arrays
    error = y_pred - y_test

    # calc histogram range
    ran = np.percentile(error, [2.5, 97.5])
    print(f'Max error: {np.max(error)}')
    print(f'Min error: {np.min(error)}')

    # plot histogram
    subplot.hist(error, bins='auto', range=ran)
    subplot.title.set_text(title)
    if add_axes:
        subplot.set_xlabel('Error ($)')
        subplot.set_ylabel('Frequency')

def create_bar_chart():
    raise NotImplemented()


if __name__ == "__main__":
    DATA_LOC = '../data/dataset_full_word2vec/500000'
    NUM_HIST_BINS = 15

    if not os.path.exists('./tmp'):
        os.makedirs('./tmp')

    title = 'Model Error Distributions on word2vec Dataset.'
    model_types = [
        ('linear_regression', 'Linear Regression'),
        ('svr', 'SVR'),
        ('random_forest', 'Random Forest'),
        ('mlp', 'MLP')
    ]
    fig = plt.figure()
    fig.title.set_title(title, pad=15)
    for i, (mt, model_name) in enumerate(model_types):
        print(f'Creating error distribution for {model_name}.')
        subplot_arg = int(f'22{i+1}')
        ax = fig.add_subplot(subplot_arg)
        y_pred_fn = os.path.join(DATA_LOC, f'{mt}_y_pred.pkl')
        y_test_fn = os.path.join(DATA_LOC, f'{mt}_y_test.pkl')

        add_axes = False
        if i == (len(model_types) - 1):
            add_axes = True

        create_hist(
            y_pred_fn,
            y_test_fn,
            model_name,
            NUM_HIST_BINS,
            ax,
            add_axes,
        )

    # increase distance between subplots
    fig.subplots_adjust(wspace=0.5)
    fig.subplots_adjust(hspace=0.5)

    # save histogram
    fig.savefig('./tmp/error_hist.png', bbox_inches='tight', dpi=500)

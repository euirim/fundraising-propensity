import os
import sys
import pickle

import matplotlib.pyplot as plt
import numpy as np


def create_hist(y_pred_fn, y_test_fn, title, subplot, add_axes, alpha):
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

    y_pred = y_pred.astype(float)
    y_test = y_test.astype(float)

    #print(y_pred[:10])
    #print(y_test[:10])

    # subtract arrays
    error = y_pred - y_test

    # calc histogram range
    ran = np.percentile(error, [5, 95])
    print(f'Max error: {np.max(np.abs(error))}')
    print(f'Min error: {np.min(np.abs(error))}')
    #print(f'y_pred max error: {y_pred[np.argmax(error)]}')
    print(f'y_test max error: {y_test[np.argmax(np.abs(error))]}')
    print(f'y_test min error: {y_test[np.argmin(np.abs(error))]}')

    # plot histogram
    subplot.hist(error, bins='auto', range=ran, alpha=alpha)
    subplot.title.set_text(title)
    if add_axes:
        subplot.set_xlabel('Error ($)')
        subplot.set_ylabel('Frequency')

def create_bar_chart():
    raise NotImplemented()

def create_hists_for_dataset(dataset, dataset_name, fig, alpha=1.0, base_index=0, num_rows=3, num_cols=4):
    data_location = f'./data/{dataset}'

    if not os.path.exists('./tmp'):
        os.makedirs('./tmp')

    title = f'Model Error Distributions on {dataset_name} Dataset.'
    model_types = [
        ('linear_regression', 'Linear Regression'),
        ('svr', 'SVR'),
        ('random_forest', 'Random Forest'),
        ('mlp', 'MLP')
    ]
    for i, (mt, model_name) in enumerate(model_types):
        print(f'Creating error distribution for {model_name}.')
        ax = fig.add_subplot(num_rows, num_cols, base_index + i + 1)
        y_pred_fn = os.path.join(data_location, f'{mt}_y_pred.pkl')
        y_test_fn = os.path.join(data_location, f'{mt}_y_test.pkl')

        add_axes = False
        if i == (len(model_types) - 1):
            add_axes = True

        create_hist(
            y_pred_fn,
            y_test_fn,
            model_name,
            ax,
            add_axes,
            alpha,
        )

        ax.legend()


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
    fig.suptitle(title, fontsize=23, y=0.99)
    for i, (mt, model_name) in enumerate(model_types):
        #print(f'Creating error distribution for {model_name}.')
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
            ax,
            add_axes,
        )

    # increase distance between subplots
    fig.subplots_adjust(wspace=0.5)
    fig.subplots_adjust(hspace=0.5)

    # save histogram
    fig.savefig('./tmp/error_hist.png', bbox_inches='tight', dpi=500)

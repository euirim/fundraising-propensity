import os
import sys
import pickle
import matplotlib.pyplot as plt


def create_hist(y_pred_fn, y_test_fn, title, subtitle, num_bins, output_fn):
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

    # subtract arrays
    error = y_pred - y_test

    # plot histogram
    fig, ax = plt.subplots(nrows=1, ncols=1)
    ax.hist(error, num_bins)
    ax.title(title)
    ax.subtitle(subtitle)

    # save histogram
    fig.savefig(output_fn, bbox_inches='tight')


def create_bar_chart():
    raise NotImplemented()


if __name__ == "__main__":
    DATA_LOC = '../data/dataset_full_word2vec/250000'
    NUM_HIST_BINS = 15

    if not os.path.exists('./tmp'):
        os.makedirs('./tmp')

    dataset = 'Dataset\'s text features vectorized with word2vec.'
    model_types = [('linear_regression', 'Linear Regression')]
    for (mt, model_name) in model_types:
        y_pred_fn = os.path.join(DATA_LOC, f'{mt}_y_pred.pkl')
        y_test_fn = os.path.join(DATA_LOC, f'{mt}_y_test.pkl')
        create_hist(
            y_pred_fn,
            y_test_fn,
            f'{model_name} Error Distribution',
            dataset,
            NUM_HIST_BINS,
            os.path.join('./out', f'{mt}_error_hist.png'),
        )

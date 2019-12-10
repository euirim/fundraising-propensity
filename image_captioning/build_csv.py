import os
import sys

import pandas as pd
from subprocess import call
import numpy as np

CSV_FILENAME = "./data/full_dataset_bert_title_doc2vec_story.csv"
CAPTIONS_DIR = "./captions_new"


def get_filename_from_url(url):
    if not url or str(url) == 'nan':
        return

    return url.strip().split('/')[-1].split('?')[0]


def main():
    CHUNK_SIZE = 10000
    num_failed_total = 0
    for i, df in enumerate(pd.read_csv(CSV_FILENAME, header=0, chunksize=CHUNK_SIZE)):
        print "Processing from row %d" % (i * CHUNK_SIZE)

        num_failed = 0

        # add new columns to dataframe for caption for cover and others
        df["cover_image_autocaption"] = np.nan
        df["story_images_autocaption"] = np.nan

        # associate captions to appropriate rows/columns
        for index, row in df.iterrows():
            cover_fn = get_filename_from_url(row['first_cover_image'])

            if cover_fn:
                try:
                    with open(os.path.join(CAPTIONS_DIR, cover_fn + '.txt'), "r") as f:
                        df['cover_image_autocaption'] = f.read()
                except IOError as err:
                    print "Error. Something went wrong."
                    print err
                    num_failed += 1

            story_images = row['story_images']
            captions = []
            if str(story_images) != 'nan':
                for img_url in story_images.strip().split(','):
                    story_fn = get_filename_from_url(img_url)
                    if not story_fn:
                        continue
                    try:
                        with open(os.path.join(CAPTIONS_DIR, story_fn + '.txt'), "r") as f:
                            captions.append(f.read())
                    except IOError as err:
                        print "Error. Something went wrong."
                        print err
                        num_failed += 1

            df["story_image_autocaption"] = ' '.join(captions)

        # save new csv
        NEW_CSV_OUTPUT = "./out_final.csv"
        if i == 0:
            df.to_csv(NEW_CSV_OUTPUT, mode='w')
        else:
            df.to_csv(NEW_CSV_OUTPUT, mode='a', header=None)

        print "Done this set of rows. Num Failed: %d" % num_failed
        num_failed_total += num_failed

    print "Done. Total Num Failed: %d" % num_failed_total

if __name__=="__main__":
    main()
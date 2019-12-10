import os
import sys

import pandas as pd
from subprocess import call
import numpy as np

CSV_FILENAME = "./data/full_dataset_bert_title_doc2vec_story.csv"
CAPTIONS_DIR = "./captions_2"


def get_filename_from_url(url):
    if not url or str(url) == 'nan':
        return

    return url.strip().split('/')[-1]


def main():
    print "Loading CSV..."
    df = pd.read_csv(CSV_FILENAME, header=0)

    # add new columns to dataframe for caption for cover and others
    df["cover_image_autocaption"] = np.nan
    df["story_images_autocaption"] = np.nan

    # associate captions to appropriate rows/columns
    print "Associating captions to appropriate rows..."
    for index, row in df.iterrows():
        cover_fn = get_filename_from_url(row['first_cover_image'])

        if cover_fn:
            with open(os.path.join(CAPTIONS_DIR, cover_fn + '.txt'), "r") as f:
                df['cover_image_autocaption'] = f.read()

        story_images = row['story_images']
        captions = []
        if str(story_images) != 'nan':
            for img_url in story_images.strip().split(','):
                story_fn = get_filename_from_url(img_url)
                with open(os.path.join(CAPTIONS_DIR, story_fn + '.txt'), "r") as f:
                    captions.append(f.read())

        df["story_image_autocaption"] = ' '.join(captions)

    # save new csv
    print "Saving CSV..."
    NEW_CSV_OUTPUT = "./out_2.csv" % sys.argv[1]
    df.to_csv(NEW_CSV_OUTPUT)

if __name__=="__main__":
    main()
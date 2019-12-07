import os
import sys

import pandas as pd
from subprocess import call
import numpy as np

CSV_FILENAME = "./data/bert_200.csv"
CAPTIONS_DIR = "./captions"


def get_filename_from_url(url):
    if not url or str(url) == 'nan':
        return

    return url.strip().split('/')[-1]


def main():
    df = pd.read_csv(CSV_FILENAME, header=0)
    df = df[int(sys.argv[1]):min(int(sys.argv[1]) + 100000, df.shape[0])]
    IMAGE_URLS_OUTPUT = "./data/image_urls_%s.txt" % sys.argv[1]

    # get all image URLs and save to text file
    cover_image_urls = [url for url in df['first_cover_image'].tolist() if str(url) != 'nan']
    story_image_urls = [url for url in df['story_images'].tolist() if str(url) != 'nan']
    story_image_urls = ','.join(story_image_urls).split(',')
    image_urls = cover_image_urls + story_image_urls
    with open(IMAGE_URLS_OUTPUT, "w") as f:
        for url in image_urls:
            f.write(url + '\n')

    # get captions for each image URL and save to text file
    call('./run.sh %s' % sys.argv[1], shell=True)

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
    NEW_CSV_OUTPUT = "./out_%s.csv" % sys.argv[1]
    df.to_csv(NEW_CSV_OUTPUT)

if __name__=="__main__":
    main()
import os
import sys

import pandas as pd
from subprocess import call
import numpy as np

CSV_FILENAME = "./data/full_dataset_bert_title_doc2vec_story.csv"


def get_filename_from_url(url):
    if not url or str(url) == 'nan':
        return

    return url.strip().split('/')[-1]


def main():
    print "Loading CSV..."
    df = pd.read_csv(CSV_FILENAME, header=0)
    # df = df[int(sys.argv[1]):min(int(sys.argv[1]) + 100000, df.shape[0])]
    IMAGE_URLS_OUTPUT = "./data/image_urls.txt"

    # get all image URLs and save to text file
    print "Getting cover image URLs."
    cover_image_urls = [url for url in df['first_cover_image'].tolist() if str(url) != 'nan']
    print "Getting story image URLs."
    story_image_urls = [url for url in df['story_images'].tolist() if str(url) != 'nan']
    story_image_urls = ','.join(story_image_urls).split(',')
    print "Accumulating image URLs."
    image_urls = cover_image_urls + story_image_urls
    print "Saving image URLs."
    with open(IMAGE_URLS_OUTPUT, "w") as f:
        for url in image_urls:
            f.write(url + '\n')

    # get captions for each image URL and save to text file
    print "Calling inference script."
    call('./run.sh', shell=True)

if __name__=="__main__":
    main()
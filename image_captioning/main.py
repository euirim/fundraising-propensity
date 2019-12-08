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

def get_image_urls():
    IMAGE_URLS_OUTPUT = "./data/image_urls.txt"
    CHUNK_SIZE = 100000
    for i, chunk in enumerate(pd.read_csv(CSV_FILENAME, header=0, chunksize=CHUNK_SIZE)):
        print "Processing starting at row %d" % (i * CHUNK_SIZE)
        # get all image URLs and save to text file
        cover_image_urls = [url for url in chunk['first_cover_image'].tolist() if str(url) != 'nan']
        story_image_urls = [url for url in chunk['story_images'].tolist() if str(url) != 'nan']
        story_image_urls = ','.join(story_image_urls).split(',')
        image_urls = cover_image_urls + story_image_urls

        read_mode = "a"
        if i == 0:
            read_mode = "w"

        with open(IMAGE_URLS_OUTPUT, read_mode) as f:
            for url in image_urls:
                f.write(url + '\n')

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--process-images":
        print "Getting Image URLs"
        get_image_urls()
    
    # get captions for each image URL and save to text file
    print "Calling inference script."
    call('./run.sh', shell=True)

if __name__=="__main__":
    main()
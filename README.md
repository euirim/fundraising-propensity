# fundraising-propensity

What makes a successful GoFundMe campaign? We independently collected data from over 1 million campaigns and compared several different model architectures to predict how much money campaigns will raise based on factors that campaign creators can control, such as the goal amount, title, story, and images. These models included random forest regression, support vector regression, and multi-layer perceptrons; we found that support vector regression (SVR) produced the best predictions, with all our models beating a baseline linear regression model. Text that we scraped and extracted from images via automated image captioning was vectorized into features using several language representation techniques like word2vec, doc2vec, and BERT. Our experiments found that support vector regression on text vectorized with BERT was the most effective language representation model on average.

## Scraper
Navigate to `scraper` subdirectory in this repo. Activate virtualenv.

```sh
source venv/bin/activate
```

Run crawler.

```sh
scrapy runspider spider.py
```

## Automated Image Captioning
Navigate to `image_captioning` in this repo. Build and start docker container.

```sh
./init.sh
```

Generate image captions. (**Warning:** will take a long time.)

```sh
python main.py --process-images
```

Build dataset using generated image captions.

```sh
python build_csv.py
```

## Text Embedding

The `read_csv/read.py` script can be used to create vector representations of text features. It takes as input a CSV with the following columns, which can be obtained by running the crawler and image captioning scripts:

* rownum
* url
* title
* story
* created
* goal
* category
* finished
* first_cover_image
* story_images
* raised
* cover_image_autocaption
* story_images_autocaption
* story_image_autocaption

An example of a properly formatted input CSV can be found in `data/data_sample.csv`.

To run, edit the `with open...` line to provide the path to the input CSV. Edit the `...vectorization_technique` variables to specify the desired text embedding techniques. For titles and captions, `doc2vec`, `word2vec`, and `bert` are supported. For stories, `doc2vec` and `word2vec` are supported.

Then call the script with:

`python read_csv/read.py start_row end_row`

or 

`python read_csv/read.py -1 -1`

to process the full file. Output will be saved to the project root directory.

## Experiments
Navigate to the `Experiments` folder in this repo. Assuming you have a CSV of the preprocessed data
(so categories are one-hot encoded and image captions/text features are vectorized), the `models.py`
script can be run as follows:

```sh
python3 models.py <model_name> <csv_file_name>
```

Here, `<csv_file_name>` should refer to the name of the CSV file that needs to be trained on, and
`<model_name>` can be one of: `linear_regression`, `svr`, `random_forest`, or `mlp`.

## Data Sample

A sample of our raw data can be found in `data/data_sample.csv`.

## Contributors
Nikhil Athreya, Euirim Choi, Anthony Li

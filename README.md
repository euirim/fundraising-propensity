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

## Contributors
Nikhil Athreya, Euirim Choi, Anthony Li

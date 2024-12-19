Data used for experiment is in `processed_trace_data.csv`

If you want to recreate the preprocessed dataset from scratch:
1. Run `download_dataset.sh` file to download and build the secmatv1 dataset. This takes a while since the dataset is about 3.75GB.
    - If you want to download the dataset manually you can download the dataset here: https://cloud.telecom-paris.fr/s/8KWK5PnApP4DNy7
    - You'll need to unzip all the parts and place all the `.bin` files in a single folder called `secmatv1_2006_04_0809`
2. Run `python preprocess_dataset.py` to generate the csv from the parsed dataset.

Data used for experiment is in `processed_trace_data.csv`

If you want to recreate the csv from scratch:
1. Run `create_dataset.sh` file to download and build the secmatv1 dataset. This takes a while since the dataset is about 3.75GB and all data is stored in binary and needs to be converted to csv.
2. Run `python preprocess_trace_data.py` to generate the csv from the parsed dataset.

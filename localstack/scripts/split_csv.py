import logging
import os

import pandas as pd
from dotenv import load_dotenv

# todo: remove after dockerization
load_dotenv("../.env")

logging.basicConfig(level=logging.INFO)

data_path = os.path.join("..", os.getenv("DATASET_PATH"))
output_csv_dir_path = os.path.join("..", os.getenv("SPLIT_DATA_DIR_PATH"))

# Schema for faster parsing. The real data types are mixed up due to heterogeneity of provided data.
schema = {
    'departure': str,  # will be parsed as Timestamp
    'return': str,  # will be parsed as Timestamp
    'departure_id': str,  # why?
    'departure_name': str,
    'return_id': str,  # what? why?
    'return_name': str,
    'distance (m)': float,
    'duration (sec.)': float,
    'avg_speed': float,
    'departure_latitude': float,
    'departure_longitude': float,
    'return_latitude': float,
    'return_longitude': float,
    'Air temperature (degC)': float

}
logging.info("Reading CSV file...")

df = pd.read_csv(data_path, parse_dates=['departure', 'return'], dtype=schema)

logging.info("Read successfully!")

if not os.path.exists(output_csv_dir_path):
    logging.warning(f"Creating directory: {output_csv_dir_path}")
    os.mkdir(output_csv_dir_path)

# Group data by month and save in different directories:
logging.info("Starting splitting by month...")
for group_name, group_body in df.groupby(pd.Grouper(key='departure', freq='M')):
    group_body.to_csv(os.path.join(output_csv_dir_path, f"{group_name:%Y-%m}.csv"))
    logging.info(f"Saved {group_name:%Y-%m}...")
logging.info(f"Splitting finished! Path to datasets: {output_csv_dir_path}")

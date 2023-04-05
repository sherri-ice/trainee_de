import logging
import os

import pandas as pd


def group_by_month_and_save(dataset_path: str, output_dir_path: str) -> None:
    # todo: delete this check before final version
    if len(os.listdir(output_dir_path)) > 0:
        return

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

    df = pd.read_csv(dataset_path, parse_dates=['departure', 'return'], dtype=schema)

    if not os.path.exists(output_dir_path):
        logging.warning(f"Creating directory: {output_dir_path}")
        os.mkdir(output_dir_path)

    # Group data by month and save in different directories:
    for group_name, group_body in df.groupby(pd.Grouper(key='departure', freq='M')):
        group_body.to_csv(os.path.join(output_dir_path, f"{group_name:%Y-%m}.csv"))
import os
import sys

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col


def _load_csv_to_spark(spark_session: SparkSession, csv_path: str) -> DataFrame:
    return spark_session.read.option('header', True).csv(csv_path)


def _count_metric_by_each_station(df: DataFrame) -> DataFrame:
    """
    The _count_metric_by_each_station function takes a DataFrame as input and do some aggregation:
        - station_name: how many bikes were taken by each station
        - taken_count: how many bikes were returned by each station
        - return_count: how many bikes were returned by each station
    The final metric is combined table with taken and return numbers.

    :param df: DataFrame: Pass the dataframe into the function
    :return: DataFrame
    """
    # Let's count how many bikes were taken by each station
    departure_metric_df = df \
        .groupby('departure_name') \
        .count() \
        .select(col('departure_name').alias('station_name'),
                col('count').alias('taken_count'))

    # Then let's count how many bikes were returned by each station
    return_metric_df = df \
        .groupby('return_name') \
        .count() \
        .select(col('return_name').alias('station_name'),
                col('count').alias('return_count'))

    # The final metric is combined table with taken and return numbers
    return departure_metric_df \
        .join(return_metric_df, on='station_name', how='left') \
        .fillna(value=0,
                subset=['taken_count',
                        'return_count'])


def _save_metrics_to_csv(df: DataFrame, path_to_save: str, filename: str = 'result.csv') -> None:
    """
    The _save_metrics_to_csv function saves the metrics dataframe to a csv file.

    :param df: DataFrame: Specify the dataframe that is passed to the function
    :param path_to_save: str: Specify the path to save the csv file
    :param filename: str: Specify the name of the file that will be saved. Default is 'result.csv'.
    :return: None
    """
    if not os.path.exists(path_to_save):
        os.mkdir(path_to_save)
    df.toPandas().to_csv(os.path.join(path_to_save, filename), header=True, index=False)


def count_metrics_with_spark(csv_path: str, path_to_save_metrics: str) -> None:
    """
    The count_metrics_with_spark function takes a csv file path and a path to save the metrics as arguments.
    It creates a SparkSession, loads the csv into it, counts the metrics for each station and saves them in another csv
    file.


    :param csv_path: str: Specify the path to the csv file
    :param path_to_save_metrics: str: Specify the path where the metrics will be saved
    :return: None
    """
    spark_session = SparkSession \
        .builder \
        .appName("Compute Metrics") \
        .master("local").getOrCreate()

    df = _load_csv_to_spark(spark_session, csv_path)
    _save_metrics_to_csv(_count_metric_by_each_station(df), path_to_save_metrics)


if __name__ == '__main__':
    csv_path = sys.argv[1]
    path_to_save_metrics = sys.argv[2]

    count_metrics_with_spark(csv_path, path_to_save_metrics)

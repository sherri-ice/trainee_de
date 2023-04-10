import os
import sys

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col


def _load_csv_to_spark(spark_session: SparkSession, csv_path: str) -> DataFrame:
    return spark_session.read.option('header', True).csv(csv_path)


def _count_metric_by_each_station(df: DataFrame) -> DataFrame:
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
    if not os.path.exists(path_to_save):
        os.mkdir(path_to_save)
    df.toPandas().to_csv(os.path.join(path_to_save, filename), header=True, index=False)


def count_metrics_with_spark(csv_path: str, path_to_save_metrics: str) -> None:
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

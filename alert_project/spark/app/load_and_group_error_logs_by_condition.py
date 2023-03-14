import sys

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_unixtime, count

if __name__ == "__main__":
    logs_path = sys.argv[1]
    group_by_this_time = sys.argv[2]
    bundle_id = sys.argv[3]

    spark = SparkSession \
        .builder \
        .appName("Mobile Logs ETL") \
        .master("local").getOrCreate()

    # Rename columns
    new_columns = ["error_code", "error_message", "severity", "log_location",
                   "mode", "model", "graphics", "session_id", "sdkv", "test_mode",
                   "flow_id", "flow_type", "sdk_date", "publisher_id", "game_id",
                   "bundle_id", "appv", "language", "os", "adv_id", "gdpr", "ccpa",
                   "country_code", "date"]
    df = spark.read.format("csv").options(header='True').load(logs_path)
    df = df.toDF(*new_columns)

    # Important! Pass time by seconds!
    time_window = from_unixtime(col('date') - col('date') % group_by_this_time)
    df = df.withColumn('minute_window', time_window)

    if bundle_id != 'all':
        df = df.filter((col('severity') == 'Error') & (col('bundle_id') == bundle_id)) \
            .groupby('minute_window') \
            .agg(count('error_code').alias('count_of_errors')) \
            .filter(col('count_of_errors') >= 10)
    else:
        df = df.filter(col('severity') == 'Error') \
            .groupby('minute_window') \
            .agg(count('error_code').alias('count_of_errors')) \
            .filter(col('count_of_errors') >= 10)

    df.toPandas().to_csv('data/failed_minutes_data.csv')

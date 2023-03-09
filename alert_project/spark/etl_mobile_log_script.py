from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_unixtime, count

if __name__ == "__main__":
    app_name = 'DataEngineering'
    spark = SparkSession.builder.appName("Mobile Logs ETL").getOrCreate()

    # Rename columns
    new_columns = ["error_code", "error_message", "severity", "log_location",
                   "mode", "model", "graphics", "session_id", "sdkv", "test_mode",
                   "flow_id", "flow_type", "sdk_date", "publisher_id", "game_id",
                   "bundle_id", "appv", "language", "os", "adv_id", "gdpr", "ccpa",
                   "country_code", "date"]
    df = spark.read.format("csv").options(header='True').load('data/data.csv')
    df = df.toDF(*new_columns)

    # For grouping by 1 minute
    minutes_in_seconds = 60
    minutes_window = from_unixtime(col('date') - col('date') % minutes_in_seconds)
    df = df.withColumn('minute_window', minutes_window)

    df = df.filter(col('severity') == 'Error') \
        .groupby('minute_window') \
        .agg(count('error_code').alias('count_of_errors')) \
        .filter(col('count_of_errors') >= 10)

    df.write.format('csv').options(header=True).save('data/failed_minutes_data.csv')

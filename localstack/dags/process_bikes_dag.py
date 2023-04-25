import datetime
import os

from airflow.decorators import dag, task, task_group
from airflow.models import Variable
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.sensors.filesystem import FileSensor
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

from scripts.split_csv import group_by_month_and_save
from helpers.prefix_solver import PrefixSolver, PredefinedPrefixSolver, YearPrefixSolver

default_args = {
    'owner': 'sherri-ice',
    'email_on_failure': 'False',
}


@dag(schedule=None, start_date=datetime.datetime.now(), catchup=False)
def process_bikes():
    """
    The process_bikes function is responsible for processing the bike dataset. It does so by first waiting for the
    dataset to be placed and then uploading it to S3. Next, it splits the dataset into monthly files and uploads them
    to S3 as well. Finally, it counts some metrics of the data using Spark and saves these metrics in a file which is also
    uploaded to S3.

    :return: A dag
    """
    # Variables from Airflow env
    dataset_path = Variable.get('DATASET_PATH')
    spark_metrics_path = Variable.get('SPARK_METRICS_PATH')
    spark_scripts_path = Variable.get('SPARK_SCRIPTS_PATH')
    split_csv_dir = Variable.get('SPLIT_CSV_DIR')
    s3_bucket_name = Variable.get('S3_BUCKET_NAME')

    s3_hook = S3Hook()

    csv_wait_sensor = FileSensor(task_id='csv_wait_sensor', filepath=dataset_path)

    @task
    def load_all_files_to_s3(source_dir_path: str, hook: S3Hook, bucket_name: str, prefix_solver: PrefixSolver) -> None:
        """
        The load_all_files_to_s3 function takes a source directory path, an S3Hook, a bucket name and
        a PrefixSolver object as arguments. It then iterates over all the files in the source directory and
        uploads them to S3 using the load_file method of the hook. The key for each file is determined by
        the get_prefix method of prefix solver.

        :param source_dir_path: str: Specify the directory path of the files to be uploaded
        :param hook: S3Hook: Connect to the s3 bucket
        :param bucket_name: str: Specify the name of the s3 bucket to which we want to upload our files
        :param prefix_solver: PrefixSolver: Determine the prefix for each file
        :return: None
        """
        for filename in os.listdir(source_dir_path):
            prefix = prefix_solver.get_prefix(filename)
            hook.load_file(bucket_name=bucket_name,
                           filename=os.path.join(source_dir_path, filename),
                           key=f'{prefix}/{filename}',
                           replace=True)

    @task
    def load_file_to_s3(source_path: str, hook: S3Hook, bucket_name: str, prefix_solver: PrefixSolver):
        """
        The load_file_to_s3 function takes a source path, an S3Hook, a bucket name and a PrefixSolver object.
        It then loads the file at the source path to S3 using the hook. The key is determined by calling get_prefix on
        the prefix solver with the source path as input.

        :param source_path: str: Specify the path of the file to be uploaded
        :param hook: S3Hook: Connect to the s3 bucket
        :param bucket_name: str: Specify the name of the s3 bucket to which we want to upload our file
        :param prefix_solver: PrefixSolver: Determine the prefix of the file
        :return: The filename and the prefix
        """
        filename = os.path.basename(source_path)
        prefix = prefix_solver.get_prefix(source_path)
        hook.load_file(bucket_name=bucket_name,
                       filename=source_path,
                       key=f'{prefix}/{filename}',
                       replace=True)

    @task
    def delete_temp_files(dir_path: str) -> None:
        for filename in os.listdir(dir_path):
            os.remove(os.path.join(dir_path, filename))
        os.rmdir(dir_path)

    @task_group
    def count_spark_metric_and_save_to_s3():
        """
        The count_spark_metric_and_save_to_s3 function is responsible for grouping Airflow operators: counting the
        metrics of the dataset with SparkOperator and save them to S3.

        :return: Airflow Task Group
        """
        count_metrics = SparkSubmitOperator(
            application=f'{spark_scripts_path}/count_metrics.py',
            task_id='count_metrics_with_spark',
            application_args=[
                dataset_path,
                spark_metrics_path
            ]
        )

        count_metrics >> load_all_files_to_s3(source_dir_path=spark_metrics_path,
                                              hook=s3_hook,
                                              bucket_name=s3_bucket_name,
                                              prefix_solver=PredefinedPrefixSolver("metrics"))

    @task_group
    def group_by_month_and_load_to_s3():
        """
        The group_by_month_and_load_to_s3 function groups the Airflow operators: PythonOperators for splitting dataset
        by month and saving each month's data to a separate CSV file. It then loads all of these files to S3.

        :return:  Airflow Task Group
        """
        split_by_month_and_save_locally = PythonOperator(task_id='split_csv_by_month_and_save_locally',
                                                         python_callable=group_by_month_and_save,
                                                         op_kwargs={
                                                             'dataset_path': dataset_path,
                                                             'output_dir_path': split_csv_dir
                                                         })

        split_by_month_and_save_locally >> load_all_files_to_s3(source_dir_path=split_csv_dir,
                                                                hook=s3_hook,
                                                                bucket_name=s3_bucket_name,
                                                                prefix_solver=YearPrefixSolver())

    csv_wait_sensor >> load_file_to_s3(source_path=dataset_path,
                                       hook=s3_hook,
                                       bucket_name=s3_bucket_name,
                                       prefix_solver=PredefinedPrefixSolver("data")) \
    >> [group_by_month_and_load_to_s3(),
        count_spark_metric_and_save_to_s3()] \
    >> delete_temp_files.expand(dir_path=[spark_metrics_path, split_csv_dir])


process_bikes()

import datetime
import os

from airflow.decorators import dag, task, task_group
from airflow.models import Variable
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.sensors.filesystem import FileSensor
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

from scripts.split_csv import group_by_month_and_save
from helpers.prefix_solver import PrefixSolver, EchoPrefixSolver, YearPrefixSolver

default_args = {
    'owner': 'sherri-ice',
    'email_on_failure': 'False',
}


@dag(schedule=None, start_date=datetime.datetime.now(), catchup=False)
def process_bikes():
    dataset_path = Variable.get('DATASET_PATH')
    spark_metrics_path = Variable.get('SPARK_METRICS_PATH')
    spark_scripts_path = Variable.get('SPARK_SCRIPTS_PATH')
    split_csv_dir = Variable.get('SPLIT_CSV_DIR')
    s3_bucket_name = Variable.get('S3_BUCKET_NAME')

    s3_hook = S3Hook()

    csv_wait_sensor = FileSensor(task_id='csv_wait_sensor', filepath=dataset_path)

    @task
    def load_all_files_to_s3(source_dir_path: str, hook: S3Hook, bucket_name: str, prefix_solver: PrefixSolver) -> None:
        for filename in os.listdir(source_dir_path):
            prefix = prefix_solver.get_prefix(filename)
            hook.load_file(bucket_name=bucket_name,
                           filename=os.path.join(source_dir_path, filename),
                           key=f'{prefix}/{filename}',
                           replace=True)

    @task
    def load_file_to_s3(source_path: str, hook: S3Hook, bucket_name: str, prefix_solver: PrefixSolver):
        filename = os.path.basename(source_path)
        prefix = prefix_solver.get_prefix(source_path)
        hook.load_file(bucket_name=bucket_name,
                       filename=source_path,
                       key=f'{prefix}/{filename}',
                       replace=True)

    @task_group
    def count_spark_metric_and_save_to_s3():
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
                                              prefix_solver=EchoPrefixSolver("metrics"))

    @task_group
    def group_by_month_and_load_to_s3():

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

    @task
    def delete_temp_files(dir_path: str) -> None:
        for filename in os.listdir(dir_path):
            os.remove(os.path.join(dir_path, filename))
        os.rmdir(dir_path)

    csv_wait_sensor >> load_file_to_s3(source_path=dataset_path,
                                       hook=s3_hook,
                                       bucket_name=s3_bucket_name,
                                       prefix_solver=EchoPrefixSolver("data")) \
    >> [group_by_month_and_load_to_s3(),
        count_spark_metric_and_save_to_s3()] \
    >> delete_temp_files.expand(dir_path=[spark_metrics_path, split_csv_dir])


process_bikes()

import datetime
import os
import re

from airflow.decorators import dag, task, task_group
from airflow.models import Variable
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.sensors.filesystem import FileSensor

from scripts.split_csv import group_by_month_and_save


@dag(schedule=None, start_date=datetime.datetime.now(), catchup=False)
def process_bikes():
    dataset_path = Variable.get('DATASET_PATH')

    csv_wait_sensor = FileSensor(task_id="csv_wait_sensor", filepath=dataset_path)

    @task_group
    def group_by_month_and_load_to_s3():
        split_csv_dir = Variable.get("SPLIT_CSV_DIR")
        s3_bucket_name = Variable.get("S3_BUCKET_NAME")

        split_by_month_and_save_locally = PythonOperator(task_id="split_csv_by_month_and_save_locally",
                                                         python_callable=group_by_month_and_save,
                                                         op_kwargs={
                                                             'dataset_path': dataset_path,
                                                             'output_dir_path': split_csv_dir
                                                         })

        @task
        def load_all_files_to_s3(source_dir_path: str, hook: S3Hook, bucket_name: str) -> None:
            for filename in os.listdir(source_dir_path):
                year_match = re.match(r'([1-2][0-9]{3})', filename)
                if year_match is None:
                    prefix = 'unclassified'
                else:
                    prefix = year_match.group(1)
                hook.load_file(bucket_name=bucket_name,
                               filename=os.path.join(source_dir_path, filename),
                               key=f'{[prefix]}/{filename}')

        @task
        def delete_temp_files(dir_path: str) -> None:
            for filename in os.listdir(dir_path):
                os.remove(os.path.join(dir_path, filename))
            os.rmdir(dir_path)

        s3_hook = S3Hook()

        csv_wait_sensor >> \
        split_by_month_and_save_locally >> \
        load_all_files_to_s3(source_dir_path=split_csv_dir,
                             hook=s3_hook,
                             bucket_name=s3_bucket_name)
        # todo: uncomment to final version
        # delete_temp_files(split_csv_dir)

    group_by_month_and_load_to_s3()


process_bikes()

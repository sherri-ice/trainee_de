import datetime
import os
import re

from airflow.decorators import dag, task
from airflow.models import Variable
from airflow.providers.amazon.aws.hooks.s3 import S3Hook


@dag(schedule=None, start_date=datetime.datetime.now(), catchup=False)
def load_all_files_to_s3_bucket():
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

    split_csv_dir = Variable.get("SPLIT_CSV_DIR")
    s3_bucket_name = Variable.get("S3_BUCKET_NAME")
    s3_hook = S3Hook()

    load_all_files_to_s3(source_dir_path=split_csv_dir, hook=s3_hook, bucket_name=s3_bucket_name)


load_all_files_to_s3_bucket()

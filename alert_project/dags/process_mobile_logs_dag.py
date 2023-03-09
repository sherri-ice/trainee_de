import os
from datetime import datetime, timedelta

from airflow.decorators import dag, task
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.models import Variable
from airflow.sensors.filesystem import FileSensor

from config_storage import EmailStorage

default_args = {
    'owner': 'sherri-ice',
    'email': EmailStorage(os.getenv('EMAIL_CONFIG_PATH')).email_list,
    'email_on_failure': 'False',
}


@dag(dag_id='process_mobile_logs', default_args=default_args, schedule=timedelta(minutes=10),
     start_date=datetime.utcnow(), catchup=False)
def process_mobile_logs():
    data_path = Variable.get('DATA_PATH')
    file_wait_sensor = FileSensor(task_id='waiting_for_log_journal', filepath=data_path)

    etl_process = SparkSubmitOperator(
        application='spark/etl_mobile_log_script.py',
        task_id='load_logs_and_analyze_mobile_logs',
        email_on_failure=True
    )

    file_wait_sensor >> etl_process


process_mobile_logs()

import os
from datetime import datetime, timedelta

import pandas as pd
from airflow.decorators import dag, task
from airflow.operators.email import EmailOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.models import Variable
from airflow.sensors.filesystem import FileSensor
from airflow.operators.python import get_current_context

from config_storage import EmailStorage

default_args = {
    'owner': 'sherri-ice',
    'email_on_failure': 'False',
}


@dag(dag_id='process_mobile_logs', default_args=default_args, schedule=timedelta(minutes=10),
     start_date=datetime.utcnow(), catchup=False)
def process_mobile_logs():
    # File sensor environment
    data_path = Variable.get('DATA_PATH')
    file_wait_sensor = FileSensor(task_id='waiting_for_log_journal', filepath=data_path)

    # Spark ETL per minute process environment
    spark_scripts_path = Variable.get("SPARK_SCRIPTS_PATH")
    etl_process_per_minute = SparkSubmitOperator(
        application=f'{spark_scripts_path}/load_and_group_error_logs_by_condition.py',
        task_id='load_and_group_error_logs_by_one_minute',
        application_args=[
            "data/data.csv",  # path for logs
            "60",  # time to group logs in seconds
            "all"  # select all bundle_id
        ]
    )

    # Spark ETL per hour and bundle_id process environment
    spark_scripts_path = Variable.get("SPARK_SCRIPTS_PATH")
    etl_process_per_hour = SparkSubmitOperator(
        application=f'{spark_scripts_path}/load_and_group_error_logs_by_condition.py',
        task_id='load_and_group_error_logs_by_one_hour',
        application_args=[
            "data/data.csv",  # path for logs
            f"{60 * 60}",  # time to group logs in seconds
            "1"  # put exact bundle_id here
        ]
    )

    # Email notification task environment
    failed_logs_path = Variable.get('FAILED_LOGS_PATH')
    emails_to_notify = EmailStorage(Variable.get('EMAIL_CONFIG_PATH')).email_list

    @task
    def notify_on_failed_logs(failed_logs_path: str):
        context = get_current_context()
        try:
            failed_log_file = open(failed_logs_path)
        except FileNotFoundError as e:
            return
        failed_log_df = pd.read_csv(failed_log_file)
        email = EmailOperator(
            task_id="send_emails_on_failed_logs",
            to=emails_to_notify,
            subject="",
            html_content=failed_log_df.to_html(),
            dag=context.get('dag')
        )
        email.execute(context=context)
        os.remove(failed_logs_path)

    file_wait_sensor >> [etl_process_per_minute, etl_process_per_hour] >> notify_on_failed_logs(failed_logs_path)


process_mobile_logs()

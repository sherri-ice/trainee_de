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
    data_path = Variable.get('DATA_PATH')
    file_wait_sensor = FileSensor(task_id='waiting_for_log_journal', filepath=data_path)

    etl_process = SparkSubmitOperator(
        application='spark/etl_mobile_log_script.py',
        task_id='load_logs_and_analyze_mobile_logs'
    )

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
            to=EmailStorage(Variable.get('EMAIL_CONFIG_PATH')).email_list,
            subject="",
            html_content=failed_log_df.to_html(),
            dag=context.get('dag')
        )
        email.execute(context=context)

    failed_logs_path = Variable.get("FAILED_LOGS_PATH")

    file_wait_sensor >> etl_process >> notify_on_failed_logs(failed_logs_path)


process_mobile_logs()

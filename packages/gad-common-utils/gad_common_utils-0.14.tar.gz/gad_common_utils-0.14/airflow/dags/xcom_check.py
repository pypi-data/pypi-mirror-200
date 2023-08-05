import logging
from datetime import datetime, timedelta

from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
from kubernetes.client import models as k8s

default_args = {
    "owner": "aiola-dev",
    "depends_on_past": False,
    "start_date": days_ago(0),
    "catchup": False,
    "email": ["aiola@example.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0,
    "retry_delay": timedelta(minutes=5),
}


@dag(
    schedule="@monthly",
    start_date=datetime(2021, 12, 1),
    catchup=False,
    default_args=default_args,
)
def taskflow():
    @task
    def send_xcom():
        logging.info("HI HI HI")
        return "Hello XCOM"

    @task
    def print_msg(msg: str):
        logging.info(f"Msg: {msg}")

    print_msg(send_xcom())


dag = taskflow()

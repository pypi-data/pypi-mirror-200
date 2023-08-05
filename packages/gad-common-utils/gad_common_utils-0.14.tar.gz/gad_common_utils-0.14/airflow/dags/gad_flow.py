from datetime import timedelta

from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow.utils.dates import days_ago
from kubernetes.client import models as k8s

from airflow import DAG

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

dag = DAG(
    "gad_flow",
    default_args=default_args,
    schedule_interval=timedelta(minutes=30),
    max_active_runs=1,
    concurrency=10,
)
environment = [
    k8s.V1EnvVar(name="PROJECTDIR", value="value1"),
    k8s.V1EnvVar(name="key2", value="value2"),
]
volume_mount = k8s.V1VolumeMount(
    name="project-volume",
    mount_path="/opt/aiola/projects",
    sub_path=None,
    read_only=True,
)

volume = k8s.V1Volume(
    name="project-volume",
    # persistent_volume_claim=k8s.V1PersistentVolumeClaimVolumeSource(claim_name="project-volume"),
    host_path=k8s.V1HostPathVolumeSource(path="/home/docker/projects"),
)
schema_checker = KubernetesPodOperator(
    volumes=[volume],
    volume_mounts=[volume_mount],
    env_vars={"PYTHONPATH": "/opt/aiola/projects/data-utils"},
    namespace="default",
    image="gad-papermill:0.1",
    cmds=["python"],
    arguments=[
        "/opt/aiola/projects/data-utils/inspection_streaming/schema_checker_for_federation.py",
        "--table_name",
        "{{ var.value.table_to_check }}",
        "--table_schema_file_path",
        "/opt/aiola/projects/data-utils/inspection_streaming/tyson/ddb_schemas/ddb_schema_items.json",
        "--aws_region",
        "eu-west-1",
    ],
    labels={"owner": "dev"},
    image_pull_policy="Never",
    name="schema_checker",
    task_id="schema_checker-test",
    is_delete_operator_pod=True,
    get_logs=True,
    dag=dag,
)
great_expectation_task = KubernetesPodOperator(
    namespace="default",
    image="gad-ge:0.1",
    cmds=["great_expectations", "init", "--help"],
    arguments=["print('HELLO')"],
    labels={"foo": "bar"},
    image_pull_policy="Never",
    name="great_expectation_task",
    task_id="great_expectation_task",
    is_delete_operator_pod=True,
    get_logs=True,
    dag=dag,
)
dbt_task = KubernetesPodOperator(
    volumes=[volume],
    volume_mounts=[volume_mount],
    # env_vars={"DBT_PROFILES_DIR": "/opt/aiola/projects/dbt/profiles"},
    namespace="default",
    image="gad-dbt:0.1",
    cmds=["dbt", "ls"],
    arguments=[
        "--project-dir",
        "/opt/aiola/projects/strauss-dbt-poc",
        "--profiles-dir",
        "/opt/aiola/projects/strauss-dbt-poc",
    ],
    labels={"Task": "DBT"},
    image_pull_policy="Never",
    name="run_dbt",
    task_id="run_dbt",
    is_delete_operator_pod=True,
    get_logs=True,
    dag=dag,
)

schema_checker >> great_expectation_task >> dbt_task
# schema_checker.dry_run()

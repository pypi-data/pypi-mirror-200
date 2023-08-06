#!/bin/bash

# PROJECTS_DIR should point to the directory where gad projects are - usually at ~/projects
# PROJECT_NAME is the folder where airflow dags are located under the gad-deliveries directory
PROJECTS_DIR=$1
LOGS_DIR=$PROJECTS_DIR/dev-logs
PROJECT_NAME=$2

if [ -z "$PROJECTS_DIR" ]; then
    echo "PROJECTS_DIR is required as first argument"
    exit 1
fi

if [ -z "$PROJECT_NAME" ]; then
    echo "PROJECT_NAME is required as second argument"
    exit 1
fi

echo 'setting DAGS directory to point to GAD delivery folder:' $PROJECT_NAME
sed -i 's/__DEPLOYMENT_DIR__/'"$PROJECT_NAME"'/' dags-pv.yaml

kubectl apply -f dags-pv.yaml
sed -i 's/'"$PROJECT_NAME"'/__DEPLOYMENT_DIR__/' dags-pv.yaml
kubectl apply -f dags-pvc.yaml
kubectl apply -f logs-pv.yaml
kubectl apply -f logs-pvc.yaml

mkdir -p $LOGS_DIR/airflow/logs
mkdir -p $LOGS_DIR/dbt/logs

sudo chmod 777 $LOGS_DIR/airflow/logs
sudo chmod 777 $LOGS_DIR/dbt/logs


echo "installing apache-airflow chart ... this may take few minutes..."
helm install -f airflow-values.yaml airflow apache-airflow/airflow

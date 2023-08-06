docker build -t gad-airflow:0.1 . -f AirflowDockerfile
docker build -t gad-dbt:0.1 . -f DBTDockerfile
docker build -t gad-ge:0.1 . -f GEDockerfile
docker build -t gad-papermill:0.1 . -f PaperMillDockerfile

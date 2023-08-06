# GAD Infra Project

## GAD Common Utils python public package

We publish a gad_common_utils python package on [pypi](https://pypi.org/)
see [PackageReadMe.md] for details
The package is publicly available and includes [common_utils](src/common_utils) code

Infrastructure for Great Expectations, Airflow and DBT

### Deploying the package

Currently on [testpypi](https://test.pypi.org/project/gad-common-utils/0.0.2/)
To install run ```pip install -i https://test.pypi.org/simple/ gad-common-utils==0.0.2```
Build the package using the build tool:
```python -m build```
Upload via twin: ```twine upload --repository testpypi dist/*```
see [packaging-projects](https://packaging.python.org/en/latest/tutorials/packaging-projects/#)

* User: aiola.gad
* Pass: data engineers password

## Runtime Environment

## Use different containers: Airflow, DBT, GE (Great Expectation) and Papermill

Required Kubernetes installed (locally with [kind](https://kind.sigs.k8s.io/docs/user/quick-start/) or [minikube](https://minikube.sigs.k8s.io/docs/start/))

1. Airflow:`docker build -t gad-airflow:0.1 . -f AirflowDockerfile`
2. DBT:`docker build -t gad-dbt:0.1 . -f DBTDockerfile`
3. Great Expectations: `docker build -t gad-ge:0.1 . -f GEDockerfile`
4. Papermill: `docker build -t gad-papermill:0.1 . -f PaperMillDockerfile`

After you have k8s, [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl-macos/) and [helm](https://helm.sh/docs/intro/install/) installed, add the airflow helm repository:

* `helm repo add apache-airflow https://airflow.apache.org`

* `helm repo update`

* see [helm directory](helm/ReadMe.md) to install on local k8s using minikube

# Howto Run GAD

## Use AMI to run GAD dev environment with

Create a new EC2 from AMI Gad-Infra (on Aiola-Dev, Ireland).  
Make sure to choose EC2 type with at least 2 CPU and 16G memory (e.g: t2xlarge).  
On the instance you already have minikube and GAD Infra git repository.

## Local install of airflow under kubernetes using [minikube](https://minikube.sigs.k8s.io/docs/start/)

### Install Minikube

Make sure to install helm and configure the airflow repo as shown [here](../ReadMe.md)
Minikube: ```brew install minikube```

## Run the chart (EC2 or Locally)

Start minikube by cmd for the first time (or after deleting the cluster):  
```minikube start --memory=12G --cpu=max --mount-string=`pwd`'/..:/home/docker/projects' --mount=true```

* On AMI the minikube is already installed and ready, so you just need to start it `minikube start`

* If the repository is being updated it requires update of docker images, you can use [this script](../create-images.sh) to recreate them.
Then you need to load them to minikube see [script](../load-images-to-minikube.sh)

### Install the chart

* Verify the [airflow](../airflow) directory and subdirectories are with read and write permissions for all users .

From this directory, Install persistence volumes and claims, the airflow helm chart [see details](./install-airflow-chart.sh):  

* On AWS: run port-forward to enable access to Airflow UI from the internet:  ```kubectl port-forward svc/airflow-webserver hostPort:8080 --namespace default --address=0.0.0.0```  Make sure the mapped `hostPort` for airflow-webserver is opened on the Security Group of the EC2 instance.



## Cleanup

Delete the helm chart and PV/PVCs by this [script](./cleanup.sh)

* Note: to clean the entire minikube cluster run `minikube delete`

## Writing task

DAG task should use [KubernetesPodOperator](https://airflow.apache.org/docs/apache-airflow-providers-cncf-kubernetes/stable/operators.html)

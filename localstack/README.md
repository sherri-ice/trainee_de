# Project based on Localstack

Localstack (AWS emulation)  project for bikes analytics. See more on [Localstack's Github](https://github.com/localstack/localstack).

Source dataset on [Kaggle](https://www.kaggle.com/geometrein/helsinki-city-bikes).


## Prerequisites
Make sure you've installed following services:
- terraform
- docker
- make
- aws (aws-cli)

### AWS credentials
Make sure you've configured local `~/.aws/config` on Linux.

## Launch
Project uses `docker-compose` for launching Localhost, Airflow, Postgresql, Redis and Spark services.
AWS infrastructure configured via Terraform scripts. To make the launch of the project easier `make` is used.

## Build
Custom Spark and Airflow images are used, so before running project you need to build them:

```bash
make build
```

## Run
To run all docker containers; initialise and create all AWS services with Terraform, run the next command:

```bash
make run
```

## Stop

To stop all containers, run:
```bash
make down
```

_Notice: all AWS infrastructure (except Dynamodb tables) will be wiped._

## Notes about Lambda

Though `lambda` uses `numpy` and `pandas`, the special version of these packages is needed.
AWS Lambda needs version which works with AWS Linux environment. For right import you can use Layers as described [here](https://sease.io/2022/11/how-to-import-pandas-in-aws-lambda.html).


In this project all needed dependencies are stored in [dependency_packages](lambda%2Fsource%2Fdependency_packages) directory.
Please, make sure you downloaded the right ones.

- [Numpy](https://files.pythonhosted.org/packages/b6/d7/b208a4a534732e4a978003768ac7b8c14fcd4ca5b1653ce4fb4c2826f3a4/numpy-1.24.2-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl)
- [Pandas](https://files.pythonhosted.org/packages/56/73/3351beeb807dca69fcc3c4966bcccc51552bd01549a9b13c04ab00a43f21/pandas-1.5.3-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl)

Note: make sure you've deleted cache folder:
```bash
rm -r *.dist-info __pycache__
```

### Lambda distribution
For creating Lambda functions following [script](infra%2Fscripts%2Fzip_lambdas.py) zips all source Python files. 
Also script sures that zipped Lambda meets size [limits](https://lumigo.io/aws-lambda-performance-optimization/aws-lambda-limits/).

## AWS infrastructure 

![aws_services.png](docs%2Faws_services.png)


# Results:
## Airflow DAG
![airflow.png](docs%2Fairflow.png)


## AWS S3 bucket
![s3.png](docs%2Fs3.png)

## Lambda execution:
![lamda.png](docs%2Flamda.png)

## Dynamodb
Scan of helsinki_city_bikes_monthly_metrics table:
![dynamodb.png](docs%2Fdynamodb.png)

## Tableau:
![tableau.png](docs%2Ftableau.png)

build:
	docker build -t sherri-ice/airflow docker/airflow/
	docker build -t sherri-ice/postgres-spark docker/postgres-spark/

run:
	docker compose -f docker/docker-compose.yml up --build --detach
	cd infra/scripts && python3 zip_lambdas.py && cd ../..
	cd infra/terraform && terraform init && terraform apply -auto-approve

down:
	docker compose down
build:
	docker build -t sherri-ice/airflow docker/airflow/
	docker build -t sherri-ice/postgres-spark docker/postgres-spark/
	cd docker && docker compose up --build --detach
	python3 infra/scripts/zip_lambdas.py
	cd infra/terraform && terraform init && terraform apply -auto-approve

down:
	docker compose down
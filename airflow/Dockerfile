FROM apache/airflow:latest-python3.9
WORKDIR /opt/airflow/
COPY requirements.txt /opt/airflow/requirements.txt
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt
WORKDIR /

FROM apache/airflow:latest-python3.9

USER root

# Install java for spark-submit option

RUN apt-get update && \
    apt-get install -y software-properties-common && \
    apt-get install -y procps &&  \
    rm -rf /var/lib/apt/lists/* && \
    apt-get install -y gnupg2 && \
    apt-key adv --keyserver keyserver.ubuntu.com --recv-keys EB9B1D8886F44E2A && \
    add-apt-repository "deb http://security.debian.org/debian-security stretch/updates main" && \
    apt-get update && \
    apt-get install -y openjdk-8-jdk && \
    java -version $$ \
    javac -version

# Setup JAVA_HOME
ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64
RUN export JAVA_HOME


USER airflow

WORKDIR /opt/airflow/
COPY requirements.txt requirements.txt
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt



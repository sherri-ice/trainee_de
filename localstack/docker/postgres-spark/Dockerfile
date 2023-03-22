FROM bitnami/spark:latest

USER root

# Add new user to root group for proper persmission
RUN useradd -rm -d /home/ubuntu -s /bin/bash -g root -G sudo -u 1001 spark

USER spark


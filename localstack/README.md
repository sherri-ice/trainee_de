# Project based on Localstack


## Что необходимо установить заранее

- terraform
- docker
- aws (aws-cli)

Настроить credentials на aws

## Почему отдельный скрипт для раздела csv
Потому что при разработке неудобно и незачем каждый раз делить огромный csv
Но блин, что-то еще отдельно запускать...
Короче в конце сделать filesensor и пихнуть это все чудо в python operator

## S3 buckets init
Для инициализации бакетов используется terraform


## Как запускать
Поднять докер, обязательно поднять локалстек, потом терраформ запустить...

## Про окружение для лямбд
# todo: вписать в изначальный скрипт сборку всех нужных пакетов
https://files.pythonhosted.org/packages/b6/d7/b208a4a534732e4a978003768ac7b8c14fcd4ca5b1653ce4fb4c2826f3a4/numpy-1.24.2-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
wget https://files.pythonhosted.org/packages/56/73/3351beeb807dca69fcc3c4966bcccc51552bd01549a9b13c04ab00a43f21/pandas-1.5.3-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
rm -r *.dist-info __pycache__

# todo: написать скрипт который сам все билдит и запускает
# todo: как внести все в один файл .env
# todo: описать префиксы
# todo: заранее ранить лямбда зип
# todo: описать структуру вызова и поч только одна sqs на одну лямбду
https://aws.plainenglish.io/end-to-end-pipeline-mocking-with-localstack-and-airflow-mwaa-ac4f019c3a0e
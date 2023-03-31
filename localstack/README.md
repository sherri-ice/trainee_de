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


# todo: написать скрипт который сам все билдит и запускает
# todo: как внести все в один файл .env
# todo: описать префиксы
https://aws.plainenglish.io/end-to-end-pipeline-mocking-with-localstack-and-airflow-mwaa-ac4f019c3a0e
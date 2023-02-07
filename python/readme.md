# Task 1. Introduction to Python

This is an **_educational project_**. It's aimed at have a practice with simple ETL process
realisation using Python. 

## Task description:

There are two datasets:
[rooms.json](sample_data%2Frooms.json) and [students.json](sample_data%2Fstudents.json). The extraction
from json and load to database processes are need to be done.

Also program must perform 4 types of select queries:
1) Determine how many rooms are there and how many students are in each room
2) Select 5 rooms which has the lowest average age
3) Select 5 rooms which has the biggest age difference
4) Select rooms where different genders are living together

## About database
As DBMS, I chose **MySQL**. 
Let's create database `hostel` and create table `Students` and `Rooms`. Full description of necessary tables are 
stored in sql files: [create_students_table.sql](sql%2Fsql_queries%2Fcreation%2Fcreate_students_table.sql),
[create_rooms_table.sql](sql%2Fsql_queries%2Fcreation%2Fcreate_rooms_table.sql).

All queries are stored in [sql_queries](sql%2Fsql_queries) directories as sql files.


## Installing dependencies
Use pip install -r requirements.txt to install packages

## Running the code
To run the code you need to launch `main.py` file

## Python tests
All tests for this project are located in /tests/ folder. 
You can create your own tests and run them by using the following command `pytest --cov-report term-missing --cov=..`
To ignore files for testing you can amend .coveragerc file.

## Code refactoring using pre-commit
If you want to continue the development you can use .pre-commit-config.yaml to 
check and refactor your code. To do this just simply run `pre-commit run --all-files --show-diff-on-failure` in terminal.


"""Airflow DAG: scrape Reddit, load to Snowflake, run dbt daily at 6 AM UTC."""

import os
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

PROJECT_PATH = os.getenv("PROJECT_PATH", "/opt/airflow/project")
PYTHON_PATH = os.getenv("PYTHON_PATH", "python")
DBT_PATH = os.getenv("DBT_PATH", "dbt")

with DAG(
    dag_id="reddit_ai_news_pipeline",
    default_args={
        "owner": "airflow",
        "retries": 2,
        "retry_delay": timedelta(minutes=5),
    },
    description="Scrape Reddit AI posts and load to Snowflake daily",
    schedule="0 6 * * *",
    start_date=datetime(2026, 2, 1),
    catchup=False,
    tags=["reddit", "ai", "data-pipeline"],
) as dag:
    scrape_and_load = BashOperator(
        task_id="scrape_and_load",
        bash_command=f'cd "{PROJECT_PATH}/scraper" && {PYTHON_PATH} main.py',
    )

    run_dbt = BashOperator(
        task_id="run_dbt",
        bash_command=f'cd "{PROJECT_PATH}/dbt_project" && {DBT_PATH} run',
    )

    test_dbt = BashOperator(
        task_id="test_dbt",
        bash_command=f'cd "{PROJECT_PATH}/dbt_project" && {DBT_PATH} test',
    )

    scrape_and_load >> run_dbt >> test_dbt

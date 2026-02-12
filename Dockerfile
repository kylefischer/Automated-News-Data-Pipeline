FROM apache/airflow:2.10.4-python3.11

USER root
RUN apt-get update && apt-get install -y --no-install-recommends gcc && rm -rf /var/lib/apt/lists/*

USER airflow
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY --chown=airflow:root scraper/ /opt/airflow/project/scraper/
COPY --chown=airflow:root dbt_project/ /opt/airflow/project/dbt_project/
COPY --chown=airflow:root airflow/dags/ /opt/airflow/dags/
COPY --chown=airflow:root docker/dbt_profiles.yml /home/airflow/.dbt/profiles.yml

WORKDIR /opt/airflow

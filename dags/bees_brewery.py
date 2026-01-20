from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import sys
import os
import logging

# Adiciona o diretório raiz ao PYTHONPATH para encontrar o módulo 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importação das funções das camadas Medallion
from scripts.bronze_ingest import fetch_and_save_bronze
from scripts.silver_transform import process_silver
from scripts.gold_agg import aggregate_gold

# Função de monitoramento e alerta
def on_failure_callback(context):
    task_id = context.get('task_instance').task_id
    error_msg = context.get('exception')
    logging.error(f"!!! Alerta de Falha !!! Task: {task_id} | Erro: {error_msg}")
    # Aqui poderia ser integrada uma chamada para API do Slack/Teams

default_args = {
    'owner': 'Karoline',
    'depends_on_past': False,
    'start_date': datetime(2026, 1, 17),
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'on_failure_callback': on_failure_callback,
    'email_on_failure': False, # Aqui poderia ser configurado para receber no e-mail corporativo sobre falhas
}

with DAG(
    'bees_brewery',
    default_args=default_args,
    description='Pipeline Medallion para Open Brewery DB',
    schedule_interval='@daily',
    catchup=False
) as dag:

    # Setup do ambiente (Limpeza e Criação de Pastas)
    setup_directories = BashOperator(
        task_id='setup_directories',
        bash_command="""
            rm -rf /opt/airflow/data_lake/bronze/* && \
            rm -rf /opt/airflow/data_lake/silver/* && \
            rm -rf /opt/airflow/data_lake/gold/* && \
            mkdir -p /opt/airflow/data_lake/bronze \
                    /opt/airflow/data_lake/silver \
                    /opt/airflow/data_lake/gold
        """
    )

    # 1. Camada Bronze: Ingestão de dados crus (JSON)
    task_bronze = PythonOperator(
        task_id='ingest_to_bronze',
        python_callable=fetch_and_save_bronze
    )

    # 2. Camada Silver: Limpeza, Parquet e Particionamento
    task_silver = PythonOperator(
        task_id='transform_to_silver',
        python_callable=process_silver
    )

    # 3. Camada Gold: Agregação Analítica
    task_gold = PythonOperator(
        task_id='aggregate_to_gold',
        python_callable=aggregate_gold
    )

    setup_directories >> task_bronze >> task_silver >> task_gold
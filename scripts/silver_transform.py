import pandas as pd
import glob
import os
import shutil
from scripts.utils import run_data_quality_checks

def process_silver():
    # Busca os arquivos .json
    path_pattern = "/opt/airflow/data_lake/bronze/breweries_raw/*.json"
    files = glob.glob(path_pattern)
    
    if not files:
        raise FileNotFoundError(f"Nenhum arquivo JSON encontrado em {path_pattern}")

    # Lê todos os arquivos da pasta bronze (o Spark particiona o output)
    df_list = [pd.read_json(f, lines=True) for f in files]
    df = pd.concat(df_list, ignore_index=True)

    # Requisito 5.b: Transformação e Particionamento
    df['state'] = df['state'].fillna('unknown').str.lower()
    df['country'] = df['country'].fillna('unknown').str.lower()

    # REMOVER DUPLICADOS: Garante que mesmo que ocorra a leitura de arquivos repetidos, 
    # cada cervejaria só apareça uma vez com base no ID único da API.
    before_count = len(df)
    df = df.drop_duplicates(subset=['id'])
    after_count = len(df)
    
    print(f"Registros lidos: {before_count} | Após remover duplicatas: {after_count}")

    output_path = "/opt/airflow/data_lake/silver/breweries"
    
    # Limpa a pasta antes de escrever para evitar arquivos fantasmas
    if os.path.exists(output_path):
        shutil.rmtree(output_path)
    
    os.makedirs(output_path, exist_ok=True)

    # EXECUÇÃO DOS TESTES DE QUALIDADE
    # Se isto falhar, o Airflow marca a task como FAILED e não chega à Gold
    run_data_quality_checks(df)

    # Salvando em Parquet particionado
    output_path = "/opt/airflow/data_lake/silver/breweries"
    os.makedirs(output_path, exist_ok=True)
    df.to_parquet(output_path, partition_cols=['country', 'state'], index=False, engine='pyarrow')
    print("Dados transformados para Silver com sucesso!")

if __name__ == "__main__":
    process_silver()
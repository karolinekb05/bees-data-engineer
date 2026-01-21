import pandas as pd
import os
import logging

def aggregate_gold():
    silver_path = "/opt/airflow/data_lake/silver/breweries"
    
    # Lendo a Silver
    df = pd.read_parquet(silver_path)
    print(f"DEBUG: A Gold leu {len(df)} linhas da Silver")
    
    df = df.drop_duplicates()

    # Agrupamento por tipo de cervejaria, país e estado
    gold_df = df.groupby(['brewery_type', 'country', 'state'], observed=True).size().reset_index(name='brewery_count')
    
    # IMPORTANTE: O número de linhas da Gold DEVE ser menor que a Silver 
    # pois estamos agrupando (Micro + California vira uma linha só com o count)
    
    output_path = "/opt/airflow/data_lake/gold/brewery_aggregation.parquet"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Salva substituindo o arquivo anterior
    gold_df.to_parquet(output_path, index=False)
    
    logging.info(f"Camada Gold gerada. Linhas no dataframe final: {len(gold_df)}")
    print(f"Sucesso! A Gold agora tem {len(gold_df)} grupos únicos.")

if __name__ == "__main__":
    aggregate_gold()
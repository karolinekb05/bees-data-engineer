import logging
import pandas as pd

def run_data_quality_checks(df):
    """
    Conjunto de testes de qualidade para serem executados no pipeline.
    """
    logging.info("A iniciar testes de Data Quality...")

    # 1. Teste de IDs Nulos
    if df['id'].isnull().any():
        raise ValueError("Data Quality Fail: IDs nulos detetados na camada Bronze.")

    # 2. Teste de Schema (Colunas Obrigatórias)
    required_columns = ['id', 'brewery_type', 'country', 'state']
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Data Quality Fail: Coluna obrigatória {col} em falta.")

    # 3. Teste de Volume
    if len(df) == 0:
        raise ValueError("Data Quality Fail: O dataset está vazio.")

    logging.info("Testes de Data Quality passaram com sucesso!")
    return True

if __name__ == "__main__":
    run_data_quality_checks(pd.DataFrame())
import requests
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, DoubleType

def fetch_and_save_bronze():
    spark = SparkSession.builder.appName("BreweryIngestion").getOrCreate()
    
    # Schema
    schema = StructType([
        StructField("id", StringType(), True),
        StructField("name", StringType(), True),
        StructField("brewery_type", StringType(), True),
        StructField("address_1", StringType(), True),
        StructField("city", StringType(), True),
        StructField("state_province", StringType(), True),
        StructField("country", StringType(), True),
        StructField("longitude", DoubleType(), True),
        StructField("latitude", DoubleType(), True),
        StructField("state", StringType(), True),
    ])
    
    base_url = "https://api.openbrewerydb.org/v1/breweries"
    all_data = []
    page = 1

    print("Iniciando coleta...")
    while True:
        response = requests.get(f"{base_url}?page={page}&per_page=200", timeout=30)
        data = response.json()
        
        if not data: # Aqui ele para caso não retorne dados
            break
            
        # Converte tipos no Python antes do Spark
        for item in data:
            for field in ['latitude', 'longitude']:
                if item.get(field) is not None:
                    item[field] = float(item[field])
        
        all_data.extend(data)
        print(f"Página {page} coletada.")
        page += 1

    if all_data:
        df = spark.createDataFrame(all_data, schema=schema)
        output_path = "/opt/airflow/data_lake/bronze/breweries_raw"
        df.write.mode("overwrite").json(output_path)
        print("Dados salvos na Bronze!")

    spark.stop()

if __name__ == "__main__":
    fetch_and_save_bronze()
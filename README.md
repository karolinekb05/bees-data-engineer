### EN-US

# Brewery Data Pipeline - BEES Case 🍻

This project is a data pipeline solution designed to consume data from the **Open Brewery DB API**, transforming and persisting it into a data lake following the **Medallion Architecture** (Bronze, Silver, and Gold layers).

## 🏗️ Data Lake Architecture
The project implements three distinct layers to ensure data integrity and analytical readiness:

* **Bronze (Raw):** Persists raw data from the API in its native format (JSON) using PySpark.
* **Silver (Curated):** Cleans and normalizes data into a columnar format (**Parquet**), partitioned by brewery location (country/state).
* **Gold (Analytical):** Provides an aggregated view showing the **quantity of breweries per type and location**.

---

## 🛠️ Tech Stack and Design Choices
* **Orchestration:** **Apache Airflow** – Selected for its robust handling of scheduling, retries, and error handling.
* **Language:** **Python/PySpark** – Chosen for efficient data transformation and scalability.
* **Containerization:** **Docker & Docker Compose** – Used for modularization and environment consistency.

---

## 🚀 How to Run the Project

### Prerequisites
* Docker and Docker Compose installed.

### Step-by-Step Instructions
1.  **Build and start the environment:**
    ```bash
    docker-compose up --build
    ```
2.  **Access the Airflow UI:**
    * URL: `http://localhost:8080`

3.  **Activate the Pipeline:**
    * Locate the `bees_brewery` DAG and toggle it to start the sequential execution of the medallion layers.

---

## 🛡️ Error Handling and Monitoring
As per the case requirements, the pipeline includes:

* **Retries:** Ingestion tasks include automatic retry policies for API stability.
* **Data Quality:** The Silver layer validates mandatory fields and data types before proceeding to Gold.
* **Monitoring/Alerting:** In a production environment, an `on_failure_callback` would trigger alerts (Slack/Email) for pipeline failures or data quality issues.

---

## ☁️ Cloud Considerations
If deployed to a cloud environment (AWS/GCP):
* Local storage is replaced by **S3** or **GCS**.
* Credentials must be managed via **Airflow Connections** or **Secrets Manager**.

---

### PT-BR

# Brewery Data Pipeline - BEES Case 🍻
Pipeline de dados seguindo a Arquitetura Medallion (Bronze → Silver → Gold) para consumo da API Open Brewery DB, focado em escalabilidade, particionamento eficiente e qualidade de dados.

## 🏗️ Arquitetura do Data Lake
O projeto implementa três camadas distintas para garantir a integridade dos dados:

**Bronze (Raw)**: Ingestão dos dados em seu formato nativo (JSON) para garantir a persistência da fonte original sem perdas com PySpark.

**Silver (Curated)**: Limpeza e normalização dos dados. O armazenamento é feito em Parquet (colunar) com particionamento por localização (país/estado) para otimização de consultas.

**Gold (Analytical)**: Camada agregada que fornece a quantidade de cervejarias por tipo e localização, pronta para consumo por ferramentas de BI.


## 🛠️ Stack Tecnológica e Decisões

**Orquestração**: Apache Airflow – escolhido pela robustez no gerenciamento de agendamento, retentativas (retries) e tratamento de falhas.

**Linguagem**: Python/PySpark – preferência técnica para manipulação eficiente de grandes volumes de dados e transformações complexas.

**Containerização**: Docker & Docker Compose – garantem a modularização e reprodutibilidade do ambiente de execução.

## 🚀 Como Executar o Projeto

**Pré-requisitos**
Docker e Docker Compose instalados.

**Passo a Passo**
1. Construir e subir o ambiente:

    ```bash
    docker-compose up --build
    ```

2. Acessar o Airflow:

URL: `http://localhost:8080`(Login/Senha padrão definidos no compose).

3. Ativar o Pipeline:

Localize a DAG `bees_brewery` e ative-a para iniciar a execução sequencial das camadas.

## 🛡️ Tratamento de Erros e Monitoramento
Conforme exigido pelo caso, o pipeline inclui:

**Retries**: As tasks de ingestão possuem política de retentativa automática em caso de falha na API.

**Data Quality Checks**: A camada Silver valida campos obrigatórios e tipos de dados antes de prosseguir para a Gold. Se um check falhar, o pipeline é interrompido para evitar poluição da camada analítica.

**Alertas Sugeridos**: Em um ambiente produtivo (Cloud), seria implementado o envio de alertas via Slack/E-mail através de on_failure_callback no Airflow.

## ☁️ Considerações de Cloud
Caso o deploy seja realizado em nuvem (AWS/GCP/Azure):

O armazenamento local seria substituído por S3 ou GCS.

As chaves de acesso devem ser configuradas via Airflow Connections ou Secrets Manager, nunca expostas no repositório.
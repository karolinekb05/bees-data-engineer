FROM apache/airflow:2.10.4

USER root
# Instalando o Java 17
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    openjdk-17-jre-headless \
    procps && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Configuração para Mac (ARM64)
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-arm64

USER airflow

# Atualiza o pip antes de instalar os pacotes
RUN pip install --no-cache-dir --upgrade pip

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Crypto Pipeline

Pipeline de ingenierìa de datos que recolecta precios de criptomonedas en tiempo real y las procesa en una arquitectura de datos medallion (bronze, silver, gold)

## Arquitectura
## Stack tecnológico

- **Apache Airflow** — orquestación del pipeline
- **MinIO** — data lake local (compatible con S3)
- **Apache Parquet** — formato de almacenamiento columnar
- **PostgreSQL** — almacenamiento de datos procesados
- **dbt** — transformaciones SQL para capa gold
- **Metabase** — visualización y dashboards
- **Docker** — containerización de todos los servicios

## Capas de datos

| Capa | Tecnología | Descripción |
|------|------------|-------------|
| Bronze | MinIO (Parquet) | Datos crudos de la API sin transformar |
| Silver | PostgreSQL | Datos limpios y tipados por columna |
| Gold | PostgreSQL + dbt | Agregaciones diarias listas para BI |

## Monedas monitoreadas

Bitcoin, Ethereum, Solana, Cardano

## Cómo levantar el proyecto

### Requisitos
- Docker
- Docker Compose

### Pasos

1. Clonar el repositorio
2. Levantar los servicios
3. Ejecutar el DAG manualmente o esperar la ejecución automática cada hora

```bash
git clone https://github.com/rserradev/crypto-pipeline.git
cd crypto-pipeline
docker compose up -d
```

### Servicios disponibles

| Servicio | URL | Credenciales |
|----------|-----|--------------|
| Airflow | http://localhost:8080 | admin / admin |
| MinIO | http://localhost:9001 | minioadmin / minioadmin |
| Metabase | http://localhost:3000 | (configurar al entrar) |
| PostgreSQL | localhost:5432 | airflow / airflow |

## Estructura del proyecto
crypto-pipeline/
├── dags/
│   └── crypto-pipeline.py    # DAG principal de Airflow
├── dbt_project/
│   ├── models/gold/          # Modelos dbt para capa gold
│   └── profiles/             # Configuración de conexión dbt
├── postgres-init/
│   └── 01_init.sql           # Inicialización automática de la BD
├── Dockerfile                # Imagen personalizada de Airflow con dbt
└── docker-compose.yml        # Definición de todos los servicios
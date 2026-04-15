# Data Platform

Plataforma de ingeniería de datos construida en homelab con arquitectura Lakehouse. Contiene múltiples pipelines de datos orquestados con Apache Airflow.

## Arquitectura
## Stack tecnológico

- **Apache Airflow** — orquestación de pipelines
- **MinIO** — data lake local (compatible con S3)
- **Apache Parquet** — formato de almacenamiento columnar
- **PostgreSQL** — almacenamiento de datos procesados
- **Apache Spark** - procesamiento distribuido
- **dbt** — transformaciones SQL
- **Metabase** — visualización y dashboards
- **Docker** — containerización de todos los servicios

## Pipelines disponibles

| Pipeline | Dominio | Frecuencia | Descripción |
|----------|---------|------------|-------------|
| crypto_pipeline | Criptomonedas | Cada hora | Precios de Bitcoin, Ethereum, Solana y Cardano |

## Cómo levantar el proyecto

### Requisitos
- Docker
- Docker Compose

### Pasos

```bash
git clone https://github.com/rserradev/data-platform.git
cd data-platform
docker compose up -d
```
```

### Servicios disponibles

| Servicio | URL | Credenciales |
|----------|-----|--------------|
| Airflow | http://localhost:8080 | admin / admin |
| MinIO | http://localhost:9001 | minioadmin / minioadmin |
| Metabase | http://localhost:3000 | (configurar al entrar) |
| Spark UI | http://localhost:8090 | — |
| PostgreSQL | localhost:5432 | airflow / airflow |

## Estructura del proyecto
data-platform/
├── dags/                         # DAGs de Airflow
├── dbt_project/                  # Modelos dbt
│   └── models/
│       └── gold/                 # Modelos de capa gold
├── postgres-init/
│   └── 01_init.sql              # Inicialización automática de BD
├── Dockerfile                    # Imagen personalizada de Airflow
└── docker-compose.yml            # Definición de servicios
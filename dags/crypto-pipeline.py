from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from airflow.operators.bash import BashOperator
import requests
import psycopg2
import json


DB_CONN = {
    "host": "postgres",
    "port": 5432,
    "dbname": "airflow",
    "user": "airflow",
    "password": "airflow"
}

def fetch_bitcoin_price():
    # 1. Llamar a la API de CoinGecko para obtener el precio actual de Bitcoin
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "ids": "bitcoin",
    }
    response = requests.get(url, params=params, timeout=30)
    data = response.json()
    print(f"Respuesta completa: {data}")

    coin = data[0]
    print(f"Moneda: {coin['name']}")
    print(f"Precio: ${coin['current_price']}")
    print(f"Market Cap: ${coin['market_cap']}")

    # 2. Guardar en el esquema bronze.prices
    conn = psycopg2.connect(**DB_CONN)
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO bronze.prices (coin_id, raw_payload) VALUES (%s, %s)",
                ("bitcoin", json.dumps(coin))
            )
        conn.commit()
        print("Dato guardado en bronze.prices")
    finally:
        conn.close()

def transform_to_silver():
    conn = psycopg2.connect(**DB_CONN)
    try:
        with conn.cursor() as cur:
            # 1. Leer el último registro de bronze
            cur.execute("""
                SELECT raw_payload, ingested_at
                FROM bronze.prices
                ORDER BY ingested_at DESC
                LIMIT 1
            """)
            row = cur.fetchone()
            payload = row[0]
            ingested_at = row[1]

            print(f"Procesando dato de bronze: {payload['name']} - ${payload['current_price']}")

            # 2. Insertar en silver con cada campo en su columna
            cur.execute("""
                INSERT INTO silver.prices (
                    coin_id, symbol, name, price_usd,
                    market_cap_usd, volume_24h_usd,
                    price_change_24h, fetched_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                payload["id"],
                payload["symbol"],
                payload["name"],
                payload["current_price"],
                payload["market_cap"],
                payload["total_volume"],
                payload["price_change_percentage_24h"],
                ingested_at,
            ))
        conn.commit()
        print("Dato guardado en silver.prices")
    finally:
        conn.close()

with DAG(
    dag_id="crypto_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@hourly",
    catchup=False,
) as dag:

    tarea_fetch = PythonOperator(
        task_id="fetch_bitcoin_price",
        python_callable=fetch_bitcoin_price,
    )

    tarea_silver = PythonOperator(
        task_id="transform_to_silver",
        python_callable=transform_to_silver,
    )

    tarea_dbt = BashOperator(
        task_id="run_dbt",
        bash_command="cd /opt/airflow/dbt_project && dbt run --profiles-dir profiles",
    )

    # Orden de ejecución: primero fetch, luego transform
    tarea_fetch >> tarea_silver >> tarea_dbt
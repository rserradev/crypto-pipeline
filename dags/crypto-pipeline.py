from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime
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

# Lista de monedas a seguir
COINS = ["bitcoin", "ethereum", "solana", "cardano"]

def fetch_prices():
    # 1. Llamar a la API de CoinGecko para obtener el precio actual de Bitcoin
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "ids": ", ".join(COINS),
    }
    response = requests.get(url, params=params, timeout=30)
    data = response.json()
    print(f"Monedas recibidas: {len(data)}")

    # 2. Insertar cada moneda en bronze
    conn = psycopg2.connect(**DB_CONN)
    try:
        with conn.cursor() as cur:
            for coin in data:
                cur.execute(
                    "INSERT INTO bronze.prices (coin_id, raw_payload) VALUES (%s, %s)",
                    (coin["id"], json.dumps(coin))
                )
                print(f"Bronze: {coin['name']} - ${coin['current_price']}")
        conn.commit()
        print(f"Total insertado en bronze: {len(data)} monedas")
    finally:
        conn.close()

def transform_to_silver():
    conn = psycopg2.connect(**DB_CONN)
    try:
        with conn.cursor() as cur:
            # Leer los últimos registros de bronze (uno por moneda)
            cur.execute("""
                SELECT DISTINCT ON (coin_id) coin_id, raw_payload, ingested_at
                FROM bronze.prices
                ORDER BY coin_id, ingested_at DESC
            """)
            rows = cur.fetchall()
            print(f"Procesando {len(rows)} monedas desde bronze")

            for row in rows:
                coin_id, payload, ingested_at = row
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
                print(f"Silver: {payload['name']} - ${payload['current_price']}")
        conn.commit()
        print("Transformación a silver completada")
    finally:
        conn.close()

with DAG(
    dag_id="crypto_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@hourly",
    catchup=False,
) as dag:

    tarea_fetch = PythonOperator(
        task_id="fetch_prices",
        python_callable=fetch_prices,
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
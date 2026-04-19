-- Modelo gold: resumen diario de indicadores económicos
-- Incluye variación respecto al día anterior

{{ config(materialized='table', schema='bcentral') }}

SELECT
    indicador,
    serie_id,
    fecha,
    valor,
    ROUND(
        valor - LAG(valor) OVER (
            PARTITION BY indicador
            ORDER BY fecha
        ), 4
    ) AS variacion_diaria,
    ROUND(
        ((valor - LAG(valor) OVER (
            PARTITION BY indicador
            ORDER BY fecha
        )) / LAG(valor) OVER (
            PARTITION BY indicador
            ORDER BY fecha
        )) * 100, 4
    ) AS variacion_porcentual
FROM bcentral.silver_indicators
ORDER BY indicador, fecha DESC
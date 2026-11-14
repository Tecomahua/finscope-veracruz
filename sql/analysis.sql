-- Último corte y tasas por 10,000 adultos usando denominador CNBV del mismo trimestre.
SELECT periodo, adultos, sucursales, sucursales_por_10k, corresponsales, corresponsales_por_10k,
 cajeros, cajeros_por_10k, terminales, terminales_por_10k
FROM indicadores_acceso ORDER BY periodo DESC LIMIT 1;
-- Cambios de conteo trimestrales, no una prueba causal.
SELECT periodo, sucursales, sucursales-lag(sucursales) OVER (ORDER BY periodo) AS cambio_sucursales,
 cajeros, cajeros-lag(cajeros) OVER (ORDER BY periodo) AS cambio_cajeros
FROM cnbv_acceso ORDER BY periodo;
-- Establecimientos DENUE por actividad: universo distinto a las cifras de CNBV.
SELECT corte,codigo_act,actividad,sum(establecimientos) AS establecimientos
FROM denue_agregado GROUP BY corte,codigo_act,actividad ORDER BY establecimientos DESC;

# Diccionario de datos procesados

| Archivo / campo | Definición |
|---|---|
| `cnbv_acceso.csv`: `municipio_clave` | Clave INEGI de cinco dígitos; únicamente 30193. |
| `periodo` | Último día del trimestre identificado en el archivo CNBV. |
| `adultos` | Población adulta reportada por CNBV en la fila municipal del trimestre. |
| `sucursales` | Campo CNBV `Total_sucursales`, suma de sectores incluidos por esa fuente. |
| `corresponsales`, `cajeros`, `terminales` | Conteos reportados por CNBV; terminales corresponde a `Terminales_punto_de_venta`. |
| `denue_agregado.csv`: `corte` | Edición DENUE, año y mes. |
| `codigo_act`, `actividad` | Código SCIAN y descripción para clases del subsector 522. |
| `localidad_clave`, `localidad` | Clave y nombre de localidad según DENUE. |
| `establecimientos` | Conteo de registros DENUE por clase y localidad. |

Tasa = conteo × 10,000 / adultos de CNBV del mismo periodo. Las dos fuentes no deben sumarse. Los archivos brutos se excluyen del repositorio y contienen datos de contacto; el procesamiento solo publica agregados.

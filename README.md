# FinScope Veracruz

[![Tests](https://github.com/Tecomahua/finscope-veracruz/actions/workflows/tests.yml/badge.svg)](https://github.com/Tecomahua/finscope-veracruz/actions/workflows/tests.yml)

Proyecto reproducible de análisis exploratorio de infraestructura financiera en el municipio de Veracruz, Veracruz (INEGI **30193**); excluye Boca del Río (30028). Combina registros municipales de CNBV y agregados del DENUE de INEGI. Es un proyecto de portafolio, no una medición directa de la inclusión financiera de las personas.

## Resultados verificables

En el archivo CNBV utilizado, el corte más reciente **dentro del archivo** es diciembre de 2025: 82 sucursales, 469 corresponsales, 426 cajeros y 4,913 terminales punto de venta. Su denominador reportado es 508,471 adultos; las tasas respectivas son 1.61, 9.22, 8.38 y 96.62 por cada 10,000 adultos. Las 82 sucursales incluyen los sectores que CNBV integra en `Total_sucursales`.

La serie del archivo contiene 24 trimestres entre marzo de 2020 y diciembre de 2025. DENUE, con corte mayo de 2026, contiene **224 establecimientos** del subsector SCIAN 522 en el municipio, de ellos 82 clasificados como banca múltiple. Sus universos y fechas son diferentes de CNBV y **no se deben sumar ni equiparar**. Los archivos procesados solo incluyen valores agregados y nunca nombres, direcciones, teléfonos ni correos de establecimientos.

## Ejecutar

Requisitos: Python 3.11 o 3.12, conexión a Internet para descargar las fuentes; PostgreSQL 15+ para la base; Poppler para verificar el PDF censal. El tablero funciona con la biblioteca estándar de Python:

```sh
python3 src/pipeline.py --download
python3 -m unittest discover -s tests -v
python3 src/dashboard.py
```

Abrir http://127.0.0.1:8050. La descarga puede tardar; los archivos brutos se guardan en `data/raw/` (ignorado por Git). Se verifican SHA-256 fijados: si una fuente cambia, el proceso se detiene para revisión y no reemplaza silenciosamente la versión. Para reproducir una versión nueva, examinar su contenido, metadatos, diccionario y actualizar huellas conscientemente.

Para cargar PostgreSQL, crear una base y ejecutar desde la raíz (la segunda carga reemplaza los agregados en una transacción):

```sh
psql "$DATABASE_URL" -v ON_ERROR_STOP=1 -f sql/schema.sql
psql "$DATABASE_URL" -v ON_ERROR_STOP=1 -f sql/load.sql
psql "$DATABASE_URL" -v ON_ERROR_STOP=1 -f sql/analysis.sql
```

Para el cuaderno, crear un entorno virtual e instalar `pip install -r requirements.txt`; ejecutar `jupyter lab` y abrir `notebooks/01_analisis.ipynb`. El verificador opcional `python3 src/verificar_censo.py` descarga el informe censal y verifica su huella y texto.

## Contenido

- `src/pipeline.py`: descarga HTTPS, validación de huellas, extracción selectiva de CNBV y agregación DENUE.
- `data/processed/`: serie CNBV, agregados DENUE y datos para el tablero.
- `sql/`: esquema, carga idempotente, vista de tasas y consultas.
- `src/dashboard.py` y `dashboard.html`: tablero local interactivo sin dependencias web externas.
- `notebooks/`: análisis con pandas; `tests/`: controles de claves, tasas y respuesta HTTP.
- [Caso de estudio y hallazgos](docs/caso-de-estudio.md) · [Diccionario](docs/diccionario.md) · [Metodología y límites](docs/metodologia.md) · [Fuentes y verificaciones](docs/estado.md).

## Límites

La disponibilidad de infraestructura no demuestra uso ni accesibilidad efectiva; una mayor o menor concentración no identifica por sí sola demanda insatisfecha. CNBV agrega distintos tipos de institución, y DENUE tiene cobertura, clasificación y fecha distintas. Los conteos por localidad no incorporan población local ni tiempos de viaje y no permiten clasificar colonias como desatendidas. La serie y denominadores pueden reflejar revisiones o cambios metodológicos; interpretar saltos con cautela. No se dispone aquí de microdatos de uso, límites geográficos ni tasas por colonia. CNBV publicó un reporte nacional con datos al primer trimestre de 2026; esta versión no ha integrado una base municipal de ese periodo.

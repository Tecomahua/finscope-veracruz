# FinScope Veracruz

Prototipo de análisis de inclusión financiera para el municipio de Veracruz, Veracruz (clave geoestadística 30193). **Estado: incompleto; no hay indicadores financieros procesados.** El único dato incluido es la población total del Censo 2020, 607,209 habitantes. La cifra es transcrita de una publicación oficial de INEGI y no pretende representar población adulta ni actual.

## Qué funciona

- Una visualización local sin dependencias externas presenta el dato censal y el estado de las fuentes.
- `src/verificar_censo.py` descarga el informe de INEGI mediante TLS, verifica su SHA-256 y comprueba el contexto de la cifra con `pdftotext` (Poppler).
- Ejemplo de consultas y esquema PostgreSQL con restricciones de municipio.
- Cuaderno pandas que examina la única observación verificable.
- Pruebas automáticas de integridad y respuestas del servidor local.

## Ejecutar

Requiere Python 3.10 o posterior. Desde la carpeta del proyecto:

```sh
python3 -m unittest discover -s tests -v
python3 src/dashboard.py
```

Abrir http://127.0.0.1:8050. Para el cuaderno: crear un entorno virtual, instalar `pip install -r requirements.txt` y ejecutar Jupyter. Para PostgreSQL 15+, ejecutar `psql "$DATABASE_URL" -v ON_ERROR_STOP=1 -f sql/schema.sql`, después `psql "$DATABASE_URL" -v ON_ERROR_STOP=1 -f sql/analysis.sql`. Se requiere una base existente y permisos de creación. El esquema incluye únicamente la población documentada; no contiene información financiera. El esquema y la consulta fueron ejecutados con PostgreSQL 16.15. Para verificar la fuente de nuevo, con Internet y Poppler instalado: `python3 src/verificar_censo.py`.

## Fuentes y pendientes

INEGI: [México en cifras, Veracruz 30193](https://www.inegi.org.mx/app/areasgeograficas/?ag=30193) y [resultados censales 2020, página 6](https://inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/nueva_estruc/702825198367.pdf). Corte censal: 2020. Transcripción verificada el 13 de noviembre de 2026; SHA-256 del PDF: `f1b1894514515611afb2f60a76352a075f02649151f4c04b572b80790b417adb`.

[CNBV: bases de inclusión financiera](https://www.cnbv.gob.mx/Inclusi%C3%B3n/Paginas/Bases-de-Datos.aspx) y [catálogo de archivos](https://datosabiertos.cnbv.gob.mx/_layouts/mobile/view.aspx?List=668bc47c-4276-41c9-83e1-d1f8b03e88b3&RootFolder=%2FDocumentos%2FServiciosFinancieros&View=b1605cdd-db7d-48b2-820d-037051802fbc). [INEGI DENUE](https://www.inegi.org.mx/app/mapa/denue/Default.aspx) y [descarga masiva](https://inegi.org.mx/app/descarga/?p=792). Son fuentes identificadas, **no descargadas ni integradas**. El nombre de un archivo CNBV no demuestra el periodo de sus observaciones: hay que inspeccionar datos y diccionario.

La descarga CNBV desde el entorno falló por validación del certificado TLS. Faltan: descarga y validación de esquemas, limpieza real CNBV y DENUE, datos de población adulta compatibles con el periodo, carga de datos financieros a PostgreSQL, métricas de acceso, series y mapa. No se calculan tasas financieras ni se identifican zonas prioritarias. Ver [metodología](docs/metodologia.md) y [estado](docs/estado.md).

No se incluyen nombres, direcciones ni coordenadas de establecimientos ni credenciales. No cargar datos personales o tokens al repositorio.

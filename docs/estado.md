# Estado de verificación — 13 de noviembre de 2026

- INEGI confirma 607,209 habitantes en el municipio 30193 en 2020. Se descargó el informe oficial, se comprobó el texto con Poppler y se registró su SHA-256. Existe un verificador reproducible.
- Los catálogos CNBV y DENUE fueron identificados, pero sus datos y diccionarios no se obtuvieron. La descarga directa de CNBV falló al verificar la cadena del certificado TLS. No se desactivó la verificación.
- Este entorno no tenía Docker, PostgreSQL, pandas, Jupyter ni el cliente gh preinstalados. Se obtuvieron pandas y componentes oficiales de PostgreSQL en directorios temporales para verificación. El repositorio se creó en GitHub; este documento describe el estado de los datos y la implementación al momento de la publicación.
- Python estándar permite probar el dashboard y las pruebas locales; el SQL se ejecutó correctamente en PostgreSQL 16.15 temporal y la celda del cuaderno se ejecutó con pandas 2.2.3. Jupyter no se ejecutó.

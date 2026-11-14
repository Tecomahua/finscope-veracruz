# Fuentes y verificación

Consultadas el 13 de noviembre de 2026:

- [CNBV, archivo de inclusión financiera](https://datosabiertos.cnbv.gob.mx/Documentos/ServiciosFinancieros/InclusionFinanciera2026octubre.zip), SHA-256 `3f623293551ef31d95863492395bb687f2c8dac601bd8b55db2673b6819b2722`. Aunque su nombre dice octubre de 2026, el contenido descargado incluye archivos anuales hasta 2025 y el corte más reciente observado es diciembre de 2025. No se afirma que sea la edición más reciente disponible de CNBV. Los periodos y nombres se validaron dentro de ZIP anidados.
- [INEGI, DENUE Veracruz CSV](https://www.inegi.org.mx/contenidos/masiva/denue/denue_30_csv.zip), [catálogo de descarga](https://www.inegi.org.mx/app/descarga/?ag=30), edición mayo 2026, SHA-256 `3295a498b87bb37a426c34b77470458af5374ffd613b6bad38a5f6e6335f69f5`. Metadatos del ZIP indican 20 de mayo de 2026. La extracción lee `cp1252` y filtra las claves oficiales.
- [INEGI, Censo 2020](https://www.inegi.org.mx/app/areasgeograficas/?ag=30193), 607,209 personas. [Informe oficial](https://inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/nueva_estruc/702825198367.pdf), SHA-256 `f1b1894514515611afb2f60a76352a075f02649151f4c04b572b80790b417adb`.

El servidor CNBV omitió un certificado intermedio. Se incluyó el intermedio público de GlobalSign obtenido desde la URL declarada por el certificado del servidor, validado contra las autoridades del sistema y fijado por SHA-256. El cliente mantiene la verificación de cadena y nombre de servidor. Ver `src/certs/`.

Verificación: extracción de 24 trimestres y 224 registros agregados DENUE, pruebas unitarias e integración HTTP; ejecución de todas las celdas de código con pandas 2.2.3; esquema, carga repetida y consultas en PostgreSQL 16.15; filtros interactivos en navegador. No se ejecutó JupyterLab como interfaz. No se han validado datos con trabajo de campo, y no se considera el tablero un producto de producción.

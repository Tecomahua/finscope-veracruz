# Metodología

## Alcance y fuentes

La unidad de análisis es el municipio INEGI 30193; se filtra `Clave_Municipio` en CNBV y `cve_ent=30`, `cve_mun=193` en DENUE. No se usa la zona metropolitana ni Boca del Río (30028). CNBV ofrece indicadores de infraestructura reportados por entidades reguladas. Se toma la serie 2020–2025 del archivo fijado. Cada trimestre se identifica por el año del archivo anual y el mes del archivo trimestral; cuando existe `Clave_Periodo`, se contrasta. Se requiere una sola fila municipal por periodo y 24 trimestres únicos.

DENUE es un directorio de unidades económicas; se selecciona el subsector SCIAN 522 y se agregan conteos por clase de actividad y clave de localidad. Se leen pero no se escriben datos de identificación o contacto de establecimientos. El ZIP nacional por estado permanece fuera de Git. Pueden existir registros con distintas fechas individuales de alta: el corte es la edición 05/2026, no una fecha de visita verificada.

## Tasas y lectura

Para cada trimestre: conteo de infraestructura / `Poblacion_adulta` reportada en la misma fila CNBV × 10,000. No sustituimos este denominador por el total del Censo 2020. El censo proporciona contexto independiente: 607,209 habitantes totales en 2020. Las tasas se redondean a dos decimales. El denominador adulto cambia entre años, por lo que no toda variación en tasas representa variación en conteos. Los reportes pueden revisarse y las definiciones de CNBV cambiar; examinar el diccionario y las notas oficiales antes de afirmar tendencias causales o comparar periodos.

## Oportunidades de investigación

Los agregados por localidad pueden orientar preguntas para trabajo de campo: verificar cobertura real, condiciones de atención, demanda, accesibilidad y conectividad. No hay población o geometrías por localidad incorporadas, así que no se clasifican zonas desatendidas ni se construye un índice de oportunidad. La serie de infraestructura tampoco indica tenencia o uso de productos.

## Diferencias entre fuentes

Sucursales CNBV comprenden banca comercial y de desarrollo, cooperativas y microfinancieras del universo reportado; DENUE clasifica unidades económicas por actividad y no es un censo de todos los cajeros o corresponsales. La igualdad numérica de dos conteos de 82 en diferentes fuentes/cortes es coincidencia y no evidencia equivalencia. Los datos de 2025 y 2026 no son simultáneos. Cada fuente tiene cobertura, actualizaciones y posibles errores propios.

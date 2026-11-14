# Caso de estudio: infraestructura financiera en Veracruz

## Pregunta y alcance

¿Cómo cambió la infraestructura financiera reportada en el municipio de Veracruz y qué preguntas conviene investigar después? Se usa únicamente la clave 30193, no la zona metropolitana. Los indicadores describen oferta registrada, no el acceso efectivo de las personas.

## Hallazgos

| Indicador CNBV | Marzo 2020 | Diciembre 2025 | Cambio en conteo |
|---|---:|---:|---:|
| Sucursales | 104 | 82 | −22 |
| Corresponsales | 492 | 469 | −23 |
| Cajeros | 378 | 426 | +48 |
| Terminales punto de venta | 11,614 | 4,913 | −6,701 |

Fuente: `data/processed/cnbv_acceso.csv`, derivado de los archivos trimestrales municipales de CNBV. Son puntos de inicio y fin, no una descripción de todos los cambios intermedios. La reducción observada en terminales amerita revisar definiciones, revisiones y cobertura antes de atribuirla a una causa. El denominador de población adulta reportado por CNBV cambia de 461,746 a 508,471 entre esos cortes; por tanto, los cambios en tasas y conteos no son intercambiables.

En la edición DENUE de mayo de 2026 se identificaron 224 registros del subsector 522 en el municipio; 82 se clasifican como banca múltiple. De estos últimos, 66 corresponden a la localidad Veracruz y 13 a Valente Díaz. Estos conteos describen registros clasificados en DENUE, no una medida de distancia o de demanda. La coincidencia de 82 con el conteo CNBV de sucursales no demuestra equivalencia: las fuentes tienen universos y cortes distintos.

## Recomendaciones para una siguiente investigación

1. Revisar las notas y revisiones de CNBV sobre terminales para determinar si la caída observada refleja cambios reales o de medición.
2. Integrar población y geometrías por localidad, y medir distancia o tiempos de viaje, antes de priorizar zonas.
3. Validar con visitas y entrevistas disponibilidad, horarios, accesibilidad y demanda. Ninguna de estas fuentes por sí sola permite concluir que una localidad está desatendida.

## Alcance temporal

El archivo CNBV procesado llega a diciembre de 2025. Existe un [reporte CNBV con datos nacionales al primer trimestre de 2026](https://www.cnbv.gob.mx/Inclusi%C3%B3n/BasesDeDatos/ReporteTrimestralBDIF_202603.pdf); no se ha integrado una base municipal equivalente para ese corte. No presentar diciembre de 2025 como el dato más reciente publicado por CNBV.

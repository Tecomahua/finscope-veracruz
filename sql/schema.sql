BEGIN;
CREATE TABLE IF NOT EXISTS population (
 municipality_code char(5) NOT NULL CHECK (municipality_code = '30193'), indicator text NOT NULL,
 period integer NOT NULL, value integer NOT NULL CHECK (value>0), source_url text NOT NULL,
 PRIMARY KEY (municipality_code,indicator,period)
);
INSERT INTO population VALUES ('30193','poblacion_total',2020,607209,'https://www.inegi.org.mx/app/areasgeograficas/?ag=30193') ON CONFLICT DO NOTHING;
CREATE TABLE IF NOT EXISTS cnbv_acceso (
 municipio_clave char(5) NOT NULL CHECK (municipio_clave='30193'), periodo date NOT NULL,
 adultos integer NOT NULL CHECK (adultos>0), sucursales integer NOT NULL CHECK (sucursales>=0),
 corresponsales integer NOT NULL CHECK (corresponsales>=0), cajeros integer NOT NULL CHECK (cajeros>=0),
 terminales integer NOT NULL CHECK (terminales>=0), PRIMARY KEY (municipio_clave,periodo)
);
CREATE TABLE IF NOT EXISTS denue_agregado (
 municipio_clave char(5) NOT NULL CHECK (municipio_clave='30193'), corte text NOT NULL,
 codigo_act char(6) NOT NULL CHECK (codigo_act LIKE '522%'), actividad text NOT NULL,
 localidad_clave char(4) NOT NULL, localidad text NOT NULL, establecimientos integer NOT NULL CHECK (establecimientos>0),
 PRIMARY KEY (municipio_clave,corte,codigo_act,localidad_clave)
);
CREATE OR REPLACE VIEW indicadores_acceso AS
SELECT *, round(sucursales::numeric*10000/adultos,2) AS sucursales_por_10k,
 round(corresponsales::numeric*10000/adultos,2) AS corresponsales_por_10k,
 round(cajeros::numeric*10000/adultos,2) AS cajeros_por_10k,
 round(terminales::numeric*10000/adultos,2) AS terminales_por_10k
FROM cnbv_acceso;
COMMIT;

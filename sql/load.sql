-- Ejecutar desde la raíz del proyecto con psql -v ON_ERROR_STOP=1.
BEGIN;
CREATE TEMP TABLE stage_cnbv (LIKE cnbv_acceso INCLUDING ALL) ON COMMIT DROP;
CREATE TEMP TABLE stage_denue (LIKE denue_agregado INCLUDING ALL) ON COMMIT DROP;
\copy stage_cnbv FROM 'data/processed/cnbv_acceso.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8')
\copy stage_denue FROM 'data/processed/denue_agregado.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8')
DO $$ BEGIN
 IF (SELECT count(*) FROM stage_cnbv) <> 24 OR NOT EXISTS (SELECT 1 FROM stage_denue) THEN
  RAISE EXCEPTION 'Datos incompletos; no se actualizó la base';
 END IF;
END $$;
DELETE FROM cnbv_acceso; INSERT INTO cnbv_acceso SELECT * FROM stage_cnbv;
DELETE FROM denue_agregado; INSERT INTO denue_agregado SELECT * FROM stage_denue;
COMMIT;

BEGIN;
CREATE TABLE IF NOT EXISTS population (
  municipality_code char(5) NOT NULL CHECK (municipality_code = '30193'),
  indicator text NOT NULL CHECK (indicator = 'poblacion_total'),
  period integer NOT NULL CHECK (period = 2020),
  value integer NOT NULL CHECK (value > 0),
  source_url text NOT NULL,
  PRIMARY KEY (municipality_code, indicator, period)
);
INSERT INTO population VALUES ('30193', 'poblacion_total', 2020, 607209, 'https://www.inegi.org.mx/app/areasgeograficas/?ag=30193')
ON CONFLICT (municipality_code, indicator, period) DO UPDATE SET value=EXCLUDED.value, source_url=EXCLUDED.source_url;
COMMIT;

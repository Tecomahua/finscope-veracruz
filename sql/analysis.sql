-- No usar como denominador de población adulta ni como población actual.
SELECT municipality_code, indicator, period, value, source_url
FROM population WHERE municipality_code = '30193' AND period = 2020;

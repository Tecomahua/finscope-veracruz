import csv
import importlib.util
import io
import json
import tempfile
import threading
import unittest
import zipfile
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import urlopen
from http.server import ThreadingHTTPServer

ROOT=Path(__file__).resolve().parents[1]
def module(name):
    spec=importlib.util.spec_from_file_location(name,ROOT/f'src/{name}.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
pipeline=module('pipeline');dashboard=module('dashboard')

class ProjectTests(unittest.TestCase):
    def test_denue_filtro_municipal_y_actividad(self):
        source='cve_ent,cve_mun,codigo_act,nombre_act,cve_loc,localidad,telefono\n30,193,522110,Banca,0001,Veracruz,123\n30,028,522110,Banca,0001,Boca,456\n30,193,541110,Otro,0001,Veracruz,789\n'
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'fixture.zip'
            with zipfile.ZipFile(p,'w') as z:z.writestr('conjunto_de_datos/denue_inegi_30_.csv',source)
            result=pipeline.read_denue(p)
        self.assertEqual(len(result),1);self.assertEqual(result[0]['establecimientos'],1)
        self.assertEqual(result[0]['municipio_clave'],'30193');self.assertNotIn('telefono',result[0])
    def test_serie_y_denominadores(self):
        with (ROOT/'data/processed/cnbv_acceso.csv').open(encoding='utf-8',newline='') as f: rows=list(csv.DictReader(f))
        self.assertEqual(len(rows),24);self.assertEqual(len({r['periodo'] for r in rows}),24)
        self.assertTrue(all(r['municipio_clave']=='30193' and int(r['adultos'])>0 for r in rows))
        latest=rows[-1];self.assertEqual((latest['periodo'],latest['sucursales'],latest['corresponsales'],latest['cajeros']),('2025-12-31','82','469','426'))
        self.assertAlmostEqual(int(latest['sucursales'])*10000/int(latest['adultos']),1.61,places=2)
    def test_dashboard_y_datos_http(self):
        server=ThreadingHTTPServer(('127.0.0.1',0),dashboard.Handler);thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        try:
            root=f'http://127.0.0.1:{server.server_port}'
            with urlopen(root+'/') as res:self.assertIn('Inclusión financiera',res.read().decode())
            with urlopen(root+'/data') as res:
                data=json.load(res);self.assertEqual(data['cnbv'][-1]['municipio_clave'],'30193');self.assertEqual(sum(x['establecimientos'] for x in data['denue']),224)
            with self.assertRaises(HTTPError) as e:urlopen(root+'/../README.md')
            self.assertEqual(e.exception.code,404)
        finally:server.shutdown();server.server_close();thread.join()

if __name__=='__main__':unittest.main()

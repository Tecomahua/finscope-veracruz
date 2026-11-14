import csv
import importlib.util
import threading
import unittest
from pathlib import Path
from urllib.request import urlopen
from urllib.error import HTTPError
from http.server import ThreadingHTTPServer

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('dashboard', ROOT / 'src/dashboard.py')
dashboard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dashboard)

class TestProject(unittest.TestCase):
    def test_scope_and_census(self):
        with (ROOT / 'data/processed/poblacion.csv').open(encoding='utf-8', newline='') as f:
            rows = list(csv.DictReader(f))
        self.assertEqual(len(rows), 1)
        self.assertEqual((rows[0]['municipio_clave'], rows[0]['periodo'], rows[0]['valor']), ('30193', '2020', '607209'))
    def test_dashboard_http(self):
        server = ThreadingHTTPServer(('127.0.0.1', 0), dashboard.Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            with urlopen(f'http://127.0.0.1:{server.server_port}/') as res:
                html = res.read().decode('utf-8')
                self.assertEqual(res.status, 200)
                self.assertIn('607,209', html)
                self.assertIn('no se han descargado', html)
            with self.assertRaises(HTTPError) as error:
                urlopen(f'http://127.0.0.1:{server.server_port}/missing')
            self.assertEqual(error.exception.code, 404)
        finally:
            server.shutdown()
            server.server_close()
            thread.join()

if __name__ == '__main__':
    unittest.main()

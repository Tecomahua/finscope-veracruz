"""Local, dependency-free presentation of verified data; no external requests."""
from csv import DictReader
from html import escape
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def render():
    with (ROOT / 'data/processed/poblacion.csv').open(encoding='utf-8', newline='') as f:
        rows = list(DictReader(f))
    if len(rows) != 1 or rows[0]['municipio_clave'] != '30193':
        raise ValueError('Se esperaba una sola observación del municipio 30193')
    row = rows[0]
    value = f"{int(row['valor']):,}"
    return f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>FinScope Veracruz</title><style>body{{font:16px system-ui;background:#f1f6f6;color:#183637;margin:0}}main{{max-width:850px;margin:auto;padding:3rem 1.5rem}}.tag{{color:#14776c;font-weight:700}}h1{{font-size:clamp(2rem,6vw,3.5rem);margin:.4rem 0}}.card{{background:white;border:1px solid #d5e5e2;border-radius:16px;padding:1.5rem;margin:1rem 0}}strong.number{{font-size:3rem;color:#087568}}.warn{{border-left:5px solid #d39c30}}a{{color:#075f58}}li{{margin:.6rem 0}}</style></head><body><main><div class="tag">FINSCOPE / MUNICIPIO 30193</div><h1>Veracruz, Veracruz</h1><p>Exploración de inclusión financiera · Prototipo</p><section class="card"><div>Población total · Censo {escape(row['periodo'])}</div><strong class="number">{value}</strong><p>Personas residentes. No es población adulta ni una estimación actual.</p><a href="{escape(row['fuente_url'], quote=True)}">Fuente: INEGI, México en cifras</a></section><section class="card warn"><h2>Datos financieros pendientes</h2><p>Las bases CNBV y DENUE todavía no se han descargado ni validado. No hay métricas de sucursales, cajeros, corresponsales ni conclusiones de oportunidad.</p></section><section class="card"><h2>Alcance</h2><ul><li>Municipio de Veracruz, clave 30193; excluye Boca del Río.</li><li>El acceso potencial no demuestra uso de servicios financieros.</li><li>Las cifras censales y financieras necesitan fechas y denominadores compatibles.</li></ul></section></main></body></html>'''

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != '/':
            self.send_error(404)
            return
        body = render().encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

if __name__ == '__main__':
    print('FinScope: http://127.0.0.1:8050', flush=True)
    ThreadingHTTPServer(('127.0.0.1', 8050), Handler).serve_forever()

"""Servidor local del tablero. Solo sirve archivos conocidos del proyecto."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
ROUTES={'/':(ROOT/'src/dashboard.html','text/html; charset=utf-8'),'/data':(ROOT/'data/processed/dashboard.json','application/json; charset=utf-8')}

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        route=ROUTES.get(self.path)
        if not route:
            self.send_error(404);return
        try: body=route[0].read_bytes()
        except FileNotFoundError:
            self.send_error(503,'Datos no disponibles; ejecutar pipeline');return
        self.send_response(200)
        self.send_header('Content-Type',route[1]);self.send_header('Content-Length',str(len(body)))
        self.send_header('X-Content-Type-Options','nosniff');self.end_headers();self.wfile.write(body)

if __name__=='__main__':
    print('FinScope: http://127.0.0.1:8050',flush=True)
    ThreadingHTTPServer(('127.0.0.1',8050),Handler).serve_forever()

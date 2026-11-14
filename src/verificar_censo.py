"""Descarga y verifica el informe censal oficial; no modifica el dato transcrito."""
import hashlib
import re
import subprocess
import tempfile
from pathlib import Path
from urllib.request import urlopen

URL = 'https://inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/nueva_estruc/702825198367.pdf'
EXPECTED_SHA256 = 'f1b1894514515611afb2f60a76352a075f02649151f4c04b572b80790b417adb'

def main():
    with tempfile.TemporaryDirectory() as tmp:
        pdf = Path(tmp) / 'censo.pdf'
        with urlopen(URL, timeout=90) as response, pdf.open('wb') as target:
            while chunk := response.read(1024 * 1024):
                target.write(chunk)
        digest = hashlib.sha256(pdf.read_bytes()).hexdigest()
        if digest != EXPECTED_SHA256:
            raise ValueError(f'El informe cambió: SHA-256 {digest}; revisar antes de usar')
        text = subprocess.check_output(['pdftotext', '-layout', str(pdf), '-'], text=True)
        if not re.search(r'municipio de Veracruz el más poblado\s+con 607\s+209 habitantes', text):
            raise ValueError('No se encontró la cifra en el contexto esperado')
        print('Informe INEGI verificado:', digest)
        print('Municipio de Veracruz, población total 2020: 607209')

if __name__ == '__main__':
    main()

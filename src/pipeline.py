"""Descarga, verifica y agrega datos públicos sin conservar datos de establecimientos."""
import argparse
import calendar
import csv
import hashlib
import io
import json
import re
import ssl
import urllib.request
import zipfile
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'data' / 'raw'
OUT = ROOT / 'data' / 'processed'
SOURCES = {
    'cnbv.zip': ('https://datosabiertos.cnbv.gob.mx/Documentos/ServiciosFinancieros/InclusionFinanciera2026octubre.zip', '3f623293551ef31d95863492395bb687f2c8dac601bd8b55db2673b6819b2722'),
    'denue_30_csv.zip': ('https://www.inegi.org.mx/contenidos/masiva/denue/denue_30_csv.zip', '3295a498b87bb37a426c34b77470458af5374ffd613b6bad38a5f6e6335f69f5'),
}
CERT_SHA = '20ab099881f1a46dd93b360ba3fd28fba95d37e36067e85e79db0ede29a5e963'
MONTHS = {'marzo': 3, 'junio': 6, 'septiembre': 9, 'diciembre': 12}
FIELDS = {'adultos':'Poblacion_adulta','sucursales':'Total_sucursales','corresponsales':'Corresponsales','cajeros':'Cajeros','terminales':'Terminales_punto_de_venta'}

def digest(path):
    with path.open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()

def download():
    RAW.mkdir(parents=True, exist_ok=True)
    context = ssl.create_default_context()
    cert = ROOT / 'src/certs/globalsign-ov-2018.pem'
    if digest(cert) != CERT_SHA:
        raise ValueError('Cambió el certificado intermedio fijado')
    context.load_verify_locations(cafile=str(cert))
    for name, (url, expected) in SOURCES.items():
        path = RAW / name
        if path.exists() and digest(path) == expected:
            continue
        tmp = path.with_suffix('.download')
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent':'FinScope-Veracruz/1.0 (+https://github.com/Tecomahua/finscope-veracruz)'}), timeout=180, context=context) as response, tmp.open('wb') as dst:
                while chunk := response.read(1024 * 1024):
                    dst.write(chunk)
            if digest(tmp) != expected:
                raise ValueError(f'{name}: SHA-256 inesperado; revisar versión de fuente')
            tmp.replace(path)
        finally:
            tmp.unlink(missing_ok=True)

def read_cnbv(path):
    records=[]
    with zipfile.ZipFile(path) as outer:
        for year in range(2020, 2026):
            with zipfile.ZipFile(io.BytesIO(outer.read(f'InclusionFinanciera/{year}.zip'))) as annual:
                for member in annual.namelist():
                    match=re.search(r'(Marzo|Junio|Septiembre|Diciembre).*?20\d\d', member, re.I)
                    if not match or not member.lower().endswith('.zip'):
                        continue
                    month=MONTHS[match.group(1).lower()]
                    with zipfile.ZipFile(io.BytesIO(annual.read(member))) as quarter:
                        files=[n for n in quarter.namelist() if 'bd acceso mun' in n.lower() and n.lower().endswith('.csv')]
                        if len(files)!=1:
                            raise ValueError(f'Archivo municipal ambiguo en {member}')
                        raw=quarter.read(files[0])
                        try: text=raw.decode('utf-8-sig')
                        except UnicodeDecodeError: text=raw.decode('cp1252')
                        reader=csv.DictReader(io.StringIO(text))
                        if not {'Clave_Municipio','Clave_Estado',*FIELDS.values()}.issubset(reader.fieldnames or []):
                            raise ValueError(f'Esquema incompatible: {member}')
                        matches=[r for r in reader if r['Clave_Municipio'].strip()=='30193']
                        if len(matches)!=1 or matches[0]['Clave_Estado'].strip() not in ('30','030'):
                            raise ValueError(f'Clave municipal ambigua: {member}')
                        row=matches[0]
                        period=f'{year}-{month:02d}-{calendar.monthrange(year,month)[1]}'
                        if row.get('Clave_Periodo') and row['Clave_Periodo'].strip() != f'{year}{month:02d}':
                            raise ValueError(f'Periodo inconsistente en {member}')
                        numbers={k:int(row[v]) for k,v in FIELDS.items()}
                        if numbers['adultos']<=0 or any(v<0 for v in numbers.values()):
                            raise ValueError('Valor inválido')
                        records.append({'municipio_clave':'30193','periodo':period,**numbers})
    records.sort(key=lambda x:x['periodo'])
    if len(records)!=24 or len({r['periodo'] for r in records})!=24:
        raise ValueError('Se esperaban 24 trimestres únicos de 2020 a 2025')
    return records

def read_denue(path):
    counts=Counter()
    with zipfile.ZipFile(path) as archive:
        name='conjunto_de_datos/denue_inegi_30_.csv'
        with io.TextIOWrapper(archive.open(name),encoding='cp1252',newline='') as f:
            reader=csv.DictReader(f)
            expected={'cve_ent','cve_mun','codigo_act','nombre_act','cve_loc','localidad'}
            if not expected.issubset(reader.fieldnames or []): raise ValueError('Esquema DENUE incompatible')
            for row in reader:
                if row['cve_ent']=='30' and row['cve_mun']=='193' and row['codigo_act'].startswith('522'):
                    counts[(row['codigo_act'],row['nombre_act'],row['cve_loc'],row['localidad'].strip())]+=1
    if not counts: raise ValueError('No hay observaciones DENUE para Veracruz')
    return [{'municipio_clave':'30193','corte':'2026-05','codigo_act':code,'actividad':name,'localidad_clave':loc,'localidad':label,'establecimientos':count} for (code,name,loc,label),count in sorted(counts.items())]

def write_csv(path, records):
    with path.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(records[0]),lineterminator='\n');w.writeheader();w.writerows(records)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--download',action='store_true');args=parser.parse_args()
    if args.download: download()
    for name,(_,expected) in SOURCES.items():
        path=RAW / name
        if not path.exists() or digest(path)!=expected: raise ValueError(f'{name}: archivo ausente o SHA-256 diferente')
    cnbv=read_cnbv(RAW/'cnbv.zip');denue=read_denue(RAW/'denue_30_csv.zip')
    OUT.mkdir(parents=True,exist_ok=True)
    write_csv(OUT/'cnbv_acceso.csv',cnbv);write_csv(OUT/'denue_agregado.csv',denue)
    (OUT/'dashboard.json').write_text(json.dumps({'cnbv':cnbv,'denue':denue},ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8')
    print(f'CNBV: {len(cnbv)} trimestres; DENUE: {sum(x["establecimientos"] for x in denue)} establecimientos agrupados')

if __name__=='__main__': main()

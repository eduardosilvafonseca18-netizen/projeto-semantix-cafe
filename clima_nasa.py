"""Coleta clima anual de um ponto próximo à sede de Espera Feliz, opcional.

Execute com acesso à API NASA POWER. Nunca trate o ponto como observação de
talhões ou como prova da causa da produtividade municipal.
"""
import csv
import json
import urllib.request
from pathlib import Path

ROOT = Path(__file__).parent
URL = ('https://power.larc.nasa.gov/api/temporal/daily/point?'
       'parameters=PRECTOTCORR,T2M&community=AG&longitude=-41.91&'
       'latitude=-20.65&start=20140101&end=20241231&format=JSON')


def run(json_path=None):
    if json_path:
        data = json.loads(Path(json_path).read_text(encoding='utf-8'))
    else:
        request = urllib.request.Request(URL, headers={'User-Agent': 'Semantix-Cafe/1.0'})
        with urllib.request.urlopen(request, timeout=120) as response:
            data = json.load(response)
    parameter = data['properties']['parameter']
    rain, temperature = parameter['PRECTOTCORR'], parameter['T2M']
    result = []
    for year in range(2014, 2025):
        days = sorted(k for k in rain if k.startswith(str(year)) and k in temperature)
        usable = [(rain[k], temperature[k]) for k in days
                  if isinstance(rain[k], (int, float)) and isinstance(temperature[k], (int, float))
                  and rain[k] > -900 and temperature[k] > -900]
        if len(usable) < 330:
            raise ValueError(f'Cobertura insuficiente de {year}: {len(usable)} dias válidos')
        result.append({'ano': year, 'precipitacao_mm_ano': round(sum(p for p, _ in usable), 1),
                       'temperatura_media_c': round(sum(t for _, t in usable) / len(usable), 2),
                       'dias_validos': len(usable), 'latitude': -20.65, 'longitude': -41.91})
    path = ROOT / 'dados' / 'clima_ponto_espera_feliz_2014_2024.csv'
    with path.open('w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, result[0].keys()); writer.writeheader(); writer.writerows(result)
    print(f'{len(result)} anos: {path}')


if __name__ == '__main__':
    import sys
    run(sys.argv[1] if len(sys.argv) > 1 else None)

"""Coleta e analisa a PAM/SIDRA 1613 para café arábica (2014–2024)."""
import csv
import json
import math
import urllib.request
from pathlib import Path

ROOT = Path(__file__).parent
BASE = 'https://apisidra.ibge.gov.br/values/t/1613'
# 216 área colhida (ha), 214 quantidade (t), 112 rendimento (kg/ha), 215 valor (mil R$).
QUERIES = {
    'ufs': f'{BASE}/n3/31,32,35/v/216,214,112,215/p/2014-2024/c82/31619?formato=json',
    'espera_feliz': f'{BASE}/n6/3124203/v/216,214,112,215/p/2014-2024/c82/31619?formato=json',
}
FIELDS = {'216':'area_colhida_ha','214':'producao_t','112':'rendimento_kg_ha','215':'valor_mil_reais'}

def fetch(url):
    request=urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0 (projeto educacional)'})
    with urllib.request.urlopen(request, timeout=90) as response:
        return json.load(response)

def number(v):
    return float(v) if v not in ('..','-','...','X','') else None

def run():
    raw={}; joined={}
    for scope,url in QUERIES.items():
        data=fetch(url)
        raw[scope]=data
        for item in data[1:]:
            key=(scope,item['D1C'],int(item['D3C']))
            row=joined.setdefault(key,{'escala':scope,'codigo_ibge':item['D1C'],'localidade':item['D1N'],'ano':int(item['D3C'])})
            if item['D2C'] in FIELDS:
                row[FIELDS[item['D2C']]]=number(item['V'])
    (ROOT/'dados'/'fonte_sidra.json').write_text(json.dumps({'consultas':QUERIES,'dados':raw},ensure_ascii=False,indent=2),encoding='utf-8')
    rows=sorted(joined.values(),key=lambda x:(x['escala'],x['codigo_ibge'],x['ano']))
    for r in rows:
        area,prod,val=(r.get(k) for k in ('area_colhida_ha','producao_t','valor_mil_reais'))
        r['sacas_60kg']=round(prod*1000/60,2) if prod is not None else None
        r['sacas_ha']=round(prod*1000/60/area,2) if prod is not None and area and area>0 else None
        r['valor_implicito_reais_saca']=round(val*1000/r['sacas_60kg'],2) if val is not None and r['sacas_60kg'] and r['sacas_60kg']>0 else None
    keys=['escala','codigo_ibge','localidade','ano','area_colhida_ha','producao_t','rendimento_kg_ha','valor_mil_reais','sacas_60kg','sacas_ha','valor_implicito_reais_saca']
    with (ROOT/'dados'/'cafe_arabica_2014_2024.csv').open('w',newline='',encoding='utf-8-sig') as f:
        writer=csv.DictWriter(f,fieldnames=keys);writer.writeheader();writer.writerows(rows)
    for r in rows:
        if r['ano'] in (2014,2023,2024):
            print(r['localidade'],r['ano'],r['sacas_ha'],r['producao_t'],r['valor_implicito_reais_saca'])
    valid=[r for r in rows if r['sacas_ha'] is not None]
    print('rows',len(rows),'valid productivity',len(valid),'missing',len(rows)-len(valid))
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
        fig,ax=plt.subplots(figsize=(10,4.4))
        for name,group in _groups(valid).items():
            ax.plot([v['ano'] for v in group],[v['sacas_ha'] for v in group],marker='o',label=name)
        ax.set(title='Café arábica: produtividade por localidade',xlabel='Ano',ylabel='Sacas de 60 kg por hectare');ax.legend(ncol=2);ax.grid(alpha=.2)
        fig.tight_layout();fig.savefig(ROOT/'graficos'/'produtividade.png',dpi=160);plt.close(fig)
        fig,ax=plt.subplots(figsize=(10,4.4))
        for name,group in _groups(rows).items():
            group=[v for v in group if v['producao_t'] is not None]
            ax.plot([v['ano'] for v in group],[v['producao_t']/1000 for v in group],marker='o',label=name)
        ax.set(title='Produção de café arábica (mil toneladas)',xlabel='Ano',ylabel='Mil toneladas');ax.legend(ncol=2);ax.grid(alpha=.2)
        fig.tight_layout();fig.savefig(ROOT/'graficos'/'producao.png',dpi=160);plt.close(fig)
    except ImportError:
        print('Instale matplotlib para gerar os gráficos.')

def _groups(rows):
    d={}
    for row in rows:d.setdefault(row['localidade'],[]).append(row)
    return d

if __name__=='__main__':run()

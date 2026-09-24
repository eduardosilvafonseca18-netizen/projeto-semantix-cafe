"""Corrige o valor da produção pelo IPCA anual, com base em dezembro de 2024.

As taxas são as variações anuais publicadas pelo IBGE. Para o valor agregado
de cada ano, dezembro é uma aproximação explícita da data de referência.
"""
import csv
from pathlib import Path

ROOT = Path(__file__).parent
TAXAS = {
    2015: 10.67, 2016: 6.29, 2017: 2.95, 2018: 3.75, 2019: 4.31,
    2020: 4.52, 2021: 10.06, 2022: 5.79, 2023: 4.62, 2024: 4.83,
}


def fator_para_2024(ano):
    if ano not in range(2014, 2025):
        raise ValueError('Recorte do IPCA: 2014–2024')
    fator = 1.0
    for seguinte in range(ano + 1, 2025):
        fator *= 1 + TAXAS[seguinte] / 100
    return fator


def run():
    path = ROOT / 'dados' / 'cafe_arabica_2014_2024.csv'
    with path.open(encoding='utf-8-sig', newline='') as f:
        rows = list(csv.DictReader(f))
    fields = ['escala', 'codigo_ibge', 'localidade', 'ano',
              'valor_mil_reais_nominal', 'valor_mil_reais_reais_2024',
              'valor_implicito_reais_saca_nominal',
              'valor_implicito_reais_saca_reais_2024', 'fator_ipca_dez2024']
    output = ROOT / 'dados' / 'valor_real_2014_2024.csv'
    with output.open('w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fields)
        writer.writeheader()
        for row in rows:
            year = int(row['ano'])
            factor = fator_para_2024(year)
            nominal = float(row['valor_mil_reais'])
            per_bag = float(row['valor_implicito_reais_saca'])
            writer.writerow({
                'escala': row['escala'], 'codigo_ibge': row['codigo_ibge'],
                'localidade': row['localidade'], 'ano': year,
                'valor_mil_reais_nominal': nominal,
                'valor_mil_reais_reais_2024': round(nominal * factor, 2),
                'valor_implicito_reais_saca_nominal': per_bag,
                'valor_implicito_reais_saca_reais_2024': round(per_bag * factor, 2),
                'fator_ipca_dez2024': round(factor, 6),
            })
    print(f'{len(rows)} observações corrigidas: {output}')


if __name__ == '__main__':
    run()

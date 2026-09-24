# Fontes de dados e método de coleta

**Projeto Semantix · Eduardo da Silva Fonseca · Setembro de 2026**

## Fonte principal

| Item | Especificação |
| --- | --- |
| Instituição | IBGE, Pesquisa Agrícola Municipal (PAM), [tabela SIDRA 1613](https://sidra.ibge.gov.br/tabela/1613) |
| Produto | Café arábica, categoria 31619 |
| Recorte | Espera Feliz (código IBGE 3124203), Minas Gerais, Espírito Santo e São Paulo; 2014 a 2024 |
| Formato | JSON estruturado, registros anuais agregados por localidade, variável e ano |
| Medidas coletadas | Área colhida (ha), quantidade produzida (t), rendimento médio (kg/ha) e valor da produção (mil R$) |
| Acesso | API SIDRA, requisições HTTPS; sem dados pessoais ou confidenciais |
| Data da coleta | 23/09/2026 |

Consultas: [município](https://apisidra.ibge.gov.br/values/t/1613/n6/3124203/v/216,214,112,215/p/2014-2024/c82/31619?formato=json) e [estados](https://apisidra.ibge.gov.br/values/t/1613/n3/31,32,35/v/216,214,112,215/p/2014-2024/c82/31619?formato=json). As respostas preservadas estão em `dados/fonte_sidra.json`; `analise.py` implementa a coleta e o tratamento. O CSV resultante, `dados/cafe_arabica_2014_2024.csv`, tem **44 observações**, uma para cada combinação das quatro localidades com os 11 anos.

## Tratamento e medidas derivadas

O script remove o primeiro registro descritivo da API, agrupa medidas por escala, código IBGE e ano, converte marcadores de ausência em nulos e interpreta valores numéricos. Foram verificados duplicatas, nulos nas medidas usadas e áreas positivas. Os valores derivados são:

| Campo | Cálculo | Unidade |
| --- | --- | --- |
| `sacas_60kg` | `producao_t * 1000 / 60` | sacas de 60 kg |
| `sacas_ha` | `sacas_60kg / area_colhida_ha` | sacas de 60 kg por hectare |
| `valor_implicito_reais_saca` | `valor_mil_reais * 1000 / sacas_60kg` | R$ nominais por saca |

O rendimento oficial em kg/ha serve como conferência; pequenas diferenças podem decorrer de arredondamento. O valor implícito é uma divisão entre duas estatísticas anuais, **não uma cotação, receita por propriedade ou lucro**. Os valores nominais não foram deflacionados. Espera Feliz integra Minas Gerais, portanto as duas escalas se sobrepõem e suas quantidades não podem ser somadas como categorias independentes.

## Reprodução e atualização

Execute `python -m pip install -r requirements.txt`, depois `python analise.py` e `python modelagem.py` na raiz do projeto. A primeira execução atualiza a coleta pela API e gera CSV e gráficos; a segunda atualiza a avaliação temporal. O notebook `notebook_eda.ipynb` lê o CSV gerado. Para reproduzir exatamente a coleta apresentada sem consultar a API, consulte o JSON preservado. Revisões posteriores da PAM podem alterar números retornados em nova consulta.

# Café arábica: produtividade e valor da produção

**Projeto de parceria Semantix · Eduardo da Silva Fonseca · Setembro de 2026**

Escolhi esta pergunta porque trabalho no agro em Espera Feliz e conheço a importância da lavoura de café para quem precisa planejar a safra. Minha leitura dos resultados está em [Relatório de insights](RELATORIO_INSIGHTS.md).

**Entregáveis:** [problema e justificativa](PROBLEMA_E_JUSTIFICATIVA.md) · [fontes e coleta](FONTES_E_COLETA.md) · [notebook de EDA](notebook_eda.ipynb) e [scripts](analise.py) ([modelagem](modelagem.py)) · [relatório de insights](RELATORIO_INSIGHTS.md) · [visualização no Looker Studio](DASHBOARD_LOOKER.md).

## 1. Problema e justificativa

Produtores de café precisam planejar colheita, investimentos e comercialização em meio à oscilação da produtividade e do valor recebido pela produção. Em Espera Feliz, município cafeeiro de Minas Gerais, a pergunta prática é: **como variam a produção e o rendimento do café arábica no município em comparação com Minas Gerais e outros estados produtores?** O valor médio implícito da produção ajuda a contextualizar a receita agrícola, mas não equivale à cotação diária nem permite estimar lucro.

A análise de séries públicas permite identificar anos atípicos e comparar rendimento por hectare. Ela apoia decisões sobre investigação agronômica, planejamento financeiro e monitoramento; não prova causas de uma queda ou alta. Fatores como clima, bienalidade, manejo e mercado exigem fontes adicionais e um desenho específico para testar hipóteses.

## 2. Coleta e fontes

| Fonte | Dados e formato | Acesso | Uso |
| --- | --- | --- | --- |
| [IBGE, PAM, tabela SIDRA 1613](https://sidra.ibge.gov.br/tabela/1613) | Dados estruturados anuais de área colhida, quantidade produzida, rendimento médio e valor da produção por produto e localidade | [API JSON, estados MG/ES/SP](https://apisidra.ibge.gov.br/values/t/1613/n3/31,32,35/v/216,214,112,215/p/2014-2024/c82/31619?formato=json) e [API JSON, Espera Feliz](https://apisidra.ibge.gov.br/values/t/1613/n6/3124203/v/216,214,112,215/p/2014-2024/c82/31619?formato=json) | Série de 2014 a 2024; café **arábica** (categoria 31619) |

Coleta em 23/09/2026. Consultas e respostas originais ficam em `dados/fonte_sidra.json`. O código municipal de Espera Feliz é 3124203. Todos os dados são agregados e públicos. Escolhemos 2024 como último ano da análise para manter um período anual consolidado e comparável, sem misturar estimativas recentes.

## 3. Tratamento e modelagem

`analise.py` busca as duas séries, remove o cabeçalho da API, une as observações pela chave **escala + código IBGE + ano**, transforma os marcadores de ausência (`..`, `-`, `...`, `X`) em nulos e converte valores numéricos. A saída `dados/cafe_arabica_2014_2024.csv` contém 44 linhas (4 localidades × 11 anos), sem valores ausentes nas medidas usadas.

- `sacas_60kg = producao_t × 1000 / 60`.
- `sacas_ha = sacas_60kg / area_colhida_ha` (se área positiva).
- `valor_implicito_reais_saca = valor_mil_reais × 1000 / sacas_60kg` (se produção positiva).

A medida de valor usa o valor anual declarado na PAM dividido pela produção anual. **Não é o preço à vista do café**, não foi corrigida pela inflação e não inclui custos. A produtividade oficial (`rendimento_kg_ha`) permite conferir `sacas_ha` com diferenças de arredondamento. Estados e município são escalas aninhadas: Espera Feliz integra Minas Gerais; suas produções **não devem ser somadas** no painel. A comparação de valores absolutos entre município e estados serve apenas para contexto; o rendimento por hectare é a comparação principal.

## 4. Análise exploratória e insights

| Localidade | Produtividade 2023 (sc/ha) | Produtividade 2024 (sc/ha) | Variação | Produção 2024 (t) |
| --- | ---: | ---: | ---: | ---: |
| Espera Feliz | 18,00 | 24,00 | +33,3% | 13.680 |
| Minas Gerais | 26,92 | 25,45 | −5,5% | 1.663.992 |
| Espírito Santo | 20,69 | 27,14 | +31,2% | 224.649 |
| São Paulo | 26,87 | 29,37 | +9,3% | 335.206 |

Em 2024, Espera Feliz registrou 24,00 sc/ha, abaixo dos 25,45 sc/ha de Minas Gerais. O município passou de 18,00 para 24,00 sc/ha entre 2023 e 2024; esse salto sugere investigar condições de safra e manejo, **sem atribuir causa** a partir da série agregada. A série mostra oscilações entre anos: tomar só o último ano como meta pode levar a uma previsão inadequada.

**Ações sugeridas:** planejar produção com cenários de rendimento baseados em vários anos; registrar por talhão área, colheita, variedade, manejo e chuva; comparar resultados locais ao histórico e ao estado antes de decidir investimentos; acrescentar preços efetivamente recebidos e custos próprios para estimar margem. As associações anuais entre valor, quantidade e área não demonstram causalidade. A avaliação do modelo abaixo quantifica o alcance limitado de previsões baseadas apenas nessa série.

## 5. Modelo estatístico e avaliação

`modelagem.py` treina regressão Ridge com as produtividades de um e dois anos antes e indicadores de localidade. A divisão é temporal: treino 2016–2021, teste 2022–2024, com 12 observações de teste. A transformação dos atributos é ajustada somente nos dados de treino. Usam-se valores passados efetivamente conhecidos na previsão de um ano à frente. Comparações de referência: repetir a produtividade do ano anterior ou a de dois anos antes.

| Modelo | MAE (sc/ha) | RMSE (sc/ha) |
| --- | ---: | ---: |
| Ridge | 3,73 | 5,63 |
| Ano anterior | 4,02 | **4,74** |
| Dois anos antes | 4,35 | 5,82 |

O Ridge teve o menor MAE, mas uma previsão excessiva para Espera Feliz em 2022 (35,05 ante 20,00 sc/ha) elevou o RMSE. A amostra é pequena e não inclui clima ou manejo. O modelo demonstra avaliação temporal e **não é recomendado para decisões operacionais** sem dados melhores e validação adicional. Previsões individuais e métricas reprodutíveis: `dados/avaliacao_modelo.csv` e `dados/metricas_modelo.csv`.

## 6. Visualizações e entrega

- [Painel em HTML publicado no GitHub Pages](https://eduardosilvafonseca18-netizen.github.io/projeto-semantix-cafe/): gráficos, filtros de localidade e leitura dos indicadores.
- [Gráfico de produtividade](graficos/produtividade.png) e [gráfico de produção](graficos/producao.png).
- [Relatório nativo no Looker Studio](https://datastudio.google.com/reporting/76ba4bf8-9e14-4180-9f15-0ac9b4114372/page/XYg9F): evolução de 2014 a 2024 e comparação de 2024, ambos conferidos em leitura. Compartilhamento **Não listado · Leitor**: segundo a configuração salva no Looker Studio, qualquer pessoa com o link pode acessar. Uma sessão independente sem login não foi verificada. A [documentação da visualização](DASHBOARD_LOOKER.md) descreve os campos e conclusões.

### Como reproduzir

```bash
python -m pip install -r requirements.txt
python analise.py
python modelagem.py
```

Abra `index.html` no navegador. O script requer acesso à API do IBGE para atualizar os dados. O arquivo CSV e os gráficos já estão incluídos, assim como as respostas originais. `notebook_eda.ipynb` organiza a leitura, checagens, análise exploratória e avaliação em células para apresentação.

### Limitações

PAM informa agregados anuais, sujeitos a revisões; dados de cada propriedade podem divergir. O valor médio é nominal e incorpora diferenças de composição e qualidade. Não há variáveis meteorológicas nem preços diários neste conjunto; portanto, não se pode concluir que clima ou mercado causaram as variações observadas. Antes de divulgar uma comparação financeira, deflacionar a série e obter preços e custos compatíveis. O modelo foi testado com apenas 12 casos e não deve ser extrapolado para outra região ou horizonte.

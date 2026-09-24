# Visualização no Looker Studio

**Projeto Semantix · Eduardo da Silva Fonseca · 24/09/2026**

## Relatório construído

Criei o [relatório nativo no Looker Studio](https://datastudio.google.com/reporting/76ba4bf8-9e14-4180-9f15-0ac9b4114372/page/XYg9F) a partir da [planilha de apoio](https://docs.google.com/spreadsheets/d/1CfKab0ZUrH8UHYA-8-CKeZjC1HIBcvOvLiFimjtoUMA/edit), que contém as 44 observações do CSV tratado. O relatório tem duas páginas, verificadas no modo de leitura:

| Página | Campos e regra | Interpretação |
| --- | --- | --- |
| Evolução 2014–2024 | `ano` em ordem crescente; `localidade` como série; **média** de `sacas_ha` | Mostra a oscilação anual de Espera Feliz, Minas Gerais, Espírito Santo e São Paulo. Cada combinação de ano e localidade tem uma observação. |
| Comparativo 2024 | `localidade`; **média** de `sacas_ha`; filtro do próprio gráfico `ano = 2024` | Compara o rendimento de 2024 sem somar produtividades de anos diferentes. |

**Acesso:** no momento da atualização, o compartilhamento do relatório estava **Restrito** à conta proprietária. O link acima identifica o relatório, mas outras pessoas só poderão abri-lo após a permissão de leitura por link ser liberada. A visualização pública já verificável é o [painel complementar no GitHub Pages](https://eduardosilvafonseca18-netizen.github.io/projeto-semantix-cafe/). Não apresente o link do Looker como público até testar o acesso sem login de proprietário.

## Coleta e modelagem para a visualização

O arquivo `dados/cafe_arabica_2014_2024.csv` deriva da PAM/SIDRA 1613 do IBGE, documentada em [FONTES_E_COLETA.md](FONTES_E_COLETA.md). A chave da observação é `escala + codigo_ibge + ano`. `sacas_ha` é a quantidade produzida, convertida de toneladas para sacas de 60 kg, dividida pela área colhida. A planilha conserva `ano` e `sacas_ha` como números e `localidade` como texto. Não se somam Espera Feliz e Minas Gerais: o município integra o estado.

## Conclusões e limites

Espera Feliz passou de 18,00 sc/ha em 2023 para 24,00 sc/ha em 2024 (+33,3%). No último ano do recorte, o município ficou abaixo de Minas Gerais (25,45), Espírito Santo (27,14) e São Paulo (29,37 sc/ha). A série varia bastante, então um único ano não deve servir como meta fixa. Eu sugiro trabalhar com cenários baseados em vários anos e investigar clima e manejo com dados por talhão antes de atribuir causas. A PAM oferece agregados anuais, não desempenho de propriedades individuais; detalhes e avaliação do modelo estão em [RELATORIO_INSIGHTS.md](RELATORIO_INSIGHTS.md).

O painel complementar em HTML inclui filtros, produção e comentários metodológicos. O Looker nativo apresenta especificamente a tendência de produtividade e o comparativo de 2024.

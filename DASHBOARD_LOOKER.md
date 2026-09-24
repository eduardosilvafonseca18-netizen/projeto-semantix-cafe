# Visualização no Looker Studio

**Projeto Semantix · Eduardo da Silva Fonseca · 24/09/2026**

## Relatório construído

Criei o [relatório nativo no Looker Studio](https://datastudio.google.com/reporting/76ba4bf8-9e14-4180-9f15-0ac9b4114372/page/XYg9F) a partir da [planilha de apoio](https://docs.google.com/spreadsheets/d/1CfKab0ZUrH8UHYA-8-CKeZjC1HIBcvOvLiFimjtoUMA/edit), que contém as 44 observações do CSV tratado. O relatório tem três páginas. As duas primeiras usam gráficos nativos ligados à planilha; a terceira apresenta uma figura estática gerada do CSV econômico corrigido por `economia.py`. Títulos, resultados e ressalvas estão visíveis nas páginas:

| Página | Campos e regra | Interpretação |
| --- | --- | --- |
| Evolução 2014–2024 | `ano` em ordem crescente; `localidade` como série; **média** de `sacas_ha` | Mostra a oscilação anual de Espera Feliz, Minas Gerais, Espírito Santo e São Paulo. Cada combinação de ano e localidade tem uma observação. |
| Comparativo 2024 | `localidade`; **média** de `sacas_ha`; filtro do próprio gráfico `ano = 2024` | Compara o rendimento de 2024 sem somar produtividades de anos diferentes. |
| Valor real e próximos dados | Figura de `graficos/valor_real_espera_feliz.png`, gerada por `economia.py` a partir do CSV tratado e das taxas anuais do IPCA do IBGE | Contrasta valor implícito nominal e em R$ de dezembro de 2024 para Espera Feliz; explica 2022 × 2024 e aponta clima/custos ausentes. A figura é estática: para atualizar, gere e reenvie a imagem. |

**Acesso:** o relatório está configurado como **Não listado · Leitor**. O Looker Studio confirma que qualquer pessoa na Internet com o link pode acessar. A permissão foi salva e conferida novamente no painel de compartilhamento; não foi possível fazer uma verificação independente em uma sessão sem login. A URL está no início deste documento. O [painel complementar no GitHub Pages](https://eduardosilvafonseca18-netizen.github.io/projeto-semantix-cafe/) também permanece disponível.

## Coleta e modelagem para a visualização

O arquivo `dados/cafe_arabica_2014_2024.csv` deriva da PAM/SIDRA 1613 do IBGE, documentada em [FONTES_E_COLETA.md](FONTES_E_COLETA.md). A chave da observação é `escala + codigo_ibge + ano`. `sacas_ha` é a quantidade produzida, convertida de toneladas para sacas de 60 kg, dividida pela área colhida. A planilha conserva `ano` e `sacas_ha` como números e `localidade` como texto. Não se somam Espera Feliz e Minas Gerais: o município integra o estado.

## Conclusões e limites

Espera Feliz passou de 18,00 sc/ha em 2023 para 24,00 sc/ha em 2024 (+33,3%). No último ano do recorte, o município ficou abaixo de Minas Gerais (25,45), Espírito Santo (27,14) e São Paulo (29,37 sc/ha). A série varia bastante, então um único ano não deve servir como meta fixa. Eu sugiro trabalhar com cenários baseados em vários anos e investigar clima e manejo com dados por talhão antes de atribuir causas. A PAM oferece agregados anuais, não desempenho de propriedades individuais; detalhes e avaliação do modelo estão em [RELATORIO_INSIGHTS.md](RELATORIO_INSIGHTS.md).

O painel complementar em HTML inclui filtros, produção e comentários metodológicos. A leitura econômica adicional está no Looker como figura estática reproduzível no repositório. Para clima, custos e talhões, consulte [AMPLIACOES.md](AMPLIACOES.md); nenhuma medição individual foi simulada.

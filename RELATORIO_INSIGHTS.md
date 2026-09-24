# O que os dados do café mostram em Espera Feliz

**Eduardo da Silva Fonseca · Projeto Semantix · Setembro de 2026**

## Por que escolhi este tema

Escolhi o café porque é uma realidade que conheço de perto em Espera Feliz, no interior de Minas Gerais. Trabalho no agro e acompanho o que acontece na lavoura. Para quem está nesse meio, uma diferença de algumas sacas por hectare muda a expectativa de colheita e o planejamento da safra. Quis usar dados públicos para olhar além da impressão de um ano bom ou ruim.

Minha pergunta foi: **como a produtividade do café arábica em Espera Feliz variou de 2014 a 2024 e o que aprendemos ao compará-la com Minas Gerais e outros estados produtores?** Também observei a produção e o valor declarado na pesquisa do IBGE. Evitei chamar o valor por saca calculado de “preço do café”, porque ele é uma média anual implícita do valor da produção, não uma cotação ou o preço recebido por cada produtor.

## O que encontrei

Em Espera Feliz, a produtividade foi de **18,00 sacas de 60 kg por hectare em 2023** e **24,00 em 2024**, um aumento de **33,3%**. Minas Gerais passou de **26,92** para **25,45 sc/ha** no mesmo intervalo. Portanto, mesmo com a recuperação local, o município ficou cerca de **1,45 sc/ha abaixo** da média estadual em 2024. A produção municipal passou de **10.260 para 13.680 toneladas**.

A série local oscila bastante: **13,00 sc/ha em 2021**, **20,00 em 2022**, **18,00 em 2023** e **24,00 em 2024**. Não seria prudente projetar a próxima colheita copiando só 2024. Esses números não informam chuva, idade do cafezal, altitude, variedade, tratos culturais ou perdas por talhão. Também não permitem afirmar qual fator provocou a mudança.

## Nova leitura: valor nominal e real

Apliquei o IPCA para expressar o valor implícito da produção em reais de dezembro de 2024. Em Espera Feliz, 2014 passou de R$ 336,11 nominais por saca para R$ 587,92 corrigidos. Para 2022, os R$ 1.233,91 nominais equivalem a R$ 1.353,27 nessa mesma base, acima dos R$ 1.200,00 de 2024. A comparação não depende só da unidade monetária, mas continua sem revelar os preços individuais, qualidade dos lotes ou custos. Fórmula, fonte e limites estão em [AMPLIACOES.md](AMPLIACOES.md).

Clima e custos entram como próximos dados necessários. Estruturei um coletor para chuva e temperatura de um ponto próximo à sede municipal e um formulário vazio de talhão. Sem observações climáticas validadas ou contas de propriedades, não calculo correlação climática ou margem de lucro.

## Modelo e avaliação

Testei uma regressão Ridge para estimar a produtividade de cada localidade com base nos rendimentos observados um e dois anos antes e na identificação da localidade. Treinei com **2016–2021** e reservei **2022–2024** para testar previsões de um ano à frente. A avaliação tem **12 casos**: três anos para cada uma das quatro localidades. Para não confundir complexidade com melhora, comparei o modelo com duas regras simples: usar o valor do ano anterior e usar o de dois anos antes.

| Método | Erro absoluto médio (sc/ha) | Raiz do erro quadrático médio (sc/ha) |
| --- | ---: | ---: |
| Ridge | 3,73 | 5,63 |
| Repetir ano anterior | 4,02 | **4,74** |
| Repetir dois anos antes | 4,35 | 5,82 |

O Ridge teve o menor erro absoluto médio, mas **não venceu em todas as métricas**. Em Espera Feliz, previu **35,05 sc/ha para 2022**, enquanto o resultado observado foi **20,00 sc/ha**. Esse erro grande mostra o limite de um modelo treinado com poucas observações e sem clima nem manejo. Eu não usaria a previsão isolada para decidir compras, contratação ou investimentos. O código e cada valor previsto estão em `modelagem.py` e `dados/avaliacao_modelo.csv`.

## O que faria com essa análise

Começaria acompanhando a produtividade de cada talhão por mais de um ano, junto de área colhida, chuva, adubação, idade das plantas e custos. Com esses registros, seria possível investigar por que áreas da mesma região respondem de maneiras diferentes. Para o planejamento, trabalharia com cenários de produção, e não um único número previsto. Para estudar renda, acrescentaria os preços efetivamente recebidos e as despesas: o valor da produção do IBGE não informa lucro.

O painel em `index.html` permite selecionar cada localidade e acompanhar a série de produtividade e produção. A metodologia completa, a fonte e a forma de reproduzir a análise estão no [README](README.md).

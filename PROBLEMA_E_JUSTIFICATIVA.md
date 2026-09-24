# Por que olhar os dados da produção de café

**Eduardo da Silva Fonseca · Projeto Semantix · Setembro de 2026**

## A pergunta que escolhi

Trabalho no agro em Espera Feliz, Minas Gerais, e escolhi uma pergunta próxima da minha realidade: **como a produtividade e a produção do café arábica variaram no município entre 2014 e 2024, e como essa trajetória se compara à de Minas Gerais e de outros estados produtores?** A dificuldade prática é planejar uma safra quando o rendimento por hectare muda muito de um ano para outro. A expectativa de colheita afeta decisões sobre mão de obra, estrutura, insumos e recursos financeiros.

Um ano de produção alta pode criar uma expectativa que não se repete; uma baixa pode ser tomada como tendência permanente. Só a experiência recente não permite medir a amplitude dessas oscilações. A série anual ajuda a colocar o último resultado em contexto e a identificar anos que merecem investigação em campo.

## Relevância

O café faz parte da atividade econômica local, e a incerteza sobre a colheita afeta produtores e pessoas envolvidas na cadeia produtiva. A análise é relevante para o planejamento, mas a informação municipal é agregada: ela **não descreve o resultado de cada propriedade**. A comparação com o estado usa principalmente produtividade por hectare, pois o volume total de um município e o de um estado têm escalas diferentes.

## Por que usar dados

Usei a Pesquisa Agrícola Municipal do IBGE para construir uma série com a mesma definição de produto, localidade, período e unidade de medida. Isso permite calcular sacas de 60 kg por hectare, verificar tendências, comparar 2023 com 2024 e testar se um modelo simples consegue prever anos reservados para avaliação. O modelo foi comparado com a regra de repetir o ano anterior; a avaliação está em [RELATORIO_INSIGHTS.md](RELATORIO_INSIGHTS.md).

Em Espera Feliz, a produtividade passou de **18,00 para 24,00 sc/ha** entre 2023 e 2024, enquanto a série completa mostra oscilações maiores. Esse achado ajuda a construir cenários em vez de extrapolar um único ano. A série **não permite atribuir a variação** a chuva, bienalidade, manejo ou preços: esses fatores não fazem parte do conjunto analisado. Para orientar decisões de uma propriedade, eu acrescentaria dados por talhão, clima, custos e preços realmente recebidos.

As fontes, o tratamento e as fórmulas estão em [FONTES_E_COLETA.md](FONTES_E_COLETA.md). A visualização publicada está no [painel do projeto](https://eduardosilvafonseca18-netizen.github.io/projeto-semantix-cafe/).

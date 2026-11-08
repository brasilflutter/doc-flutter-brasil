---
title: Recomendações e recursos de arquitetura
shortTitle: Recomendações de arquitetura
description: >
  Recomendações para construir aplicações Flutter escaláveis.
prev:
  title: Estudo de caso de arquitetura
  path: /app-architecture/case-study
next:
  title: Padrões de projeto
  path: /app-architecture/design-patterns
ia-translate: true
---

Esta página apresenta as melhores práticas de arquitetura, por que elas são importantes e
se nós as recomendamos para a sua aplicação Flutter.
Você deve tratar estas recomendações como recomendações,
e não como regras inflexíveis, e você deve
adaptá-las aos requisitos únicos do seu app.

As melhores práticas nesta página têm uma prioridade,
que reflete o quão fortemente o time Flutter a recomenda.

* **Fortemente recomendado:** Você deve sempre implementar esta recomendação se
  você está começando a construir um novo aplicativo. Você deve considerar fortemente
  refatorar um aplicativo existente para implementar esta prática a menos que isso
  entre em conflito fundamentalmente com sua abordagem atual.
* **Recomendado**: Esta prática provavelmente irá melhorar o seu aplicativo.
* **Condicional**: Esta prática pode melhorar seu aplicativo em certas circunstâncias.

## Separação de responsabilidades {:#separation-of-concerns}

Você deve separar seu app em uma camada de UI e uma camada de dados. Dentro dessas camadas,
você deve separar ainda mais a lógica em classes por responsabilidade.

<ArchitectureRecommendations category="separation-of-concerns" />

## Manipulação de dados {:#handling-data}

Manipular dados com cuidado torna seu código mais fácil de entender, menos propenso a erros e
evita que dados malformados ou inesperados sejam criados.

<ArchitectureRecommendations category="handling-data" />

## Estrutura do app {:#app-structure}

Um código bem organizado beneficia tanto a saúde do próprio app quanto a equipe que trabalha no código.

<ArchitectureRecommendations category="app-structure" />

## Testes {:#testing}

Boas práticas de teste tornam seu app flexível.
Elas também tornam simples e de baixo risco adicionar nova lógica e nova UI.

<ArchitectureRecommendations category="testing" />

<a id="recommended-resources" aria-hidden="true"></a>

## Recursos recomendados {:#resources}

* Código e templates
  * [Código fonte do aplicativo Compass][Compass app source code] -
    Código fonte de um aplicativo Flutter robusto e completo que
    implementa muitas dessas recomendações.
  * [very_good_cli][] -
    Um template de aplicativo Flutter feito por
    especialistas Flutter da Very Good Ventures.
    Este template gera uma estrutura de aplicativo similar.
* Documentação
  * [Documentação de arquitetura da Very Good Engineering][Very Good Engineering architecture documentation] -
    Very Good Engineering é um site de documentação da VGV que possui
    artigos técnicos, demos e projetos de código aberto.
    Inclui documentação sobre arquitetura de aplicativos Flutter.
* Ferramentas
  * [Ferramentas de desenvolvedor Flutter][Flutter developer tools] -
    DevTools é um conjunto de ferramentas de desempenho e depuração para Dart e Flutter.
  * [flutter_lints][] -
    Um package que contém os lints para
    aplicativos Flutter recomendados pelo time Flutter.
    Use este package para incentivar boas práticas de codificação em uma equipe.


[Compass app source code]: https://github.com/flutter/samples/tree/main/compass_app
[very_good_cli]: https://cli.vgv.dev/
[Very Good Engineering architecture documentation]: https://engineering.verygood.ventures/architecture/architecture/
[Flutter developer tools]: /tools/devtools
[flutter_lints]: https://pub.dev/packages/flutter_lints

## Feedback

Como esta seção do site está evoluindo,
nós [agradecemos seu feedback][welcome your feedback]!

[welcome your feedback]: https://google.qualtrics.com/jfe/form/SV_4T0XuR9Ts29acw6?page="recommendations"

---
title: Arquitetando apps Flutter
shortTitle: Arquitetura
description: >
  Aprenda como estruturar apps Flutter.
showToc: false
next:
  title: Conceitos de arquitetura
  path: /app-architecture/concepts
ia-translate: true
---

<div class="side-by-side">
<div>

Arquitetura é uma parte importante para construir
um app Flutter que seja sustentável, resiliente
e escalável. Neste guia, você aprenderá os princípios
de arquitetura e as melhores práticas para criar apps Flutter.

'Arquitetura' é uma palavra difícil de definir.
É um termo amplo que pode se referir a diversos
tópicos dependendo do contexto. Neste guia,
'arquitetura' se refere a como estruturar, organizar e projetar
seu app Flutter para escalar conforme os requisitos do projeto e o time crescem.

</div>
<div class="centered-rows">
<img src='/assets/images/docs/app-architecture/hero-image.png' style="max-height: 480px;" alt="Imagem de destaque">
</div>
</div>


## O que você vai aprender {:#what-youll-learn}

* Benefícios de uma arquitetura intencional
* Princípios arquiteturais comuns
* A arquitetura recomendada pelo time do Flutter
* MVVM e gerenciamento de estado
* Injeção de dependência
* Padrões de design comuns para escrever aplicações Flutter robustas

{% comment %}
TODO @ewindmill complete this list as pages land, add links.
{% endcomment %}

## Benefícios de uma arquitetura intencional {:#benefits-of-intentional-architecture}

Uma boa arquitetura de app oferece vários benefícios
para as equipes de engenharia e seus usuários finais.

* Manutenibilidade - A arquitetura de um app torna mais fácil modificar, atualizar e corrigir
  problemas ao longo do tempo.
* Escalabilidade - Um aplicativo bem planejado permite que mais pessoas contribuam
  para o mesmo código simultaneamente, com conflitos mínimos de código.
* Testabilidade - Aplicativos com arquitetura intencional geralmente possuem
  classes simples com entradas e saídas bem definidas, o que os torna mais fáceis
  de 'mockar' e testar.
* Menor carga cognitiva - Desenvolvedores novos no projeto serão mais produtivos
  em menos tempo, e revisões de código geralmente levam menos tempo quando
  o código é mais fácil de entender.
* Melhor experiência do usuário - Recursos podem ser lançados mais rápido e com menos bugs.

## Como usar este guia {:#how-to-use-this-guide}

Este é um guia para criar aplicativos Flutter escaláveis e foi escrito
para equipes com vários desenvolvedores contribuindo para o mesmo código,
que estão construindo um aplicativo rico em recursos.
Se você está criando um app Flutter com uma *equipe e base de código em crescimento*,
estas orientações são para você.

Além de conselhos arquiteturais gerais, este guia apresenta exemplos concretos de
melhores práticas e inclui recomendações específicas.
Algumas bibliotecas podem ser substituídas, e equipes muito grandes com complexidades
únicas podem descobrir que algumas partes não se aplicam.
Em qualquer caso, as ideias continuam válidas.
Este é o jeito recomendado de construir um app Flutter.

Na primeira parte deste guia, você aprenderá sobre princípios arquiteturais
comuns de forma ampla. Na segunda parte,
o guia apresenta recomendações específicas e concretas
sobre como arquitetar apps Flutter.
Por fim, ao final do guia, você encontrará uma lista de padrões de design
e códigos de exemplo que mostram as recomendações em ação.

[Common architectural principles]: /app-architecture/concepts
[recommended app architecture]: /app-architecture/guide
[MVVM]: /app-architecture/guide#mvvm


## Feedback

Como esta seção do site está em evolução,
[agradecemos seu feedback][welcome your feedback]!

[welcome your feedback]: https://google.qualtrics.com/jfe/form/SV_4T0XuR9Ts29acw6?page="index"

---
title: Como o Flutter funciona
description: >-
  Entenda mais a fundo como o Flutter funciona com uma série de vídeos em seis partes.
layout: tutorial
ia-translate: true
---

<Stepper level="2">

## Arquitetura do Flutter {:#architecture}


<div class="video-wrapper">
  <YouTubeEmbed id="0Xn1QhNtPkQ" title="Como o Flutter funciona" fullWidth />
</div>

Boas-vindas ao primeiro episódio de "How Flutter Works" (Como o Flutter funciona),
uma série em seis partes criada para explorar o que acontece com
seu código Dart depois que você o entrega ao framework Flutter.
Este episódio dá uma visão geral da arquitetura do Flutter,
abordando código declarativo, frameworks multiplataforma e
o papel do Dart.
Este vídeo é perfeito para quem está começando a
pesquisar sobre Flutter e quer entender o panorama geral.

## Widgets e as três árvores {:#three-trees}

<div class="video-wrapper">
  <YouTubeEmbed id="xiW3ahr4CRU" title="As três árvores" fullWidth />
</div>

Mergulhe na arquitetura do Flutter explorando suas
três árvores principais: `Widget`, `Element` e `RenderObject`.
Descubra como os widgets fornecem a API declarativa para quem desenvolve com Flutter e
veja como os elements conectam os widgets à camada de renderização.
Você também vai aprender o papel dos render objects na
tradução dos valores dos widgets em chamadas de pintura.

## Objetos State e seu ciclo de vida {:#state}

<div class="video-wrapper">
  <YouTubeEmbed id="FP737UMx7ss" title="A classe State" fullWidth />
</div>

O episódio 3 de "How Flutter Works" se aprofunda na classe `State`,
uma peça fundamental por trás de todo `StatefulWidget`.
Acompanhe o ciclo de vida completo de um objeto `State`: desde o `initState`,
onde você inicializa recursos, até o `dispose`, onde você faz a limpeza.
No caminho, explore métodos importantes como `didChangeDependencies`,
`didUpdateWidget` e o essencial método `build`.
Ao final do episódio, você vai entender como os objetos `State`
acompanham, respondem e gerenciam mudanças nos seus apps Flutter, e
como o ciclo de vida do `State` permite atualizações de UI eficientes.

Este episódio também mostra os bastidores de como o Flutter
percorre recursivamente a árvore de widgets depois de uma chamada a `setState`,
reconstruindo apenas as partes do app que precisam mudar.
Você vai aprender por que construtores `const` importam para a performance,
por que as closures de `setState` precisam ser síncronas e como
os elements (e não os próprios widgets) gerenciam o processo de rebuild de fato.
Se você tem curiosidade sobre como o Flutter mantém os apps rápidos e responsivos, ou
só quer entender de verdade o que acontece nos bastidores,
este episódio está repleto dos fundamentos essenciais.

## Os widgets que realmente renderizam {:#render-object-widgets}

<div class="video-wrapper">
  <YouTubeEmbed id="zcJlHVVM84I" title="O RenderObjectWidget" fullWidth />
</div>

Já se perguntou como seu app Flutter é de fato renderizado na tela?
Este vídeo se aprofunda no `RenderObjectWidget`, o único tipo de
widget do Flutter que cria algo visual.
Enquanto widgets stateless e stateful ajudam a estruturar seu app,
são os render object widgets que transformam seu código de UI em pixels de verdade.

Você vai aprender como o Flutter constrói as árvores
`Widget`, `Element` e `RenderObject`,
por que muitos widgets comuns não renderizam nada diretamente e
como o Flutter usa o `RenderObjectWidget` para criar e
atualizar os render objects que dão vida à sua UI.

## Um dia na vida de um render object {:#render-objects}

<div class="video-wrapper">
  <YouTubeEmbed id="EuG12bebwac" title="Um dia na vida de um RenderObject" fullWidth />
</div>

No episódio 5 de "How Flutter Works", Craig mostra
um dia inteiro na vida de um `RenderObject`.
Partindo dos conceitos do episódio 4,
este vídeo explica as responsabilidades centrais dos render objects:
layout, pintura, hit testing e acessibilidade. Craig desmistifica como
as restrições (constraints) descem pela árvore de renderização, como os tamanhos voltam para cima e
como os render objects pais definem as posições dos filhos.
Ele também detalha métodos-chave como
`layout`, `paint` e `describeSemanticsConfiguration`,
mostrando como eles se encaixam para manter sua UI responsiva e precisa.

## A engine do Flutter e os embedders {:#engine}

<div class="video-wrapper">
  <YouTubeEmbed id="Y2aBMjWVv2Y" title="A engine do Flutter e os embedders" fullWidth />
</div>

No episódio 6 de "How Flutter Works", Craig nos leva
para baixo do código Dart para explorar a engine do Flutter e os embedders.
Este episódio explica como os apps mobile Flutter dependem de
código nativo Android e iOS para iniciar e funcionar,
como a engine do Flutter conecta seu código Dart à plataforma hospedeira e
como os embedders facilitam a comunicação entre os dois.
Craig também destaca a estrutura de um projeto Flutter recém-gerado,
se aprofunda em como as threads são gerenciadas em um app Flutter e
explica o papel dos platform channels e do package [Pigeon][].

Você também vai aprender por que a engine do Flutter é
escrita em C++ e não em Dart,
como ela evoluiu a partir de um fork do Chrome e
como ela usa o Skia ou o Impeller para renderizar cada frame.
O episódio termina olhando para frente, para
as futuras melhorias de arquitetura do Flutter,
que buscam simplificar ainda mais a interoperabilidade nativa.
Se você quer um modelo mental claro de como os apps Flutter funcionam por baixo dos panos,
esta é a forma perfeita de conectar todas as camadas.

[Pigeon]: {{site.pub-pkg}}/pigeon

</Stepper>

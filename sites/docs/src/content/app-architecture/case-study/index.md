---
title: Estudo de caso de arquitetura
shortTitle: Estudo de caso de arquitetura
description: >-
  Um passo a passo de um aplicativo Flutter que implementa o padrão arquitetural MVVM.
prev:
  title: Guia para arquitetura de aplicativos
  path: /app-architecture/guide
next:
  title: Camada de UI
  path: /app-architecture/case-study/ui-layer
ia-translate: true
---

Os exemplos de código neste guia são do [aplicativo de exemplo Compass][Compass sample application],
um aplicativo que ajuda os usuários a criar e reservar itinerários para viagens.
É um aplicativo de amostra robusto com muitos recursos, rotas e telas.
O aplicativo se comunica com um servidor HTTP,
possui ambientes de desenvolvimento e produção,
inclui estilo específico da marca e contém alta cobertura de testes.
Dessas e de outras formas, ele simula um aplicativo Flutter
do mundo real e rico em recursos.

<div class="wrapping-row" style="margin-block-end: 2rem">
  <DashImage figure image="app-architecture/case-study/splash_screen.png" alt="Uma captura de tela da tela de abertura do aplicativo Compass." img-style="max-height: 400px;" />
  <DashImage figure image="app-architecture/case-study/home_screen.png" alt="Uma captura de tela da tela inicial do aplicativo Compass." img-style="max-height: 400px;" />
  <DashImage figure image="app-architecture/case-study/search_form_screen.png" alt="Uma captura de tela da tela de formulário de pesquisa do aplicativo Compass." img-style="max-height: 400px;" />
  <DashImage figure image="app-architecture/case-study/booking_screen.png" alt="Uma captura de tela da tela de reserva do aplicativo Compass." img-style="max-height: 400px;" />
</div>

A arquitetura do aplicativo Compass se assemelha mais ao [padrão arquitetural MVVM][MVVM architectural pattern]
conforme descrito nas [diretrizes de arquitetura de aplicativos][app architecture guidelines] do Flutter.
Este estudo de caso de arquitetura demonstra como
implementar essas diretrizes percorrendo
o recurso "Home" do aplicativo compass.
Se você não está familiarizado com MVVM, você deve ler essas diretrizes primeiro.

A tela inicial do aplicativo Compass exibe informações da conta do usuário e
uma lista das viagens salvas do usuário.
A partir desta tela, você pode fazer logout, abrir páginas detalhadas de viagens,
excluir viagens salvas e navegar para a primeira página do fluxo principal do aplicativo,
o que permite ao usuário criar um novo itinerário.

Neste estudo de caso, você aprenderá o seguinte:

* Como implementar as [diretrizes de arquitetura de aplicativos][app architecture guidelines] do Flutter
  usando repositórios e serviços na [camada de dados][data layer] e
  o padrão arquitetural MVVM na [camada de UI][UI layer]
* Como usar o [padrão Command][Command pattern] para renderizar a UI com segurança à medida que os dados mudam
* Como usar objetos [`ChangeNotifier`][] e [`Listenable`][] para gerenciar o estado
* Como implementar a [Injeção de Dependência][Dependency Injection] usando `package:provider`
* Como [configurar testes][set up tests] ao seguir a arquitetura recomendada
* [Estrutura de pacotes eficaz][package structure] para grandes aplicativos Flutter

Este estudo de caso foi escrito para ser lido em ordem.
Qualquer página pode referenciar as páginas anteriores.

Os exemplos de código neste estudo de caso incluem todos os detalhes necessários para
entender a arquitetura, mas não são trechos completos e executáveis.
Se você preferir acompanhar com o aplicativo completo,
você pode encontrá-lo no [GitHub][].

## Estrutura do pacote {:#package-structure}

Código bem organizado é mais fácil para vários engenheiros trabalharem com
conflitos de código mínimos e é mais fácil para novos engenheiros
navegar e entender.
A organização do código beneficia e é beneficiada por uma arquitetura bem definida.

Existem duas maneiras populares de organizar o código:

1. Por feature (recurso) - As classes necessárias para cada recurso são agrupadas. Por
   exemplo, você pode ter um diretório `auth`, que conteria arquivos
   como `auth_viewmodel.dart`, `login_usecase.dart`, `logout_usecase.dart`,
   `login_screen.dart`, `logout_button.dart`, etc.
2. Por tipo - Cada "tipo" de arquitetura é agrupado.
   Por exemplo, você pode ter diretórios como
   `repositories`, `models`, `services` e `viewmodels`.

A arquitetura recomendada neste guia se presta a
uma combinação dos dois.
Objetos da camada de dados (repositórios e serviços) não estão vinculados a um único recurso,
enquanto objetos da camada de UI (views e view models) estão.
A seguir, veja como o código está organizado no aplicativo Compass.

<FileTree>

- lib/
  - ui/
    - core/
      - ui/ 
        - <shared_widgets>
      - themes/
    - <feature_name>/
      - view_models/
        - <view_model_class>.dart
      - widgets/
        - <feature_name>_screen.dart
        - <other_widgets>
  - domain/
    - models/
      - <model_name>.dart
  - data/
    - repositories/
      - <repository_class>.dart
    - services/
      - <service_class>.dart
    - model/
      - <api_model_class>.dart
  - config/
  - utils/
  - routing/
  - main_staging.dart
  - main_development.dart
  - main.dart
- test/ // Contém testes de unidade e de widget.
  - data/
  - domain/
  - ui/
  - utils/
- testing/ // Contém mocks que outras classes precisam para executar testes.
  - fakes/
  - models/

</FileTree>

A maior parte do código do aplicativo está nas pastas
`data`, `domain` e `ui`.
A pasta data organiza o código por tipo,
porque repositórios e serviços podem ser usados em
diferentes recursos e por vários view models.
A pasta ui organiza o código por recurso,
porque cada recurso tem exatamente uma view e exatamente um view model.

Outros recursos notáveis desta estrutura de pastas:

* A pasta UI também contém um subdiretório chamado "core".
  O core contém widgets e lógica de tema que são compartilhados por várias views,
  como botões com o estilo da sua marca.
* A pasta domain contém os tipos de dados do aplicativo, porque eles são
  usados pelas camadas de dados e ui.
* O aplicativo contém três arquivos "main", que atuam como diferentes pontos de entrada para
  o aplicativo para desenvolvimento, teste e produção.
* Existem dois diretórios relacionados a testes no mesmo nível que `lib`: `test/` possui
  o código de teste e sua própria estrutura corresponde a `lib/`. `testing/` é um
  subpacote que contém mocks e outros utilitários de teste que podem ser usados
  no código de teste de outros pacotes. A pasta `testing/` poderia ser descrita como uma
  versão do seu aplicativo que você não envia. É o conteúdo que é testado.

Há código adicional no aplicativo compass que não pertence à arquitetura.
Para a estrutura completa do pacote, [veja no GitHub][view it on GitHub].

## Outras opções de arquitetura {:#other-architecture-options}

O exemplo neste estudo de caso demonstra como um aplicativo segue nossas
regras arquitetônicas recomendadas, mas existem muitos outros aplicativos de exemplo que
poderiam ter sido escritos. A UI deste aplicativo depende muito de view models
e `ChangeNotifier`, mas poderia facilmente ter sido escrito
com streams ou com outras bibliotecas, como [`riverpod`][],
[`flutter_bloc`][] e [`signals`][].
A comunicação entre as camadas deste aplicativo tratou
tudo com chamadas de método, incluindo a busca por novos dados.
Poderia ter usado streams para expor dados de um repositório para
um view model e ainda seguir as regras abordadas neste guia.

Mesmo se você seguir este guia exatamente,
e optar por não introduzir bibliotecas adicionais, você tem decisões a tomar:
Você terá uma camada de domínio?
Se sim, como você gerenciará o acesso aos dados?
A resposta depende tanto das necessidades de uma equipe individual que
não existe uma única resposta certa.
Independentemente de como você responder a essas perguntas,
os princípios neste guia ajudarão você a escrever aplicativos Flutter escaláveis.

E se você observar bem, todas as arquiteturas não são MVVM de qualquer maneira?

[Compass sample application]: https://github.com/flutter/samples/tree/main/compass_app
[MVVM architectural pattern]: https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93viewmodel
[app architecture guidelines]: /app-architecture/guide
[data layer]: /app-architecture/case-study/data-layer
[UI layer]: /app-architecture/case-study/ui-layer
[Command pattern]: /app-architecture/case-study/ui-layer#command-objects
[`ChangeNotifier`]: {{site.api}}/flutter/foundation/ChangeNotifier-class.html
[`Listenable`]: {{site.api}}/flutter/foundation/Listenable-class.html
[Dependency Injection]: /app-architecture/case-study/dependency-injection
[set up tests]: /app-architecture/case-study/testing
[view it on GitHub]: https://github.com/flutter/samples/tree/main/compass_app
[GitHub]: https://github.com/flutter/samples/tree/main/compass_app
[`riverpod`]: {{site.pub-pkg}}/riverpod
[`flutter_bloc`]: {{site.pub-pkg}}/flutter_bloc
[`signals`]: {{site.pub-pkg}}/signals
[package structure]: /app-architecture/case-study#package-structure

## Feedback

Como esta seção do site está evoluindo,
nós [agradecemos seu feedback][welcome your feedback]!

[welcome your feedback]: https://google.qualtrics.com/jfe/form/SV_4T0XuR9Ts29acw6?page="case-study/index"

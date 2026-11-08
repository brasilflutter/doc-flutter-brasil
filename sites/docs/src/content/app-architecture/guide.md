---
title: Guia para arquitetura de aplicativos
shortTitle: Guia de arquitetura
description: >-
  A maneira recomendada de arquitetar um aplicativo Flutter.
prev:
    title: Conceitos comuns de arquitetura
    path: /app-architecture/concepts
next:
  title: Estudo de caso de arquitetura
  path: /app-architecture/case-study
ia-translate: true
---

As páginas a seguir demonstram como construir um aplicativo usando as boas práticas.
As recomendações neste guia podem ser aplicadas à maioria dos aplicativos,
tornando-os mais fáceis de escalar, testar e manter.
No entanto, elas são diretrizes, não regras inflexíveis,
e você deve adaptá-las às suas necessidades específicas.

Esta seção fornece uma visão geral de alto nível de como os aplicativos Flutter podem ser
arquitetados. Ela explica as camadas de um aplicativo,
juntamente com as classes que existem dentro de cada camada.
A seção seguinte fornece exemplos de código concretos e
percorre um aplicativo Flutter que implementou essas recomendações.

## Visão geral da estrutura do projeto

[Separação de preocupações][Separation-of-concerns] (Separation of concerns) é o princípio mais importante a ser seguido ao
projetar seu aplicativo Flutter.
Seu aplicativo Flutter deve ser dividido em duas grandes camadas,
a camada de UI e a camada de Dados.

Cada camada é ainda dividida em diferentes componentes,
cada um com responsabilidades distintas, uma interface bem definida,
limites e dependências.
Este guia recomenda que você divida seu aplicativo nos seguintes componentes:

* Views (Visões)
* View models (Modelos da view)
* Repositórios
* Services (Serviços)

### MVVM

Se você já se deparou com o [padrão arquitetural Model-View-ViewModel][Model-View-ViewModel architectural pattern] (MVVM),
isso será familiar.
MVVM é um padrão arquitetural que separa uma
funcionalidade de um aplicativo em três partes:
o `Model`, o `ViewModel` e a `View`.
Views e view models compõem a camada de UI de um aplicativo.
Repositórios e serviços representam os dados de um aplicativo,
ou a camada de modelo do MVVM.
Cada um desses componentes é definido na próxima seção.

<img src='/assets/images/docs/app-architecture/guide/mvvm-intro-with-layers.png' alt="Padrão arquitetural MVVM">

Cada funcionalidade em um aplicativo conterá uma view para descrever a UI e
um view model para lidar com a lógica,
um ou mais repositórios como as fontes da verdade para os dados do seu aplicativo,
e zero ou mais services que interagem com APIs externas,
como servidores cliente e plugins de plataforma.

Uma única funcionalidade de um aplicativo pode exigir todos os seguintes objetos:

<img src='/assets/images/docs/app-architecture/guide/feature-architecture-example.png' alt="Um exemplo dos objetos Dart que podem existir em uma funcionalidade usando a arquitetura descrita na página.">

Cada um desses objetos e as setas que os conectam serão explicados
minuciosamente ao final desta página. Ao longo deste guia,
a seguinte versão simplificada desse diagrama será usada como uma âncora.

<img src='/assets/images/docs/app-architecture/guide/feature-architecture-simplified.png' alt="Um diagrama simplificado da arquitetura descrita nesta página.">

:::note
Aplicativos com lógica complexa também podem ter uma camada de lógica que se encontra entre
a camada de UI e a camada de dados. Essa camada de lógica é comumente chamada de *camada de domínio*.
A camada de domínio contém componentes adicionais frequentemente chamados de *interatores* ou
*use-cases* (casos de uso). A camada de domínio é abordada posteriormente neste guia.
:::

[Model-View-ViewModel architectural pattern]: https://en.wikipedia.org/wiki/Model–view–viewmodel

## Camada de UI

A camada de UI de um aplicativo é responsável por interagir com o usuário.
Ela exibe os dados de um aplicativo para o usuário e recebe entrada do usuário,
como eventos de toque e entradas de formulário.

A UI reage a mudanças de dados ou entradas do usuário.
Quando a UI recebe novos dados de um Repositório,
ela deve renderizar novamente para exibir esses novos dados.
Quando o usuário interage com a UI,
ela deve mudar para refletir essa interação.

A camada de UI é composta por dois componentes arquitetônicos,
baseados no padrão de projeto MVVM:

* **Views** descrevem como apresentar os dados do aplicativo ao usuário.
  Especificamente, elas se referem a *composições de widgets* que compõem uma funcionalidade.
  Por exemplo, uma view é frequentemente (mas nem sempre) uma tela que
  possui um widget `Scaffold`, juntamente com
  todos os widgets abaixo dele na árvore de widgets.
  As views também são responsáveis por passar eventos para
  o view model em resposta às interações do usuário.
* **View models** contêm a lógica que converte os dados do aplicativo em *Estado da UI*,
  porque os dados dos repositórios geralmente são formatados de maneira diferente dos
  dados que precisam ser exibidos.
  Por exemplo, pode ser necessário combinar dados de vários repositórios,
  ou você pode querer filtrar uma lista de registros de dados.

Views e view models devem ter uma relação um-para-um.

<img src='/assets/images/docs/app-architecture/guide/feature-architecture-simplified-UI-highlighted.png' alt="Um diagrama simplificado da arquitetura descrita nesta página com os objetos view e view model destacados.">

Em termos mais simples,
um view model gerencia o estado da UI e a view exibe esse estado.
Usando views e view models, sua camada de UI pode manter o estado durante
mudanças de configuração (como rotações de tela),
e você pode testar a lógica de sua UI independentemente dos widgets Flutter.

:::note
'View' é um termo abstrato, e uma view não é igual a um widget.
Widgets são combináveis, e vários podem ser combinados para criar uma view.
Portanto, view models não têm uma relação um-para-um com widgets,
mas sim uma relação um-para-um com uma *coleção* de widgets.
:::

Uma funcionalidade de um aplicativo é centrada no usuário,
e, portanto, definida pela camada de UI.
Cada instância de um par de *view* e *view model* define uma funcionalidade em seu aplicativo.
Essa funcionalidade geralmente é uma tela em seu aplicativo, mas não precisa ser.
Por exemplo, considere fazer login e logout.
O login geralmente é feito em uma tela específica cujo
único propósito é fornecer ao usuário uma maneira de fazer login.
No código do aplicativo, a tela de login seria
composta por uma classe `LoginViewModel` e uma classe `LoginView`.

Por outro lado,
o logout de um aplicativo geralmente não é feito em uma tela dedicada.
A capacidade de fazer logout geralmente é apresentada ao usuário como um botão em
um menu, uma tela de conta de usuário ou qualquer número de locais diferentes.
Geralmente é apresentado em vários locais.
Em cenários como esse, você pode ter um `LogoutViewModel` e um `LogoutView` que
contém apenas um único botão que pode ser colocado em outros widgets.

### Views

No Flutter, views são as classes de widget do seu aplicativo.
Views são o principal método de renderização da UI,
e não devem conter nenhuma lógica de negócios.
Todos os dados de que precisam para renderizar devem ser passados pelo view model.

<img src='/assets/images/docs/app-architecture/guide/feature-architecture-simplified-View-highlighted.png' alt="Um diagrama simplificado da arquitetura descrita nesta página com o objeto view destacado.">

A única lógica que uma view deve conter é:

* Instruções if simples para mostrar e ocultar widgets com base em uma flag ou campo null
  no view model
* Lógica de animação
* Lógica de layout com base em informações do dispositivo, como tamanho ou orientação da tela.
* Lógica de roteamento simples

Toda a lógica relacionada a dados deve ser tratada no view model.

### View models

Um view model expõe os dados do aplicativo necessários para renderizar uma view.
No design de arquitetura descrito nesta página,
a maior parte da lógica do seu aplicativo Flutter reside em view models.

<img src='/assets/images/docs/app-architecture/guide/feature-architecture-simplified-ViewModel-highlighted.png' alt="Um diagrama simplificado da arquitetura descrita nesta página com o objeto view model destacado.">

As principais responsabilidades de um view model incluem:

* Recuperar dados do aplicativo de repositórios e transformá-los em um
  formato adequado para apresentação na view.
  Por exemplo, ele pode filtrar, classificar ou agregar dados.
* Manter o estado atual necessário na view,
  para que a view possa ser reconstruída sem perder dados.
  Por exemplo, ele pode conter flags booleanas para
  renderizar widgets condicionalmente na view, ou um campo que
  rastreia qual seção de um carrossel está ativa na tela.
* Expor callbacks (chamados de **commands**) à view que podem ser
  anexados a um manipulador de eventos, como um pressionamento de botão ou envio de formulário.

Os commands recebem esse nome devido ao [command pattern][],
e são funções Dart que permitem que views
executem lógica complexa sem conhecimento de sua implementação.
Os commands são escritos como membros da classe view model para
serem chamados pelos manipuladores de gestos na classe view.

Você pode encontrar exemplos de views, view models e commands em
a parte da [camada de UI][UI layer] do [Estudo de caso de arquitetura de aplicativo][App architecture case study].

Para uma introdução suave ao MVVM no Flutter,
confira os [fundamentos de gerenciamento de estado][state management fundamentals].

[UI layer]: /app-architecture/case-study/ui-layer
[App architecture case study]: /app-architecture/case-study
[state management fundamentals]: /data-and-backend/state-mgmt/intro

## Camada de dados

A camada de dados de um aplicativo lida com os dados e a lógica de negócios.
Duas partes da arquitetura compõem a camada de dados: serviços e repositórios.
Essas partes devem ter entradas e saídas bem definidas
para simplificar sua reutilização e testabilidade.

<img src='/assets/images/docs/app-architecture/guide/feature-architecture-simplified-Data-highlighted.png' alt="Um diagrama simplificado da arquitetura descrita nesta página com a camada de dados destacada.">

Usando a linguagem MVVM, serviços e repositórios compõem sua *camada de modelo*.

### Repositórios

As classes de [Repositório][Repository] são a fonte da verdade para os dados do seu modelo.
Elas são responsáveis por pesquisar dados de serviços,
e transformar esses dados brutos em **modelos de domínio**.
Modelos de domínio representam os dados que o aplicativo precisa,
formatados de uma forma que suas classes de view model possam consumir.
Deve haver uma classe de repositório para
cada tipo diferente de dados gerenciados em seu aplicativo.

Os repositórios lidam com a lógica de negócios associada aos serviços, como:

* Caching (Armazenamento em cache)
* Tratamento de erros
* Lógica de retry
* Atualização de dados
* Pesquisa de serviços por novos dados
* Atualização de dados com base nas ações do usuário

<img src='/assets/images/docs/app-architecture/guide/feature-architecture-simplified-Repository-highlighted.png' alt="Um diagrama simplificado da arquitetura descrita nesta página com o objeto Repositório destacado.">

Os repositórios geram dados de aplicativo como modelos de domínio.
Por exemplo, um aplicativo de mídia social pode ter uma
classe `UserProfileRepository` que expõe um `Stream<UserProfile?>`,
que emite um novo valor sempre que o usuário faz login ou logout.

Os modelos gerados pelos repositórios são consumidos pelos view models.
Repositórios e view models têm uma relação muitos para muitos.
Um view model pode usar vários repositórios para obter os dados de que precisa,
e um repositório pode ser usado por vários view models.

Os repositórios nunca devem estar cientes uns dos outros.
Se seu aplicativo tiver lógica de negócios que precisa de dados de dois repositórios,
você deve combinar os dados no view model ou na camada de domínio,
especialmente se sua relação repositório-para-view-model for complexa.

#### Gerenciando o estado de sessão de todo o aplicativo

Como os repositórios são a fonte única da verdade para os dados do aplicativo,
eles também são o lugar ideal para gerenciar o **estado de ciclo de vida de todo o aplicativo**: o estado que
precisa ser compartilhado entre vários view models, mas não deve persistir além da
sessão atual do aplicativo.

Exemplos de estado de ciclo de vida de todo o aplicativo incluem uma sessão de usuário ativa,
caches de dados em memória ou configurações transitórias do aplicativo.
Como view models e repositórios têm uma relação de muitos para muitos,
vários view models podem depender da mesma instância de repositório
(normalmente gerenciada por meio de um service locator ou de um contêiner de injeção de dependência).
Isso permite que funcionalidades distintas observem e modifiquem de forma reativa
o mesmo estado compartilhado por meio de streams e métodos expostos pelo repositório,
sem violar a fronteira limpa de um-para-um entre uma view e seu view model.

### Services

Os serviços estão na camada mais baixa do seu aplicativo.
Eles encapsulam endpoints de API e expõem objetos de resposta assíncronos,
como objetos `Future` e `Stream`.
Eles são usados apenas para isolar o carregamento de dados e não mantêm nenhum estado.
Seu aplicativo deve ter uma classe de serviço por fonte de dados.
Exemplos de endpoints que os serviços podem encapsular incluem:

* A plataforma subjacente, como APIs iOS e Android
* Endpoints REST
* Arquivos locais

Como regra geral, os serviços são mais úteis quando
os dados necessários residem fora do código Dart do seu aplicativo -
o que é verdade para cada um dos exemplos anteriores.

Serviços e repositórios têm uma relação muitos para muitos.
Um único Repositório pode usar vários serviços,
e um serviço pode ser usado por vários repositórios.

<img src='/assets/images/docs/app-architecture/guide/feature-architecture-simplified-Service-highlighted.png' alt="Um diagrama simplificado da arquitetura descrita nesta página com o objeto Serviço destacado.">

## Opcional: Camada de domínio

À medida que seu aplicativo cresce e adiciona recursos, você pode precisar abstrair a lógica
que adiciona muita complexidade aos seus view models.
Essas classes são frequentemente chamadas de interatores ou **use-cases** (casos de uso).

Os use-cases são responsáveis por tornar as interações entre
as camadas de UI e de Dados mais simples e reutilizáveis.
Eles pegam dados de repositórios e os tornam adequados para a camada de UI.

<img src='/assets/images/docs/app-architecture/guide/mvvm-intro-with-domain-layer.png' alt="Padrão de projeto MVVM com um objeto de camada de domínio adicionado">

Os use-cases são usados principalmente para encapsular a lógica de negócios que, de outra forma,
estaria no view model e atende a uma ou mais das seguintes condições:

1. Requer a junção de dados de vários repositórios
2. É extremamente complexo
3. A lógica será reutilizada por diferentes view models

Essa camada é opcional porque nem todos os aplicativos ou funcionalidades dentro de um
aplicativo têm esses requisitos.
Se você suspeitar que seu aplicativo se
beneficiaria dessa camada adicional, considere os prós e contras:

| Prós                                                                     | Contras                                                                                       |
|--------------------------------------------------------------------------|--------------------------------------------------------------------------------------------|
| ✅ Evitar duplicação de código em view models                                  | ❌ Aumenta a complexidade de sua arquitetura, adicionando mais classes e maior carga cognitiva |
| ✅ Melhora a testabilidade separando a lógica de negócios complexa da lógica de UI | ❌ O teste requer mocks adicionais                                                        |
| ✅ Melhora a legibilidade do código em view models                                | ❌ Adiciona boilerplate adicional ao seu código                                                 |

{:.table .table-striped}

### Acesso a dados com use-cases

Outra consideração ao adicionar uma camada de domínio é se os view models
continuarão a ter acesso direto aos dados do repositório, ou se você aplicará
view models para passar por use-cases para obter seus dados. Em outras palavras,
você adicionará use-cases conforme precisar deles?
Talvez quando você perceber lógica repetida em seus view models?
Ou, você criará um caso de uso cada vez que um view model precisar de dados,
mesmo que a lógica no caso de uso seja simples?

Se você optar por fazer o último,
ele intensifica os prós e contras descritos anteriormente.
O código do seu aplicativo será extremamente modular e testável,
mas também adiciona uma quantidade significativa de sobrecarga desnecessária.

Uma boa abordagem é adicionar use-cases apenas quando necessário.
Se você descobrir que seus view models estão
acessando dados por meio de use-cases na maioria das vezes,
você sempre pode refatorar seu código para utilizar use-cases exclusivamente.
O aplicativo de exemplo usado posteriormente neste guia tem use-cases para algumas funcionalidades,
mas também tem view models que interagem diretamente com repositórios.
Uma funcionalidade complexa pode acabar se parecendo com isso:

<img src='/assets/images/docs/app-architecture/guide/feature-architecture-simplified-with-logic-layer.png'
alt="Um diagrama simplificado da arquitetura descrita nesta página com um objeto de caso de uso.">

Este método de adicionar use-cases é definido pelas seguintes regras:

* Use-cases dependem de repositórios
* Use-cases e repositórios têm uma relação muitos para muitos
* View models dependem de um ou mais use-cases *e* um ou mais repositórios

Este método de usar use-cases acaba parecendo
menos uma lasanha em camadas, e mais um jantar com
dois pratos principais (camadas de UI e dados) e um acompanhamento (camada de domínio).
Use-cases são apenas classes de utilitário que têm entradas e saídas bem definidas.
Essa abordagem é flexível e extensível,
mas requer maior diligência para manter a ordem.

[Separation-of-concerns]: https://en.wikipedia.org/wiki/Separation_of_concerns
[command pattern]: https://en.wikipedia.org/wiki/Command_pattern
[Repository]: https://martinfowler.com/eaaCatalog/repository.html

## Feedback

Como esta seção do site está evoluindo,
nós [agradecemos seu feedback][welcome your feedback]!

[welcome your feedback]: https://google.qualtrics.com/jfe/form/SV_4T0XuR9Ts29acw6?page="guide"

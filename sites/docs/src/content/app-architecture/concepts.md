---
title: Conceitos comuns de arquitetura
shortTitle: Conceitos de arquitetura
description: >
  Aprenda sobre conceitos comuns de arquitetura no design de aplicações
  e como eles se aplicam ao Flutter.
prev:
    title: Arquitetando apps Flutter
    path: /app-architecture
next:
    title: Guia de arquitetura de apps
    path: /app-architecture/guide
ia-translate: true
---

Nesta seção, você encontrará princípios comprovados que orientam
decisões arquitetônicas no desenvolvimento de aplicativos em geral,
bem como informações sobre como eles se encaixam especificamente no Flutter.
É uma introdução suave ao vocabulário e aos conceitos relacionados
à arquitetura recomendada e às melhores práticas,
para que possam ser explorados em mais detalhes ao longo deste guia.

## Separação de responsabilidades {:#separation-of-concerns}

A [separação de responsabilidades][Separation-of-concerns] é um princípio central no desenvolvimento de aplicativos
que promove a modularidade e a manutenção ao dividir a funcionalidade de um aplicativo
em unidades distintas e independentes. De forma geral, isso significa separar a lógica de UI
da lógica de negócios.
Isso é frequentemente descrito como arquitetura *em camadas*.
Dentro de cada camada, você deve dividir sua aplicação por funcionalidade ou recurso.
Por exemplo, a lógica de autenticação do aplicativo deve estar em uma classe diferente
da lógica de busca.

No Flutter, isso também se aplica aos [widgets](/resources/glossary#widget) na camada de UI. Você deve escrever widgets
reutilizáveis e enxutos, que contenham o mínimo de lógica possível.

## Arquitetura em camadas {:#layered-architecture}

Aplicações Flutter devem ser escritas em *camadas*. A arquitetura em camadas é um padrão
de design de software que organiza uma aplicação em camadas distintas, cada uma com
responsabilidades específicas. Tipicamente, aplicações são divididas em 2 a 3 camadas,
dependendo da complexidade.

<img src='/assets/images/docs/app-architecture/common-architecture-concepts/horizontal-layers-with-icons.png' alt="As três camadas comuns da arquitetura de apps: camada de UI, camada de lógica e camada de dados.">

* **Camada de UI** - Exibe dados ao usuário que são expostos pela camada de lógica
  de negócios e lida com a interação do usuário. Também é conhecida como
  "camada de apresentação".
* **Camada de lógica** - Implementa a lógica de negócios central e facilita
  a interação entre a camada de dados e a camada de UI. Frequentemente chamada
  de "camada de domínio".
  Essa camada é opcional e só deve ser implementada se sua aplicação tiver lógica
  de negócios complexa no cliente. Muitos aplicativos estão apenas preocupados em
  apresentar dados a um usuário e permitir que o usuário altere esses dados
  (conhecidos informalmente como apps CRUD). Esses aplicativos podem não precisar dessa camada opcional.
* **Camada de dados** - Gerencia interações com fontes de dados, como bancos de dados ou
  plugins da plataforma. Expõe dados e métodos para a camada de lógica de negócios.

Essas são chamadas de "camadas" porque cada camada pode se comunicar apenas com
as camadas diretamente abaixo ou acima dela. A camada de UI não deve saber que a
camada de dados existe, e vice-versa.

## Fonte única da verdade {:#single-source-of-truth}

Cada tipo de dado no seu aplicativo deve ter uma [fonte única da verdade][single source of truth].
A fonte da verdade é responsável por representar o estado local ou remoto.
Se os dados podem ser modificados no aplicativo, a classe SSOT (Fonte Única da Verdade)
deve ser a única classe capaz de fazê-lo.

Isso pode reduzir drasticamente o número de bugs no aplicativo,
e simplificar o código, já que você terá apenas uma cópia de cada dado.

Geralmente, a fonte da verdade para um dado específico é mantida em uma classe chamada
**Repositório**, que faz parte da camada de dados. Normalmente, existe uma classe
de repositório para cada tipo de dado no seu aplicativo.

Esse princípio pode ser aplicado entre camadas e componentes da aplicação,
bem como dentro de classes individuais. Por exemplo,
uma classe Dart pode usar [getters][] para derivar valores de um campo SSOT
(em vez de ter múltiplos campos que precisam ser atualizados de forma independente)
ou uma lista de [registros][records] para agrupar valores relacionados
(em vez de listas paralelas cujos índices podem ficar desalinhados).

## Fluxo unidirecional de dados {:#unidirectional-data-flow}

O [fluxo unidirecional de dados][Unidirectional data flow] (UDF) refere-se a um padrão de design que ajuda
a desacoplar o estado da UI que exibe esse estado. Em termos simples,
o estado flui da camada de dados através da camada de lógica e,
eventualmente, para os widgets na camada de UI.
Os eventos da interação do usuário fluem na direção oposta,
da camada de apresentação de volta pela camada de lógica até a camada de dados.

<img src='/assets/images/docs/app-architecture/common-architecture-concepts/horizontal-layers-with-UDF.png' alt="As três camadas comuns da arquitetura de apps: camada de UI, camada de lógica e camada de dados, com o fluxo de estado da camada de dados para a camada de UI.">

No UDF, o ciclo de atualização da interação do usuário até a reconstrução da UI segue
estes passos:

1. [Camada de UI] Um evento ocorre devido à interação do usuário, como o clique em um botão.
   O callback do manipulador de eventos do widget chama um método exposto por uma classe
   na camada de lógica.
2. [Camada de lógica] A classe de lógica chama métodos expostos por um repositório
   que sabe como modificar os dados.
3. [Camada de dados] O repositório atualiza os dados (se necessário) e fornece os novos dados
   para a classe de lógica.
4. [Camada de lógica] A classe de lógica salva seu novo estado, que envia para a UI.
5. [Camada de UI] A UI exibe o novo estado do modelo de visualização.

Novos dados também podem começar na camada de dados.
Por exemplo, um repositório pode realizar polling em um servidor HTTP por novos dados.
Nesse caso, o fluxo de dados realiza apenas a segunda metade da jornada.
O mais importante é que as mudanças de dados sempre acontecem
na [SSOT][], que é a camada de dados.
Isso torna seu código mais fácil de entender, menos propenso a erros e
evita a criação de dados malformados ou inesperados.

## A UI é uma função do estado (imutável) {:#ui-is-a-function-of-immutable-state}

O Flutter é declarativo,
o que significa que ele constrói a UI para refletir o estado atual
do seu aplicativo. Quando o estado muda,
seu aplicativo deve disparar uma reconstrução da UI
dependente desse estado. No Flutter, isso é frequentemente descrito como
"UI é uma função do estado".

<img src='/assets/images/docs/app-architecture/common-architecture-concepts/ui-f-state.png' style="width:50%; margin:auto; display:block" alt="UI é uma função do estado.">

É crucial que os dados sejam os motores da sua UI, e não o contrário.
Os dados devem ser imutáveis e persistentes,
e as visualizações devem conter o mínimo possível de lógica.
Isso minimiza a possibilidade de perda de dados quando um aplicativo é fechado
e torna o aplicativo mais testável e resiliente a bugs.

## Extensibilidade {:#extensibility}

Cada componente da arquitetura deve ter uma lista bem definida de entradas e saídas.
Por exemplo, um modelo de visualização na camada de lógica deve apenas
receber fontes de dados como entradas, tais como repositórios,
e deve apenas expor comandos e dados formatados para visualizações como saídas.

O uso de interfaces bem definidas dessa maneira permite trocar
implementações concretas das suas classes sem a necessidade de
alterar nenhum código que consuma essas interfaces.

## Testabilidade {:#testability}

Os princípios que tornam o software extensível também o tornam mais fácil de testar.
Por exemplo, é possível testar a lógica autônoma de um modelo de visualização
simulando um repositório.
Os testes do modelo de visualização não precisam simular outras partes do aplicativo,
e você pode testar a lógica da UI separadamente dos widgets do Flutter em si.

Isso também torna seu aplicativo mais flexível.
Será simples e de baixo risco adicionar nova lógica e novos elementos de UI.
Por exemplo, adicionar um novo modelo de visualização não pode quebrar nenhuma lógica
das camadas de dados ou lógica de negócios.

A próxima seção explica a ideia de entradas e saídas para qualquer componente
na arquitetura do seu aplicativo.

[Separation-of-concerns]: https://en.wikipedia.org/wiki/Separation_of_concerns
[single source of truth]: https://en.wikipedia.org/wiki/Single_source_of_truth
[SSOT]: https://en.wikipedia.org/wiki/Single_source_of_truth
[getters]: {{site.dart-site}}/effective-dart/design#do-use-getters-for-operations-that-conceptually-access-properties
[records]: {{site.dart-site}}/language/records
[Unidirectional data flow]: https://en.wikipedia.org/wiki/Unidirectional_Data_Flow_(computer_science)

## Feedback

Como esta seção do site está em evolução,
[suas sugestões são bem-vindas][welcome your feedback]!

[welcome your feedback]: https://google.qualtrics.com/jfe/form/SV_4T0XuR9Ts29acw6?page="concepts"

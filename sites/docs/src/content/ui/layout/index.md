---
title: Layouts em Flutter
shortTitle: Layout
description: >-
  Aprenda como funciona o mecanismo de layout do Flutter e como construir o layout do seu aplicativo.
ia-translate: true
---

## Visão geral {:#overview}

:::secondary Qual é o objetivo?
* Layouts no Flutter são construídos com widgets.
* Widgets são classes usadas para construir interfaces de usuário.
* Widgets também são usados para construir elementos de UI.
* Combine widgets simples para criar widgets complexos.
:::

O núcleo do mecanismo de layout do Flutter são os widgets.
No Flutter, quase tudo é um widget&mdash;até mesmo
os modelos de layout são widgets. As imagens, ícones
e textos que você vê em um app Flutter são todos widgets.
Mas coisas que você não vê também são widgets,
como linhas, colunas e grades que organizam,
limitam e alinham os widgets visíveis.
Você cria um layout combinando widgets para construir widgets
mais complexos.

## Exemplo conceitual {:#conceptual-example}

No exemplo a seguir, a primeira captura de tela exibe
três ícones com legendas e a segunda captura de tela inclui
o layout visual de linhas e colunas. Na segunda
captura de tela, `debugPaintSizeEnabled` está definido como `true` para que você
possa ver o layout visual.

<div class="side-by-side">
  <div class="centered-rows">
    <img src='/assets/images/docs/ui/layout/lakes-icons.png' alt="Exemplo de layout">
  </div>
  <div class="centered-rows">
    <img src='/assets/images/docs/ui/layout/lakes-icons-visual.png' alt="Exemplo de layout com depuração visual">
  </div>
</div>

Aqui está um diagrama da árvore de widgets do exemplo
anterior:

<img src='/assets/images/docs/ui/layout/sample-flutter-layout.png' class="text-center diagram-wrap" alt="Árvore de nós">

A maior parte disso deve parecer como você espera, mas você pode estar se perguntando
sobre os containers (mostrados em rosa). [`Container`][] é uma classe de widget
que permite personalizar seu widget filho. Use um `Container` quando
quiser adicionar padding, margens, bordas ou cor de fundo,
para citar algumas de suas capacidades.

Cada widget [`Text`][] é colocado em um `Container`
para adicionar margens. A [`Row`][] inteira também é colocada em um
`Container` para adicionar padding ao redor da linha.

O restante da UI é controlado por propriedades.
Defina a cor de um [`Icon`][] usando sua propriedade `color`.
Use a propriedade `Text.style` para definir a fonte, sua cor, peso etc.
As colunas e linhas têm propriedades que permitem especificar como seus
filhos são alinhados vertical ou horizontalmente e quanto espaço
os filhos devem ocupar.

:::note
A maioria das capturas de tela neste tutorial é exibida com
`debugPaintSizeEnabled` definido como `true` para que você possa ver o
layout visual. Para obter mais informações, consulte
[Depurando problemas de layout visualmente][Debugging layout issues visually].
:::

[`Container`]: {{site.api}}/flutter/widgets/Container-class.html
[Debugging layout issues visually]: /tools/devtools/inspector#debugging-layout-issues-visually
[`Icon`]: {{site.material_ui}}/Icons-class.html
[`Row`]: {{site.api}}/flutter/widgets/Row-class.html
[`Text`]: {{site.api}}/flutter/widgets/Text-class.html

## Posicionando (lay out) um widget {:#lay-out-a-widget}

Como posicionar (lay out) um único widget no Flutter? Esta seção
mostra como criar e exibir um widget simples.
Também mostra todo o código de um simples aplicativo Hello World.

No Flutter, são necessários apenas alguns passos para colocar texto, um ícone
ou uma imagem na tela.

### 1. Selecionar um widget de layout {:#1-select-a-layout-widget}

Escolha entre uma variedade de [widgets de layout][layout widgets] com base
em como você deseja alinhar ou restringir um widget visível,
já que essas características são geralmente transmitidas para o
widget contido.

Por exemplo, você pode usar o widget de layout
[`Center`][] para centralizar um widget visível
horizontal e verticalmente:

```dart
Center(
  // Content to be centered here.
)
```

[`Center`]: {{site.api}}/flutter/widgets/Center-class.html
[layout widgets]: /ui/widgets/layout

### 2. Criar um widget visível {:#2-create-a-visible-widget}

Escolha um [widget visível][visible widget] para o seu aplicativo conter
elementos visíveis, como [texto][text], [imagens][images] ou
[ícones][icons].

Por exemplo, você pode usar o widget [`Text`][] para exibir
algum texto:

```dart
Text('Hello World')
```

[icons]: {{site.material_ui}}/Icons-class.html
[images]: {{site.api}}/flutter/widgets/Image-class.html
[text]: {{site.api}}/flutter/widgets/Text-class.html
[`Text`]: {{site.api}}/flutter/widgets/Text-class.html
[visible widget]: /ui/widgets

### 3. Adicionar o widget visível ao widget de layout {:#3-add-the-visible-widget-to-the-layout-widget}

<?code-excerpt path-base="layout/base"?>

Todos os widgets de layout possuem um dos seguintes:

* Uma propriedade `child` se eles receberem um único filho&mdash;por exemplo,
  `Center` ou `Container`
* Uma propriedade `children` se eles receberem uma lista de widgets&mdash;por exemplo,
  `Row`, `Column`, `ListView` ou `Stack`.

Adicione o widget `Text` ao widget `Center`:

<?code-excerpt "lib/main.dart (centered-text)" replace="/body: //g"?>
```dart
const Center(
  child: Text('Hello World'),
),
```

### 4. Adicionar o widget de layout à página {:#4-add-the-layout-widget-to-the-page}

Um aplicativo Flutter é, em si, um widget, e a maioria dos widgets tem um método [`build()`][].
Instanciar e retornar um widget no método `build()` do aplicativo
exibe o widget.

<a id="non-material-apps" aria-hidden="true"></a>
<a id="material-apps" aria-hidden="true"></a>
<a id="cupertino-apps" aria-hidden="true"></a>

<Tabs key="app-type-tabs" wrapped="true">

<Tab name="Aplicativos padrão">

Para um aplicativo genérico, você pode adicionar o widget `Container`
ao método `build()` do aplicativo:

<?code-excerpt path-base="layout/non_material"?>
<?code-excerpt "lib/main.dart (my-app)"?>
```dart
class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: const BoxDecoration(color: Colors.white),
      child: const Center(
        child: Text(
          'Hello World',
          textDirection: TextDirection.ltr,
          style: TextStyle(fontSize: 32, color: Colors.black87),
        ),
      ),
    );
  }
}
```

Por padrão, um aplicativo genérico não inclui um `AppBar`,
um título ou uma cor de fundo. Se você deseja ter esses recursos em um
aplicativo genérico, precisará construí-los você mesmo. Este aplicativo
altera a cor de fundo para branco e o texto para
cinza escuro para imitar um aplicativo Material.

</Tab>

<Tab name="Aplicativos Material">

Para um aplicativo `Material`, você pode usar um widget [`Scaffold`][];
ele fornece um banner padrão, cor de fundo
e tem uma API para adicionar drawers, snack bars e bottom sheets.
Então você pode adicionar o widget `Center` diretamente à propriedade `body`
da página inicial.

<?code-excerpt path-base="layout/base"?>
<?code-excerpt "lib/main.dart (my-app)"?>
```dart
class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    const String appTitle = 'Flutter layout demo';
    return MaterialApp(
      title: appTitle,
      home: Scaffold(
        appBar: AppBar(title: const Text(appTitle)),
        body: const Center(
          child: Text('Hello World'),
        ),
      ),
    );
  }
}
```

:::note
A [biblioteca Material][Material library] implementa widgets que seguem os
princípios do [Material Design][]. Ao projetar sua UI, você pode
usar exclusivamente widgets da [biblioteca de widgets][widgets library] padrão, ou pode usar
widgets da biblioteca Material. Você pode combinar widgets de ambas as
bibliotecas, personalizar widgets existentes
ou criar seu próprio conjunto de widgets personalizados.
:::

</Tab>

<Tab name="Aplicativos Cupertino">

Para criar um aplicativo `Cupertino`,
use os widgets `CupertinoApp` e [`CupertinoPageScaffold`][].

Diferentemente do `Material`, ele não fornece um banner ou cor de fundo padrão.
Você precisa defini-los você mesmo.

* Para definir cores padrão, passe um [`CupertinoThemeData`][] configurado
  para a propriedade `theme` do seu aplicativo.
* Para adicionar uma barra de navegação no estilo iOS ao topo do seu aplicativo, adicione um
  widget [`CupertinoNavigationBar`][] à propriedade `navigationBar`
  do seu scaffold.
  Você pode usar as cores fornecidas por [`CupertinoColors`][] para
  configurar seus widgets de acordo com o design do iOS.

* Para organizar o corpo do seu aplicativo, defina a propriedade `child` do seu scaffold
  com o widget desejado como valor, como `Center` ou `Column`.

Para saber quais outros componentes de UI você pode adicionar, confira a
[biblioteca Cupertino][Cupertino library].

<?code-excerpt "lib/cupertino.dart (my-app)"?>
```dart
class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return const CupertinoApp(
      title: 'Flutter layout demo',
      theme: CupertinoThemeData(
        brightness: Brightness.light,
        primaryColor: CupertinoColors.systemBlue,
      ),
      home: CupertinoPageScaffold(
        navigationBar: CupertinoNavigationBar(
          backgroundColor: CupertinoColors.systemGrey,
          middle: Text('Flutter layout demo'),
        ),
        child: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [Text('Hello World')],
          ),
        ),
      ),
    );
  }
}
```

:::note
A [biblioteca Cupertino][Cupertino library] implementa widgets que seguem as
[Human Interface Guidelines da Apple para iOS][Apple's Human Interface Guidelines for iOS].
Ao projetar sua UI, você pode usar
widgets da [biblioteca de widgets][widgets library] padrão ou da biblioteca Cupertino.
Você pode combinar widgets de ambas as bibliotecas, personalizar widgets existentes
ou criar seu próprio conjunto de widgets personalizados.
:::

</Tab>

</Tabs>

[`CupertinoColors`]: {{site.cupertino_ui}}/CupertinoColors-class.html
[`CupertinoPageScaffold`]: {{site.cupertino_ui}}/CupertinoPageScaffold-class.html
[`CupertinoThemeData`]: {{site.cupertino_ui}}/CupertinoThemeData-class.html
[`CupertinoNavigationBar`]: {{site.cupertino_ui}}/CupertinoNavigationBar-class.html
[Cupertino library]: {{site.cupertino_ui}}
[Apple's Human Interface Guidelines for iOS]: {{site.apple-dev}}/design/human-interface-guidelines/designing-for-ios
[`build()`]: {{site.api}}/flutter/widgets/StatelessWidget/build.html
[Material library]: {{site.material_ui}}
[`Scaffold`]: {{site.material_ui}}/Scaffold-class.html
[widgets library]: {{site.api}}/flutter/widgets/widgets-library.html

### 5. Executar seu aplicativo {:#5-run-your-app}

<div class="side-by-side">
<div>

Depois de adicionar seus widgets, execute seu aplicativo. Quando você executar
o aplicativo, deverá ver _Hello World_.

Código-fonte do aplicativo:

* [Aplicativo Material]({{site.repo.this}}/tree/main/examples/layout/base)
* [Aplicativo não-Material]({{site.repo.this}}/tree/main/examples/layout/non_material)

</div>
<DashImage figure image="ui/layout/hello-world.png" alt="Captura de tela do aplicativo exibindo Hello World" img-style="max-height: 400px;"  />
</div>
<hr>

## Organizar múltiplos widgets vertical e horizontalmente {:#lay-out-multiple-widgets-vertically-and-horizontally}

<?code-excerpt path-base=""?>

Um dos padrões de layout mais comuns é organizar
widgets vertical ou horizontalmente. Você pode usar um
widget `Row` para organizar widgets horizontalmente,
e um widget `Column` para organizar widgets verticalmente.

:::secondary Qual é o objetivo?
* `Row` e `Column` são dois dos padrões de layout mais comumente usados.
* `Row` e `Column` recebem, cada um, uma lista de widgets filhos.
* Um widget filho pode ser, ele próprio, uma `Row`, uma `Column`
    ou outro widget complexo.
* Você pode especificar como uma `Row` ou `Column` alinha seus filhos,
    tanto vertical quanto horizontalmente.
* Você pode esticar ou limitar widgets filhos específicos.
* Você pode especificar como os widgets filhos usam o
    espaço disponível da `Row` ou da `Column`.
:::

Para criar uma linha ou coluna no Flutter, você adiciona uma lista de widgets
filhos a um widget [`Row`][] ou [`Column`][]. Por sua vez,
cada filho pode ser, ele próprio, uma linha ou coluna, e assim por diante.
O exemplo a seguir mostra como é possível aninhar linhas ou
colunas dentro de linhas ou colunas.

Este layout é organizado como uma `Row`. A linha contém dois filhos:
uma coluna à esquerda e uma imagem à direita:

<img src='/assets/images/docs/ui/layout/pavlova-diagram.png' class="diagram-wrap" alt="Captura de tela com anotações mostrando a linha que contém dois filhos">

A árvore de widgets da coluna da esquerda contém linhas e colunas aninhadas.

<img src='/assets/images/docs/ui/layout/pavlova-left-column-diagram.png' class="diagram-wrap" alt="Diagrama mostrando a coluna da esquerda dividida em suas sublinhas e subcolunas">

Você irá implementar parte do código de layout da Pavlova em
[Aninhando linhas e colunas](#nesting-rows-and-columns).

:::note
`Row` e `Column` são widgets primitivos básicos para layouts horizontais
e verticais&mdash;esses widgets de baixo nível permitem a máxima
personalização. O Flutter também oferece widgets especializados de nível
mais alto que podem ser suficientes para suas necessidades. Por exemplo,
em vez de `Row`, você pode preferir [`ListTile`][],
um widget fácil de usar com propriedades para ícones à esquerda (leading) e à direita (trailing)
e até 3 linhas de texto. Em vez de `Column`, você pode preferir
[`ListView`][], um layout semelhante a uma coluna que rola automaticamente
se o conteúdo for muito longo para caber no espaço disponível.
Para mais informações, consulte [Widgets de layout comuns][Common layout widgets].
:::

[Common layout widgets]: #common-layout-widgets
[`Column`]: {{site.api}}/flutter/widgets/Column-class.html
[`ListTile`]: {{site.material_ui}}/ListTile-class.html
[`ListView`]: {{site.api}}/flutter/widgets/ListView-class.html
[`Row`]: {{site.api}}/flutter/widgets/Row-class.html

### Alinhando widgets {:#aligning-widgets}

Você controla como uma linha ou coluna alinha seus filhos usando as
propriedades `mainAxisAlignment` e `crossAxisAlignment`.
Para uma linha, o eixo principal é horizontal e o eixo cruzado é
vertical. Para uma coluna, o eixo principal é vertical e o eixo
cruzado é horizontal.

<div class="side-by-side">
  <div class="centered-rows">
    <img src='/assets/images/docs/ui/layout/row-diagram.png' class="diagram-wrap" alt="Diagrama mostrando o eixo principal e o eixo cruzado de uma linha">
  </div>
  <div class="centered-rows">
    <img src='/assets/images/docs/ui/layout/column-diagram.png' class="diagram-wrap" alt="Diagrama mostrando o eixo principal e o eixo cruzado de uma coluna">
  </div>
</div>

Os enums [`MainAxisAlignment`][] e [`CrossAxisAlignment`][]
oferecem uma variedade de constantes para controlar o alinhamento.

:::note
Ao adicionar imagens ao seu projeto,
você precisa atualizar o arquivo `pubspec.yaml` para
acessá-las&mdash;este exemplo usa `Image.asset` para exibir
as imagens. Para mais informações, consulte o
[arquivo `pubspec.yaml`][`pubspec.yaml` file] deste exemplo ou [Adicionando assets e imagens][Adding assets and images].
Você não precisa fazer isso se estiver referenciando imagens online
usando `Image.network`.
:::

No exemplo a seguir, cada uma das 3 imagens tem 100 pixels de largura.
A render box (neste caso, a tela inteira)
tem mais de 300 pixels de largura, então definir o alinhamento do eixo principal
como `spaceEvenly` divide o espaço horizontal livre
igualmente entre, antes e depois de cada imagem.

<div class="code-and-content">
<div>

<?code-excerpt "layout/row_column/lib/main.dart (row)" replace="/Row/[!$&!]/g"?>
```dart
[!Row!](
  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
  children: [
    Image.asset('images/pic1.jpg'),
    Image.asset('images/pic2.jpg'),
    Image.asset('images/pic3.jpg'),
  ],
);
```

</div>
<div>
  <img src='/assets/images/docs/ui/layout/row-spaceevenly-visual.png' class="small-diagram-wrap" alt="Linha com 3 imagens espaçadas igualmente">

  **Código-fonte do aplicativo:** [row_column]({{site.repo.this}}/tree/main/examples/layout/row_column)
</div>
</div>

As colunas funcionam da mesma maneira que as linhas. O exemplo a seguir mostra uma coluna
de 3 imagens, cada uma com 100 pixels de altura. A altura da render box
(neste caso, a tela inteira) é superior a 300 pixels, portanto,
definir o alinhamento do eixo principal como `spaceEvenly` divide o espaço vertical
livre igualmente entre, acima e abaixo de cada imagem.

<div class="code-and-content">
<div>

  <?code-excerpt "layout/row_column/lib/main.dart (column)" replace="/Column/[!$&!]/g"?>
  ```dart
  [!Column!](
    mainAxisAlignment: MainAxisAlignment.spaceEvenly,
    children: [
      Image.asset('images/pic1.jpg'),
      Image.asset('images/pic2.jpg'),
      Image.asset('images/pic3.jpg'),
    ],
  );
  ```

</div>
<div class="text-center">
  <img src='/assets/images/docs/ui/layout/column-visual.png' height="250px" class="small-diagram-wrap" alt="Coluna mostrando 3 imagens espaçadas igualmente">

  **Código-fonte do aplicativo:** [row_column]({{site.repo.this}}/tree/main/examples/layout/row_column)
</div>
</div>

[`CrossAxisAlignment`]: {{site.api}}/flutter/rendering/CrossAxisAlignment.html
[`MainAxisAlignment`]: {{site.api}}/flutter/rendering/MainAxisAlignment.html
[`pubspec.yaml` file]: {{site.repo.this}}/tree/main/examples/layout/row_column/pubspec.yaml

### Dimensionando widgets {:#sizing-widgets}

Quando um layout é grande demais para caber em um dispositivo, um padrão listrado
amarelo e preto aparece ao longo da borda afetada.
Aqui está um [exemplo][sizing] de uma linha que é larga demais:

<img src='/assets/images/docs/ui/layout/layout-too-large.png' class="text-center" style="max-height: 15rem;" alt="Linha larga demais">

Widgets podem ser dimensionados para caber em uma linha ou coluna usando o widget
[`Expanded`][]. Para corrigir o exemplo anterior, em que a
linha de imagens é larga demais para sua render box,
envolva cada imagem com um widget `Expanded`.

<div class="code-and-content">
<div>

  <?code-excerpt "layout/sizing/lib/main.dart (expanded-images)" replace="/Expanded/[!$&!]/g"?>
  ```dart
  Row(
    crossAxisAlignment: CrossAxisAlignment.center,
    children: [
      [!Expanded!](child: Image.asset('images/pic1.jpg')),
      [!Expanded!](child: Image.asset('images/pic2.jpg')),
      [!Expanded!](child: Image.asset('images/pic3.jpg')),
    ],
  );
  ```

</div>
<div>
  <img src='/assets/images/docs/ui/layout/row-expanded-2-visual.png' class="small-diagram-wrap" alt="Linha de 3 imagens que são largas demais, mas cada uma é restringida a ocupar apenas 1/3 do espaço">

  **Código-fonte do aplicativo:** [sizing]({{site.repo.this}}/tree/main/examples/layout/sizing)
</div>
</div>

Talvez você queira que um widget ocupe o dobro do espaço de seus
irmãos. Para isso, use a propriedade `flex` do widget `Expanded`,
um inteiro que determina o fator flex de um widget.
O fator flex padrão é 1. O código a seguir define
o fator flex da imagem do meio como 2:

<div class="code-and-content">
<div>

  <?code-excerpt "layout/sizing/lib/main.dart (expanded-images-with-flex)" replace="/flex.*/[!$&!]/g"?>
  ```dart
  Row(
    crossAxisAlignment: CrossAxisAlignment.center,
    children: [
      Expanded(child: Image.asset('images/pic1.jpg')),
      Expanded([!flex: 2, child: Image.asset('images/pic2.jpg')),!]
      Expanded(child: Image.asset('images/pic3.jpg')),
    ],
  );
  ```

</div>
<div>
  <img src='/assets/images/docs/ui/layout/row-expanded-visual.png' class="small-diagram-wrap" alt="Linha de 3 imagens com a imagem do meio duas vezes mais larga que as outras">

  **Código-fonte do aplicativo:** [sizing]({{site.repo.this}}/tree/main/examples/layout/sizing)
</div>
</div>

[`Expanded`]: {{site.api}}/flutter/widgets/Expanded-class.html
[sizing]: {{site.repo.this}}/tree/main/examples/layout/sizing

### Agrupando widgets {:#packing-widgets}

Por padrão, uma linha ou coluna ocupa o máximo de espaço possível ao longo de seu eixo principal,
mas se você quiser agrupar os filhos bem próximos,
defina seu `mainAxisSize` como `MainAxisSize.min`. O exemplo a seguir
usa essa propriedade para agrupar os ícones de estrela.

<div class="code-and-content">
<div>

  <?code-excerpt "layout/pavlova/lib/main.dart (stars)" replace="/mainAxisSize.*/[!$&!]/g; /\w+ \w+ = //g; /;//g"?>
  ```dart
  Row(
    [!mainAxisSize: MainAxisSize.min,!]
    children: [
      Icon(Icons.star, color: Colors.green[500]),
      Icon(Icons.star, color: Colors.green[500]),
      Icon(Icons.star, color: Colors.green[500]),
      const Icon(Icons.star, color: Colors.black),
      const Icon(Icons.star, color: Colors.black),
    ],
  )
  ```

</div>
<div>
  <img src='/assets/images/docs/ui/layout/packed.png' class="small-diagram-wrap" alt="Linha de 5 estrelas, agrupadas no meio da linha">

  **Código-fonte do aplicativo:** [pavlova]({{site.repo.this}}/tree/main/examples/layout/pavlova)
</div>
</div>

### Aninhando linhas e colunas {:#nesting-rows-and-columns}

O framework de layout permite que você aninhe linhas e colunas
dentro de linhas e colunas com a profundidade que precisar.
Vamos dar uma olhada no código da seção contornada
do seguinte layout:

<img src='/assets/images/docs/ui/layout/pavlova-large-annotated.png' class="border text-center" alt="Captura de tela do aplicativo pavlova, com as linhas de classificações e de ícones contornadas em vermelho">

A seção contornada é implementada como duas linhas. A linha de classificações contém
cinco estrelas e o número de avaliações. A linha de ícones contém três
colunas de ícones e texto.

A árvore de widgets da linha de classificações:

<img src='/assets/images/docs/ui/layout/widget-tree-pavlova-rating-row.png' class="text-center diagram-wrap" alt="Árvore de widgets da linha de classificações">

A variável `ratings` cria uma linha contendo uma linha menor
de ícones de 5 estrelas e texto:

<?code-excerpt "layout/pavlova/lib/main.dart (ratings)" replace="/ratings/[!$&!]/g"?>
```dart
final stars = Row(
  mainAxisSize: MainAxisSize.min,
  children: [
    Icon(Icons.star, color: Colors.green[500]),
    Icon(Icons.star, color: Colors.green[500]),
    Icon(Icons.star, color: Colors.green[500]),
    const Icon(Icons.star, color: Colors.black),
    const Icon(Icons.star, color: Colors.black),
  ],
);

final [!ratings!] = Container(
  padding: const EdgeInsets.all(20),
  child: Row(
    mainAxisAlignment: MainAxisAlignment.spaceEvenly,
    children: [
      stars,
      const Text(
        '170 Reviews',
        style: TextStyle(
          color: Colors.black,
          fontWeight: FontWeight.w800,
          fontFamily: 'Roboto',
          letterSpacing: 0.5,
          fontSize: 20,
        ),
      ),
    ],
  ),
);
```

:::tip
Para minimizar a confusão visual que pode resultar de
código de layout muito aninhado, implemente partes da UI
em variáveis e funções.
:::

A linha de ícones, abaixo da linha de classificações, contém 3 colunas;
cada coluna contém um ícone e duas linhas de texto,
como você pode ver em sua árvore de widgets:

<img src='/assets/images/docs/ui/layout/widget-tree-pavlova-icon-row.png' class="text-center diagram-wrap" alt="Árvore de widgets de ícones">

A variável `iconList` define a linha de ícones:

<?code-excerpt "layout/pavlova/lib/main.dart (icon-list)" replace="/iconList/[!$&!]/g"?>
```dart
const descTextStyle = TextStyle(
  color: Colors.black,
  fontWeight: FontWeight.w800,
  fontFamily: 'Roboto',
  letterSpacing: 0.5,
  fontSize: 18,
  height: 2,
);

// DefaultTextStyle.merge() allows you to create a default text
// style that is inherited by its child and all subsequent children.
final [!iconList!] = DefaultTextStyle.merge(
  style: descTextStyle,
  child: Container(
    padding: const EdgeInsets.all(20),
    child: Row(
      mainAxisAlignment: MainAxisAlignment.spaceEvenly,
      children: [
        Column(
          children: [
            Icon(Icons.kitchen, color: Colors.green[500]),
            const Text('PREP:'),
            const Text('25 min'),
          ],
        ),
        Column(
          children: [
            Icon(Icons.timer, color: Colors.green[500]),
            const Text('COOK:'),
            const Text('1 hr'),
          ],
        ),
        Column(
          children: [
            Icon(Icons.restaurant, color: Colors.green[500]),
            const Text('FEEDS:'),
            const Text('4-6'),
          ],
        ),
      ],
    ),
  ),
);
```

A variável `leftColumn` contém as linhas de classificações e de ícones,
bem como o título e o texto que descrevem a Pavlova:

<?code-excerpt "layout/pavlova/lib/main.dart (left-column)" replace="/leftColumn/[!$&!]/g"?>
```dart
final [!leftColumn!] = Container(
  padding: const EdgeInsets.fromLTRB(20, 30, 20, 20),
  child: Column(children: [titleText, subTitle, ratings, iconList]),
);
```

A coluna da esquerda é colocada em um `SizedBox` para restringir sua largura.
Finalmente, a UI é construída com a linha inteira (contendo a
coluna da esquerda e a imagem) dentro de um `Card`.

A [imagem da Pavlova][Pavlova image] é do [Pixabay][].
Você pode incorporar uma imagem da rede usando `Image.network()`, mas,
para este exemplo, a imagem é salva em um diretório de imagens no projeto,
adicionada ao [arquivo pubspec][pubspec file] e acessada usando `Images.asset()`.
Para obter mais informações, consulte [Adicionando assets e imagens][Adding assets and images].

<?code-excerpt "layout/pavlova/lib/main.dart (body)"?>
```dart
body: Center(
  child: Container(
    margin: const EdgeInsets.fromLTRB(0, 40, 0, 30),
    height: 600,
    child: Card(
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          SizedBox(width: 440, child: leftColumn),
          mainImage,
        ],
      ),
    ),
  ),
),
```

:::tip
O exemplo da Pavlova funciona melhor na horizontal em um dispositivo largo,
como um tablet. Se você estiver executando este exemplo no simulador iOS,
pode selecionar um dispositivo diferente usando o menu **Hardware > Device**.
Para este exemplo, recomendamos o iPad Pro.
Você pode alterar sua orientação para o modo paisagem usando
**Hardware > Rotate**. Você também pode alterar o tamanho da
janela do simulador (sem alterar o número de pixels lógicos)
usando **Window > Scale**.
:::

**Código-fonte do aplicativo:** [pavlova]({{site.repo.this}}/tree/main/examples/layout/pavlova)

<hr>

[Pavlova image]: https://pixabay.com/en/photos/pavlova
[Pixabay]: https://pixabay.com/en/photos/pavlova
[pubspec file]: {{site.repo.this}}/tree/main/examples/layout/pavlova/pubspec.yaml

## Widgets de layout comuns {:#common-layout-widgets}

O Flutter possui uma rica biblioteca de widgets de layout.
Aqui estão alguns dos mais comumente usados.
A intenção é fazer você começar a trabalhar o mais rápido possível,
em vez de sobrecarregá-lo com uma lista completa.
Para obter informações sobre outros widgets disponíveis,
consulte o [Catálogo de widgets][Widget catalog]
ou use a caixa de pesquisa na [documentação de referência da API][API reference docs].
Além disso, as páginas de widgets na documentação da API geralmente fazem sugestões
sobre widgets semelhantes que podem atender melhor às suas necessidades.

Os widgets a seguir se dividem em duas categorias: widgets padrão
da [biblioteca de widgets][widgets library] e widgets especializados da
[biblioteca Material][Material library]. Qualquer aplicativo pode usar a biblioteca de widgets, mas
apenas aplicativos Material podem usar a biblioteca Material Components.

<a id="standard-widgets" aria-hidden="true"></a>
<a id="materials-widgets" aria-hidden="true"></a>

<Tabs key="widget-types-tabs" wrapped="true">

<Tab name="Widgets padrão">

[`Container`](#container)
: Adiciona padding, margens, bordas,
  cor de fundo ou outras decorações a um widget.

[`GridView`](#gridview)
: Organiza widgets em uma grade com scroll.

[`ListView`](#listview)
: Organiza widgets em uma lista com scroll.

[`Stack`](#stack)
: Sobrepõe um widget a outro.

</Tab>

<Tab name="Widgets Material">

[`Scaffold`][]
: Fornece uma estrutura de layout
  com espaços para elementos comuns de aplicativos Material Design.

[`AppBar`][]
: Cria uma barra horizontal que normalmente é
  exibida no topo de uma tela.

[`Card`](#card)
: Organiza informações relacionadas em uma caixa com
  cantos arredondados e uma sombra projetada.

[`ListTile`](#listtile)
: Organiza até 3 linhas de texto,
  e ícones opcionais à esquerda e à direita, em uma linha.

</Tab>

<Tab name="Widgets Cupertino">

[`CupertinoPageScaffold`][]
: Fornece a estrutura básica de layout para uma página no estilo iOS.

[`CupertinoNavigationBar`][]
: Cria uma barra de navegação no estilo iOS no topo da tela.

[`CupertinoSegmentedControl`][]
: Cria um controle segmentado para seleção.

[`CupertinoTabBar`][] e [`CupertinoTabScaffold`][]
: Cria a barra de abas inferior característica do iOS.

</Tab>

</Tabs>

[`Scaffold`]: {{site.material_ui}}/Scaffold-class.html
[`AppBar`]: {{site.material_ui}}/AppBar-class.html
[`Container`]: {{site.api}}/flutter/widgets/Container-class.html
[`CupertinoPageScaffold`]: {{site.cupertino_ui}}/CupertinoPageScaffold-class.html
[`CupertinoNavigationBar`]: {{site.cupertino_ui}}/CupertinoNavigationBar-class.html
[`CupertinoSegmentedControl`]: {{site.cupertino_ui}}/CupertinoSegmentedControl-class.html
[`CupertinoTabBar`]: {{site.cupertino_ui}}/CupertinoTabBar-class.html
[`CupertinoTabScaffold`]: {{site.cupertino_ui}}/CupertinoTabScaffold-class.html
[`GridView`]: {{site.api}}/flutter/widgets/GridView-class.html
[`ListTile`]: {{site.material_ui}}/ListTile-class.html
[`ListView`]: {{site.api}}/flutter/widgets/ListView-class.html
[Material library]: {{site.material_ui}}
[widgets library]: {{site.api}}/flutter/widgets/widgets-library.html

### Container

Muitos layouts usam [`Container`][]s livremente para separar
widgets usando padding ou para adicionar bordas ou margens.
Você pode alterar o plano de fundo do dispositivo colocando o
layout inteiro em um `Container` e alterando sua cor
ou imagem de fundo.

<div class="side-by-side">
<div>

[`Container`]: {{site.api}}/flutter/widgets/Container-class.html

#### Resumo (Container) {:#summary-container}

* Adiciona padding, margens, bordas
* Altera a cor ou imagem de fundo
* Contém um único widget filho, mas esse filho pode ser uma `Row`,
  uma `Column` ou até mesmo a raiz de uma árvore de widgets

</div>
<div class="text-center">
  <img src='/assets/images/docs/ui/layout/margin-padding-border.png' class="diagram-wrap" alt="Diagrama mostrando: margem, borda, padding e conteúdo">
</div>
</div>

#### Exemplos (Container) {:#examples-container}

Este layout consiste em uma coluna com duas linhas, cada uma contendo
2 imagens. Um [`Container`][] é usado para alterar a cor de fundo
da coluna para um cinza mais claro.

<div class="code-and-content">
<div>

  <?code-excerpt "layout/container/lib/main.dart (column)" replace="/\bContainer/[!$&!]/g;"?>
  ```dart
  Widget _buildImageColumn() {
    return [!Container!](
      decoration: const BoxDecoration(color: Colors.black26),
      child: Column(children: [_buildImageRow(1), _buildImageRow(3)]),
    );
  }
  ```

</div>
<div class="text-center">
  <img src='/assets/images/docs/ui/layout/container.png' class="mb-4" width="230px" alt="Captura de tela mostrando 2 linhas, cada uma contendo 2 imagens">
</div>
</div>

Um `Container` também é usado para adicionar uma borda arredondada e margens
a cada imagem:

<?code-excerpt "layout/container/lib/main.dart (row)" replace="/\bContainer/[!$&!]/g;"?>
```dart
Widget _buildDecoratedImage(int imageIndex) => Expanded(
  child: [!Container!](
    decoration: BoxDecoration(
      border: Border.all(width: 10, color: Colors.black38),
      borderRadius: const BorderRadius.all(Radius.circular(8)),
    ),
    margin: const EdgeInsets.all(4),
    child: Image.asset('images/pic$imageIndex.jpg'),
  ),
);

Widget _buildImageRow(int imageIndex) => Row(
  children: [
    _buildDecoratedImage(imageIndex),
    _buildDecoratedImage(imageIndex + 1),
  ],
);
```

Você pode encontrar mais exemplos de `Container` no [tutorial][].

**Código-fonte do aplicativo:** [container]({{site.repo.this}}/tree/main/examples/layout/container)

<hr>

[`Container`]: {{site.api}}/flutter/widgets/Container-class.html
[tutorial]: /ui/layout/tutorial

### GridView

Use [`GridView`][] para organizar widgets como uma lista
bidimensional. `GridView` fornece duas listas pré-fabricadas,
ou você pode construir sua própria grade personalizada. Quando um `GridView`
detecta que seu conteúdo é longo demais para caber na render box,
ele faz scroll automaticamente.

[`GridView`]: {{site.api}}/flutter/widgets/GridView-class.html

#### Resumo (GridView) {:#summary-gridview}

* Organiza widgets em uma grade
* Detecta quando o conteúdo da coluna excede a render box
  e fornece scroll automaticamente
* Construa sua própria grade personalizada ou use uma das grades fornecidas:
  * `GridView.count` permite especificar o número de colunas
  * `GridView.extent` permite especificar a largura máxima em pixels
  de um bloco
{% comment %}
* Use `MediaQuery.of(context).orientation` to create a grid
  that changes its layout depending on whether the device
  is in landscape or portrait mode.
{% endcomment %}

:::note
Ao exibir uma lista bidimensional em que é importante qual
linha e coluna uma célula ocupa (por exemplo,
é a entrada na coluna "calorias" da linha "abacate"), use
[`Table`][] ou [`DataTable`][].
:::

[`DataTable`]: {{site.material_ui}}/DataTable-class.html
[`Table`]: {{site.api}}/flutter/widgets/Table-class.html

#### Exemplos (GridView) {:#examples-gridview}

<div class="side-by-side">
<div>
  <img src='/assets/images/docs/ui/layout/gridview-extent.png' class="text-center" alt="Uma grade de fotos com 3 colunas" height="440px">

  Usa `GridView.extent` para criar uma grade com blocos de no máximo
  150 pixels de largura.

  **Código-fonte do aplicativo:** [grid_and_list]({{site.repo.this}}/tree/main/examples/layout/grid_and_list)
</div>
<div>
  <img src='/assets/images/docs/ui/layout/gridview-count-flutter-gallery.png' class="text-center" alt="Uma grade de 2 colunas com rodapés" height="440px">

  Usa `GridView.count` para criar uma grade com 2 blocos
  de largura no modo retrato e 3 blocos de largura no modo paisagem.
  Os títulos são criados definindo a propriedade `footer` de
  cada [`GridTile`][].

  **Código Dart:**
  [`grid_list_demo.dart`]({{site.repo.this}}/tree/main/examples/layout/gallery/lib/grid_list_demo.dart)
</div>
</div>

<?code-excerpt "layout/grid_and_list/lib/main.dart (grid)" replace="/\GridView/[!$&!]/g;"?>
```dart
Widget _buildGrid() => [!GridView!].extent(
  maxCrossAxisExtent: 150,
  padding: const EdgeInsets.all(4),
  mainAxisSpacing: 4,
  crossAxisSpacing: 4,
  children: _buildGridTileList(30),
);

// The images are saved with names pic0.jpg, pic1.jpg...pic29.jpg.
// The List.generate() constructor allows an easy way to create
// a list when objects have a predictable naming pattern.
List<Widget> _buildGridTileList(int count) =>
    List.generate(count, (i) => Image.asset('images/pic$i.jpg'));
```

<hr>

[`GridTile`]: {{site.material_ui}}/GridTile-class.html

### ListView

[`ListView`][], um widget semelhante a uma coluna, fornece
scroll automaticamente quando seu conteúdo é longo demais para
sua render box.

[`ListView`]: {{site.api}}/flutter/widgets/ListView-class.html

#### Resumo (ListView) {:#summary-listview}

* Uma [`Column`][] especializada para organizar uma lista de caixas
* Pode ser disposto horizontal ou verticalmente
* Detecta quando seu conteúdo não cabe e fornece scroll
* Menos configurável que `Column`, mas mais fácil de usar e
  suporta scroll

[`Column`]: {{site.api}}/flutter/widgets/Column-class.html

#### Exemplos (ListView) {:#examples-listview}

<div class="side-by-side">
<div>
  <img src='/assets/images/docs/ui/layout/listview.png' height="400px" class="simple-border text-center" alt="ListView contendo cinemas e restaurantes">

  Usa `ListView` para exibir uma lista de estabelecimentos usando
  `ListTile`s. Um `Divider` separa os cinemas dos
  restaurantes.

  **Código-fonte do aplicativo:** [grid_and_list]({{site.repo.this}}/tree/main/examples/layout/grid_and_list)
</div>
<div>
  <img src='/assets/images/docs/ui/layout/listview-color-gallery.png' height="400px" class="simple-border text-center" alt="ListView contendo tons de azul">

  Usa `ListView` para exibir as [`Colors`][] da
  [paleta do Material Design 2][Material 2 Design palette]
  para uma determinada família de cores.

  **Código Dart:**
  [`colors_demo.dart`]({{site.repo.this}}/tree/main/examples/layout/gallery/lib/colors_demo.dart)
</div>
</div>

<?code-excerpt "layout/grid_and_list/lib/main.dart (list)" replace="/\ListView/[!$&!]/g;"?>
```dart
Widget _buildList() {
  return [!ListView!](
    children: [
      _tile('CineArts at the Empire', '85 W Portal Ave', Icons.theaters),
      _tile('The Castro Theater', '429 Castro St', Icons.theaters),
      _tile('Alamo Drafthouse Cinema', '2550 Mission St', Icons.theaters),
      _tile('Roxie Theater', '3117 16th St', Icons.theaters),
      _tile(
        'United Artists Stonestown Twin',
        '501 Buckingham Way',
        Icons.theaters,
      ),
      _tile('AMC Metreon 16', '135 4th St #3000', Icons.theaters),
      const Divider(),
      _tile('K\'s Kitchen', '757 Monterey Blvd', Icons.restaurant),
      _tile('Emmy\'s Restaurant', '1923 Ocean Ave', Icons.restaurant),
      _tile('Chaiya Thai Restaurant', '272 Claremont Blvd', Icons.restaurant),
      _tile('La Ciccia', '291 30th St', Icons.restaurant),
    ],
  );
}

ListTile _tile(String title, String subtitle, IconData icon) {
  return ListTile(
    title: Text(
      title,
      style: const TextStyle(fontWeight: FontWeight.w500, fontSize: 20),
    ),
    subtitle: Text(subtitle),
    leading: Icon(icon, color: Colors.blue[500]),
  );
}
```

<hr>

[`Colors`]: {{site.material_ui}}/Colors-class.html
[Material 2 Design palette]: {{site.material2}}/design/color/the-color-system.html#tools-for-picking-colors

### Stack

Use [`Stack`][] para organizar widgets em cima de um widget
base&mdash;geralmente uma imagem. Os widgets podem sobrepor
completa ou parcialmente o widget base.

[`Stack`]: {{site.api}}/flutter/widgets/Stack-class.html

#### Resumo (Stack) {:#summary-stack}

* Use para widgets que se sobrepõem a outro widget
* O primeiro widget na lista de filhos é o widget base;
  os filhos subsequentes são sobrepostos a esse widget base
* O conteúdo de um `Stack` não pode ter scroll
* Você pode optar por recortar filhos que excedam a render box

#### Exemplos (Stack) {:#examples-stack}

<div class="side-by-side">
<div>
  <img src='/assets/images/docs/ui/layout/stack.png' class="text-center" height="200px" alt="Imagem de avatar circular com um rótulo">

  Usa `Stack` para sobrepor um `Container`
  (que exibe seu `Text` em um fundo preto
  translúcido) em cima de um `CircleAvatar`.
  O `Stack` desloca o texto usando a propriedade `alignment` e
  `Alignment`s.

  **Código-fonte do aplicativo:** [card_and_stack]({{site.repo.this}}/tree/main/examples/layout/card_and_stack)
</div>
<div>
  <img src='/assets/images/docs/ui/layout/stack-flutter-gallery.png' class="text-center" height="200px" alt="Uma imagem com um ícone sobreposto">

  Usa `Stack` para sobrepor um ícone em cima de uma imagem.

  **Código Dart:**
  [`bottom_navigation_demo.dart`]({{site.repo.this}}/tree/main/examples/layout/gallery/lib/bottom_navigation_demo.dart)
</div>
</div>

<?code-excerpt "layout/card_and_stack/lib/main.dart (stack)" replace="/\bStack/[!$&!]/g;"?>
```dart
Widget _buildStack() {
  return [!Stack!](
    alignment: const Alignment(0.6, 0.6),
    children: [
      const CircleAvatar(
        backgroundImage: AssetImage('images/pic.jpg'),
        radius: 100,
      ),
      Container(
        decoration: const BoxDecoration(color: Colors.black45),
        child: const Text(
          'Mia B',
          style: TextStyle(
            fontSize: 20,
            fontWeight: FontWeight.bold,
            color: Colors.white,
          ),
        ),
      ),
    ],
  );
}
```

<hr>

### Card

Um [`Card`][], da [biblioteca Material][Material library],
contém trechos relacionados de informação e pode
ser composto por quase qualquer widget, mas geralmente é usado com
[`ListTile`][]. `Card` tem um único filho,
mas esse filho pode ser uma coluna, linha, lista, grade
ou outro widget que suporte múltiplos filhos.
Por padrão, um `Card` reduz seu tamanho para 0 por 0 pixels.
Você pode usar [`SizedBox`][] para restringir o tamanho de um card.

No Flutter, um `Card` possui cantos levemente arredondados
e uma sombra projetada, dando-lhe um efeito 3D.
Alterar a propriedade `elevation` de um `Card` permite controlar
o efeito de sombra projetada. Definir a elevação como 24,
por exemplo, eleva visualmente o `Card` ainda mais da
superfície e faz com que a sombra fique mais dispersa.
Para uma lista de valores de elevação suportados, consulte [Elevation][] nas
[diretrizes do Material][Material Design].
Especificar um valor não suportado desativa completamente a sombra projetada.

[`Card`]: {{site.material_ui}}/Card-class.html
[Elevation]: {{site.material}}/styles/elevation
[`ListTile`]: {{site.material_ui}}/ListTile-class.html
[Material Design]: {{site.material}}/styles
[`SizedBox`]: {{site.api}}/flutter/widgets/SizedBox-class.html
[Material library]: {{site.material_ui}}

#### Resumo (Card) {:#summary-card}

* Implementa um [card do Material][Material card]
* Usado para apresentar trechos relacionados de informação
* Aceita um único filho, mas esse filho pode ser uma `Row`,
  uma `Column` ou outro widget que contenha uma lista de filhos
* Exibido com cantos arredondados e uma sombra projetada
* O conteúdo de um `Card` não pode ter scroll
* Da [biblioteca Material][Material library]

[Material card]: {{site.material}}/components/cards
[Material library]: {{site.material_ui}}

#### Exemplos (Card) {:#examples-card}

<div class="side-by-side">
<div>
  <img src='/assets/images/docs/ui/layout/card.png' height="200px" class="text-center" alt="Card contendo 3 ListTiles">

  Um `Card` contendo 3 ListTiles e dimensionado ao envolvê-lo
  com um `SizedBox`. Um `Divider` separa o primeiro
  e o segundo `ListTiles`.

  **Código-fonte do aplicativo:** [card_and_stack]({{site.repo.this}}/tree/main/examples/layout/card_and_stack)
</div>
<div>
  <img src='/assets/images/docs/ui/layout/card-flutter-gallery.png' height="200px" class="text-center" alt="Card tocável contendo uma imagem e várias formas de texto">

  Um `Card` contendo uma imagem e texto.

  **Código Dart:**
  [`cards_demo.dart`]({{site.repo.this}}/tree/main/examples/layout/gallery/lib/cards_demo.dart)
</div>
</div>

<?code-excerpt "layout/card_and_stack/lib/main.dart (card)" replace="/\bCard/[!$&!]/g;"?>
```dart
Widget _buildCard() {
  return SizedBox(
    height: 210,
    child: [!Card!](
      child: Column(
        children: [
          ListTile(
            title: const Text(
              '1625 Main Street',
              style: TextStyle(fontWeight: FontWeight.w500),
            ),
            subtitle: const Text('My City, CA 99984'),
            leading: Icon(Icons.restaurant_menu, color: Colors.blue[500]),
          ),
          const Divider(),
          ListTile(
            title: const Text(
              '(408) 555-1212',
              style: TextStyle(fontWeight: FontWeight.w500),
            ),
            leading: Icon(Icons.contact_phone, color: Colors.blue[500]),
          ),
          ListTile(
            title: const Text('costa@example.com'),
            leading: Icon(Icons.contact_mail, color: Colors.blue[500]),
          ),
        ],
      ),
    ),
  );
}
```

<hr>

### ListTile

Use [`ListTile`][], um widget de linha especializado da
[biblioteca Material][Material library], para uma maneira fácil de criar uma linha
contendo até 3 linhas de texto e ícones opcionais à esquerda (leading)
e à direita (trailing). `ListTile` é mais comumente usado em
[`Card`][] ou [`ListView`][], mas pode ser usado em outros lugares.

[`Card`]: {{site.material_ui}}/Card-class.html
[`ListTile`]: {{site.material_ui}}/ListTile-class.html
[`ListView`]: {{site.api}}/flutter/widgets/ListView-class.html
[Material library]: {{site.material_ui}}

#### Resumo (ListTile) {:#summary-listtile}

* Uma linha especializada que contém até 3 linhas de texto e
  ícones opcionais
* Menos configurável que `Row`, mas mais fácil de usar
* Da [biblioteca Material][Material library]

[Material library]: {{site.material_ui}}

#### Exemplos (ListTile) {:#examples-listtile}

<div class="side-by-side">
<div>
  <img src='/assets/images/docs/ui/layout/card.png' class="text-center" alt="Card contendo 3 ListTiles">

  Um `Card` contendo 3 `ListTile`s.

  **Código-fonte do aplicativo:** [card_and_stack]({{site.repo.this}}/tree/main/examples/layout/card_and_stack)
</div>
<div>
  <img src='/assets/images/docs/ui/layout/listtile-flutter-gallery.png' height="200px" class="simple-border text-center" alt="4 ListTiles, cada um contendo um avatar à esquerda">

  Usa `ListTile` com widgets à esquerda (leading).

  **Código Dart:**
  [`list_demo.dart`]({{site.repo.this}}/tree/main/examples/layout/gallery/lib/list_demo.dart)
</div>
</div>

<hr>

## Restrições (constraints) {:#constraints}

Para entender completamente o sistema de layout do Flutter, você precisa
aprender como o Flutter posiciona e dimensiona
os componentes em um layout. Para mais informações,
consulte [Entendendo constraints][Understanding constraints].

[Understanding constraints]: /ui/layout/constraints

## Vídeos {:#videos}

Os vídeos a seguir, parte da
série [Flutter in Focus][],
explicam os widgets `Stateless` e `Stateful`.

<YouTubeEmbed id="wE7khGHVkYY" title="Como criar widgets stateless"></YouTubeEmbed>

<YouTubeEmbed id="AqCMFXEmf3w" title="Como e quando widgets stateful são mais bem utilizados"></YouTubeEmbed>

[Playlist Flutter in Focus]({{site.yt.playlist}}PLjxrf2q8roU2HdJQDjJzOeO6J3FoFLWr2)

---

Cada episódio da [série Widget of the Week][Widget of the Week series] foca em um widget.
Vários deles incluem widgets de layout.

<YouTubeEmbed id="b_sQ9bMltGU" title="Apresentando o Widget of the Week"></YouTubeEmbed>

[Playlist Flutter Widget of the Week]({{site.yt.playlist}}PLjxrf2q8roU23XGwz3Km7sQZFTdB996iG)

[Widget of the Week series]: {{site.yt.playlist}}PLjxrf2q8roU23XGwz3Km7sQZFTdB996iG
[Flutter in Focus]: {{site.yt.watch}}?v=wgTBLj7rMPM&list=PLjxrf2q8roU2HdJQDjJzOeO6J3FoFLWr2

## Outros recursos {:#other-resources}

Os recursos a seguir podem ajudar ao escrever código de layout.

[Tutorial de layout][Layout tutorial]
: Aprenda a construir um layout.

[Catálogo de widgets][Widget catalog]
: Descreve muitos dos widgets disponíveis no Flutter.

[Análogos de HTML/CSS no Flutter][HTML/CSS Analogs in Flutter]
: Para quem está familiarizado com programação web,
  esta página mapeia funcionalidades de HTML/CSS para recursos do Flutter.

[Documentação de referência da API][API reference docs]
: Documentação de referência de todas as bibliotecas do Flutter.

[Adicionando assets e imagens][Adding assets and images]
: Explica como adicionar imagens e outros assets ao package do seu aplicativo.

[Do zero ao primeiro aplicativo com Flutter][Zero to One with Flutter]
: A experiência de uma pessoa escrevendo seu primeiro aplicativo Flutter.

[Layout tutorial]: /ui/layout/tutorial
[Widget catalog]: /ui/widgets
[HTML/CSS Analogs in Flutter]: /flutter-for/web-devs
[API reference docs]: {{site.api}}/flutter
[Adding assets and images]: /ui/assets/assets-and-images
[Zero to One with Flutter]: https://medium.com/@mravn/zero-to-one-with-flutter-43b13fd7b354

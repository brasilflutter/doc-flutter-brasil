---
title: Entendendo restrições
description: O modelo do Flutter para restrições, dimensionamento, posicionamento de widgets e como eles interagem.
showToc: false
ia-translate: true
---

<?code-excerpt path-base="layout/constraints/"?>

<img src='/assets/images/docs/ui/layout/article-hero-image.png' alt="Imagem de destaque do artigo">

:::note
Se você está enfrentando erros de layout específicos,
talvez queira conferir [Erros comuns do Flutter][Common Flutter errors].
:::

[Common Flutter errors]: /testing/common-errors

Quando alguém aprendendo Flutter pergunta por que um widget
com `width: 100` não tem 100 pixels de largura,
a resposta padrão é dizer que ele deve colocar o widget
dentro de um `Center`, certo?

**Não faça isso.**

Se você fizer isso, eles voltarão várias vezes,
perguntando por que algum `FittedBox` não está funcionando,
por que aquela `Column` está transbordando ou o que
`IntrinsicWidth` deveria estar fazendo.

Em vez disso, primeiro diga que o layout do Flutter é muito diferente
do layout HTML (provavelmente de onde eles estão vindo),
e então faça-os memorizar a seguinte regra:

<center><font size="+2">
<b>Restrições descem. Tamanhos sobem. O pai define a posição.</b>
</font></center>

O layout do Flutter não pode ser realmente entendido sem conhecer
esta regra, então os desenvolvedores Flutter devem aprendê-la logo no início.

Em mais detalhes:

* Um widget recebe suas próprias **restrições** de seu **pai**.
  Uma _restrição_ é apenas um conjunto de 4 doubles:
  uma largura mínima e máxima e uma altura mínima e máxima.
* Em seguida, o widget percorre sua própria lista de **filhos**.
  Um por um, o widget diz a seus filhos quais são suas
  **restrições** (que podem ser diferentes para cada filho),
  e então pergunta a cada filho qual tamanho ele deseja ter.
* Depois, o widget posiciona seus **filhos**
  (horizontalmente no eixo `x` e verticalmente no eixo `y`),
  um por um.
* E, finalmente, o widget informa ao seu pai sobre seu próprio **tamanho**
  (dentro das restrições originais, é claro).

Por exemplo, se um widget composto contiver uma coluna
com algum padding e quiser organizar seus dois filhos
da seguinte maneira:

<img src='/assets/images/docs/ui/layout/children.png' alt="Layout visual">

A negociação acontece mais ou menos assim:

**Widget**: "Ei, pai, quais são as minhas restrições?"

**Pai**: "Você deve ter de `0` a `300` pixels de largura
   e de `0` a `85` de altura."

**Widget**: "Hmmm, como eu quero ter `5` pixels de padding,
   então meus filhos podem ter no máximo `290` pixels de largura
   e `75` pixels de altura."

**Widget**: "Ei, primeiro filho, você deve ter de `0` a `290`
   pixels de largura e de `0` a `75` de altura."

**Primeiro filho**: "OK, então eu quero ter `290` pixels de largura
   e `20` pixels de altura."

**Widget**: "Hmmm, já que quero colocar meu segundo filho abaixo do
   primeiro, isso deixa apenas `55` pixels de altura para
   o meu segundo filho."

**Widget**: "Ei, segundo filho, você deve ter de `0` a `290` de largura
   e de `0` a `55` de altura."

**Segundo filho**: "OK, eu quero ter `140` pixels de largura
   e `30` pixels de altura."

**Widget**: "Muito bem. Meu primeiro filho tem posição `x: 5` e `y: 5`,
   e meu segundo filho tem `x: 80` e `y: 25`."

**Widget**: "Ei, pai, decidi que meu tamanho será de `300`
   pixels de largura e `60` pixels de altura."

## Limitações {:#limitations}

O mecanismo de layout do Flutter foi projetado para ser um processo de
passagem única. Isso significa que o Flutter faz o layout de seus widgets
de forma muito eficiente, mas resulta em algumas limitações:

* Um widget pode decidir seu próprio tamanho apenas dentro das
  restrições dadas a ele por seu pai.
  Isso significa que um widget geralmente
  **não pode ter qualquer tamanho que desejar**.

* Um widget **não pode saber e não decide sua própria posição
  na tela**, já que é o pai do widget que decide
  a posição do widget.

* Como o tamanho e a posição do pai, por sua vez,
  também dependem de seu próprio pai, é impossível
  definir com precisão o tamanho e a posição de qualquer widget
  sem levar em consideração a árvore como um todo.

* Se um filho quer um tamanho diferente do de seu pai e
  o pai não tem informações suficientes para alinhá-lo,
  então o tamanho do filho pode ser ignorado.
  **Seja específico ao definir o alinhamento.**

No Flutter, widgets são renderizados pelos seus
objetos [`RenderBox`][] subjacentes. Muitos boxes no Flutter,
especialmente os que recebem apenas um único filho,
passam suas restrições para seus filhos.

Geralmente, há três tipos de boxes,
com base em como eles lidam com suas restrições:

* Aqueles que tentam ser o maior possível.
  Por exemplo, os boxes usados por [`Center`][] e
  [`ListView`][].
* Aqueles que tentam ter o mesmo tamanho que seus filhos.
  Por exemplo, os boxes usados por [`Transform`][] e
  [`Opacity`][].
* Aqueles que tentam ter um tamanho específico.
  Por exemplo, os boxes usados por [`Image`][] e
  [`Text`][].

Alguns widgets, como o [`Container`][],
variam de tipo para tipo com base nos argumentos do construtor.
O construtor de [`Container`][] tenta, por padrão,
ser o maior possível, mas se você definir uma `width`,
por exemplo, ele tentará respeitá-la e ter esse tamanho específico.

Outros, como [`Row`][] e [`Column`][] (boxes flex),
variam com base nas restrições recebidas,
como descrito na seção [Flex](#flex).

[`Center`]: {{site.api}}/flutter/widgets/Center-class.html
[`Column`]: {{site.api}}/flutter/widgets/Column-class.html
[`Container`]: {{site.api}}/flutter/widgets/Container-class.html
[`Image`]: {{site.api}}/flutter/dart-ui/Image-class.html
[`ListView`]: {{site.api}}/flutter/widgets/ListView-class.html
[`Opacity`]: {{site.api}}/flutter/widgets/Opacity-class.html
[`Row`]: {{site.api}}/flutter/widgets/Row-class.html
[`Text`]: {{site.api}}/flutter/widgets/Text-class.html
[`Transform`]: {{site.api}}/flutter/widgets/Transform-class.html

## Exemplos {:#examples}

Para uma experiência interativa, use o seguinte DartPad.
Use a barra de rolagem horizontal numerada para alternar entre
29 exemplos diferentes.

<?code-excerpt "lib/main.dart"?>
```dartpad title="Constraints DartPad hands-on example" run="true"
import 'package:flutter/material.dart';

void main() => runApp(const HomePage());

const Color red = Colors.red;
const Color green = Colors.green;
const Color blue = Colors.blue;
const TextStyle big = TextStyle(fontSize: 30);

//////////////////////////////////////////////////

class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return const FlutterLayoutArticle([
      Example1(),
      Example2(),
      Example3(),
      Example4(),
      Example5(),
      Example6(),
      Example7(),
      Example8(),
      Example9(),
      Example10(),
      Example11(),
      Example12(),
      Example13(),
      Example14(),
      Example15(),
      Example16(),
      Example17(),
      Example18(),
      Example19(),
      Example20(),
      Example21(),
      Example22(),
      Example23(),
      Example24(),
      Example25(),
      Example26(),
      Example27(),
      Example28(),
      Example29(),
    ]);
  }
}

//////////////////////////////////////////////////

abstract class Example extends StatelessWidget {
  const Example({super.key});

  String get code;

  String get explanation;
}

//////////////////////////////////////////////////

class FlutterLayoutArticle extends StatefulWidget {
  const FlutterLayoutArticle(this.examples, {super.key});

  final List<Example> examples;

  @override
  State<FlutterLayoutArticle> createState() => _FlutterLayoutArticleState();
}

//////////////////////////////////////////////////

class _FlutterLayoutArticleState extends State<FlutterLayoutArticle> {
  late int count;
  late Widget example;
  late String code;
  late String explanation;

  @override
  void initState() {
    count = 1;
    code = const Example1().code;
    explanation = const Example1().explanation;

    super.initState();
  }

  @override
  void didUpdateWidget(FlutterLayoutArticle oldWidget) {
    super.didUpdateWidget(oldWidget);
    var example = widget.examples[count - 1];
    code = example.code;
    explanation = example.explanation;
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Flutter Layout Article',
      home: SafeArea(
        child: Material(
          color: Colors.black,
          child: FittedBox(
            child: Container(
              width: 400,
              height: 670,
              color: const Color(0xFFCCCCCC),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.center,
                children: [
                  Expanded(
                    child: ConstrainedBox(
                      constraints: const BoxConstraints.tightFor(
                        width: double.infinity,
                        height: double.infinity,
                      ),
                      child: widget.examples[count - 1],
                    ),
                  ),
                  Container(
                    height: 50,
                    width: double.infinity,
                    color: Colors.black,
                    child: SingleChildScrollView(
                      scrollDirection: Axis.horizontal,
                      child: Row(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          for (int i = 0; i < widget.examples.length; i++)
                            Container(
                              width: 58,
                              padding: const EdgeInsets.only(left: 4, right: 4),
                              child: button(i + 1),
                            ),
                        ],
                      ),
                    ),
                  ),
                  Container(
                    height: 273,
                    color: Colors.grey[50],
                    child: Scrollbar(
                      child: SingleChildScrollView(
                        key: ValueKey(count),
                        child: Padding(
                          padding: const EdgeInsets.all(10),
                          child: Column(
                            children: [
                              Center(child: Text(code)),
                              const SizedBox(height: 15),
                              Text(
                                explanation,
                                style: TextStyle(
                                  color: Colors.blue[900],
                                  fontStyle: FontStyle.italic,
                                ),
                              ),
                            ],
                          ),
                        ),
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }

  Widget button(int exampleNumber) {
    return Button(
      key: ValueKey('button$exampleNumber'),
      isSelected: count == exampleNumber,
      exampleNumber: exampleNumber,
      onPressed: () {
        showExample(
          exampleNumber,
          widget.examples[exampleNumber - 1].code,
          widget.examples[exampleNumber - 1].explanation,
        );
      },
    );
  }

  void showExample(int exampleNumber, String code, String explanation) {
    setState(() {
      count = exampleNumber;
      this.code = code;
      this.explanation = explanation;
    });
  }
}

//////////////////////////////////////////////////

class Button extends StatelessWidget {
  final bool isSelected;
  final int exampleNumber;
  final VoidCallback onPressed;

  const Button({
    super.key,
    required this.isSelected,
    required this.exampleNumber,
    required this.onPressed,
  });

  @override
  Widget build(BuildContext context) {
    return TextButton(
      style: TextButton.styleFrom(
        foregroundColor: Colors.white,
        backgroundColor: isSelected ? Colors.grey : Colors.grey[800],
      ),
      child: Text(exampleNumber.toString()),
      onPressed: () {
        Scrollable.ensureVisible(
          context,
          duration: const Duration(milliseconds: 350),
          curve: Curves.easeOut,
          alignment: 0.5,
        );
        onPressed();
      },
    );
  }
}
//////////////////////////////////////////////////

class Example1 extends Example {
  const Example1({super.key});

  @override
  final code = 'Container(color: red)';

  @override
  final explanation =
      'The screen is the parent of the Container, '
      'and it forces the Container to be exactly the same size as the screen.'
      '\n\n'
      'So the Container fills the screen and paints it red.';

  @override
  Widget build(BuildContext context) {
    return Container(color: red);
  }
}

//////////////////////////////////////////////////

class Example2 extends Example {
  const Example2({super.key});

  @override
  final code = 'Container(width: 100, height: 100, color: red)';
  @override
  final String explanation =
      'The red Container wants to be 100x100, but it can\'t, '
      'because the screen forces it to be exactly the same size as the screen.'
      '\n\n'
      'So the Container fills the screen.';

  @override
  Widget build(BuildContext context) {
    return Container(width: 100, height: 100, color: red);
  }
}

//////////////////////////////////////////////////

class Example3 extends Example {
  const Example3({super.key});

  @override
  final code =
      'Center(\n'
      '   child: Container(width: 100, height: 100, color: red))';
  @override
  final String explanation =
      'The screen forces the Center to be exactly the same size as the screen, '
      'so the Center fills the screen.'
      '\n\n'
      'The Center tells the Container that it can be any size it wants, but not bigger than the screen.'
      'Now the Container can indeed be 100x100.';

  @override
  Widget build(BuildContext context) {
    return Center(child: Container(width: 100, height: 100, color: red));
  }
}

//////////////////////////////////////////////////

class Example4 extends Example {
  const Example4({super.key});

  @override
  final code =
      'Align(\n'
      '   alignment: Alignment.bottomRight,\n'
      '   child: Container(width: 100, height: 100, color: red))';
  @override
  final String explanation =
      'This is different from the previous example in that it uses Align instead of Center.'
      '\n\n'
      'Align also tells the Container that it can be any size it wants, but if there is empty space it won\'t center the Container. '
      'Instead, it aligns the Container to the bottom-right of the available space.';

  @override
  Widget build(BuildContext context) {
    return Align(
      alignment: Alignment.bottomRight,
      child: Container(width: 100, height: 100, color: red),
    );
  }
}

//////////////////////////////////////////////////

class Example5 extends Example {
  const Example5({super.key});

  @override
  final code =
      'Center(\n'
      '   child: Container(\n'
      '              color: red,\n'
      '              width: double.infinity,\n'
      '              height: double.infinity))';
  @override
  final String explanation =
      'The screen forces the Center to be exactly the same size as the screen, '
      'so the Center fills the screen.'
      '\n\n'
      'The Center tells the Container that it can be any size it wants, but not bigger than the screen.'
      'The Container wants to be of infinite size, but since it can\'t be bigger than the screen, it just fills the screen.';

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Container(
        width: double.infinity,
        height: double.infinity,
        color: red,
      ),
    );
  }
}

//////////////////////////////////////////////////

class Example6 extends Example {
  const Example6({super.key});

  @override
  final code = 'Center(child: Container(color: red))';
  @override
  final String explanation =
      'The screen forces the Center to be exactly the same size as the screen, '
      'so the Center fills the screen.'
      '\n\n'
      'The Center tells the Container that it can be any size it wants, but not bigger than the screen.'
      '\n\n'
      'Since the Container has no child and no fixed size, it decides it wants to be as big as possible, so it fills the whole screen.'
      '\n\n'
      'But why does the Container decide that? '
      'Simply because that\'s a design decision by those who created the Container widget. '
      'It could have been created differently, and you have to read the Container documentation to understand how it behaves, depending on the circumstances. ';

  @override
  Widget build(BuildContext context) {
    return Center(child: Container(color: red));
  }
}

//////////////////////////////////////////////////

class Example7 extends Example {
  const Example7({super.key});

  @override
  final code =
      'Center(\n'
      '   child: Container(color: red\n'
      '      child: Container(color: green, width: 30, height: 30)))';
  @override
  final String explanation =
      'The screen forces the Center to be exactly the same size as the screen, '
      'so the Center fills the screen.'
      '\n\n'
      'The Center tells the red Container that it can be any size it wants, but not bigger than the screen.'
      'Since the red Container has no size but has a child, it decides it wants to be the same size as its child.'
      '\n\n'
      'The red Container tells its child that it can be any size it wants, but not bigger than the screen.'
      '\n\n'
      'The child is a green Container that wants to be 30x30.'
      '\n\n'
      'Since the red `Container` has no size but has a child, it decides it wants to be the same size as its child. '
      'The red color isn\'t visible, since the green Container entirely covers all of the red Container.';

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Container(
        color: red,
        child: Container(color: green, width: 30, height: 30),
      ),
    );
  }
}

//////////////////////////////////////////////////

class Example8 extends Example {
  const Example8({super.key});

  @override
  final code =
      'Center(\n'
      '   child: Container(color: red\n'
      '      padding: const EdgeInsets.all(20),\n'
      '      child: Container(color: green, width: 30, height: 30)))';
  @override
  final String explanation =
      'The red Container sizes itself to its children size, but it takes its own padding into consideration. '
      'So it is also 30x30 plus padding. '
      'The red color is visible because of the padding, and the green Container has the same size as in the previous example.';

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Container(
        padding: const EdgeInsets.all(20),
        color: red,
        child: Container(color: green, width: 30, height: 30),
      ),
    );
  }
}

//////////////////////////////////////////////////

class Example9 extends Example {
  const Example9({super.key});

  @override
  final code =
      'ConstrainedBox(\n'
      '   constraints: BoxConstraints(\n'
      '              minWidth: 70, minHeight: 70,\n'
      '              maxWidth: 150, maxHeight: 150),\n'
      '      child: Container(color: red, width: 10, height: 10)))';
  @override
  final String explanation =
      'You might guess that the Container has to be between 70 and 150 pixels, but you would be wrong. '
      'The ConstrainedBox only imposes ADDITIONAL constraints from those it receives from its parent.'
      '\n\n'
      'Here, the screen forces the ConstrainedBox to be exactly the same size as the screen, '
      'so it tells its child Container to also assume the size of the screen, '
      'thus ignoring its \'constraints\' parameter.';

  @override
  Widget build(BuildContext context) {
    return ConstrainedBox(
      constraints: const BoxConstraints(
        minWidth: 70,
        minHeight: 70,
        maxWidth: 150,
        maxHeight: 150,
      ),
      child: Container(color: red, width: 10, height: 10),
    );
  }
}

//////////////////////////////////////////////////

class Example10 extends Example {
  const Example10({super.key});

  @override
  final code =
      'Center(\n'
      '   child: ConstrainedBox(\n'
      '      constraints: BoxConstraints(\n'
      '                 minWidth: 70, minHeight: 70,\n'
      '                 maxWidth: 150, maxHeight: 150),\n'
      '        child: Container(color: red, width: 10, height: 10))))';
  @override
  final String explanation =
      'Now, Center allows ConstrainedBox to be any size up to the screen size.'
      '\n\n'
      'The ConstrainedBox imposes ADDITIONAL constraints from its \'constraints\' parameter onto its child.'
      '\n\n'
      'The Container must be between 70 and 150 pixels. It wants to have 10 pixels, so it will end up having 70 (the MINIMUM).';

  @override
  Widget build(BuildContext context) {
    return Center(
      child: ConstrainedBox(
        constraints: const BoxConstraints(
          minWidth: 70,
          minHeight: 70,
          maxWidth: 150,
          maxHeight: 150,
        ),
        child: Container(color: red, width: 10, height: 10),
      ),
    );
  }
}

//////////////////////////////////////////////////

class Example11 extends Example {
  const Example11({super.key});

  @override
  final code =
      'Center(\n'
      '   child: ConstrainedBox(\n'
      '      constraints: BoxConstraints(\n'
      '                 minWidth: 70, minHeight: 70,\n'
      '                 maxWidth: 150, maxHeight: 150),\n'
      '        child: Container(color: red, width: 1000, height: 1000))))';
  @override
  final String explanation =
      'Center allows ConstrainedBox to be any size up to the screen size.'
      'The ConstrainedBox imposes ADDITIONAL constraints from its \'constraints\' parameter onto its child'
      '\n\n'
      'The Container must be between 70 and 150 pixels. It wants to have 1000 pixels, so it ends up having 150 (the MAXIMUM).';

  @override
  Widget build(BuildContext context) {
    return Center(
      child: ConstrainedBox(
        constraints: const BoxConstraints(
          minWidth: 70,
          minHeight: 70,
          maxWidth: 150,
          maxHeight: 150,
        ),
        child: Container(color: red, width: 1000, height: 1000),
      ),
    );
  }
}

//////////////////////////////////////////////////

class Example12 extends Example {
  const Example12({super.key});

  @override
  final code =
      'Center(\n'
      '   child: ConstrainedBox(\n'
      '      constraints: BoxConstraints(\n'
      '                 minWidth: 70, minHeight: 70,\n'
      '                 maxWidth: 150, maxHeight: 150),\n'
      '        child: Container(color: red, width: 100, height: 100))))';
  @override
  final String explanation =
      'Center allows ConstrainedBox to be any size up to the screen size.'
      'ConstrainedBox imposes ADDITIONAL constraints from its \'constraints\' parameter onto its child.'
      '\n\n'
      'The Container must be between 70 and 150 pixels. It wants to have 100 pixels, and that\'s the size it has, since that\'s between 70 and 150.';

  @override
  Widget build(BuildContext context) {
    return Center(
      child: ConstrainedBox(
        constraints: const BoxConstraints(
          minWidth: 70,
          minHeight: 70,
          maxWidth: 150,
          maxHeight: 150,
        ),
        child: Container(color: red, width: 100, height: 100),
      ),
    );
  }
}

//////////////////////////////////////////////////

class Example13 extends Example {
  const Example13({super.key});

  @override
  final code =
      'UnconstrainedBox(\n'
      '   child: Container(color: red, width: 20, height: 50));';
  @override
  final String explanation =
      'The screen forces the UnconstrainedBox to be exactly the same size as the screen.'
      'However, the UnconstrainedBox lets its child Container be any size it wants.';

  @override
  Widget build(BuildContext context) {
    return UnconstrainedBox(
      child: Container(color: red, width: 20, height: 50),
    );
  }
}

//////////////////////////////////////////////////

class Example14 extends Example {
  const Example14({super.key});

  @override
  final code =
      'UnconstrainedBox(\n'
      '   child: Container(color: red, width: 4000, height: 50));';
  @override
  final String explanation =
      'The screen forces the UnconstrainedBox to be exactly the same size as the screen, '
      'and UnconstrainedBox lets its child Container be any size it wants.'
      '\n\n'
      'Unfortunately, in this case the Container has 4000 pixels of width and is too big to fit in the UnconstrainedBox, '
      'so the UnconstrainedBox displays the much dreaded "overflow warning".';

  @override
  Widget build(BuildContext context) {
    return UnconstrainedBox(
      child: Container(color: red, width: 4000, height: 50),
    );
  }
}

//////////////////////////////////////////////////

class Example15 extends Example {
  const Example15({super.key});

  @override
  final code =
      'OverflowBox(\n'
      '   minWidth: 0,'
      '   minHeight: 0,'
      '   maxWidth: double.infinity,'
      '   maxHeight: double.infinity,'
      '   child: Container(color: red, width: 4000, height: 50));';
  @override
  final String explanation =
      'The screen forces the OverflowBox to be exactly the same size as the screen, '
      'and OverflowBox lets its child Container be any size it wants.'
      '\n\n'
      'OverflowBox is similar to UnconstrainedBox, and the difference is that it won\'t display any warnings if the child doesn\'t fit the space.'
      '\n\n'
      'In this case the Container is 4000 pixels wide, and is too big to fit in the OverflowBox, '
      'but the OverflowBox simply shows as much as it can, with no warnings given.';

  @override
  Widget build(BuildContext context) {
    return OverflowBox(
      minWidth: 0,
      minHeight: 0,
      maxWidth: double.infinity,
      maxHeight: double.infinity,
      child: Container(color: red, width: 4000, height: 50),
    );
  }
}

//////////////////////////////////////////////////

class Example16 extends Example {
  const Example16({super.key});

  @override
  final code =
      'UnconstrainedBox(\n'
      '   child: Container(color: Colors.red, width: double.infinity, height: 100));';
  @override
  final String explanation =
      'This won\'t render anything, and you\'ll see an error in the console.'
      '\n\n'
      'The UnconstrainedBox lets its child be any size it wants, '
      'however its child is a Container with infinite size.'
      '\n\n'
      'Flutter can\'t render infinite sizes, so it throws an error with the following message: '
      '"BoxConstraints forces an infinite width."';

  @override
  Widget build(BuildContext context) {
    return UnconstrainedBox(
      child: Container(color: Colors.red, width: double.infinity, height: 100),
    );
  }
}

//////////////////////////////////////////////////

class Example17 extends Example {
  const Example17({super.key});

  @override
  final code =
      'UnconstrainedBox(\n'
      '   child: LimitedBox(maxWidth: 100,\n'
      '      child: Container(color: Colors.red,\n'
      '                       width: double.infinity, height: 100));';
  @override
  final String explanation =
      'Here you won\'t get an error anymore, '
      'because when the LimitedBox is given an infinite size by the UnconstrainedBox, '
      'it passes a maximum width of 100 down to its child.'
      '\n\n'
      'If you swap the UnconstrainedBox for a Center widget, '
      'the LimitedBox won\'t apply its limit anymore (since its limit is only applied when it gets infinite constraints), '
      'and the width of the Container is allowed to grow past 100.'
      '\n\n'
      'This explains the difference between a LimitedBox and a ConstrainedBox.';

  @override
  Widget build(BuildContext context) {
    return UnconstrainedBox(
      child: LimitedBox(
        maxWidth: 100,
        child: Container(
          color: Colors.red,
          width: double.infinity,
          height: 100,
        ),
      ),
    );
  }
}

//////////////////////////////////////////////////

class Example18 extends Example {
  const Example18({super.key});

  @override
  final code =
      'FittedBox(\n'
      '   child: Text(\'Some Example Text.\'));';
  @override
  final String explanation =
      'The screen forces the FittedBox to be exactly the same size as the screen.'
      'The Text has some natural width (also called its intrinsic width) that depends on the amount of text, its font size, and so on.'
      '\n\n'
      'The FittedBox lets the Text be any size it wants, '
      'but after the Text tells its size to the FittedBox, '
      'the FittedBox scales the Text until it fills all of the available width.';

  @override
  Widget build(BuildContext context) {
    return const FittedBox(child: Text('Some Example Text.'));
  }
}

//////////////////////////////////////////////////

class Example19 extends Example {
  const Example19({super.key});

  @override
  final code =
      'Center(\n'
      '   child: FittedBox(\n'
      '      child: Text(\'Some Example Text.\')));';
  @override
  final String explanation =
      'But what happens if you put the FittedBox inside of a Center widget? '
      'The Center lets the FittedBox be any size it wants, up to the screen size.'
      '\n\n'
      'The FittedBox then sizes itself to the Text, and lets the Text be any size it wants.'
      '\n\n'
      'Since both FittedBox and the Text have the same size, no scaling happens.';

  @override
  Widget build(BuildContext context) {
    return const Center(child: FittedBox(child: Text('Some Example Text.')));
  }
}

////////////////////////////////////////////////////

class Example20 extends Example {
  const Example20({super.key});

  @override
  final code =
      'Center(\n'
      '   child: FittedBox(\n'
      '      child: Text(\'…\')));';
  @override
  final String explanation =
      'However, what happens if FittedBox is inside of a Center widget, but the Text is too large to fit the screen?'
      '\n\n'
      'FittedBox tries to size itself to the Text, but it can\'t be bigger than the screen. '
      'It then assumes the screen size, and resizes Text so that it fits the screen, too.';

  @override
  Widget build(BuildContext context) {
    return const Center(
      child: FittedBox(
        child: Text(
          'This is some very very very large text that is too big to fit a regular screen in a single line.',
        ),
      ),
    );
  }
}

//////////////////////////////////////////////////

class Example21 extends Example {
  const Example21({super.key});

  @override
  final code =
      'Center(\n'
      '   child: Text(\'…\'));';
  @override
  final String explanation =
      'If, however, you remove the FittedBox, '
      'the Text gets its maximum width from the screen, '
      'and breaks the line so that it fits the screen.';

  @override
  Widget build(BuildContext context) {
    return const Center(
      child: Text(
        'This is some very very very large text that is too big to fit a regular screen in a single line.',
      ),
    );
  }
}

//////////////////////////////////////////////////

class Example22 extends Example {
  const Example22({super.key});

  @override
  final code =
      'FittedBox(\n'
      '   child: Container(\n'
      '      height: 20, width: double.infinity));';
  @override
  final String explanation =
      'FittedBox can only scale a widget that is BOUNDED (has non-infinite width and height).'
      'Otherwise, it won\'t render anything, and you\'ll see an error in the console.';

  @override
  Widget build(BuildContext context) {
    return FittedBox(
      child: Container(height: 20, width: double.infinity, color: Colors.red),
    );
  }
}

//////////////////////////////////////////////////

class Example23 extends Example {
  const Example23({super.key});

  @override
  final code =
      'Row(children:[\n'
      '   Container(color: red, child: Text(\'Hello!\'))\n'
      '   Container(color: green, child: Text(\'Goodbye!\'))]';
  @override
  final String explanation =
      'The screen forces the Row to be exactly the same size as the screen.'
      '\n\n'
      'Just like an UnconstrainedBox, the Row won\'t impose any constraints onto its children, '
      'and instead lets them be any size they want.'
      '\n\n'
      'The Row then puts them side-by-side, and any extra space remains empty.';

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Container(
          color: red,
          child: const Text('Hello!', style: big),
        ),
        Container(
          color: green,
          child: const Text('Goodbye!', style: big),
        ),
      ],
    );
  }
}

//////////////////////////////////////////////////

class Example24 extends Example {
  const Example24({super.key});

  @override
  final code =
      'Row(children:[\n'
      '   Container(color: red, child: Text(\'…\'))\n'
      '   Container(color: green, child: Text(\'Goodbye!\'))]';
  @override
  final String explanation =
      'Since the Row won\'t impose any constraints onto its children, '
      'it\'s quite possible that the children might be too big to fit the available width of the Row.'
      'In this case, just like an UnconstrainedBox, the Row displays the "overflow warning".';

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Container(
          color: red,
          child: const Text(
            'This is a very long text that '
            'won\'t fit the line.',
            style: big,
          ),
        ),
        Container(
          color: green,
          child: const Text('Goodbye!', style: big),
        ),
      ],
    );
  }
}

//////////////////////////////////////////////////

class Example25 extends Example {
  const Example25({super.key});

  @override
  final code =
      'Row(children:[\n'
      '   Expanded(\n'
      '       child: Container(color: red, child: Text(\'…\')))\n'
      '   Container(color: green, child: Text(\'Goodbye!\'))]';
  @override
  final String explanation =
      'When a Row\'s child is wrapped in an Expanded widget, the Row won\'t let this child define its own width anymore.'
      '\n\n'
      'Instead, it defines the Expanded width according to the other children, and only then the Expanded widget forces the original child to have the Expanded\'s width.'
      '\n\n'
      'In other words, once you use Expanded, the original child\'s width becomes irrelevant, and is ignored.';

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Expanded(
          child: Center(
            child: Container(
              color: red,
              child: const Text(
                'This is a very long text that won\'t fit the line.',
                style: big,
              ),
            ),
          ),
        ),
        Container(
          color: green,
          child: const Text('Goodbye!', style: big),
        ),
      ],
    );
  }
}

//////////////////////////////////////////////////

class Example26 extends Example {
  const Example26({super.key});

  @override
  final code =
      'Row(children:[\n'
      '   Expanded(\n'
      '       child: Container(color: red, child: Text(\'…\')))\n'
      '   Expanded(\n'
      '       child: Container(color: green, child: Text(\'Goodbye!\'))]';
  @override
  final String explanation =
      'If all of Row\'s children are wrapped in Expanded widgets, each Expanded has a size proportional to its flex parameter, '
      'and only then each Expanded widget forces its child to have the Expanded\'s width.'
      '\n\n'
      'In other words, Expanded ignores the preferred width of its children.';

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Expanded(
          child: Container(
            color: red,
            child: const Text(
              'This is a very long text that won\'t fit the line.',
              style: big,
            ),
          ),
        ),
        Expanded(
          child: Container(
            color: green,
            child: const Text('Goodbye!', style: big),
          ),
        ),
      ],
    );
  }
}

//////////////////////////////////////////////////

class Example27 extends Example {
  const Example27({super.key});

  @override
  final code =
      'Row(children:[\n'
      '   Flexible(\n'
      '       child: Container(color: red, child: Text(\'…\')))\n'
      '   Flexible(\n'
      '       child: Container(color: green, child: Text(\'Goodbye!\'))]';
  @override
  final String explanation =
      'The only difference if you use Flexible instead of Expanded, '
      'is that Flexible lets its child be SMALLER than the Flexible width, '
      'while Expanded forces its child to have the same width of the Expanded.'
      '\n\n'
      'But both Expanded and Flexible ignore their children\'s width when sizing themselves.'
      '\n\n'
      'This means that it\'s IMPOSSIBLE to expand Row children proportionally to their sizes. '
      'The Row either uses the exact child\'s width, or ignores it completely when you use Expanded or Flexible.';

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Flexible(
          child: Container(
            color: red,
            child: const Text(
              'This is a very long text that won\'t fit the line.',
              style: big,
            ),
          ),
        ),
        Flexible(
          child: Container(
            color: green,
            child: const Text('Goodbye!', style: big),
          ),
        ),
      ],
    );
  }
}

//////////////////////////////////////////////////

class Example28 extends Example {
  const Example28({super.key});

  @override
  final code =
      'Scaffold(\n'
      '   body: Container(color: blue,\n'
      '   child: Column(\n'
      '      children: [\n'
      '         Text(\'Hello!\'),\n'
      '         Text(\'Goodbye!\')])))';

  @override
  final String explanation =
      'The screen forces the Scaffold to be exactly the same size as the screen, '
      'so the Scaffold fills the screen.'
      '\n\n'
      'The Scaffold tells the Container that it can be any size it wants, but not bigger than the screen.'
      '\n\n'
      'When a widget tells its child that it can be smaller than a certain size, '
      'we say the widget supplies "loose" constraints to its child. More on that later.';

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        color: blue,
        child: const Column(children: [Text('Hello!'), Text('Goodbye!')]),
      ),
    );
  }
}

//////////////////////////////////////////////////

class Example29 extends Example {
  const Example29({super.key});

  @override
  final code =
      'Scaffold(\n'
      '   body: Container(color: blue,\n'
      '   child: SizedBox.expand(\n'
      '      child: Column(\n'
      '         children: [\n'
      '            Text(\'Hello!\'),\n'
      '            Text(\'Goodbye!\')]))))';

  @override
  final String explanation =
      'If you want the Scaffold\'s child to be exactly the same size as the Scaffold itself, '
      'you can wrap its child with SizedBox.expand.'
      '\n\n'
      'When a widget tells its child that it must be of a certain size, '
      'we say the widget supplies "tight" constraints to its child. More on that later.';

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SizedBox.expand(
        child: Container(
          color: blue,
          child: const Column(children: [Text('Hello!'), Text('Goodbye!')]),
        ),
      ),
    );
  }
}

//////////////////////////////////////////////////
```

Se preferir, você pode pegar o código
[deste repositório no GitHub][this GitHub repo].

Os exemplos são explicados nas seções a seguir.

[this GitHub repo]: https://github.com/marcglasberg/flutter_layout_article

### Exemplo 1 {:#example-1}

<img src='/assets/images/docs/ui/layout/layout-1.png' alt="Layout do exemplo 1">

<?code-excerpt "lib/main.dart (Example1)" replace="/(return |;)//g"?>
```dart
Container(color: red)
```

A tela é o pai do `Container`, e ela força o `Container`
a ter exatamente o mesmo tamanho da tela.

Então o `Container` preenche a tela e a pinta de vermelho.

### Exemplo 2 {:#example-2}

<img src='/assets/images/docs/ui/layout/layout-2.png' alt="Layout do exemplo 2">

<?code-excerpt "lib/main.dart (Example2)" replace="/(return |;)//g"?>
```dart
Container(width: 100, height: 100, color: red)
```

O `Container` vermelho quer ter 100 × 100,
mas não pode, porque a tela o obriga a ter
exatamente o mesmo tamanho da tela.

Então o `Container` preenche a tela.

### Exemplo 3 {:#example-3}

<img src='/assets/images/docs/ui/layout/layout-3.png' alt="Layout do exemplo 3">

<?code-excerpt "lib/main.dart (Example3)" replace="/(return |;)//g"?>
```dart
Center(child: Container(width: 100, height: 100, color: red))
```

A tela obriga o `Center` a ter exatamente o mesmo tamanho
que a tela, então o `Center` preenche a tela.

O `Center` diz ao `Container` que ele pode ter qualquer tamanho que
quiser, mas não maior que a tela. Agora o `Container`
pode realmente ter 100 × 100.

### Exemplo 4 {:#example-4}

<img src='/assets/images/docs/ui/layout/layout-4.png' alt="Layout do exemplo 4">

<?code-excerpt "lib/main.dart (Example4)" replace="/(return |;)//g"?>
```dart
Align(
  alignment: Alignment.bottomRight,
  child: Container(width: 100, height: 100, color: red),
)
```

Este exemplo é diferente do anterior porque usa
`Align` em vez de `Center`.

`Align` também diz ao `Container` que ele pode ter qualquer
tamanho que desejar, mas se houver espaço vazio, ele
não centralizará o `Container`. Em vez disso, alinha
o container ao canto inferior direito do espaço disponível.

### Exemplo 5 {:#example-5}

<img src='/assets/images/docs/ui/layout/layout-5.png' alt="Layout do exemplo 5">

<?code-excerpt "lib/main.dart (Example5)" replace="/(return |;)//g"?>
```dart
Center(
  child: Container(
    width: double.infinity,
    height: double.infinity,
    color: red,
  ),
)
```

A tela força o `Center` a ter exatamente o mesmo tamanho que a tela,
então o `Center` preenche a tela.

O `Center` diz ao `Container` que ele pode ter qualquer
tamanho que desejar, mas não maior que a tela.
O `Container` deseja ter tamanho infinito, mas como
não pode ser maior que a tela, apenas preenche a tela.

### Exemplo 6 {:#example-6}

<img src='/assets/images/docs/ui/layout/layout-6.png' alt="Layout do exemplo 6">

<?code-excerpt "lib/main.dart (Example6)" replace="/(return |;)//g"?>
```dart
Center(child: Container(color: red))
```

A tela força o `Center` a ter exatamente o mesmo
tamanho que a tela, então o `Center` preenche a tela.

O `Center` diz ao `Container` que ele pode ter qualquer
tamanho que desejar, mas não maior que a tela.
Como o `Container` não tem filho e não tem
tamanho fixo, decide que quer ser o maior possível,
então preenche a tela inteira.

Mas por que o `Container` decide isso?
Simplesmente porque é uma decisão de design de quem
criou o widget `Container`. Ele poderia ter sido
criado de forma diferente, e você precisa ler a
documentação da API de [`Container`][] para entender
como ele se comporta, dependendo das circunstâncias.

### Exemplo 7 {:#example-7}

<img src='/assets/images/docs/ui/layout/layout-7.png' alt="Layout do exemplo 7">

<?code-excerpt "lib/main.dart (Example7)" replace="/(return |;)//g"?>
```dart
Center(
  child: Container(
    color: red,
    child: Container(color: green, width: 30, height: 30),
  ),
)
```

A tela força o `Center` a ter exatamente o mesmo
tamanho que a tela, então o `Center` preenche a tela.

O `Center` diz ao `Container` vermelho que ele pode ter qualquer
tamanho que desejar, mas não maior que a tela. Como o `Container`
vermelho não tem tamanho, mas tem um filho, ele decide que
quer ter o mesmo tamanho que seu filho.

O `Container` vermelho diz ao seu filho que ele pode ter qualquer
tamanho que desejar, mas não maior que a tela.

O filho é um `Container` verde que deseja ter 30 × 30.
Como o `Container` vermelho ajusta seu tamanho ao tamanho
de seu filho, ele também tem 30 × 30. A cor vermelha não
é visível porque o `Container` verde cobre completamente
o `Container` vermelho.

### Exemplo 8 {:#example-8}

<img src='/assets/images/docs/ui/layout/layout-8.png' alt="Layout do exemplo 8">

<?code-excerpt "lib/main.dart (Example8)" replace="/(return |;)//g"?>
```dart
Center(
  child: Container(
    padding: const EdgeInsets.all(20),
    color: red,
    child: Container(color: green, width: 30, height: 30),
  ),
)
```

O `Container` vermelho ajusta seu tamanho ao tamanho de seus
filhos, mas leva em consideração seu próprio padding.
Então ele também tem 30 × 30 mais o padding. A cor vermelha é
visível por causa do padding, e o `Container` verde tem
o mesmo tamanho que no exemplo anterior.

### Exemplo 9 {:#example-9}

<img src='/assets/images/docs/ui/layout/layout-9.png' alt="Layout do exemplo 9">

<?code-excerpt "lib/main.dart (Example9)" replace="/(return |;)//g"?>
```dart
ConstrainedBox(
  constraints: const BoxConstraints(
    minWidth: 70,
    minHeight: 70,
    maxWidth: 150,
    maxHeight: 150,
  ),
  child: Container(color: red, width: 10, height: 10),
)
```

Você pode imaginar que o `Container` deve ter entre 70 e 150 pixels,
mas estaria errado. O `ConstrainedBox` impõe apenas
restrições **adicionais** àquelas que recebe de seu pai.

Aqui, a tela força o `ConstrainedBox` a ter exatamente o
mesmo tamanho que a tela, então ele diz ao seu filho
`Container` para também assumir o tamanho da tela,
ignorando assim seu parâmetro `constraints`.

### Exemplo 10 {:#example-10}

<img src='/assets/images/docs/ui/layout/layout-10.png' alt="Layout do exemplo 10">

<?code-excerpt "lib/main.dart (Example10)" replace="/(return |;)//g"?>
```dart
Center(
  child: ConstrainedBox(
    constraints: const BoxConstraints(
      minWidth: 70,
      minHeight: 70,
      maxWidth: 150,
      maxHeight: 150,
    ),
    child: Container(color: red, width: 10, height: 10),
  ),
)
```

Agora, `Center` permite que `ConstrainedBox` tenha qualquer
tamanho até o tamanho da tela. O `ConstrainedBox` impõe
restrições **adicionais** de seu parâmetro `constraints` ao seu filho.

O Container deve ter entre 70 e 150 pixels.
Ele quer ter 10 pixels,
então acaba tendo 70 (o mínimo).

### Exemplo 11 {:#example-11}

<img src='/assets/images/docs/ui/layout/layout-11.png' alt="Layout do exemplo 11">

<?code-excerpt "lib/main.dart (Example11)" replace="/(return |;)//g"?>
```dart
Center(
  child: ConstrainedBox(
    constraints: const BoxConstraints(
      minWidth: 70,
      minHeight: 70,
      maxWidth: 150,
      maxHeight: 150,
    ),
    child: Container(color: red, width: 1000, height: 1000),
  ),
)
```

`Center` permite que `ConstrainedBox` tenha qualquer tamanho
até o tamanho da tela. O `ConstrainedBox` impõe restrições
**adicionais** de seu parâmetro `constraints` ao seu filho.

O `Container` deve ter entre 70 e 150 pixels.
Ele quer ter 1000 pixels,
então acaba tendo 150 (o máximo).

### Exemplo 12 {:#example-12}

<img src='/assets/images/docs/ui/layout/layout-12.png' alt="Layout do exemplo 12">

<?code-excerpt "lib/main.dart (Example12)" replace="/(return |;)//g"?>
```dart
Center(
  child: ConstrainedBox(
    constraints: const BoxConstraints(
      minWidth: 70,
      minHeight: 70,
      maxWidth: 150,
      maxHeight: 150,
    ),
    child: Container(color: red, width: 100, height: 100),
  ),
)
```

`Center` permite que `ConstrainedBox` tenha qualquer tamanho
até o tamanho da tela. O `ConstrainedBox` impõe restrições
**adicionais** de seu parâmetro `constraints` ao seu filho.

O `Container` deve ter entre 70 e 150 pixels.
Ele quer ter 100 pixels, e é esse o tamanho que tem,
já que está entre 70 e 150.

### Exemplo 13 {:#example-13}

<img src='/assets/images/docs/ui/layout/layout-13.png' alt="Layout do exemplo 13">

<?code-excerpt "lib/main.dart (Example13)" replace="/(return |;)//g"?>
```dart
UnconstrainedBox(
  child: Container(color: red, width: 20, height: 50),
)
```

A tela força o `UnconstrainedBox` a ter exatamente o
mesmo tamanho que a tela. No entanto, o `UnconstrainedBox`
permite que seu filho `Container` tenha qualquer tamanho que desejar.

### Exemplo 14 {:#example-14}

<img src='/assets/images/docs/ui/layout/layout-14.png' alt="Layout do exemplo 14">

<?code-excerpt "lib/main.dart (Example14)" replace="/(return |;)//g"?>
```dart
UnconstrainedBox(
  child: Container(color: red, width: 4000, height: 50),
)
```

A tela força o `UnconstrainedBox` a ter exatamente o mesmo tamanho
que a tela, e o `UnconstrainedBox` permite que seu filho
`Container` tenha qualquer tamanho que desejar.

Infelizmente, neste caso, o `Container` tem 4000 pixels de
largura e é grande demais para caber no `UnconstrainedBox`,
então o `UnconstrainedBox` exibe o tão temido
"aviso de overflow" ("overflow warning").

### Exemplo 15 {:#example-15}

<img src='/assets/images/docs/ui/layout/layout-15.png' alt="Layout do exemplo 15">

<?code-excerpt "lib/main.dart (Example15)" replace="/(return |;)//g"?>
```dart
OverflowBox(
  minWidth: 0,
  minHeight: 0,
  maxWidth: double.infinity,
  maxHeight: double.infinity,
  child: Container(color: red, width: 4000, height: 50),
)
```

A tela força o `OverflowBox` a ter exatamente o mesmo tamanho
que a tela, e o `OverflowBox` permite que seu filho `Container`
tenha qualquer tamanho que desejar.

O `OverflowBox` é semelhante ao `UnconstrainedBox`;
a diferença é que ele não exibirá nenhum aviso se o
filho não couber no espaço.

Neste caso, o `Container` tem 4000 pixels de largura
e é grande demais para caber no `OverflowBox`, mas o
`OverflowBox` simplesmente mostra o máximo
que pode, sem avisos.

### Exemplo 16 {:#example-16}

<img src='/assets/images/docs/ui/layout/layout-16.png' alt="Layout do exemplo 16">

<?code-excerpt "lib/main.dart (Example16)" replace="/(return |;)//g"?>
```dart
UnconstrainedBox(
  child: Container(color: Colors.red, width: double.infinity, height: 100),
)
```

Isso não renderizará nada, e você verá um erro no console.

O `UnconstrainedBox` permite que seu filho tenha qualquer
tamanho que desejar; no entanto, seu filho é um `Container` com tamanho infinito.

O Flutter não pode renderizar tamanhos infinitos, então ele
lança um erro com a seguinte mensagem: `BoxConstraints forces an infinite width.`

### Exemplo 17 {:#example-17}

<img src='/assets/images/docs/ui/layout/layout-17.png' alt="Layout do exemplo 17">

<?code-excerpt "lib/main.dart (Example17)" replace="/(return |;)//g"?>
```dart
UnconstrainedBox(
  child: LimitedBox(
    maxWidth: 100,
    child: Container(
      color: Colors.red,
      width: double.infinity,
      height: 100,
    ),
  ),
)
```

Aqui você não terá mais erros,
porque quando o `LimitedBox` recebe um tamanho
infinito do `UnconstrainedBox`,
ele passa uma largura máxima de 100 para o seu filho.

Se você trocar o `UnconstrainedBox` por um widget `Center`,
o `LimitedBox` não aplicará mais seu limite
(já que seu limite é aplicado apenas quando recebe restrições
infinitas), e a largura do `Container`
pode crescer além de 100.

Isso explica a diferença entre um `LimitedBox`
e um `ConstrainedBox`.

### Exemplo 18 {:#example-18}

<img src='/assets/images/docs/ui/layout/layout-18.png' alt="Layout do exemplo 18">

<?code-excerpt "lib/main.dart (Example18)" replace="/(return |;)//g"?>
```dart
const FittedBox(child: Text('Some Example Text.'))
```

A tela força o `FittedBox` a ter exatamente o mesmo tamanho
que a tela. O `Text` tem uma largura natural (também
chamada de largura intrínseca) que depende da quantidade
de texto, do tamanho da fonte e assim por diante.

O `FittedBox` permite que o `Text` tenha qualquer
tamanho que desejar, mas depois que o `Text` informa
seu tamanho ao `FittedBox`, o `FittedBox` dimensiona
o texto até preencher toda a largura disponível.

### Exemplo 19 {:#example-19}

<img src='/assets/images/docs/ui/layout/layout-19.png' alt="Layout do exemplo 19">

<?code-excerpt "lib/main.dart (Example19)" replace="/(return |;)//g"?>
```dart
const Center(child: FittedBox(child: Text('Some Example Text.')))
```

Mas o que acontece se você colocar o `FittedBox` dentro
de um widget `Center`? O `Center` permite que o `FittedBox`
tenha qualquer tamanho que desejar, até o tamanho da tela.

O `FittedBox` então se dimensiona de acordo com o `Text`
e permite que o `Text` tenha qualquer tamanho que desejar.
Como o `FittedBox` e o `Text` têm o mesmo tamanho,
não ocorre nenhum redimensionamento.

### Exemplo 20 {:#example-20}

<img src='/assets/images/docs/ui/layout/layout-20.png' alt="Layout do exemplo 20">

<?code-excerpt "lib/main.dart (Example20)" replace="/(return |;)//g"?>
```dart
const Center(
  child: FittedBox(
    child: Text(
      'This is some very very very large text that is too big to fit a regular screen in a single line.',
    ),
  ),
)
```

No entanto, o que acontece se o `FittedBox` estiver dentro de um widget
`Center`, mas o `Text` for grande demais para caber na tela?

O `FittedBox` tenta se ajustar ao tamanho do `Text`,
mas não pode ser maior do que a tela.
Então ele assume o tamanho da tela
e redimensiona o `Text` para que ele também caiba na tela.

### Exemplo 21 {:#example-21}

<img src='/assets/images/docs/ui/layout/layout-21.png' alt="Layout do exemplo 21">

<?code-excerpt "lib/main.dart (Example21)" replace="/(return |;)//g"?>
```dart
const Center(
  child: Text(
    'This is some very very very large text that is too big to fit a regular screen in a single line.',
  ),
)
```

Se, no entanto, você remover o `FittedBox`, o `Text`
obtém sua largura máxima da tela
e quebra a linha para que caiba na tela.

### Exemplo 22 {:#example-22}

<img src='/assets/images/docs/ui/layout/layout-22.png' alt="Layout do exemplo 22">

<?code-excerpt "lib/main.dart (Example22)" replace="/(return |;)//g"?>
```dart
FittedBox(
  child: Container(height: 20, width: double.infinity, color: Colors.red),
)
```

O `FittedBox` só pode dimensionar um widget que seja limitado
(com largura e altura não infinitas). Caso contrário,
ele não renderizará nada,
e você verá um erro no console.

### Exemplo 23 {:#example-23}

<img src='/assets/images/docs/ui/layout/layout-23.png' alt="Layout do exemplo 23">

<?code-excerpt "lib/main.dart (Example23)" replace="/(return |;)//g"?>
```dart
Row(
  children: [
    Container(
      color: red,
      child: const Text('Hello!', style: big),
    ),
    Container(
      color: green,
      child: const Text('Goodbye!', style: big),
    ),
  ],
)
```

A tela força a `Row` a ter exatamente o mesmo tamanho
que a tela.

Assim como um `UnconstrainedBox`, a `Row` não
impõe restrições aos seus filhos e, em vez disso,
permite que eles tenham qualquer tamanho que desejarem.
A `Row` então os coloca lado a lado,
e qualquer espaço extra permanece vazio.

### Exemplo 24 {:#example-24}

<img src='/assets/images/docs/ui/layout/layout-24.png' alt="Layout do exemplo 24">

<?code-excerpt "lib/main.dart (Example24)" replace="/(return |;)//g"?>
```dart
Row(
  children: [
    Container(
      color: red,
      child: const Text(
        'This is a very long text that '
        'won\'t fit the line.',
        style: big,
      ),
    ),
    Container(
      color: green,
      child: const Text('Goodbye!', style: big),
    ),
  ],
)
```

Como a `Row` não impõe restrições aos seus filhos,
é bem possível que os filhos sejam grandes demais para caber
na largura disponível da `Row`. Nesse caso, assim como um
`UnconstrainedBox`, a `Row` exibe o "aviso de overflow" ("overflow warning").

### Exemplo 25 {:#example-25}

<img src='/assets/images/docs/ui/layout/layout-25.png' alt="Layout do exemplo 25">

<?code-excerpt "lib/main.dart (Example25)" replace="/(return |;)//g"?>
```dart
Row(
  children: [
    Expanded(
      child: Center(
        child: Container(
          color: red,
          child: const Text(
            'This is a very long text that won\'t fit the line.',
            style: big,
          ),
        ),
      ),
    ),
    Container(
      color: green,
      child: const Text('Goodbye!', style: big),
    ),
  ],
)
```

Quando um filho de uma `Row` é envolvido por um widget `Expanded`,
a `Row` não permite mais que esse filho defina sua própria largura.

Em vez disso, ela define a largura do `Expanded` de acordo com os
outros filhos e, só então, o widget `Expanded` força
o filho original a ter a largura do `Expanded`.

Em outras palavras, ao usar o `Expanded`,
a largura original do filho se torna irrelevante e é ignorada.

### Exemplo 26 {:#example-26}

<img src='/assets/images/docs/ui/layout/layout-26.png' alt="Layout do exemplo 26">

<?code-excerpt "lib/main.dart (Example26)" replace="/(return |;)//g"?>
```dart
Row(
  children: [
    Expanded(
      child: Container(
        color: red,
        child: const Text(
          'This is a very long text that won\'t fit the line.',
          style: big,
        ),
      ),
    ),
    Expanded(
      child: Container(
        color: green,
        child: const Text('Goodbye!', style: big),
      ),
    ),
  ],
)
```

Se todos os filhos da `Row` estiverem envolvidos por widgets `Expanded`,
cada `Expanded` terá um tamanho proporcional ao seu parâmetro flex
e, só então, cada widget `Expanded` forçará seu filho a ter
a largura do `Expanded`.

Em outras palavras, o `Expanded` ignora a largura preferida
de seus filhos.

### Exemplo 27 {:#example-27}

<img src='/assets/images/docs/ui/layout/layout-27.png' alt="Layout do exemplo 27">

<?code-excerpt "lib/main.dart (Example27)" replace="/(return |;)//g"?>
```dart
Row(
  children: [
    Flexible(
      child: Container(
        color: red,
        child: const Text(
          'This is a very long text that won\'t fit the line.',
          style: big,
        ),
      ),
    ),
    Flexible(
      child: Container(
        color: green,
        child: const Text('Goodbye!', style: big),
      ),
    ),
  ],
)
```

A única diferença ao usar `Flexible` em vez de `Expanded`
é que `Flexible` permite que seu filho tenha a mesma largura ou uma
largura menor que o próprio `Flexible`, enquanto `Expanded` força
seu filho a ter exatamente a mesma largura do `Expanded`.
Mas tanto `Expanded` quanto `Flexible` ignoram a largura de seus filhos
ao dimensionar a si mesmos.

:::note
Isso significa que é impossível expandir os filhos da `Row`
proporcionalmente a seus tamanhos. A `Row` usa
a largura exata do filho ou a ignora completamente
quando você usa `Expanded` ou `Flexible`.
:::

### Exemplo 28 {:#example-28}

<img src='/assets/images/docs/ui/layout/layout-28.png' alt="Layout do exemplo 28">

<?code-excerpt "lib/main.dart (Example28)" replace="/(return |;)//g"?>
```dart
Scaffold(
  body: Container(
    color: blue,
    child: const Column(children: [Text('Hello!'), Text('Goodbye!')]),
  ),
)
```

A tela força o `Scaffold` a ter exatamente o mesmo tamanho
que a tela, então o `Scaffold` preenche a tela.
O `Scaffold` diz ao `Container` que ele pode ter qualquer tamanho que quiser,
mas não maior que a tela.

:::note
Quando um widget diz ao seu filho que ele pode ser menor que um
certo tamanho, dizemos que o widget fornece restrições _loose_
(flexíveis) para seu filho. Mais sobre isso adiante.
:::

### Exemplo 29 {:#example-29}

<img src='/assets/images/docs/ui/layout/layout-29.png' alt="Layout do exemplo 29">

<?code-excerpt "lib/main.dart (Example29)" replace="/(return |;)//g"?>
```dart
Scaffold(
  body: SizedBox.expand(
    child: Container(
      color: blue,
      child: const Column(children: [Text('Hello!'), Text('Goodbye!')]),
    ),
  ),
)
```

Se você quiser que o filho do `Scaffold` tenha exatamente o mesmo tamanho
que o próprio `Scaffold`, você pode envolver seu filho com
`SizedBox.expand`.

## Restrições tight vs. loose (rígidas vs. flexíveis) {:#tight-vs-loose-constraints}

É muito comum ouvir que alguma restrição é
"tight" ou "loose", então o que isso significa?

### Restrições tight (rígidas) {:#tight-constraints}

Uma restrição _tight_ oferece uma única possibilidade,
um tamanho exato. Em outras palavras, uma restrição tight
tem sua largura máxima igual à sua largura mínima
e sua altura máxima igual à sua altura mínima.

Um exemplo disso é o widget `App`,
que é contido pela classe [`RenderView`][]:
o box usado pelo filho retornado pela
função [`build`][] da aplicação recebe uma restrição
que o força a preencher exatamente a área de conteúdo da aplicação
(tipicamente, a tela inteira).

Outro exemplo: se você aninhar vários boxes uns dentro
dos outros na raiz da árvore de renderização da sua aplicação,
eles vão se encaixar exatamente uns nos outros,
forçados pelas restrições tight do box.

Se você acessar o arquivo `box.dart` do Flutter e buscar pelos
construtores de `BoxConstraints`,
encontrará o seguinte:

```dart
BoxConstraints.tight(Size size)
   : minWidth = size.width,
     maxWidth = size.width,
     minHeight = size.height,
     maxHeight = size.height;
```

Se você revisitar o [Exemplo 2](#example-2),
a tela força o `Container` vermelho a ter
exatamente o mesmo tamanho da tela.
A tela faz isso, é claro, passando restrições tight
para o `Container`.

### Restrições loose (flexíveis) {:#loose-constraints}

Uma restrição _loose_ é aquela que tem um valor mínimo
de zero e um valor máximo diferente de zero.

Alguns boxes _afrouxam_ (loosen) as restrições recebidas,
o que significa que o máximo é mantido, mas o
mínimo é removido, de modo que o widget pode ter
uma largura e uma altura **mínimas** iguais a **zero**.

Em última análise, o propósito do `Center` é transformar
as restrições tight que recebeu de seu pai
(a tela) em restrições loose para seu filho
(o `Container`).

Se você revisitar o [Exemplo 3](#example-3),
o `Center` permite que o `Container` vermelho seja menor,
mas não maior que a tela.

[`build`]: {{site.api}}/flutter/widgets/State/build.html
[`RenderView`]: {{site.api}}/flutter/rendering/RenderView-class.html

<a id="unbounded"></a>

## Restrições unbounded (sem limite) {:#unbounded-constraints}

:::note
Você pode ser direcionado para cá se o framework
detectar um problema envolvendo restrições de box.
A seção `Flex` abaixo também pode se aplicar.
:::

Em certas situações,
a restrição de um box é _unbounded_ (sem limite), ou infinita.
Isso significa que a largura máxima ou
a altura máxima é definida como [`double.infinity`][].

Um box que tenta ser o maior possível não funcionará
de forma útil quando receber uma restrição sem limite e,
no modo debug, lança uma exceção.

O caso mais comum em que um render box acaba
com uma restrição sem limite é dentro de um box flex
([`Row`][] ou [`Column`][])
e **dentro de uma região rolável**
(como [`ListView`][] e outras subclasses de [`ScrollView`][]).

O [`ListView`][], por exemplo,
tenta se expandir para preencher o espaço disponível
na sua direção cruzada
(talvez seja um bloco rolável verticalmente e
tente ser tão largo quanto seu pai).
Se você aninhar um [`ListView`][] rolável verticalmente
dentro de um `ListView` rolável horizontalmente,
a lista interna tenta ser o mais larga possível,
o que é infinitamente larga,
já que a externa é rolável nessa direção.

A próxima seção descreve o erro que você pode
encontrar com restrições sem limite em um widget `Flex`.

## Flex

Um box flex ([`Row`][] e [`Column`][]) se comporta
de maneira diferente dependendo se sua
restrição é limitada ou sem limite na sua
direção principal.

Um box flex com uma restrição limitada na sua
direção principal tenta ser o maior possível.

Um box flex com uma restrição sem limite
na sua direção principal tenta encaixar seus filhos
nesse espaço. O valor `flex` de cada filho deve ser
definido como zero, o que significa que não é possível usar
[`Expanded`][] quando o box flex está dentro
de outro box flex ou de um scrollable;
caso contrário, ele lança uma exceção.

A direção _cruzada_
(largura para [`Column`][] ou altura para [`Row`][])
_nunca_ deve ser sem limite,
ou ele não conseguirá alinhar seus filhos de forma razoável.

[`double.infinity`]: {{site.api}}/flutter/dart-core/double/infinity-constant.html
[`Expanded`]: {{site.api}}/flutter/widgets/Expanded-class.html
[`RenderBox`]: {{site.api}}/flutter/rendering/RenderBox-class.html
[`ScrollView`]: {{site.api}}/flutter/widgets/ScrollView-class.html

## Aprendendo as regras de layout para widgets específicos {:#learning-the-layout-rules-for-specific-widgets}

Conhecer a regra geral de layout é necessário, mas não é suficiente.

Cada widget tem muita liberdade ao aplicar a regra geral,
então não há como saber como ele se comporta apenas lendo
o nome do widget.

Se você tentar adivinhar, provavelmente vai errar.
Você não pode saber exatamente como um widget se comporta a menos que
tenha lido sua documentação ou estudado seu código-fonte.

O código-fonte de layout geralmente é complexo,
então provavelmente é melhor apenas ler a documentação.
No entanto, se você decidir estudar o código-fonte de layout,
pode encontrá-lo facilmente usando os recursos de navegação
da sua IDE.

Aqui está um exemplo:

* Encontre uma `Column` em seu código e navegue até o
  código-fonte dela. Para fazer isso, use `command+B` (macOS)
  ou `control+B` (Windows/Linux) no Android Studio ou IntelliJ.
  Você será levado ao arquivo `basic.dart`.
  Como `Column` estende `Flex`, navegue até o código-fonte de `Flex`
  (também em `basic.dart`).

* Role para baixo até encontrar um método chamado
  `createRenderObject()`. Como você pode ver,
  este método retorna um `RenderFlex`.
  Este é o render object da `Column`.
  Agora navegue até o código-fonte de `RenderFlex`,
  o que leva você ao arquivo `flex.dart`.

* Role para baixo até encontrar um método chamado
  `performLayout()`. Este é o método que faz
  o layout da `Column`.

<img src='/assets/images/docs/ui/layout/layout-final.png' alt="Um layout de despedida">

---

Artigo original de Marcelo Glasberg

Marcelo publicou originalmente este conteúdo como
[Flutter: The Advanced Layout Rule Even Beginners Must Know][article]
no Medium. Nós adoramos e pedimos que ele nos permitisse publicá-lo
em docs.flutter.dev, ao que ele gentilmente concordou. Obrigado, Marcelo!
Você pode encontrar Marcelo no [GitHub][] e no [pub.dev][].

Também agradecemos a [Simon Lightfoot][] por criar a
imagem do cabeçalho no topo do artigo.

[article]: https://medium.com/flutter-community/flutter-the-advanced-layout-rule-even-beginners-must-know-edc9516d1a2
[GitHub]: https://github.com/marcglasberg
[pub.dev]: {{site.pub}}/publishers/glasberg.dev/packages
[Simon Lightfoot]: https://github.com/slightfoot

:::note
Para entender melhor como o Flutter implementa as
restrições de layout, confira o seguinte vídeo de 5 minutos:

<YouTubeEmbed id="jckqXR5CrPI" title="Decoding Flutter: Unbounded height and width"></YouTubeEmbed>
:::

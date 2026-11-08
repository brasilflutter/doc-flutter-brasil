---
title: Estudo de caso da camada de UI
shortTitle: Camada de UI
description: >-
  Um passo a passo da camada de UI de um aplicativo que implementa a arquitetura MVVM.
prev:
  title: Visão geral do estudo de caso
  path: /app-architecture/case-study
next:
  title: Camada de dados
  path: /app-architecture/case-study/data-layer
ia-translate: true
---

A [camada de UI][UI layer] de cada recurso em seu aplicativo Flutter deve ser
composta por dois componentes: uma **[`View`][]** e
um **[`ViewModel`][].**

![Uma captura de tela da tela de reserva do aplicativo compass.](/assets/images/docs/app-architecture/case-study/mvvm-case-study-ui-layer-highlighted.png)

Em termos gerais, os view models gerenciam o estado da UI,
e as views exibem o estado da UI.
As views e os view models têm uma relação um-para-um;
para cada view, existe exatamente um view model correspondente que
gerencia o estado dessa view.
Cada par de view e view model compõe a UI de um único recurso.
Por exemplo, um aplicativo pode ter classes chamadas
`LogOutView` e `LogOutViewModel`.

## Definir um view model

Um view model é uma classe Dart responsável por lidar com a lógica da UI.
Os view models recebem modelos de dados de domínio como entrada e expõem esses dados como
estado da UI para suas views correspondentes.
Eles encapsulam a lógica que a view pode anexar a
manipuladores de eventos, como cliques de botão, e
gerenciar o envio desses eventos para a camada de dados do aplicativo,
onde as alterações de dados acontecem.

O snippet de código a seguir é uma declaração de classe para
uma classe view model chamada `HomeViewModel`.
Suas entradas são os [repositórios][repositories] que fornecem seus dados.
Neste caso,
o view model depende do
`BookingRepository` e `UserRepository` como argumentos.

```dart title=home_viewmodel.dart
class HomeViewModel {
  HomeViewModel({
    required BookingRepository bookingRepository,
    required UserRepository userRepository,
  }) :
    // Os repositórios são atribuídos manualmente porque são membros privados.
    _bookingRepository = bookingRepository,
    _userRepository = userRepository;

  final BookingRepository _bookingRepository;
  final UserRepository _userRepository;
  // ...
}
```

Os view models sempre dependem de repositórios de dados,
que são fornecidos como argumentos para o construtor do view model.
View models e repositórios têm uma relação de muitos para muitos,
e a maioria dos view models dependerá de vários repositórios.

Como na declaração de exemplo `HomeViewModel` anterior,
os repositórios devem ser membros privados no view model,
caso contrário, as views teriam acesso direto a
a camada de dados do aplicativo.

### Estado da UI

A saída de um view model são dados que uma view precisa para renderizar, geralmente
referido como **Estado da UI**, ou apenas estado. O estado da UI é um snapshot imutável de
dados necessários para renderizar totalmente uma view.

![Uma captura de tela da tela de reserva do aplicativo compass.](/assets/images/docs/app-architecture/case-study/mvvm-case-study-ui-state-highlighted.png)

O view model expõe o estado como membros públicos.
No view model no exemplo de código a seguir,
os dados expostos são um objeto `User`,
assim como os itinerários salvos do usuário que
são expostos como um objeto do tipo `List<BookingSummary>`.

```dart title=home_viewmodel.dart
class HomeViewModel {
  HomeViewModel({
   required BookingRepository bookingRepository,
   required UserRepository userRepository,
  }) : _bookingRepository = bookingRepository,
      _userRepository = userRepository;

  final BookingRepository _bookingRepository;
  final UserRepository _userRepository;

  User? _user;
  User? get user => _user;

  List<BookingSummary> _bookings = [];

  /// Items in an [UnmodifiableListView] can't be directly modified,
  /// but changes in the source list can be modified. Since _bookings
  /// is private and bookings is not, the view has no way to modify the
  /// list directly.
  UnmodifiableListView<BookingSummary> get bookings => UnmodifiableListView(_bookings);

  // ...
}
```

Como mencionado, o estado da UI deve ser imutável.
Esta é uma parte crucial do software livre de bugs.

O aplicativo compass usa o [`package:freezed`][] para
impor imutabilidade em classes de dados. Por exemplo,
o código a seguir mostra a definição da classe `User`.
`freezed` fornece imutabilidade profunda,
e gera a implementação para métodos úteis como
`copyWith` e `toJson`.

```dart title=user.dart
@freezed
class User with _$User {
  const factory User({
    /// O nome do usuário.
    required String name,

    /// A URL da foto do usuário.
    required String picture,
  }) = _User;

  factory User.fromJson(Map<String, Object?> json) => _$UserFromJson(json);
}
```

:::note
No exemplo do view model,
dois objetos são necessários para renderizar a view.
À medida que o estado da UI para qualquer modelo aumenta em complexidade,
um view model pode ter muito mais dados de
muito mais repositórios expostos à view.
Em alguns casos,
você pode querer criar objetos que representem especificamente o estado da UI.
Por exemplo, você pode criar uma classe chamada `HomeUiState`.
:::

### Atualizando o estado da UI

Além de armazenar o estado,
os view models precisam informar ao Flutter para renderizar novamente as views quando
a camada de dados fornece um novo estado.
No aplicativo Compass, os view models estendem [`ChangeNotifier`][] para conseguir isso.

```dart title=home_viewmodel.dart
class HomeViewModel [!extends ChangeNotifier!] {
  HomeViewModel({
   required BookingRepository bookingRepository,
   required UserRepository userRepository,
  }) : _bookingRepository = bookingRepository,
      _userRepository = userRepository;
  final BookingRepository _bookingRepository;
  final UserRepository _userRepository;

  User? _user;
  User? get user => _user;

  List<BookingSummary> _bookings = [];
  List<BookingSummary> get bookings => _bookings;

  // ...
}
```

`HomeViewModel.user` é um membro público do qual a view depende.
Quando novos dados fluem da camada de dados e
um novo estado precisa ser emitido, [`notifyListeners`][] é chamado.

<figure>

![Uma captura de tela da tela de reserva do aplicativo compass.](/assets/images/docs/app-architecture/case-study/mvvm-case-study-update-ui-steps.png)

    <figcaption>
Esta figura mostra de forma geral como novos dados no repositório
se propagam até a camada de UI e acionam uma reconstrução de seus widgets Flutter.
    </figcaption>
</figure>

1. Um novo estado é fornecido ao view model de um Repositório.
2. O view model atualiza seu estado de UI para refletir os novos dados.
3. `ViewModel.notifyListeners` é chamado, alertando a View sobre o novo estado da UI.
4. A view (widget) é renderizada novamente.

Por exemplo, quando o usuário navega para a tela inicial e o view model é
criado, o método `_load` é chamado.
Até que este método seja concluído, o estado da UI está vazio,
a view exibe um indicador de carregamento.
Quando o método `_load` é concluído, se for bem-sucedido,
há novos dados no view model e ele deve
notificar a view de que novos dados estão disponíveis.

```dart title=home_viewmodel.dart highlightLines=19
class HomeViewModel extends ChangeNotifier {
  // ...

 Future<Result> _load() async {
    try {
      final userResult = await _userRepository.getUser();
      switch (userResult) {
        case Ok<User>():
          _user = userResult.value;
          _log.fine('Loaded user');
        case Error<User>():
          _log.warning('Failed to load user', userResult.error);
      }

      // ...

      return userResult;
    } finally {
      notifyListeners();
    }
  }
}
```

:::note
`ChangeNotifier` e [`ListenableBuilder`][] (discutido mais adiante nesta página) são
parte do SDK Flutter,
e fornecem uma boa solução para atualizar a UI quando o estado muda.
Você também pode usar uma solução robusta de gerenciamento de estado de terceiros, como
[`package:riverpod`][], [`package:flutter_bloc`][] ou [`package:signals`][].
Essas bibliotecas oferecem ferramentas diferentes para lidar com atualizações de UI.
Leia mais sobre como usar `ChangeNotifier` em
nossa [documentação de gerenciamento de estado][state-management documentation].
:::

[`package:riverpod`]: {{site.pub-pkg}}/riverpod
[`package:flutter_bloc`]: {{site.pub-pkg}}/flutter_bloc
[`package:signals`]: {{site.pub-pkg}}/signals
[state-management documentation]: /data-and-backend/state-mgmt/intro

## Definir uma view

Uma view é um widget dentro do seu aplicativo.
Frequentemente, uma view representa uma tela em seu aplicativo que
tem sua própria rota e inclui um [`Scaffold`][] no topo do
subárvore de widgets, como o `HomeScreen`, mas nem sempre é este o caso.

Às vezes, uma view é um único elemento de UI que
encapsula a funcionalidade que precisa ser reutilizada em todo o aplicativo.
Por exemplo, o aplicativo Compass tem uma view chamada `LogoutButton`,
que pode ser colocada em qualquer lugar na árvore de widgets em que um usuário possa
esperar encontrar um botão de logout.
A view `LogoutButton` tem seu próprio view model chamado `LogoutViewModel`.
E em telas maiores, pode haver várias views na tela que
ocupariam a tela inteira no celular.

:::note
"View" é um termo abstrato e uma view não é igual a um widget.
Os widgets são componíveis e vários podem ser combinados para criar uma view.
Portanto, os view models não têm uma relação um-para-um com widgets,
mas sim uma relação um-para-um com uma *coleção* de widgets.
:::

Os widgets dentro de uma view têm três responsabilidades:

*   Eles exibem as propriedades de dados do view model.
*   Eles ouvem as atualizações do view model e renderizam novamente quando novos dados estão disponíveis.
*   Eles anexam callbacks do view model a manipuladores de eventos, se aplicável.

![Um diagrama mostrando a relação de uma view com um view model.](/assets/images/docs/app-architecture/guide/feature-architecture-simplified-View-highlighted.png)

Continuando o exemplo do recurso Home,
o código a seguir mostra a definição da view `HomeScreen`.

```dart title=home_screen.dart
class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key, required this.viewModel});

  final HomeViewModel viewModel;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      // ...
    );
  }
}
```

Na maioria das vezes, as únicas entradas de uma view devem ser uma `key`,
que todos os widgets Flutter recebem como um argumento opcional,
e o view model correspondente da view.

### Exibir dados da UI em uma view

Uma view depende de um view model para seu estado. No aplicativo Compass,
o view model é passado como um argumento no construtor da view.
O seguinte trecho de código de exemplo é do widget `HomeScreen`.

```dart title=home_screen.dart
class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key, [!required this.viewModel!]});

  [!final HomeViewModel viewModel;!]

  @override
  Widget build(BuildContext context) {
    // ...
  }
}
```

Dentro do widget, você pode acessar as reservas passadas do `viewModel`.
No código a seguir,
a propriedade `booking` está sendo fornecida a um sub-widget.

```dart title=home_screen.dart
@override
  Widget build(BuildContext context) {
    return Scaffold(
      // Algum código foi removido para brevidade.
      body: SafeArea(
        child: ListenableBuilder(
          listenable: viewModel,
          builder: (context, _) {
            return CustomScrollView(
              slivers: [
                SliverToBoxAdapter(...),
                SliverList.builder(
                   itemCount: [!viewModel.bookings.length!],
                    itemBuilder: (_, index) => _Booking(
                      key: ValueKey([!viewModel.bookings[index].id!]),
                      booking:viewModel.bookings[index],
                      onTap: () => context.push(Routes.bookingWithId(
                         viewModel.bookings[index].id)),
                      onDismissed: (_) => viewModel.deleteBooking.execute(
                           viewModel.bookings[index].id,
                         ),
                    ),
                ),
              ],
            );
          },
        ),
      ),
```

### Atualizar a UI

O widget `HomeScreen` escuta as atualizações do view model com
o widget [`ListenableBuilder`][].
Tudo na subárvore de widgets sob o widget `ListenableBuilder`
é renderizado novamente quando o [`Listenable`][] fornecido muda.
Neste caso, o `Listenable` fornecido é o view model.
Lembre-se de que o view model é do tipo [`ChangeNotifier`][]
que é um subtipo do tipo `Listenable`.

```dart title=home_screen.dart
@override
Widget build(BuildContext context) {
  return Scaffold(
    // Algum código foi removido para brevidade.
      body: SafeArea(
        child: ListenableBuilder(
          listenable: viewModel,
          builder: (context, _) {
            return CustomScrollView(
              slivers: [
                SliverToBoxAdapter(),
                SliverList.builder(
                  itemCount: viewModel.bookings.length,
                  itemBuilder: (_, index) =>
                      _Booking(
                        key: ValueKey(viewModel.bookings[index].id),
                        booking: viewModel.bookings[index],
                        onTap: () =>
                            context.push(Routes.bookingWithId(
                                viewModel.bookings[index].id)
                            ),
                        onDismissed: (_) =>
                            viewModel.deleteBooking.execute(
                              viewModel.bookings[index].id,
                            ),
                      ),
                ),
              ],
            );
          }
        )
      )
  );
}
```

### Tratamento de eventos do usuário

Finalmente, uma view precisa ouvir *eventos* dos usuários,
para que o view model possa lidar com esses eventos.
Isso é conseguido expondo um método de callback na classe view model que
encapsula toda a lógica.

![Um diagrama mostrando a relação de uma view com um view model.](/assets/images/docs/app-architecture/guide/feature-architecture-simplified-UI-highlighted.png)

Na `HomeScreen`, os usuários podem excluir eventos reservados anteriormente deslizando
um widget [`Dismissible`][].

Lembre-se deste código do trecho anterior:

<CodePreview direction="row">
  <DashImage
    image="app-architecture/case-study/dismissible.webp"
    alt="Um clipe que demonstra a funcionalidade 'dismissible' do aplicativo Compass."
    img-style="max-height: 480px; border-radius: 12px; border: black 2px solid;"
    />

  ```dart title=home_screen.dart highlightLines=9-10
  SliverList.builder(
    itemCount: widget.viewModel.bookings.length,
    itemBuilder: (_, index) => _Booking(
      key: ValueKey(viewModel.bookings[index].id),
      booking: viewModel.bookings[index],
      onTap: () => context.push(
        Routes.bookingWithId(viewModel.bookings[index].id)
      ),
      onDismissed: (_) =>
        viewModel.deleteBooking.execute(widget.viewModel.bookings[index].id),
    ),
  ),
  ```
</CodePreview>

Na `HomeScreen`, a viagem salva de um usuário é representada por
o widget `_Booking`. Quando um `_Booking` é dispensado,
o método `viewModel.deleteBooking` é executado.

Uma reserva salva é um estado de aplicativo que persiste além
de uma sessão ou da vida útil de uma view,
e apenas os repositórios devem modificar esse estado do aplicativo.
Portanto, o método `HomeViewModel.deleteBooking` se transforma e
chama um método exposto por um repositório na camada de dados,
conforme mostrado no seguinte trecho de código.

```dart title=home_viewmodel.dart highlightLines=3
Future<Result<void>> _deleteBooking(int id) async {
  try {
    final resultDelete = await _bookingRepository.delete(id);
    switch (resultDelete) {
      case Ok<void>():
        _log.fine('Deleted booking $id');
      case Error<void>():
        _log.warning('Failed to delete booking $id', resultDelete.error);
        return resultDelete;
    }

    // Algum código foi omitido para brevidade.
    // final  resultLoadBookings = ...;

    return resultLoadBookings;
  } finally {
    notifyListeners();
  }
}
```

No aplicativo Compass,
esses métodos que tratam de eventos do usuário são chamados **comandos**.

### Objetos de comando

Os comandos são responsáveis ​​pela interação que começa na camada de UI e
flui de volta para a camada de dados. Neste aplicativo especificamente,
um `Command` também é um tipo que ajuda a atualizar a UI com segurança,
independentemente do tempo de resposta ou do conteúdo.

A classe `Command` envolve um método e
ajuda a lidar com os diferentes estados desse método,
como `running`, `complete` e `error`.
Esses estados facilitam a exibição de uma UI diferente,
como indicadores de carregamento quando `Command.running` é true.

A seguir está o código da classe `Command`.
Algum código foi omitido para fins de demonstração.

```dart title=command.dart
abstract class Command<T> extends ChangeNotifier {
  Command();
  bool running = false;
  Result<T>? _result;

  /// true se a ação for concluída com erro
  bool get error => _result is Error;

  /// true se a ação for concluída com sucesso
  bool get completed => _result is Ok;

  /// Implementação interna de execução
  Future<void> _execute(action) async {
    if (_running) return;

    // Emitir estado em execução - por exemplo, o botão mostra o estado de carregamento
    _running = true;
    _result = null;
    notifyListeners();

    try {
      _result = await action();
    } finally {
      _running = false;
      notifyListeners();
    }
  }
}
```

A própria classe `Command` estende `ChangeNotifier`,
e dentro do método `Command.execute`,
`notifyListeners` é chamado várias vezes.
Isso permite que a view lide com diferentes estados com muito pouca lógica,
do qual você verá um exemplo mais adiante nesta página.

Você também pode ter notado que `Command` é uma classe abstrata.
Ele é implementado por classes concretas como `Command0` `Command1`.
O inteiro no nome da classe se refere a
o número de argumentos que o método subjacente espera.
Você pode ver exemplos dessas classes de implementação no
[diretório `utils`][`utils` directory] do aplicativo Compass.

:::tip Opção de pacote
Para usar este padrão sem escrever suas próprias classes de comando,
considere usar um pacote como o [`command_it`][],
que fornece tipos de comando para encapsular ações e
acompanhar seus estados de execução, conclusão e erro.
:::

[`command_it`]: {{site.pub-pkg}}/command_it

### Garantindo que as views possam ser renderizadas antes que os dados existam

Nas classes view model, os comandos são criados no construtor.

```dart title=home_viewmodel.dart highlightLines=8-9,15-16,24-30
class HomeViewModel extends ChangeNotifier {
  HomeViewModel({
   required BookingRepository bookingRepository,
   required UserRepository userRepository,
  }) : _bookingRepository = bookingRepository,
      _userRepository = userRepository {
    // Carregar dados necessários quando esta tela for construída.
    load = Command0(_load)..execute();
    deleteBooking = Command1(_deleteBooking);
  }

  final BookingRepository _bookingRepository;
  final UserRepository _userRepository;

  late Command0 load;
  late Command1<void, int> deleteBooking;

  User? _user;
  User? get user => _user;

  List<BookingSummary> _bookings = [];
  List<BookingSummary> get bookings => _bookings;

  Future<Result> _load() async {
    // ...
  }

  Future<Result<void>> _deleteBooking(int id) async {
    // ...
  }

  // ...
}
```

O método `Command.execute` é assíncrono,
então ele não pode garantir que os dados estarão disponíveis quando
a view quer renderizar. Isso chega ao *por que* o aplicativo Compass usa `Commands`.
No método `Widget.build` da view,
o comando é usado para renderizar condicionalmente diferentes widgets.

```dart title=home_screen.dart
// ...
child: ListenableBuilder(
  listenable: [!viewModel.load!],
  builder: (context, child) {
    if ([!viewModel.load.running!]) {
      return const Center(child: CircularProgressIndicator());
    }

    if ([!viewModel.load.error!]) {
      return ErrorIndicator(
        title: AppLocalization.of(context).errorWhileLoadingHome,
        label: AppLocalization.of(context).tryAgain,
          onPressed: viewModel.load.execute,
        );
     }

    // O comando foi concluído sem erro.
    // Retornar o widget de view principal.
    return child!;
  },
),

// ...
```

Como o comando `load` é uma propriedade que existe em
o view model em vez de algo efêmero,
não importa quando o método `load` é chamado ou quando ele é resolvido.
Por exemplo, se o comando de carregamento for resolvido antes
que o widget `HomeScreen` fosse criado,
não é um problema porque o objeto `Command` ainda existe,
e expõe o estado correto.

Este padrão padroniza como os problemas comuns de UI são resolvidos no aplicativo,
tornando sua base de código menos propensa a erros e mais escalável,
mas não é um padrão que todos os aplicativos desejam implementar.
Se você deseja usá-lo depende muito de
outras escolhas arquitetônicas que você faz.
Muitas bibliotecas que ajudam você a gerenciar o estado têm
suas próprias ferramentas para resolver esses problemas.
Por exemplo, se você fosse usar
[streams][] e [`StreamBuilders`][] em seu aplicativo,
as classes [`AsyncSnapshot`][] fornecidas pelo Flutter têm
essa funcionalidade integrada.

:::note Exemplo do mundo real
Ao construir o aplicativo Compass, encontramos um bug que foi resolvido usando
o padrão Command. [Leia sobre isso no GitHub][Read about it on GitHub].
:::

[UI layer]: /app-architecture/guide#ui-layer
[`View`]: /app-architecture/guide#views
[`ViewModel`]: /app-architecture/guide#view-models
[repositories]: /app-architecture/guide#repositories
[commands]: /app-architecture/guide#command-objects
[`package:freezed`]: {{site.pub-pkg}}/freezed
[`ChangeNotifier`]: {{site.api}}/flutter/foundation/ChangeNotifier-class.html
[`Listenable`]: {{site.api}}/flutter/foundation/Listenable-class.html
[`ListenableBuilder`]: {{site.api}}/flutter/widgets/ListenableBuilder-class.html
[`notifyListeners`]: {{site.api}}/flutter/foundation/ChangeNotifier/notifyListeners.html
[`Scaffold`]: {{site.material_ui}}/Scaffold-class.html
[`Dismissible`]: {{site.api}}/flutter/widgets/Dismissible-class.html
[`utils` directory]: https://github.com/flutter/samples/blob/main/compass_app/app/lib/utils/command.dart
[streams]: {{site.api}}/flutter/dart-async/Stream-class.html
[`StreamBuilders`]: {{site.api}}/flutter/widgets/StreamBuilder-class.html
[`AsyncSnapshot`]: {{site.api}}/flutter/widgets/AsyncSnapshot-class.html
[Read about it on GitHub]: https://github.com/flutter/samples/pull/2449#pullrequestreview-2328333146

## Feedback

Como esta seção do site está evoluindo,
nós [agradecemos seu feedback][welcome your feedback]!

[welcome your feedback]: https://google.qualtrics.com/jfe/form/SV_4T0XuR9Ts29acw6?page="case-study/ui-layer"

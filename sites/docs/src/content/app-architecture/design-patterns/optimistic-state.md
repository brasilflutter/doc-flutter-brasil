---
title: Estado otimista
description: "Melhore a percepção de capacidade de resposta de um aplicativo implementando o estado otimista."
contentTags:
  - user experience
  - asynchronous dart
iconPath: /assets/images/docs/app-architecture/design-patterns/optimistic-state-icon.svg
order: 0
ia-translate: true
---

<?code-excerpt path-base="app-architecture/optimistic_state"?>

Ao construir experiências de usuário,
a percepção de desempenho às vezes é tão importante quanto
o desempenho real do código.
Em geral, os usuários não gostam de esperar que uma ação termine para ver o resultado,
e qualquer coisa que leve mais do que alguns milissegundos pode ser considerada "lenta"
ou "sem resposta" da perspectiva do usuário.

Os desenvolvedores podem ajudar a mitigar essa percepção negativa
apresentando um estado de UI bem-sucedido
antes que a tarefa em segundo plano seja totalmente concluída.
Um exemplo disso seria tocar em um botão “Inscrever-se” e
vê-lo mudar para "Inscrito" instantaneamente,
mesmo que a chamada em segundo plano para a API de inscrição ainda esteja em execução.

Essa técnica é conhecida como Estado Otimista, UI Otimista ou
Experiência de Usuário Otimista.
Nesta receita,
você implementará um recurso de aplicativo usando o Estado Otimista e
seguindo as [diretrizes de arquitetura do Flutter][Flutter architecture guidelines].

## Recurso de exemplo: um botão de inscrição

Este exemplo implementa um botão de inscrição semelhante a
o que você poderia encontrar em um aplicativo de streaming de vídeo ou um boletim informativo.

<img src='/assets/images/docs/cookbook/architecture/optimistic-state.png'
class="site-mobile-screenshot" alt="Aplicativo com botão de inscrição" >

Quando o botão é tocado, o aplicativo chama uma API externa,
executando uma ação de inscrição,
por exemplo, registrando em um banco de dados que o usuário agora está
na lista de inscritos.
Para fins de demonstração, você não implementará o código de backend real,
em vez disso, você substituirá esta chamada por
uma ação falsa que simulará uma solicitação de rede.

Caso a chamada seja bem-sucedida,
o texto do botão mudará de "Inscrever-se" para "Inscrito".
A cor de fundo do botão também mudará.

Ao contrário, se a chamada falhar,
o texto do botão deverá voltar para "Inscrever-se",
e a UI deve mostrar uma mensagem de erro ao usuário,
por exemplo, usando um Snackbar.

Seguindo a ideia do Estado Otimista,
o botão deve mudar instantaneamente para "Inscrito" assim que for tocado,
e só voltar para “Inscrever-se” se a solicitação falhar.

<img src='/assets/images/docs/cookbook/architecture/optimistic-state.webp'
class="site-mobile-screenshot" alt="Animação do aplicativo com botão de inscrição" >

## Arquitetura de recursos

Comece definindo a arquitetura do recurso.
Seguindo as diretrizes de arquitetura,
crie estas classes Dart em um projeto Flutter:

- Um `StatefulWidget` chamado `SubscribeButton`
- Uma classe chamada `SubscribeButtonViewModel` estendendo `ChangeNotifier`
- Uma classe chamada `SubscriptionRepository`

<?code-excerpt "lib/starter.dart (Starter)"?>
```dart
class SubscribeButton extends StatefulWidget {
  const SubscribeButton({super.key});

  @override
  State<SubscribeButton> createState() => _SubscribeButtonState();
}

class _SubscribeButtonState extends State<SubscribeButton> {
  @override
  Widget build(BuildContext context) {
    return const Placeholder();
  }
}

class SubscribeButtonViewModel extends ChangeNotifier {}

class SubscriptionRepository {}
```

O widget `SubscribeButton` e o `SubscribeButtonViewModel` representam
a camada de apresentação desta solução.
O widget exibirá um botão
que mostrará o texto “Inscrever-se” ou “Inscrito”
dependendo do estado da inscrição.
O view model conterá o estado da inscrição.
Quando o botão for tocado,
o widget chamará o view model para realizar a ação.

O `SubscriptionRepository` implementará um método de inscrição
que lançará uma exceção quando a ação falhar.
O view model chamará este método ao realizar a ação de inscrição.

Em seguida, conecte-os adicionando o `SubscriptionRepository`
ao `SubscribeButtonViewModel`:

<?code-excerpt "lib/main.dart (ViewModelStart)" replace="/y;$/y;\n}/g"?>
```dart
class SubscribeButtonViewModel extends ChangeNotifier {
  SubscribeButtonViewModel({required this.subscriptionRepository});

  final SubscriptionRepository subscriptionRepository;
}
```

E adicione o `SubscribeButtonViewModel` ao widget `SubscribeButton`:

<?code-excerpt "lib/main.dart (Widget)"?>
```dart
class SubscribeButton extends StatefulWidget {
  const SubscribeButton({super.key, required this.viewModel});

  /// Subscribe button view model.
  final SubscribeButtonViewModel viewModel;

  @override
  State<SubscribeButton> createState() => _SubscribeButtonState();
}
```

Agora que você criou a arquitetura básica da solução,
você pode criar o widget `SubscribeButton` da seguinte maneira:

<?code-excerpt "lib/main.dart (SubscribeButton)" replace="/^child: //g;/^\),$/)/g"?>
```dart
SubscribeButton(
  viewModel: SubscribeButtonViewModel(
    subscriptionRepository: SubscriptionRepository(),
  ),
)
```
### Implemente o `SubscriptionRepository`

Adicione um novo método assíncrono chamado `subscribe()`
ao `SubscriptionRepository` com o seguinte código:

<?code-excerpt "lib/main.dart (SubscriptionRepository)"?>
```dart
class SubscriptionRepository {
  /// Simulates a network request and then fails.
  Future<void> subscribe() async {
    // Simulate a network request.
    await Future<void>.delayed(const Duration(seconds: 1));
    // Fail after one second.
    throw Exception('Failed to subscribe');
  }
}
```

A chamada para `await Future.delayed()` com uma duração de um segundo
foi adicionada para simular uma solicitação de longa duração.
A execução do método será pausada por um segundo e, em seguida, continuará sendo executada.

Para simular uma solicitação com falha,
o método de inscrição lança uma exceção no final.
Isso será usado mais tarde para mostrar como se recuperar de uma solicitação com falha
ao implementar o Estado Otimista.

### Implemente o `SubscribeButtonViewModel`

Para representar o estado da inscrição, bem como um possível estado de erro,
adicione os seguintes membros públicos ao `SubscribeButtonViewModel`:

<?code-excerpt "lib/main.dart (States)"?>
```dart
/// Whether the user is subscribed.
bool subscribed = false;

/// Whether the subscription action has failed.
bool error = false;
```

Ambos são definidos como `false` no início.

Seguindo as ideias do Estado Otimista,
o estado `subscribed` mudará para `true`
assim que o usuário tocar no botão de inscrição.
E só voltará a `false` se a ação falhar.

O estado `error` mudará para `true` quando a ação falhar,
indicando ao widget `SubscribeButton` para mostrar uma mensagem de erro ao usuário.
A variável deve voltar para `false` assim que o erro for exibido.

Em seguida, implemente um método `subscribe()` assíncrono:

<?code-excerpt "lib/main.dart (subscribe)"?>
```dart
// Subscription action
Future<void> subscribe() async {
  // Ignore taps when subscribed.
  if (subscribed) {
    return;
  }

  // Optimistic state.
  // It will be reverted if the subscription fails.
  subscribed = true;
  // Notify listeners to update the UI.
  notifyListeners();

  try {
    await subscriptionRepository.subscribe();
  } catch (e) {
    print('Failed to subscribe: $e');
    // Revert to the previous state.
    subscribed = false;
    // Set the error state.
    error = true;
  } finally {
    notifyListeners();
  }
}
```

Conforme descrito anteriormente, primeiro o método define o estado `subscribed` como `true`
e então chama `notifyListeners()`.
Isso força a UI a atualizar e o botão altera sua aparência,
mostrando o texto "Inscrito" para o usuário.

Então, o método realiza a chamada real para o repositório.
Essa chamada é envolvida por um `try-catch`
para capturar quaisquer exceções que ele possa lançar.
Caso uma exceção seja capturada, o estado `subscribed` é definido de volta para `false`,
e o estado `error` é definido como `true`.
Uma chamada final para `notifyListeners()` é feita
para mudar a UI de volta para 'Inscrever-se'.

Se não houver exceção, o processo estará concluído
porque a UI já está refletindo o estado de sucesso.

O `SubscribeButtonViewModel` completo deve ser assim:

<?code-excerpt "lib/main.dart (ViewModelFull)"?>
```dart
/// Subscribe button view model.
/// Handles the subscribe action and exposes the state to the subscription.
class SubscribeButtonViewModel extends ChangeNotifier {
  SubscribeButtonViewModel({required this.subscriptionRepository});

  final SubscriptionRepository subscriptionRepository;

  /// Whether the user is subscribed.
  bool subscribed = false;

  /// Whether the subscription action has failed.
  bool error = false;

  // Subscription action
  Future<void> subscribe() async {
    // Ignore taps when subscribed.
    if (subscribed) {
      return;
    }

    // Optimistic state.
    // It will be reverted if the subscription fails.
    subscribed = true;
    // Notify listeners to update the UI.
    notifyListeners();

    try {
      await subscriptionRepository.subscribe();
    } catch (e) {
      print('Failed to subscribe: $e');
      // Revert to the previous state.
      subscribed = false;
      // Set the error state.
      error = true;
    } finally {
      notifyListeners();
    }
  }
}
```

### Implemente o `SubscribeButton`

Nesta etapa,
você primeiro implementará o método build do `SubscribeButton`,
e então implementará o tratamento de erros do recurso.

Adicione o seguinte código ao método build:

<?code-excerpt "lib/main.dart (build)"?>
```dart
@override
Widget build(BuildContext context) {
  return ListenableBuilder(
    listenable: widget.viewModel,
    builder: (context, _) {
      return FilledButton(
        onPressed: widget.viewModel.subscribe,
        style: widget.viewModel.subscribed
            ? SubscribeButtonStyle.subscribed
            : SubscribeButtonStyle.unsubscribed,
        child: widget.viewModel.subscribed
            ? const Text('Subscribed')
            : const Text('Subscribe'),
      );
    },
  );
}
```

Este método build contém um `ListenableBuilder`
que ouve as mudanças do view model.
O builder então cria um `FilledButton`
que exibirá o texto "Inscrito" ou "Inscrever-se"
dependendo do estado do view model.
O estilo do botão também mudará dependendo desse estado.
Além disso, quando o botão é tocado,
ele executa o método `subscribe()` do view model.

O `SubscribeButtonStyle` pode ser encontrado aqui.
Adicione esta classe ao lado do `SubscribeButton`.
Sinta-se à vontade para modificar o `ButtonStyle`.

<?code-excerpt "lib/main.dart (style)"?>
```dart
class SubscribeButtonStyle {
  static const unsubscribed = ButtonStyle(
    backgroundColor: WidgetStatePropertyAll(Colors.red),
  );

  static const subscribed = ButtonStyle(
    backgroundColor: WidgetStatePropertyAll(Colors.green),
  );
}
```

Se você executar o aplicativo agora,
você verá como o botão muda quando você o pressiona,
no entanto, ele voltará ao estado original sem mostrar um erro.

### Tratamento de erros

Para tratar erros,
adicione os métodos `initState()` e `dispose()` ao `SubscribeButtonState`,
e então adicione o método `_onViewModelChange()`.

<?code-excerpt "lib/main.dart (listener1)"?>
```dart
@override
void initState() {
  super.initState();
  widget.viewModel.addListener(_onViewModelChange);
}

@override
void dispose() {
  widget.viewModel.removeListener(_onViewModelChange);
  super.dispose();
}
```

<?code-excerpt "lib/main.dart (listener2)"?>
```dart
/// Listen to ViewModel changes.
void _onViewModelChange() {
  // If the subscription action has failed.
  if (widget.viewModel.error) {
    // Reset the error state.
    widget.viewModel.error = false;
    // Show an error message.
    ScaffoldMessenger.of(context)
        .showSnackBar(const SnackBar(content: Text('Failed to subscribe')));
  }
}
```

A chamada `addListener()` registra o método `_onViewModelChange()`
para ser chamado quando o view model notificar os listeners.
É importante chamar `removeListener()` quando o widget é descartado,
para evitar erros.

O método `_onViewModelChange()` verifica o estado `error` e,
se for `true`,
exibe um `Snackbar` para o usuário mostrando uma mensagem de erro.
Além disso, o estado `error` é definido de volta para `false`,
para evitar exibir a mensagem de erro várias vezes
se `notifyListeners()` for chamado novamente no view model.

## Estado otimista avançado

Neste tutorial,
você aprendeu como implementar um Estado Otimista com um único estado binário,
mas você pode usar esta técnica para criar uma solução mais avançada
incorporando um terceiro estado temporal
que indica que a ação ainda está em execução.

Por exemplo, em um aplicativo de bate-papo, quando o usuário envia uma nova mensagem,
o aplicativo exibirá a nova mensagem de bate-papo na janela de bate-papo,
mas com um ícone indicando que a mensagem ainda está pendente para ser entregue.
Quando a mensagem for entregue, esse ícone seria removido.

No exemplo do botão de inscrição,
você pode adicionar outro flag no view model
indicando que o método `subscribe()` ainda está em execução,
ou use o estado em execução do padrão Command,
em seguida, modifique ligeiramente o estilo do botão para mostrar que a operação está em execução.

## Exemplo interativo

Este exemplo mostra o widget `SubscribeButton`
junto com o `SubscribeButtonViewModel`
e `SubscriptionRepository`,
que implementam uma ação de toque de inscrição com Estado Otimista.

Quando você toca no botão,
o texto do botão muda de “Inscrever-se” para “Inscrito”. Depois de um segundo,
o repositório lança uma exceção,
que é capturada pelo view model,
e o botão volta a exibir "Inscrever-se",
enquanto também exibe um Snackbar com uma mensagem de erro.

<?code-excerpt "lib/main.dart"?>
```dartpad title="Flutter Optimistic State example in DartPad" run="true"
// ignore_for_file: avoid_print

import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        body: Center(
          child: SubscribeButton(
            viewModel: SubscribeButtonViewModel(
              subscriptionRepository: SubscriptionRepository(),
            ),
          ),
        ),
      ),
    );
  }
}

/// A button that simulates a subscription action.
/// For example, subscribing to a newsletter or a streaming channel.
class SubscribeButton extends StatefulWidget {
  const SubscribeButton({super.key, required this.viewModel});

  /// Subscribe button view model.
  final SubscribeButtonViewModel viewModel;

  @override
  State<SubscribeButton> createState() => _SubscribeButtonState();
}

class _SubscribeButtonState extends State<SubscribeButton> {
  @override
  void initState() {
    super.initState();
    widget.viewModel.addListener(_onViewModelChange);
  }

  @override
  void dispose() {
    widget.viewModel.removeListener(_onViewModelChange);
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return ListenableBuilder(
      listenable: widget.viewModel,
      builder: (context, _) {
        return FilledButton(
          onPressed: widget.viewModel.subscribe,
          style: widget.viewModel.subscribed
              ? SubscribeButtonStyle.subscribed
              : SubscribeButtonStyle.unsubscribed,
          child: widget.viewModel.subscribed
              ? const Text('Subscribed')
              : const Text('Subscribe'),
        );
      },
    );
  }

  /// Listen to ViewModel changes.
  void _onViewModelChange() {
    // If the subscription action has failed.
    if (widget.viewModel.error) {
      // Reset the error state.
      widget.viewModel.error = false;
      // Show an error message.
      ScaffoldMessenger.of(context)
          .showSnackBar(const SnackBar(content: Text('Failed to subscribe')));
    }
  }
}

class SubscribeButtonStyle {
  static const unsubscribed = ButtonStyle(
    backgroundColor: WidgetStatePropertyAll(Colors.red),
  );

  static const subscribed = ButtonStyle(
    backgroundColor: WidgetStatePropertyAll(Colors.green),
  );
}

/// Subscribe button view model.
/// Handles the subscribe action and exposes the state to the subscription.
class SubscribeButtonViewModel extends ChangeNotifier {
  SubscribeButtonViewModel({required this.subscriptionRepository});

  final SubscriptionRepository subscriptionRepository;

  /// Whether the user is subscribed.
  bool subscribed = false;

  /// Whether the subscription action has failed.
  bool error = false;

  // Subscription action
  Future<void> subscribe() async {
    // Ignore taps when subscribed.
    if (subscribed) {
      return;
    }

    // Optimistic state.
    // It will be reverted if the subscription fails.
    subscribed = true;
    // Notify listeners to update the UI.
    notifyListeners();

    try {
      await subscriptionRepository.subscribe();
    } catch (e) {
      print('Failed to subscribe: $e');
      // Revert to the previous state.
      subscribed = false;
      // Set the error state.
      error = true;
    } finally {
      notifyListeners();
    }
  }
}

/// Repository of subscriptions.
class SubscriptionRepository {
  /// Simulates a network request and then fails.
  Future<void> subscribe() async {
    // Simulate a network request.
    await Future<void>.delayed(const Duration(seconds: 1));
    // Fail after one second.
    throw Exception('Failed to subscribe');
  }
}
```

[Flutter Architecture guidelines]:/app-architecture

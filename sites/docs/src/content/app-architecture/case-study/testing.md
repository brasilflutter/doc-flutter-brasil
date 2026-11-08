---
title: Testando cada camada
shortTitle: Testando
description: >-
  Como testar um aplicativo que implementa a arquitetura MVVM.
prev:
  title: Injeção de dependência
  path: /app-architecture/case-study/dependency-injection
ia-translate: true
---

## Testando a camada de UI {:#testing-the-ui-layer}

Uma maneira de determinar se sua arquitetura é sólida é
considerar o quão fácil (ou difícil) o aplicativo é de testar.
Como os view models e as views têm entradas bem definidas,
suas dependências podem ser facilmente simuladas ou falsificadas,
e os testes unitários são facilmente escritos.

### Testes unitários de ViewModel {:#viewmodel-unit-tests}

Para testar a lógica da UI do view model, você deve escrever testes unitários que
não dependam de bibliotecas Flutter ou frameworks de teste.

Repositórios são as únicas dependências de um view model
(a menos que você esteja implementando [use-cases][]),
e escrever `mocks` ou `fakes` do repositório é
a única configuração que você precisa fazer.
Neste teste de exemplo, um fake chamado `FakeBookingRepository` é usado.

```dart title=home_screen_test.dart
void main() {
  group('HomeViewModel tests', () {
    test('Load bookings', () {
      // HomeViewModel._load is called in the constructor of HomeViewModel.
      final viewModel = HomeViewModel(
        bookingRepository: FakeBookingRepository()
          ..createBooking(kBooking),
        userRepository: FakeUserRepository(),
      );

      expect(viewModel.bookings.isNotEmpty, true);
    });
  });
}
```

A classe [`FakeBookingRepository`][] implementa [`BookingRepository`][].
Na [seção da camada de dados][data layer section] deste estudo de caso,
a classe `BookingRepository` é explicada detalhadamente.

```dart title=fake_booking_repository.dart
class FakeBookingRepository implements BookingRepository {
  List<Booking> bookings = List.empty(growable: true);

  @override
  Future<Result<void>> createBooking(Booking booking) async {
    bookings.add(booking);
    return Result.ok(null);
  }
  // ...
}
```

:::note
Se você estiver usando esta arquitetura com [use-cases][], estes também
precisariam ser falsificados da mesma forma.
:::

### Testes de widget da View {:#view-widget-tests}

Depois de escrever testes para seu view model,
você já criou os fakes que precisa para escrever testes de widget também.
O exemplo a seguir mostra como os testes de widget `HomeScreen`
são configurados usando o `HomeViewModel` e os repositórios necessários:

```dart title=home_screen_test.dart
void main() {
  group('HomeScreen tests', () {
    late HomeViewModel viewModel;
    late MockGoRouter goRouter;
    late FakeBookingRepository bookingRepository;

    setUp(() {
      bookingRepository = FakeBookingRepository()
        ..createBooking(kBooking);
      viewModel = HomeViewModel(
        bookingRepository: bookingRepository,
        userRepository: FakeUserRepository(),
      );
      goRouter = MockGoRouter();
      when(() => goRouter.push(any())).thenAnswer((_) => Future.value(null));
    });

    // ...
  });
}
```

Esta configuração cria os dois repositórios fake necessários
e os passa para um objeto `HomeViewModel`.
Esta classe não precisa ser falsificada.

:::note
O código também define um `MockGoRouter`.
O roteador é simulado usando [`package:mocktail`][],
e está fora do escopo deste estudo de caso.
Você pode encontrar orientação geral de testes na [documentação de testes do Flutter][Flutter's testing documentation].
:::

Depois que o view model e suas dependências são definidos,
a árvore de widgets que será testada precisa ser criada.
Nos testes para `HomeScreen`, um método `loadWidget` é definido.

```dart title=home_screen_test.dart highlightLines=11-23
void main() {
  group('HomeScreen tests', () {
    late HomeViewModel viewModel;
    late MockGoRouter goRouter;
    late FakeBookingRepository bookingRepository;

    setUp(
      // ...
    );

    void loadWidget(WidgetTester tester) async {
      await testApp(
        tester,
        ChangeNotifierProvider.value(
          value: FakeAuthRepository() as AuthRepository,
          child: Provider.value(
            value: FakeItineraryConfigRepository() as ItineraryConfigRepository,
            child: HomeScreen(viewModel: viewModel),
          ),
        ),
        goRouter: goRouter,
      );
    }

    // ...
  });
}
```

Este método se transforma e chama `testApp`,
um método generalizado usado para todos os testes de widget no aplicativo compass.
Ele se parece com isto:

```dart title=testing/app.dart
void testApp(
  WidgetTester tester,
  Widget body, {
  GoRouter? goRouter,
}) async {
  tester.view.devicePixelRatio = 1.0;
  await tester.binding.setSurfaceSize(const Size(1200, 800));
  await mockNetworkImages(() async {
    await tester.pumpWidget(
      MaterialApp(
        localizationsDelegates: [
          GlobalWidgetsLocalizations.delegate,
          GlobalMaterialLocalizations.delegate,
          AppLocalizationDelegate(),
        ],
        theme: AppTheme.lightTheme,
        home: InheritedGoRouter(
          goRouter: goRouter ?? MockGoRouter(),
          child: Scaffold(
            body: body,
          ),
        ),
      ),
    );
  });
}
```

O único trabalho desta função é criar uma árvore de widgets que possa ser testada.

O método `loadWidget` passa as partes exclusivas de uma árvore de widgets para teste.
Neste caso, isso inclui o `HomeScreen` e seu view model,
bem como alguns repositórios falsificados adicionais que
estão mais acima na árvore de widgets.

A coisa mais importante a se notar é que os testes de view e view model
só exigem simulação de repositórios se sua arquitetura for sólida.

## Testando a camada de dados {:#testing-the-data-layer}

Semelhante à camada de UI, os componentes da camada de dados têm
entradas e saídas bem definidas, tornando ambos os lados falsificáveis.
Para escrever testes unitários para qualquer repositório,
simule os serviços dos quais ele depende.
O exemplo a seguir mostra um teste unitário para o `BookingRepository`.

```dart title=booking_repository_remote_test.dart
void main() {
  group('BookingRepositoryRemote tests', () {
    late BookingRepository bookingRepository;
    late FakeApiClient fakeApiClient;

    setUp(() {
      fakeApiClient = FakeApiClient();
      bookingRepository = BookingRepositoryRemote(
        apiClient: fakeApiClient,
      );
    });

    test('should get booking', () async {
      final result = await bookingRepository.getBooking(0);
      final booking = result.asOk.value;
      expect(booking, kBooking);
    });
  });
}
```

Para saber mais sobre como escrever mocks e fakes,
confira exemplos no [diretório `testing` do aplicativo Compass][Compass App `testing` directory] ou
leia a [documentação de testes do Flutter][Flutter's testing documentation].

[use-cases]: /app-architecture/guide#optional-domain-layer
[`FakeBookingRepository`]: https://github.com/flutter/samples/blob/main/compass_app/app/testing/fakes/repositories/fake_booking_repository.dart
[`BookingRepository`]: https://github.com/flutter/samples/tree/main/compass_app/app/lib/data/repositories/booking
[data layer section]: /app-architecture/case-study/data-layer
[`package:mocktail`]: {{site.pub-pkg}}/mocktail
[Flutter's testing documentation]: /testing/overview
[Compass App `testing` directory]: https://github.com/flutter/samples/tree/main/compass_app/app/testing

## Feedback

Como esta seção do site está evoluindo,
nós [agradecemos seu feedback][welcome your feedback]!

[welcome your feedback]: https://google.qualtrics.com/jfe/form/SV_4T0XuR9Ts29acw6?page="case-study/testing"

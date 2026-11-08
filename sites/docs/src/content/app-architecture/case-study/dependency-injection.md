---
title: Comunicação entre camadas
shortTitle: Injeção de dependência
description: >-
  Como implementar a injeção de dependência para comunicar entre as camadas MVVM.
prev:
  title: Camada de dados
  path: /app-architecture/case-study/data-layer
next:
  title: Testando
  path: /app-architecture/case-study/testing
ia-translate: true
---

Além de definir responsabilidades claras para cada componente da arquitetura,
é importante considerar como os componentes se comunicam.
Isso se refere tanto às regras que ditam a comunicação,
quanto à implementação técnica de como os componentes se comunicam.
A arquitetura de um aplicativo deve responder às seguintes perguntas:

* Quais componentes têm permissão para se comunicar com quais outros componentes
  (incluindo componentes do mesmo tipo)?
* O que esses componentes expõem como saída uns para os outros?
* Como qualquer camada é 'conectada' a outra camada?

![Um diagrama mostrando os componentes da arquitetura do aplicativo.](/assets/images/docs/app-architecture/guide/feature-architecture-simplified.png)

Usando este diagrama como um guia, as regras de engajamento são as seguintes:

| Componente  | Regras de engajamento                                                                                                                                                                                                                                                         |
|------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| View       | <ol><li> Uma view só tem conhecimento de exatamente um view model e nunca tem conhecimento de nenhuma outra camada ou componente. Quando criada, o Flutter passa o view model para a view como um argumento, expondo os dados do view model e os callbacks de comando para a view. </li></ol> |
| ViewModel  | <ol><li>Um ViewModel pertence a exatamente uma view, que pode ver seus dados, mas o model nunca precisa saber que uma view existe.</li><li>Um view model tem conhecimento de um ou mais repositórios, que são passados para o construtor do view model.</li></ol>         |
| Repositório | <ol><li>Um repositório pode ter conhecimento de muitos serviços, que são passados como argumentos para o construtor do repositório.</li><li>Um repositório pode ser usado por muitos view models, mas nunca precisa ter conhecimento deles.</li></ol>                                  |
| Serviço    | <ol><li>Um serviço pode ser usado por muitos repositórios, mas nunca precisa ter conhecimento de um repositório (ou qualquer outro objeto).</li></ol>                                                                                                                             |

{:.table .table-striped}

## Injeção de dependência

Este guia mostrou como esses diferentes componentes se comunicam
uns com os outros usando entradas e saídas.
Em todos os casos, a comunicação entre duas camadas é facilitada pela passagem
de um componente para os métodos construtores (dos componentes que
consomem seus dados), como um `Service` em um `Repository.`

```dart
class MyRepository {
  MyRepository({required MyService myService})
          : _myService = myService;

  late final MyService _myService;
}
```

Uma coisa que está faltando, no entanto, é a criação de objetos. Onde,
em um aplicativo, a instância `MyService` é criada para que ela possa ser
passada para `MyRepository`?
A resposta para esta pergunta envolve um
padrão conhecido como [injeção de dependência][dependency injection].

No aplicativo Compass, a *injeção de dependência* é gerenciada usando
[`package:provider`][]. Com base em sua experiência na criação de aplicativos Flutter,
as equipes do Google recomendam o uso de `package:provider` para implementar
a injeção de dependência.

Serviços e repositórios são expostos ao nível superior da árvore de widgets do
aplicativo Flutter como objetos `Provider`.

```dart title=dependencies.dart
runApp(
  MultiProvider(
    providers: [
      Provider(create: (context) => AuthApiClient()),
      Provider(create: (context) => ApiClient()),
      Provider(create: (context) => SharedPreferencesService()),
      ChangeNotifierProvider(
        create: (context) => AuthRepositoryRemote(
          authApiClient: context.read(),
          apiClient: context.read(),
          sharedPreferencesService: context.read(),
        ) as AuthRepository,
      ),
      Provider(create: (context) =>
        DestinationRepositoryRemote(
          apiClient: context.read(),
        ) as DestinationRepository,
      ),
      Provider(create: (context) =>
        ContinentRepositoryRemote(
          apiClient: context.read(),
        ) as ContinentRepository,
      ),
      // No aplicativo Compass, provedores de serviços e repositórios adicionais estão aqui.
    ],
    child: const MainApp(),
  ),
);
```

Os serviços são expostos apenas para que possam ser imediatamente
injetados em repositórios através do método `BuildContext.read` do `provider`,
conforme mostrado no snippet anterior.
Os repositórios são então expostos para que possam ser
injetados em view models conforme necessário.

Um pouco mais abaixo na árvore de widgets, os view models que correspondem a
uma tela inteira são criados na configuração [`package:go_router`][],
onde o provider é usado novamente para injetar os repositórios necessários.

```dart title=router.dart
// Este código foi modificado para fins de demonstração.
GoRouter router(
  AuthRepository authRepository,
) =>
    GoRouter(
      initialLocation: Routes.home,
      debugLogDiagnostics: true,
      redirect: _redirect,
      refreshListenable: authRepository,
      routes: [
        GoRoute(
          path: Routes.login,
          builder: (context, state) {
            return LoginScreen(
              viewModel: LoginViewModel(
                authRepository: context.read(),
              ),
            );
          },
        ),
        GoRoute(
          path: Routes.home,
          builder: (context, state) {
            final viewModel = HomeViewModel(
              bookingRepository: context.read(),
            );
            return HomeScreen(viewModel: viewModel);
          },
          routes: [
            // ...
          ],
        ),
      ],
    );
```

Dentro do view model ou repositório, o componente injetado deve ser privado.
Por exemplo, a classe `HomeViewModel` se parece com isto:

```dart title=home_viewmodel.dart
class HomeViewModel extends ChangeNotifier {
  HomeViewModel({
    required BookingRepository bookingRepository,
    required UserRepository userRepository,
  })  : _bookingRepository = bookingRepository,
        _userRepository = userRepository;

  final BookingRepository _bookingRepository;
  final UserRepository _userRepository;

  // ...
}
```

Métodos privados impedem que a view, que tem acesso ao view model,
chame métodos no repositório diretamente.

Isso conclui o passo a passo do código do aplicativo Compass. Esta página apenas passou
pelo código relacionado à arquitetura, mas não conta toda a história. A maior parte
do código de utilitários, código de widgets e estilo de UI foi ignorada. Navegue pelo código no
[repositório do aplicativo Compass][Compass app repository] para um exemplo completo
de um aplicativo Flutter robusto construído seguindo esses princípios.

[`package:provider`]: {{site.pub-pkg}}/provider
[`package:go_router`]: {{site.pub-pkg}}/go_router
[Compass app repository]: https://github.com/flutter/samples/tree/main/compass_app
[dependency injection]: https://en.wikipedia.org/wiki/Dependency_injection

## Feedback

Como esta seção do site está evoluindo,
[agradecemos seu feedback][welcome your feedback]!

[welcome your feedback]: https://google.qualtrics.com/jfe/form/SV_4T0XuR9Ts29acw6?page="case-study/dependency-injection"

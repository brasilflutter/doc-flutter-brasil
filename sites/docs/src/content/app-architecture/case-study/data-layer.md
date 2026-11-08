---
title: Camada de dados
shortTitle: Camada de dados
description: >-
  Um passo a passo da camada de dados de um aplicativo que implementa a arquitetura MVVM.
prev:
  title: Camada de UI
  path: /app-architecture/case-study/ui-layer
next:
  title: Injeção de Dependência
  path: /app-architecture/case-study/dependency-injection
ia-translate: true
---

A camada de dados de um aplicativo, conhecida como *modelo* na terminologia MVVM,
é a fonte da verdade para todos os dados do aplicativo.
Como a fonte da verdade,
é o único lugar onde os dados do aplicativo devem ser atualizados.

Ela é responsável por consumir dados de várias APIs externas,
expondo esses dados para a UI,
tratando eventos da UI que requerem que os dados sejam atualizados,
e enviando solicitações de atualização para essas APIs externas conforme necessário.

A camada de dados neste guia possui dois componentes principais,
[repositórios][repositories] e [serviços][services].

![Um diagrama que destaca os componentes da camada de dados de um aplicativo.](/assets/images/docs/app-architecture/guide/feature-architecture-simplified-Data-highlighted.png)

* **Repositórios** são a fonte da verdade para os dados do aplicativo e contêm
  lógica relacionada a esses dados, como atualizar os dados em resposta a novos
  eventos do usuário ou consultar dados de serviços. Os repositórios são responsáveis
  por sincronizar os dados quando recursos offline são suportados, gerenciar
  a lógica de repetição e o armazenamento em cache de dados.
* **Serviços** são classes Dart sem estado que interagem com APIs, como
  servidores HTTP e plugins de plataforma. Quaisquer dados que seu aplicativo precise que não sejam
  criados dentro do próprio código do aplicativo devem ser obtidos de dentro das
  classes de serviço.

## Definir um serviço {:#define-a-service}

Uma classe de serviço é a menos ambígua de todos os componentes da arquitetura.
Ela não tem estado e suas funções não têm efeitos colaterais.
Seu único trabalho é envolver uma API externa.
Geralmente há uma classe de serviço por fonte de dados,
como um servidor HTTP cliente ou um plugin de plataforma.

![Um diagrama que mostra as entradas e saídas de objetos de serviço.](/assets/images/docs/app-architecture/case-study/mvvm-case-study-services-architecture.png)

No aplicativo Compass, por exemplo, há um serviço [`APIClient`][] que
manipula as chamadas CRUD para o servidor voltado para o cliente.

```dart title=api_client.dart
class ApiClient {
  // Some code omitted for demo purposes.

  Future<Result<List<ContinentApiModel>>> getContinents() async { /* ... */ }

  Future<Result<List<DestinationApiModel>>> getDestinations() async { /* ... */ }

  Future<Result<List<ActivityApiModel>>> getActivityByDestination(String ref) async { /* ... */ }

  Future<Result<List<BookingApiModel>>> getBookings() async { /* ... */ }

  Future<Result<BookingApiModel>> getBooking(int id) async { /* ... */ }

  Future<Result<BookingApiModel>> postBooking(BookingApiModel booking) async { /* ... */ }

  Future<Result<void>> deleteBooking(int id) async { /* ... */ }

  Future<Result<UserApiModel>> getUser() async { /* ... */ }
}
```

O próprio serviço é uma classe,
onde cada método envolve um endpoint de API diferente e
expõe objetos de resposta assíncronos.
Continuando o exemplo anterior de exclusão de uma reserva salva,
o método `deleteBooking` retorna um `Future<Result<void>>`.

:::note
Alguns métodos retornam classes de dados que são
especificamente para dados brutos da API,
como a classe `BookingApiModel`.
Como você verá em breve, os repositórios extraem dados e
os expõem em um formato diferente.
:::

## Definir um repositório {:#define-a-repository}

A única responsabilidade de um repositório é gerenciar os dados do aplicativo.
Um repositório é a fonte da verdade para um único tipo de dados de aplicativo,
e deve ser o único lugar onde esse tipo de dados é alterado.
O repositório é responsável por consultar novos dados de fontes externas,
gerenciar a lógica de repetição, gerenciar dados em cache
e transformar dados brutos em modelos de domínio.

![Um diagrama que destaca o componente do repositório de um aplicativo.](/assets/images/docs/app-architecture/guide/feature-architecture-simplified-Repository-highlighted.png)

Você deve ter um repositório separado para
cada tipo diferente de dados em seu aplicativo.
Por exemplo, o aplicativo Compass possui repositórios chamados `UserRepository`,
`BookingRepository`, `AuthRepository`, `DestinationRepository` e mais.

O exemplo a seguir é o `BookingRepository` do aplicativo Compass,
e mostra a estrutura básica de um repositório.

```dart title=booking_repository_remote.dart
class BookingRepositoryRemote implements BookingRepository {
  BookingRepositoryRemote({
    required ApiClient apiClient,
  }) : _apiClient = apiClient;

  final ApiClient _apiClient;
  List<Destination>? _cachedDestinations;

  Future<Result<void>> createBooking(Booking booking) async {...}
  Future<Result<Booking>> getBooking(int id) async {...}
  Future<Result<List<BookingSummary>>> getBookingsList() async {...}
  Future<Result<void>> delete(int id) async {...}
}
```

:::note Ambientes de desenvolvimento versus teste
A classe no exemplo anterior é `BookingRepositoryRemote`,
que estende uma classe abstrata chamada `BookingRepository`.
Esta classe base é usada para criar repositórios para diferentes ambientes.
Por exemplo, o aplicativo Compass também possui uma classe chamada `BookingRepositoryLocal`,
que é usada para desenvolvimento local.

Você pode ver as diferenças entre as
classes [`BookingRepository` no GitHub][`BookingRepository` classes on GitHub].
:::

O `BookingRepository` recebe o serviço `ApiClient` como entrada,
que ele usa para obter e atualizar os dados brutos do servidor.
É importante que o serviço seja um membro privado,
para que a camada de UI não possa ignorar o repositório e chamar um serviço diretamente.

Com o serviço `ApiClient`,
o repositório pode consultar atualizações para as reservas salvas de um usuário que
podem ocorrer no servidor, e fazer solicitações `POST` para excluir reservas salvas.

Os dados brutos que um repositório transforma em modelos de aplicativo podem vir de
várias fontes e vários serviços,
e, portanto, repositórios e serviços têm uma relação de muitos para muitos.
Um serviço pode ser usado por qualquer número de repositórios,
e um repositório pode usar mais de um serviço.

![Um diagrama que destaca os componentes da camada de dados de um aplicativo.](/assets/images/docs/app-architecture/guide/feature-architecture-simplified-Data-highlighted.png)

### Modelos de domínio {:#domain-models}

O `BookingRepository` gera objetos `Booking` e `BookingSummary`,
que são *modelos de domínio*.
Todos os repositórios geram modelos de domínio correspondentes.
Esses modelos de dados diferem dos modelos de API porque eles contêm apenas os dados
necessários para o resto do aplicativo.
Os modelos de API contêm dados brutos que muitas vezes precisam ser filtrados,
combinados ou excluídos para serem úteis para os view models do aplicativo.
O repositório refina os dados brutos e os gera como modelos de domínio.

No aplicativo de exemplo, os modelos de domínio são expostos por meio de
valores de retorno em métodos como `BookingRepository.getBooking`.
O método `getBooking` é responsável por obter os dados brutos do
serviço `ApiClient` e transformá-los em um objeto `Booking`.
Ele faz isso combinando dados de vários endpoints de serviço.

```dart title=booking_repository_remote.dart highlightLines=14-21
// This method was edited for brevity.
Future<Result<Booking>> getBooking(int id) async {
  try {
    // Get the booking by ID from server.
    final resultBooking = await _apiClient.getBooking(id);
    if (resultBooking is Error<BookingApiModel>) {
      return Result.error(resultBooking.error);
    }
    final booking = resultBooking.asOk.value;

    final destination = _apiClient.getDestination(booking.destinationRef);
    final activities = _apiClient.getActivitiesForBooking(
            booking.activitiesRef);

    return Result.ok(
      Booking(
        startDate: booking.startDate,
        endDate: booking.endDate,
        destination: destination,
        activity: activities,
      ),
    );
  } on Exception catch (e) {
    return Result.error(e);
  }
}
```

:::note
No aplicativo Compass, as classes de serviço retornam objetos `Result`.
`Result` é uma classe de utilitário que envolve chamadas assíncronas e
facilita o tratamento de erros e o gerenciamento do estado da UI que depende
de chamadas assíncronas.

Este padrão é uma recomendação, mas não um requisito.
A arquitetura recomendada neste guia pode ser implementada sem ele.

Você pode aprender sobre esta classe na [receita do cookbook Result][Result cookbook recipe].
:::

### Concluir o ciclo de eventos {:#complete-the-event-cycle}

Ao longo desta página, você viu como um usuário pode excluir uma reserva salva,
começando com um evento—um usuário deslizando em um widget `Dismissible`.
O view model trata esse evento delegando
a mutação real dos dados para o `BookingRepository`.
O snippet a seguir mostra o método `BookingRepository.deleteBooking`.

```dart title=booking_repository_remote.dart
Future<Result<void>> delete(int id) async {
  try {
    return _apiClient.deleteBooking(id);
  } on Exception catch (e) {
    return Result.error(e);
  }
}
```

O repositório envia uma solicitação `POST` para o cliente da API com
o método `_apiClient.deleteBooking` e retorna um `Result`.
O `HomeViewModel` consome o `Result` e os dados que ele contém
e, por fim, chama `notifyListeners`, concluindo o ciclo.

[repositories]: /app-architecture/guide#repositories
[services]:  /app-architecture/guide#services
[`APIClient`]: https://github.com/flutter/samples/blob/main/compass_app/app/lib/data/services/api/api_client.dart
[`sealed`]: {{site.dart-site}}/language/class-modifiers#sealed
[`BookingRepository` classes on GitHub]: https://github.com/flutter/samples/tree/main/compass_app/app/lib/data/repositories/booking
[Result cookbook recipe]: /app-architecture/design-patterns/result

## Feedback

Como esta seção do site está evoluindo,
nós [agradecemos seu feedback][welcome your feedback]!

[welcome your feedback]: https://google.qualtrics.com/jfe/form/SV_4T0XuR9Ts29acw6?page="case-study/data-layer"

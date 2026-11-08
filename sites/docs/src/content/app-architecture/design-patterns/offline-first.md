---
title: "Suporte offline-first"
description: Implemente o suporte offline-first para um recurso em um aplicativo.
contentTags:
  - data
  - user experience
  - repository pattern
iconPath: /assets/images/docs/app-architecture/design-patterns/offline-first-icon.svg
order: 3
ia-translate: true
---

<?code-excerpt path-base="app-architecture/offline_first"?>

Um aplicativo offline-first é um aplicativo capaz de oferecer a maior parte
ou toda a sua funcionalidade enquanto está desconectado da internet.
Aplicativos offline-first geralmente dependem de dados armazenados
para oferecer aos usuários acesso temporário a dados
que, de outra forma, estariam disponíveis apenas online.

Alguns aplicativos offline-first combinam dados locais e remotos perfeitamente,
enquanto outros aplicativos informam ao usuário
quando o aplicativo está usando dados em cache.
Da mesma forma,
alguns aplicativos sincronizam dados em segundo plano
enquanto outros exigem que o usuário os sincronize explicitamente.
Tudo depende dos requisitos do aplicativo e da funcionalidade que ele oferece,
e cabe ao desenvolvedor decidir qual implementação se adapta às suas necessidades.

Neste guia,
você aprenderá como implementar diferentes abordagens
para aplicativos offline-first no Flutter,
seguindo as [diretrizes de arquitetura do Flutter][Flutter Architecture guidelines].

## Arquitetura offline-first {:#offline-first-architecture}

Conforme explicado no guia de conceitos comuns de arquitetura,
os repositórios atuam como a única fonte da verdade.
Eles são responsáveis ​​por apresentar dados locais ou remotos,
e devem ser o único lugar onde os dados podem ser modificados.
Em aplicativos offline-first,
os repositórios combinam diferentes fontes de dados locais e remotos
para apresentar dados em um único ponto de acesso,
independentemente do estado de conectividade do dispositivo.

Este exemplo usa o `UserProfileRepository`,
um repositório que permite obter e armazenar objetos `UserProfile`
com suporte offline-first.

O `UserProfileRepository` usa dois serviços de dados diferentes:
um funciona com dados remotos,
e o outro funciona com um banco de dados local.

O cliente API, `ApiClientService`,
se conecta a um serviço remoto usando chamadas HTTP REST.

<?code-excerpt "lib/data/services/api_client_service.dart (ApiClientService)"?>
```dart
class ApiClientService {
  /// performs GET network request to obtain a UserProfile
  Future<UserProfile> getUserProfile() async {
    // ···
  }

  /// performs PUT network request to update a UserProfile
  Future<void> putUserProfile(UserProfile userProfile) async {
    // ···
  }
}
```

O serviço de banco de dados, `DatabaseService`, armazena dados usando SQL,
semelhante ao encontrado na receita [Arquitetura de armazenamento persistente: SQL][Persistent Storage Architecture: SQL].

<?code-excerpt "lib/data/services/database_service.dart (DatabaseService)"?>
```dart
class DatabaseService {
  /// Fetches the UserProfile from the database.
  /// Returns null if the user profile is not found.
  Future<UserProfile?> fetchUserProfile() async {
    // ···
  }

  /// Update UserProfile in the database.
  Future<void> updateUserProfile(UserProfile userProfile) async {
    // ···
  }
}
```

Este exemplo também usa a classe de dados `UserProfile`
que foi criada usando o pacote [`freezed`][].

<?code-excerpt "lib/domain/model/user_profile.dart (UserProfile)" remove="@Default(false) bool synchronized,"?>
```dart
@freezed
abstract class UserProfile with _$UserProfile {
  const factory UserProfile({
    required String name,
    required String photoUrl,
  }) = _UserProfile;
}
```

Em aplicativos que possuem dados complexos,
como quando os dados remotos contêm mais campos do que o necessário para a UI,
você pode querer ter uma classe de dados para os serviços de API e banco de dados,
e outra para a UI.
Por exemplo,
`UserProfileLocal` para a entidade de banco de dados,
`UserProfileRemote` para o objeto de resposta da API,
e então `UserProfile` para a classe de modelo de dados da UI.
O `UserProfileRepository` cuidaria
de converter de um para o outro quando necessário.

Este exemplo também inclui o `UserProfileViewModel`,
um view model que usa o `UserProfileRepository`
para exibir o `UserProfile` em um widget.

<?code-excerpt "lib/ui/user_profile/user_profile_viewmodel.dart (UserProfileViewModel)"?>
```dart
class UserProfileViewModel extends ChangeNotifier {
  // ···
  final UserProfileRepository _userProfileRepository;

  UserProfile? get userProfile => _userProfile;
  // ···

  /// Load the user profile from the database or the network
  Future<void> load() async {
    // ···
  }

  /// Save the user profile with the new name
  Future<void> save(String newName) async {
    // ···
  }
}
```

## Lendo dados {:#reading-data}

A leitura de dados é uma parte fundamental de qualquer aplicativo
que dependa de serviços de API remotos.

Em aplicativos offline-first,
você deseja garantir que o acesso a esses dados seja o mais rápido possível,
e que não dependa do dispositivo estar online
para fornecer dados ao usuário.
Isso é semelhante ao [padrão de design de estado otimista][Optimistic State design pattern].

Nesta seção,
você aprenderá duas abordagens diferentes,
uma que usa o banco de dados como um fallback,
e outra que combina dados locais e remotos usando um `Stream`.

### Usando dados locais como fallback {:#using-local-data-as-a-fallback}

Como uma primeira abordagem,
você pode implementar o suporte offline tendo um mecanismo de fallback
para quando o usuário está offline ou uma chamada de rede falha.

Nesse caso, o `UserProfileRepository` tenta obter o `UserProfile`
do servidor da API remota usando o `ApiClientService`.
Se esta solicitação falhar,
retorna o `UserProfile` armazenado localmente do `DatabaseService`.

<?code-excerpt "lib/data/repositories/user_profile_repository.dart (getUserProfileFallback)" replace="/Fallback//g"?>
```dart
Future<UserProfile> getUserProfile() async {
  try {
    // Fetch the user profile from the API
    final apiUserProfile = await _apiClientService.getUserProfile();
    //Update the database with the API result
    await _databaseService.updateUserProfile(apiUserProfile);

    return apiUserProfile;
  } catch (e) {
    // If the network call failed,
    // fetch the user profile from the database
    final databaseUserProfile = await _databaseService.fetchUserProfile();

    // If the user profile was never fetched from the API
    // it will be null, so throw an  error
    if (databaseUserProfile != null) {
      return databaseUserProfile;
    } else {
      // Handle the error
      throw Exception('User profile not found');
    }
  }
}
```

### Usando um Stream {:#using-a-stream}

Uma alternativa melhor apresenta os dados usando um `Stream`.
No melhor cenário,
o `Stream` emite dois valores,
os dados armazenados localmente e os dados do servidor.

Primeiro, o stream emite os dados armazenados localmente usando o `DatabaseService`.
Essa chamada geralmente é mais rápida e menos propensa a erros do que uma chamada de rede,
e ao fazê-lo primeiro, o view model já pode exibir dados para o usuário.

Se o banco de dados não contiver nenhum dado em cache,
o `Stream` depende completamente da chamada de rede,
emitindo apenas um valor.

Então, o método realiza a chamada de rede usando o `ApiClientService`
para obter dados atualizados.
Se a solicitação foi bem-sucedida,
ele atualiza o banco de dados com os dados recém-obtidos,
e então envia o valor para o view model,
para que possa ser exibido para o usuário.

<?code-excerpt "lib/data/repositories/user_profile_repository.dart (getUserProfile)"?>
```dart
Stream<UserProfile> getUserProfile() async* {
  // Fetch the user profile from the database
  final userProfile = await _databaseService.fetchUserProfile();
  // Returns the database result if it exists
  if (userProfile != null) {
    yield userProfile;
  }

  // Fetch the user profile from the API
  try {
    final apiUserProfile = await _apiClientService.getUserProfile();
    //Update the database with the API result
    await _databaseService.updateUserProfile(apiUserProfile);
    // Return the API result
    yield apiUserProfile;
  } catch (e) {
    // Handle the error
  }
}
```

O view model deve se inscrever
neste `Stream` e esperar até que ele seja concluído.
Para isso, chame `asFuture()` com o objeto `Subscription` e aguarde o resultado.

Para cada valor obtido,
atualize os dados do view model e chame `notifyListeners()`
para que a UI mostre os dados mais recentes.

<?code-excerpt "lib/ui/user_profile/user_profile_viewmodel.dart (load)"?>
```dart
Future<void> load() async {
  await _userProfileRepository
      .getUserProfile()
      .listen(
        (userProfile) {
          _userProfile = userProfile;
          notifyListeners();
        },
        onError: (error) {
          // handle error
        },
      )
      .asFuture<void>();
}
```
### Usando apenas dados locais {:#using-only-local-data}

Outra abordagem possível usa dados armazenados localmente para operações de leitura.
Essa abordagem exige que os dados tenham sido pré-carregados
em algum momento no banco de dados,
e requer um mecanismo de sincronização que possa manter os dados atualizados.

<?code-excerpt "lib/data/repositories/user_profile_repository.dart (getUserProfileLocal)" replace="/Local//g;/Read//g"?>
```dart
Future<UserProfile> getUserProfile() async {
  // Fetch the user profile from the database
  final userProfile = await _databaseService.fetchUserProfile();

  // Return the database result if it exists
  if (userProfile == null) {
    throw Exception('Data not found');
  }

  return userProfile;
}

Future<void> sync() async {
  try {
    // Fetch the user profile from the API
    final userProfile = await _apiClientService.getUserProfile();

    // Update the database with the API result
    await _databaseService.updateUserProfile(userProfile);
  } catch (e) {
    // Try again later
  }
}
```

Essa abordagem pode ser útil para aplicativos
que não exigem que os dados estejam sincronizados com o servidor o tempo todo.
Por exemplo, um aplicativo de clima
onde os dados meteorológicos são atualizados apenas uma vez por dia.

A sincronização pode ser feita manualmente pelo usuário,
por exemplo, uma ação de pull-to-refresh que então chama o método `sync()`,
ou feita periodicamente por um `Timer` ou um processo em segundo plano.
Você pode aprender como implementar uma tarefa de sincronização
na seção sobre sincronização de estado.

## Escrevendo dados {:#writing-data}

A gravação de dados em aplicativos offline-first depende fundamentalmente
do caso de uso do aplicativo.

Alguns aplicativos podem exigir que os dados de entrada do usuário
estejam imediatamente disponíveis no lado do servidor,
enquanto outros aplicativos podem ser mais flexíveis
e permitir que os dados fiquem dessincronizados temporariamente.

Esta seção explica duas abordagens diferentes
para implementar a gravação de dados em aplicativos offline-first.

### Gravação apenas online {:#online-only-writing}

Uma abordagem para gravar dados em aplicativos offline-first
é impor estar online para gravar dados.
Embora isso possa parecer contra-intuitivo,
isso garante que os dados que o usuário modificou
estejam totalmente sincronizados com o servidor,
e o aplicativo não tenha um estado diferente do servidor.

Neste caso, você primeiro tenta enviar os dados para o serviço API,
e se a solicitação for bem-sucedida,
armazena os dados no banco de dados.

<?code-excerpt "lib/data/repositories/user_profile_repository.dart (updateUserProfileOnline)" replace="/Online//g"?>
```dart
Future<void> updateUserProfile(UserProfile userProfile) async {
  try {
    // Update the API with the user profile
    await _apiClientService.putUserProfile(userProfile);

    // Only if the API call was successful
    // update the database with the user profile
    await _databaseService.updateUserProfile(userProfile);
  } catch (e) {
    // Handle the error
  }
}
```

A desvantagem neste caso é que a funcionalidade offline-first
está disponível apenas para operações de leitura,
mas não para operações de gravação, pois elas exigem que o usuário esteja online.

### Gravação offline-first {:#offline-first-writing}

A segunda abordagem funciona ao contrário.
Em vez de realizar a chamada de rede primeiro,
o aplicativo primeiro armazena os novos dados no banco de dados,
e então tenta enviá-los para o serviço API depois que ele foi armazenado localmente.

<?code-excerpt "lib/data/repositories/user_profile_repository.dart (updateUserProfileOffline)" replace="/Offline//g"?>
```dart
Future<void> updateUserProfile(UserProfile userProfile) async {
  // Update the database with the user profile
  await _databaseService.updateUserProfile(userProfile);

  try {
    // Update the API with the user profile
    await _apiClientService.putUserProfile(userProfile);
  } catch (e) {
    // Handle the error
  }
}
```

Essa abordagem permite que os usuários armazenem dados localmente
mesmo quando o aplicativo está offline,
no entanto, se a chamada de rede falhar,
o banco de dados local e o serviço API não estão mais sincronizados.
Na próxima seção,
você aprenderá diferentes abordagens para lidar com a sincronização
entre dados locais e remotos.

## Sincronizando estado {:#synchronizing-state}

Manter os dados locais e remotos sincronizados
é uma parte importante dos aplicativos offline-first,
já que as alterações que foram feitas localmente
precisam ser copiadas para o serviço remoto.
O aplicativo também deve garantir que, quando o usuário retornar ao aplicativo,
os dados armazenados localmente sejam os mesmos do serviço remoto.

### Escrevendo uma tarefa de sincronização {:#writing-a-synchronization-task}

Existem diferentes abordagens para implementar
a sincronização em uma tarefa em segundo plano.

Uma solução simples é criar um `Timer`
no `UserProfileRepository` que é executado periodicamente,
por exemplo, a cada cinco minutos.

<?code-excerpt "lib/data/repositories/user_profile_repository.dart (Timer)"?>
```dart
Timer.periodic(const Duration(minutes: 5), (timer) => sync());
```

O método `sync()` então busca o `UserProfile` do banco de dados,
e se ele exigir sincronização, ele é enviado para o serviço API.

<?code-excerpt "lib/data/repositories/user_profile_repository.dart (sync)"?>
```dart
Future<void> sync() async {
  try {
    // Fetch the user profile from the database
    final userProfile = await _databaseService.fetchUserProfile();

    // Check if the user profile requires synchronization
    if (userProfile == null || userProfile.synchronized) {
      return;
    }

    // Update the API with the user profile
    await _apiClientService.putUserProfile(userProfile);

    // Set the user profile as synchronized
    await _databaseService.updateUserProfile(
      userProfile.copyWith(synchronized: true),
    );
  } catch (e) {
    // Try again later
  }
}
```

Uma solução mais complexa usa processos em segundo plano
como o plugin [`workmanager`][].
Isso permite que seu aplicativo execute o processo de sincronização
em segundo plano, mesmo quando o aplicativo não está em execução.

:::note
Executar operações em segundo plano continuamente
pode descarregar a bateria do dispositivo drasticamente,
e alguns dispositivos limitam os recursos de processamento em segundo plano,
portanto, essa abordagem precisa ser ajustada
para os requisitos do aplicativo e uma solução pode não ser adequada para todos os casos.
:::

Também é recomendável executar a tarefa de sincronização apenas
quando a rede está disponível.
Por exemplo, você pode usar o plugin [`connectivity_plus`][]
para verificar se o dispositivo está conectado ao WiFi.
Você também pode usar [`battery_plus`][] para verificar
que o dispositivo não está com pouca bateria.

No exemplo anterior, a tarefa de sincronização é executada a cada 5 minutos.
Em alguns casos, isso pode ser excessivo,
enquanto em outros pode não ser frequente o suficiente.
O tempo real do período de sincronização para seu aplicativo
depende das necessidades do seu aplicativo e é algo que você terá que decidir.

### Armazenando um flag de sincronização {:#storing-a-synchronization-flag}

Para saber se os dados exigem sincronização,
adicione um flag à classe de dados indicando se as alterações precisam ser sincronizadas.

Por exemplo, `bool synchronized`:

<?code-excerpt "lib/domain/model/user_profile.dart (UserProfile)"?>
```dart
@freezed
abstract class UserProfile with _$UserProfile {
  const factory UserProfile({
    required String name,
    required String photoUrl,
    @Default(false) bool synchronized,
  }) = _UserProfile;
}
```

Sua lógica de sincronização deve tentar
enviá-lo para o serviço API
apenas quando o flag `synchronized` for `false`.
Se a solicitação for bem-sucedida, altere-o para `true`.

### Enviando dados do servidor {:#pushing-data-from-server}

Uma abordagem diferente para a sincronização
é usar um serviço de push para fornecer dados atualizados para o aplicativo.
Nesse caso, o servidor notifica o aplicativo quando os dados são alterados,
em vez de ser o aplicativo solicitando atualizações.

Por exemplo, você pode usar o [Firebase messaging][],
para enviar pequenos payloads de dados para o dispositivo,
bem como acionar tarefas de sincronização remotamente usando mensagens em segundo plano.

Em vez de ter uma tarefa de sincronização em execução em segundo plano,
o servidor notifica o aplicativo
quando os dados armazenados precisam ser atualizados com uma notificação push.

Você pode combinar as duas abordagens,
tendo uma tarefa de sincronização em segundo plano e usando mensagens push em segundo plano,
para manter o banco de dados do aplicativo sincronizado com o servidor.

## Juntando tudo {:#putting-it-all-together}

Escrever um aplicativo offline-first
exige tomar decisões sobre
a forma como as operações de leitura, gravação e sincronização são implementadas,
que dependem dos requisitos do aplicativo que você está desenvolvendo.

As principais conclusões são:

- Ao ler dados,
você pode usar um `Stream` para combinar dados armazenados localmente com dados remotos.
- Ao gravar dados,
decida se você precisa estar online ou offline,
e se você precisa sincronizar dados mais tarde ou não.
- Ao implementar uma tarefa de sincronização em segundo plano,
leve em consideração o status do dispositivo e as necessidades do seu aplicativo,
já que diferentes aplicativos podem ter requisitos diferentes.

[Flutter Architecture guidelines]:/app-architecture
[Persistent Storage Architecture: SQL]:/app-architecture/design-patterns/sql
[`freezed`]:{{site.pub}}/packages/freezed
[Optimistic State design pattern]:/app-architecture/design-patterns/optimistic-state
[`workmanager`]:{{site.pub}}/packages/workmanager
[`connectivity_plus`]:{{site.pub}}/packages/connectivity_plus
[`battery_plus`]:{{site.pub}}/packages/battery_plus
[Firebase messaging]:{{site.firebase}}/docs/cloud-messaging/flutter/client

---
title: "Suporte offline-first"
description: Implemente o suporte offline-first para um recurso em um aplicativo.
contentTags:
  - data
  - user experience
  - repository pattern
iconPath: /assets/images/docs/app-architecture/design-patterns/offline-first-icon.svg
order: 3
js:
  - defer: true
    url: /assets/js/inject_dartpad.js
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
seguindo as [diretrizes de arquitetura do Flutter][].

## Arquitetura offline-first

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
  /// executa solicitação de rede GET para obter um UserProfile
  Future<UserProfile> getUserProfile() async {
    // ···
  }

  /// executa solicitação de rede PUT para atualizar um UserProfile
  Future<void> putUserProfile(UserProfile userProfile) async {
    // ···
  }
}
```

O serviço de banco de dados, `DatabaseService`, armazena dados usando SQL,
semelhante ao encontrado na receita [Arquitetura de armazenamento persistente: SQL][].

<?code-excerpt "lib/data/services/database_service.dart (DatabaseService)"?>
```dart
class DatabaseService {
  /// Busca o UserProfile do banco de dados.
  /// Retorna null se o perfil de usuário não for encontrado.
  Future<UserProfile?> fetchUserProfile() async {
    // ···
  }

  /// Atualiza UserProfile no banco de dados.
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
class UserProfile with _$UserProfile {
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

  /// Carrega o perfil de usuário do banco de dados ou da rede
  Future<void> load() async {
    // ···
  }

  /// Salva o perfil de usuário com o novo nome
  Future<void> save(String newName) async {
    // ···
  }
}
```

## Lendo dados

A leitura de dados é uma parte fundamental de qualquer aplicativo
que dependa de serviços de API remotos.

Em aplicativos offline-first,
você deseja garantir que o acesso a esses dados seja o mais rápido possível,
e que não dependa do dispositivo estar online
para fornecer dados ao usuário.
Isso é semelhante ao [padrão de design de estado otimista][].

Nesta seção,
você aprenderá duas abordagens diferentes,
uma que usa o banco de dados como um fallback,
e outra que combina dados locais e remotos usando um `Stream`.

### Usando dados locais como fallback

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
    // Busca o perfil de usuário da API
    final apiUserProfile = await _apiClientService.getUserProfile();
    // Atualiza o banco de dados com o resultado da API
    await _databaseService.updateUserProfile(apiUserProfile);

    return apiUserProfile;
  } catch (e) {
    // Se a chamada de rede falhou,
    // busca o perfil de usuário do banco de dados
    final databaseUserProfile = await _databaseService.fetchUserProfile();

    // Se o perfil de usuário nunca foi buscado da API
    // será nulo, então lança um erro
    if (databaseUserProfile != null) {
      return databaseUserProfile;
    } else {
      // Trata o erro
      throw Exception('Perfil de usuário não encontrado');
    }
  }
}
```

### Usando um Stream

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
  // Busca o perfil de usuário do banco de dados
  final userProfile = await _databaseService.fetchUserProfile();
  // Retorna o resultado do banco de dados se ele existir
  if (userProfile != null) {
    yield userProfile;
  }

  // Busca o perfil de usuário da API
  try {
    final apiUserProfile = await _apiClientService.getUserProfile();
    // Atualiza o banco de dados com o resultado da API
    await _databaseService.updateUserProfile(apiUserProfile);
    // Retorna o resultado da API
    yield apiUserProfile;
  } catch (e) {
    // Trata o erro
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
  await _userProfileRepository.getUserProfile().listen((userProfile) {
    _userProfile = userProfile;
    notifyListeners();
  }, onError: (error) {
    // tratar erro
  }).asFuture();
}
```

### Usando apenas dados locais

Outra abordagem possível usa dados armazenados localmente para operações de leitura.
Essa abordagem exige que os dados tenham sido pré-carregados
em algum momento no banco de dados,
e requer um mecanismo de sincronização que possa manter os dados atualizados.

<?code-excerpt "lib/data/repositories/user_profile_repository.dart (getUserProfileLocal)" replace="/Local//g;/Read//g"?>
```dart
Future<UserProfile> getUserProfile() async {
  // Busca o perfil de usuário do banco de dados
  final userProfile = await _databaseService.fetchUserProfile();

  // Retorna o resultado do banco de dados se ele existir
  if (userProfile == null) {
    throw Exception('Dados não encontrados');
  }

  return userProfile;
}

Future<void> sync() async {
  try {
    // Busca o perfil de usuário da API
    final userProfile = await _apiClientService.getUserProfile();

    // Atualiza o banco de dados com o resultado da API
    await _databaseService.updateUserProfile(userProfile);
  } catch (e) {
    // Tentar novamente mais tarde
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

## Escrevendo dados

A gravação de dados em aplicativos offline-first depende fundamentalmente
do caso de uso do aplicativo.

Alguns aplicativos podem exigir que os dados de entrada do usuário
estejam imediatamente disponíveis no lado do servidor,
enquanto outros aplicativos podem ser mais flexíveis
e permitir que os dados fiquem dessincronizados temporariamente.

Esta seção explica duas abordagens diferentes
para implementar a gravação de dados em aplicativos offline-first.

### Gravação apenas online

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
    // Atualiza a API com o perfil de usuário
    await _apiClientService.putUserProfile(userProfile);

    // Apenas se a chamada API foi bem-sucedida
    // atualiza o banco de dados com o perfil de usuário
    await _databaseService.updateUserProfile(userProfile);
  } catch (e) {
    // Trata o erro
  }
}
```

A desvantagem neste caso é que a funcionalidade offline-first
está disponível apenas para operações de leitura,
mas não para operações de gravação, pois elas exigem que o usuário esteja online.

### Gravação offline-first

A segunda abordagem funciona ao contrário.
Em vez de realizar a chamada de rede primeiro,
o aplicativo primeiro armazena os novos dados no banco de dados,
e então tenta enviá-los para o serviço API depois que ele foi armazenado localmente.

<?code-excerpt "lib/data/repositories/user_profile_repository.dart (updateUserProfileOffline)" replace="/Offline//g"?>
```dart
Future<void> updateUserProfile(UserProfile userProfile) async {
  // Atualiza o banco de dados com o perfil de usuário
  await _databaseService.updateUserProfile(userProfile);

  try {
    // Atualiza a API com o perfil de usuário
    await _apiClientService.putUserProfile(userProfile);
  } catch (e) {
    // Trata o erro
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

## Sincronizando estado

Manter os dados locais e remotos sincronizados
é uma parte importante dos aplicativos offline-first,
já que as alterações que foram feitas localmente
precisam ser copiadas para o serviço remoto.
O aplicativo também deve garantir que, quando o usuário retornar ao aplicativo,
os dados armazenados localmente sejam os mesmos do serviço remoto.

### Escrevendo uma tarefa de sincronização

Existem diferentes abordagens para implementar
a sincronização em uma tarefa em segundo plano.

Uma solução simples é criar um `Timer`
no `UserProfileRepository` que é executado periodicamente,
por exemplo, a cada cinco minutos.

<?code-excerpt "lib/data/repositories/user_profile_repository.dart (Timer)"?>
```dart
Timer.periodic(
  const Duration(minutes: 5),
  (timer) => sync(),
);
```

O método `sync()` então busca o `UserProfile` do banco de dados,
e se ele exigir sincronização, ele é enviado para o serviço API.

<?code-excerpt "lib/data/repositories/user_profile_repository.dart (sync)"?>
```dart
Future<void> sync() async {
  try {
    // Busca o perfil de usuário do banco de dados
    final userProfile = await _databaseService.fetchUserProfile();

    // Verifica se o perfil de usuário requer sincronização
    if (userProfile == null || userProfile.synchronized) {
      return;
    }

    // Atualiza a API com o perfil de usuário
    await _apiClientService.putUserProfile(userProfile);

    // Define o perfil de usuário como sincronizado
    await _databaseService
        .updateUserProfile(userProfile.copyWith(synchronized: true));
  } catch (e) {
    // Tentar novamente mais tarde
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

### Armazenando um flag de sincronização

Para saber se os dados exigem sincronização,
adicione um flag à classe de dados indicando se as alterações precisam ser sincronizadas.

Por exemplo, `bool synchronized`:

<?code-excerpt "lib/domain/model/user_profile.dart (UserProfile)"?>
```dart
@freezed
class UserProfile with _$UserProfile {
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

### Enviando dados do servidor

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

## Juntando tudo

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

[diretrizes de arquitetura do Flutter]:/app-architecture
[Arquitetura de armazenamento persistente: SQL]:/app-architecture/design-patterns/sql
[`freezed`]:{{site.pub}}/packages/freezed
[padrão de design de estado otimista]:/app-architecture/design-patterns/optimistic-state
[`workmanager`]:{{site.pub}}/packages/workmanager
[`connectivity_plus`]:{{site.pub}}/packages/connectivity_plus
[`battery_plus`]:{{site.pub}}/packages/battery_plus
[Firebase messaging]:{{site.firebase}}/docs/cloud-messaging/flutter/client

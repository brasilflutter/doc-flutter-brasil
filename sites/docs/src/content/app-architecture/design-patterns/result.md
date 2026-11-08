---
title: Tratamento de erros com objetos Result
description: "Melhore o tratamento de erros entre classes com objetos Result."
contentTags:
  - error handling
  - services
iconPath: /assets/images/docs/app-architecture/design-patterns/result-icon.svg
order: 5
ia-translate: true
---

<?code-excerpt path-base="app-architecture/result"?>

O Dart fornece um mecanismo de tratamento de erros integrado
com a capacidade de lançar e capturar exceções.

Conforme mencionado na [documentação de tratamento de erros][Error handling documentation],
as exceções do Dart são exceções não tratadas.
Isso significa que os métodos que lançam exceções não precisam declará-las,
e os métodos de chamada também não são obrigados a capturá-las.

Isso pode levar a situações em que as exceções não são tratadas adequadamente.
Em projetos grandes,
os desenvolvedores podem se esquecer de capturar exceções,
e as diferentes camadas e componentes do aplicativo
podem lançar exceções que não são documentadas.
Isso pode levar a erros e falhas.

Neste guia,
você aprenderá sobre essa limitação
e como atenuá-la usando o padrão _result_.

## Fluxo de erro em aplicativos Flutter

Os aplicativos que seguem as [diretrizes de arquitetura do Flutter][Flutter architecture guidelines]
geralmente são compostos por view models,
repositórios e serviços, entre outras partes.
Quando uma função em um desses componentes falha,
ele deve comunicar o erro ao componente de chamada.

Normalmente, isso é feito com exceções.
Por exemplo,
um serviço de cliente API que não consegue se comunicar com o servidor remoto
pode lançar uma Exceção de Erro HTTP.
O componente de chamada,
por exemplo, um Repositório,
teria que capturar esta exceção
ou ignorá-la e deixar o view model de chamada tratá-la.

Isso pode ser observado no exemplo a seguir. Considere estas classes:

- Um serviço, `ApiClientService`, executa chamadas de API para um serviço remoto.
- Um repositório, `UserProfileRepository`,
  fornece o `UserProfile` fornecido pelo `ApiClientService`.
- Um view model, `UserProfileViewModel`, usa o `UserProfileRepository`.

O `ApiClientService` contém um método, `getUserProfile`,
que lança exceções em determinadas situações:

- O método lança uma `HttpException` se o código de resposta não for 200.
- O método de análise JSON lança uma exceção
  se a resposta não estiver formatada corretamente.
- O cliente HTTP pode lançar uma exceção devido a problemas de rede.

O código a seguir testa uma variedade de possíveis exceções:

<?code-excerpt "lib/no_result.dart (ApiClientService)"?>
```dart
class ApiClientService {
  // ···

  Future<UserProfile> getUserProfile() async {
    try {
      final request = await client.get(_host, _port, '/user');
      final response = await request.close();
      if (response.statusCode == 200) {
        final stringData = await response.transform(utf8.decoder).join();
        return UserProfile.fromJson(jsonDecode(stringData));
      } else {
        throw const HttpException('Invalid response');
      }
    } finally {
      client.close();
    }
  }
}
```

O `UserProfileRepository` não precisa lidar
com as exceções do `ApiClientService`.
Neste exemplo, ele apenas retorna o valor do cliente API.

<?code-excerpt "lib/no_result.dart (UserProfileRepository)"?>
```dart
class UserProfileRepository {
  // ···

  Future<UserProfile> getUserProfile() async {
    return await _apiClientService.getUserProfile();
  }
}
```

Finalmente, o `UserProfileViewModel`
deve capturar todas as exceções e tratar os erros.

Isso pode ser feito envolvendo
a chamada para o `UserProfileRepository` com um try-catch:

<?code-excerpt "lib/no_result.dart (UserProfileViewModel)"?>
```dart
class UserProfileViewModel extends ChangeNotifier {
  // ···

  Future<void> load() async {
    try {
      _userProfile = await userProfileRepository.getUserProfile();
      notifyListeners();
    } on Exception catch (exception) {
      // handle exception
    }
  }
}
```

Na realidade, um desenvolvedor pode se esquecer de capturar exceções adequadamente e
acabar com o seguinte código.
Ele compila e é executado, mas falha se
uma das exceções mencionadas anteriormente ocorrer:

<?code-excerpt "lib/no_result.dart (UserProfileViewModelNoTryCatch)" replace="/NoTryCatch//g"?>
```dart
class UserProfileViewModel extends ChangeNotifier {
  // ···

  Future<void> load() async {
    _userProfile = await userProfileRepository.getUserProfile();
    notifyListeners();
  }
}
```

Você pode tentar resolver isso documentando o `ApiClientService`,
avisando sobre as possíveis exceções que ele pode lançar.
No entanto, como o view model não usa o serviço diretamente,
outros desenvolvedores que trabalham no código podem perder essa informação.

## Usando o padrão result

Uma alternativa para lançar exceções
é envolver a saída da função em um objeto `Result`.

Quando a função é executada com sucesso,
o `Result` contém o valor retornado.
No entanto, se a função não for concluída com sucesso,
o objeto `Result` contém o erro.

Um `Result` é uma classe [`sealed`][]
que pode ser uma subclasse de `Ok` ou da classe `Error`.
Retorne o valor bem-sucedido com a subclasse `Ok`,
e o erro capturado com a subclasse `Error`.

O código a seguir mostra uma amostra da classe `Result` que
foi simplificado para fins de demonstração.
Uma implementação completa está no final desta página.

<?code-excerpt "lib/simple_result.dart"?>
```dart
/// Utility class that simplifies handling errors.
///
/// Return a [Result] from a function to indicate success or failure.
///
/// A [Result] is either an [Ok] with a value of type [T]
/// or an [Error] with an [Exception].
///
/// Use [Result.ok] to create a successful result with a value of type [T].
/// Use [Result.error] to create an error result with an [Exception].
sealed class Result<T> {
  const Result();

  /// Creates an instance of Result containing a value
  factory Result.ok(T value) => Ok(value);

  /// Create an instance of Result containing an error
  factory Result.error(Exception error) => Error(error);
}

/// Subclass of Result for values
final class Ok<T> extends Result<T> {
  const Ok(this.value);

  /// Returned value in result
  final T value;
}

/// Subclass of Result for errors
final class Error<T> extends Result<T> {
  const Error(this.error);

  /// Returned error in result
  final Exception error;
}
```

Neste exemplo,
a classe `Result` usa um tipo genérico `T` para representar qualquer valor de retorno,
que pode ser um tipo Dart primitivo como `String` ou um `int` ou uma classe personalizada como `UserProfile`.

### Criando um objeto `Result`

Para funções que usam a classe `Result` para retornar valores,
em vez de um valor,
a função retorna um objeto `Result` contendo o valor.

Por exemplo, no `ApiClientService`,
`getUserProfile` é alterado para retornar um `Result`:

<?code-excerpt "lib/main.dart (ApiClientService1)"?>
```dart
class ApiClientService {
  // ···

  Future<Result<UserProfile>> getUserProfile() async {
    // ···
  }
}
```

Em vez de retornar o `UserProfile` diretamente,
ele retorna um objeto `Result` contendo um `UserProfile`.

Para facilitar o uso da classe `Result`,
ele contém dois construtores nomeados, `Result.ok` e `Result.error`.
Use-os para construir o `Result` dependendo da saída desejada.
Além disso, capture quaisquer exceções lançadas pelo código
e envolva-as no objeto `Result`.

Por exemplo, aqui o método `getUserProfile()`
foi alterado para usar a classe `Result`:

<?code-excerpt "lib/main.dart (ApiClientService2)"?>
```dart
class ApiClientService {
  // ···

  Future<Result<UserProfile>> getUserProfile() async {
    try {
      final request = await client.get(_host, _port, '/user');
      final response = await request.close();
      if (response.statusCode == 200) {
        final stringData = await response.transform(utf8.decoder).join();
        return Result.ok(UserProfile.fromJson(jsonDecode(stringData)));
      } else {
        return const Result.error(HttpException('Invalid response'));
      }
    } on Exception catch (exception) {
      return Result.error(exception);
    } finally {
      client.close();
    }
  }
}
```

A instrução de retorno original foi substituída
por uma instrução que retorna o valor usando `Result.ok`.
O `throw HttpException()`
foi substituído por uma instrução que retorna `Result.error(HttpException())`,
envolvendo o erro em um `Result`.
Além disso, o método é envolvido com um bloco `try-catch`
para capturar quaisquer exceções lançadas pelo cliente Http
ou o analisador JSON em um `Result.error`.

A classe do repositório também precisa ser modificada,
e em vez de retornar um `UserProfile` diretamente,
agora ele retorna um `Result<UserProfile>`.

<?code-excerpt "lib/main.dart (getUserProfile1)" replace="/1//g"?>
```dart
Future<Result<UserProfile>> getUserProfile() async {
  return await _apiClientService.getUserProfile();
}
```

### Desembrulhando o objeto Result

Agora, o view model não recebe o `UserProfile` diretamente,
mas recebe um `Result` contendo um `UserProfile`.

Isso força o desenvolvedor a implementar o view model
para desembrulhar o `Result` para obter o `UserProfile`,
e evita ter exceções não capturadas.

<?code-excerpt "lib/main.dart (UserProfileViewModel)"?>
```dart
class UserProfileViewModel extends ChangeNotifier {
  // ···

  UserProfile? userProfile;

  Exception? error;

  Future<void> load() async {
    final result = await userProfileRepository.getUserProfile();
    switch (result) {
      case Ok<UserProfile>():
        userProfile = result.value;
      case Error<UserProfile>():
        error = result.error;
    }
    notifyListeners();
  }
}
```

A classe `Result` é implementada usando uma classe `sealed`,
o que significa que ela só pode ser do tipo `Ok` ou `Error`.
Isso permite que o código avalie o resultado com um
[resultado ou expressão switch][switch result or expression].

No caso `Ok<UserProfile>`,
obtenha o valor usando a propriedade `value`.

No caso `Error<UserProfile>`,
obtenha o objeto de erro usando a propriedade `error`.

## Melhorando o fluxo de controle

Envolver o código em um bloco `try-catch` garante que
exceções lançadas sejam capturadas e não propagadas para outras partes do código.

Considere o código a seguir.

<?code-excerpt "lib/no_result.dart (UserProfileRepository2)" replace="/2//g"?>
```dart
class UserProfileRepository {
  // ···

  Future<UserProfile> getUserProfile() async {
    try {
      return await _apiClientService.getUserProfile();
    } catch (e) {
      try {
        return await _databaseService.createTemporaryUser();
      } catch (e) {
        throw Exception('Failed to get user profile');
      }
    }
  }
}
```

Neste método, o `UserProfileRepository`
tenta obter o `UserProfile`
usando o `ApiClientService`.
Se falhar, ele tenta criar um usuário temporário em um `DatabaseService`.

Como o método de qualquer serviço pode falhar,
o código deve capturar as exceções em ambos os casos.

Isso pode ser melhorado usando o padrão `Result`:

<?code-excerpt "lib/main.dart (getUserProfile)"?>
```dart
Future<Result<UserProfile>> getUserProfile() async {
  final apiResult = await _apiClientService.getUserProfile();
  if (apiResult is Ok) {
    return apiResult;
  }

  final databaseResult = await _databaseService.createTemporaryUser();
  if (databaseResult is Ok) {
    return databaseResult;
  }

  return Result.error(Exception('Failed to get user profile'));
}
```

Neste código, se o objeto `Result` for uma instância `Ok`,
então a função retorna esse objeto;
caso contrário, retorna `Result.Error`.

## Juntando tudo

Neste guia, você aprendeu
como usar uma classe `Result` para retornar valores de resultado.

Os principais pontos são:

- As classes `Result` forçam o método de chamada a verificar se há erros,
  reduzindo a quantidade de bugs causados por exceções não capturadas.
- As classes `Result` ajudam a melhorar o fluxo de controle em comparação com os blocos try-catch.
- As classes `Result` são `sealed` e só podem retornar instâncias `Ok` ou `Error`,
  permitindo que o código as desembrulhe com uma instrução switch.

Abaixo você pode encontrar a classe `Result` completa
conforme implementada no [exemplo do aplicativo Compass][Compass App example]
para as [diretrizes de arquitetura do Flutter][Flutter architecture guidelines].

:::note
Verifique [pub.dev][] para diferentes
implementações prontas para uso da classe `Result`,
como os pacotes [`result_dart`][], [`result_type`][] e [`multiple_result`][].
:::

<?code-excerpt "lib/result.dart (Result)"?>
```dart
/// Utility class that simplifies handling errors.
///
/// Return a [Result] from a function to indicate success or failure.
///
/// A [Result] is either an [Ok] with a value of type [T]
/// or an [Error] with an [Exception].
///
/// Use [Result.ok] to create a successful result with a value of type [T].
/// Use [Result.error] to create an error result with an [Exception].
///
/// Evaluate the result using a switch statement:
/// ```dart
/// switch (result) {
///   case Ok(): {
///     print(result.value);
///   }
///   case Error(): {
///     print(result.error);
///   }
/// }
/// ```
sealed class Result<T> {
  const Result();

  /// Creates a successful [Result], completed with the specified [value].
  const factory Result.ok(T value) = Ok._;

  /// Creates an error [Result], completed with the specified [error].
  const factory Result.error(Exception error) = Error._;
}

/// A successful [Result] with a returned [value].
final class Ok<T> extends Result<T> {
  const Ok._(this.value);

  /// The returned value of this result.
  final T value;

  @override
  String toString() => 'Result<$T>.ok($value)';
}

/// An error [Result] with a resulting [error].
final class Error<T> extends Result<T> {
  const Error._(this.error);

  /// The resulting error of this result.
  final Exception error;

  @override
  String toString() => 'Result<$T>.error($error)';
}
```

[Error handling documentation]: https://dart.dev/language/error-handling
[Flutter architecture guidelines]: /app-architecture
[Compass App example]: {{site.repo.samples}}/tree/main/compass_app
[pub.dev]: {{site.pub}}
[`result_dart`]: {{site.pub-pkg}}/result_dart
[`result_type`]: {{site.pub-pkg}}/result_type
[`multiple_result`]: {{site.pub-pkg}}/multiple_result
[`sealed`]: {{site.dart-site}}/language/class-modifiers#sealed
[switch result or expression]: {{site.dart-site}}/language/branches#switch-statements

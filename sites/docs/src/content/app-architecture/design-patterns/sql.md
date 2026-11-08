---
title: "Arquitetura de armazenamento persistente: SQL"
description: Salve dados complexos de aplicativos no dispositivo de um usuário com SQL.
contentTags:
  - data
  - SQL
iconPath: /assets/images/docs/app-architecture/design-patterns/sql-icon.svg
order: 2
ia-translate: true
---

<?code-excerpt path-base="app-architecture/todo_data_service"?>

A maioria dos aplicativos Flutter,
não importa quão pequenos ou grandes eles sejam,
pode exigir o armazenamento de dados no dispositivo do usuário em algum momento.
Por exemplo, chaves de API,
preferências do usuário ou dados que devem estar disponíveis offline.

Nesta receita,
você aprenderá como integrar o armazenamento persistente de dados complexos usando SQL
em um aplicativo Flutter seguindo o padrão de design de arquitetura Flutter.

Para aprender como armazenar dados de chave-valor mais simples,
dê uma olhada na receita do Cookbook:
[Arquitetura de armazenamento persistente: dados de chave-valor][Persistent storage architecture: Key-value data].

Para ler esta receita,
você deve estar familiarizado com SQL e SQLite.
Se precisar de ajuda, você pode ler a receita
[Persistir dados com SQLite][Persist data with SQLite] antes de ler esta.

Este exemplo usa [`sqflite`][] com o plugin [`sqflite_common_ffi`][],
que combinado oferece suporte para dispositivos móveis e desktop.
O suporte para web é fornecido no plugin experimental
[`sqflite_common_ffi_web`][], mas não está incluído neste exemplo.

## Aplicativo de exemplo: aplicativo de lista de tarefas {:#example-application-todo-list-application}

O aplicativo de exemplo consiste em uma única tela com uma barra de aplicativo na parte superior,
uma lista de itens e uma entrada de campo de texto na parte inferior.

<img src='/assets/images/docs/cookbook/architecture/todo_app_light.png'
class="site-mobile-screenshot" alt="Aplicativo ToDo em modo claro" >

O corpo do aplicativo contém o `TodoListScreen`.
Esta tela contém uma `ListView` de itens `ListTile`,
cada um representando um item ToDo.
Na parte inferior, um `TextField` permite que os usuários criem novos itens ToDo
escrevendo a descrição da tarefa e, em seguida, tocando no `FilledButton` "Adicionar".

Os usuários podem tocar no `IconButton` de exclusão para excluir o item ToDo.

A lista de itens ToDo é armazenada localmente usando um serviço de banco de dados,
e restaurada quando o usuário inicia o aplicativo.

:::note
O código-fonte completo e executável para este exemplo está
disponível em [`/examples/app-architecture/todo_data_service/`][].
:::

## Armazenando dados complexos com SQL {:#storing-complex-data-with-sql}

Essa funcionalidade segue o [design de arquitetura do Flutter][Flutter Architecture design] recomendado,
contendo uma camada de UI e uma camada de dados.
Além disso, na camada de domínio você encontrará o modelo de dados usado.

- Camada de UI com `TodoListScreen` e `TodoListViewModel`
- Camada de domínio com classe de dados `Todo`
- Camada de dados com `TodoRepository` e `DatabaseService`

### Camada de apresentação da lista de tarefas {:#todo-list-presentation-layer}

O `TodoListScreen` é um Widget que contém a UI responsável por exibir
e criar os itens ToDo.
Ele segue o [padrão MVVM][MVVM pattern]
e é acompanhado pelo `TodoListViewModel`,
que contém a lista de itens ToDo
e três comandos para carregar, adicionar e excluir itens ToDo.

Esta tela é dividida em duas partes,
uma contendo a lista de itens ToDo,
implementada usando um `ListView`,
e a outra é um `TextField`
e um `Button`, usado para criar novos itens ToDo.

O `ListView` é envolvido por um `ListenableBuilder`,
que ouve as mudanças no `TodoListViewModel`,
e mostra um `ListTile` para cada item ToDo.

<?code-excerpt "lib/ui/todo_list/widgets/todo_list_screen.dart (ListenableBuilder)" replace="/child: //g;/^\),$/)/g"?>
```dart
ListenableBuilder(
  listenable: widget.viewModel,
  builder: (context, child) {
    return ListView.builder(
      itemCount: widget.viewModel.todos.length,
      itemBuilder: (context, index) {
        final todo = widget.viewModel.todos[index];
        return ListTile(
          title: Text(todo.task),
          trailing: IconButton(
            icon: const Icon(Icons.delete),
            onPressed: () => widget.viewModel.delete.execute(todo.id),
          ),
        );
      },
    );
  },
)
```

A lista de itens ToDo é definida no `TodoListViewModel`,
e carregada pelo comando `load`.
Este método chama o `TodoRepository` e busca a lista de itens ToDo.

<?code-excerpt "lib/ui/todo_list/viewmodel/todo_list_viewmodel.dart (TodoListViewModel)"?>
```dart
List<Todo> _todos = [];

List<Todo> get todos => _todos;

Future<Result<void>> _load() async {
  try {
    final result = await _todoRepository.fetchTodos();
    switch (result) {
      case Ok<List<Todo>>():
        _todos = result.value;
        return Result.ok(null);
      case Error():
        return Result.error(result.error);
    }
  } on Exception catch (e) {
    return Result.error(e);
  } finally {
    notifyListeners();
  }
}
```

Pressionar o `FilledButton`,
executa o comando `add`
e passa o valor do controlador de texto.

<?code-excerpt "lib/ui/todo_list/widgets/todo_list_screen.dart (FilledButton)" replace="/^\),$/)/g"?>
```dart
FilledButton.icon(
  onPressed: () =>
      widget.viewModel.add.execute(_controller.text),
  label: const Text('Add'),
  icon: const Icon(Icons.add),
)
```

O comando `add` então chama o método `TodoRepository.createTodo()`
com o texto de descrição da tarefa e cria um novo item ToDo.

O método `createTodo()` retorna o ToDo recém-criado,
que é então adicionado à lista `_todo` no view model.

Os itens ToDo contêm um identificador exclusivo gerado pelo banco de dados.
É por isso que o view model não cria o item ToDo,
mas sim o `TodoRepository`.

<?code-excerpt "lib/ui/todo_list/viewmodel/todo_list_viewmodel.dart (Add)"?>
```dart
Future<Result<void>> _add(String task) async {
  try {
    final result = await _todoRepository.createTodo(task);
    switch (result) {
      case Ok<Todo>():
        _todos.add(result.value);
        return Result.ok(null);
      case Error():
        return Result.error(result.error);
    }
  } on Exception catch (e) {
    return Result.error(e);
  } finally {
    notifyListeners();
  }
}
```

Finalmente, o `TodoListScreen` também ouve o resultado no comando `add`.
Quando a ação é concluída, o `TextEditingController` é limpo.

<?code-excerpt "lib/ui/todo_list/widgets/todo_list_screen.dart (Add)"?>
```dart
void _onAdd() {
  // Clear the text field when the add command completes.
  if (widget.viewModel.add.completed) {
    widget.viewModel.add.clearResult();
    _controller.clear();
  }
}
```

Quando um usuário toca no `IconButton` no `ListTile`, o comando de exclusão é executado.

<?code-excerpt "lib/ui/todo_list/widgets/todo_list_screen.dart (Delete)" replace="/trailing: //g;/^\),$/)/g"?>
```dart
IconButton(
  icon: const Icon(Icons.delete),
  onPressed: () => widget.viewModel.delete.execute(todo.id),
)
```

Então, o view model chama o método `TodoRepository.deleteTodo()`,
passando o identificador exclusivo do item ToDo.
Um resultado correto remove o item ToDo do view
model *e* da tela.

<?code-excerpt "lib/ui/todo_list/viewmodel/todo_list_viewmodel.dart (Delete)"?>
```dart
Future<Result<void>> _delete(int id) async {
  try {
    final result = await _todoRepository.deleteTodo(id);
    switch (result) {
      case Ok<void>():
        _todos.removeWhere((todo) => todo.id == id);
        return Result.ok(null);
      case Error():
        return Result.error(result.error);
    }
  } on Exception catch (e) {
    return Result.error(e);
  } finally {
    notifyListeners();
  }
}
```

### Camada de domínio da lista de tarefas {:#todo-list-domain-layer}

A camada de domínio deste aplicativo de exemplo contém
o modelo de dados do item `Todo`.

Os itens são apresentados por uma classe de dados imutável.
Nesse caso, o aplicativo usa o pacote `freezed` para gerar o código.

A classe tem duas propriedades, um ID representado por um `int`,
e uma descrição de tarefa, representada por uma `String`.

<?code-excerpt "lib/business/model/todo.dart (Todo)"?>
```dart
@freezed
abstract class Todo with _$Todo {
  const factory Todo({
    /// The unique identifier of the Todo item.
    required int id,

    /// The task description of the Todo item.
    required String task,
  }) = _Todo;
}
```

### Camada de dados da lista de tarefas {:#todo-list-data-layer}

A camada de dados desta funcionalidade é composta por duas classes,
o `TodoRepository` e o `DatabaseService`.

O `TodoRepository` atua como a fonte da verdade para todos os itens ToDo.
Os view models devem usar este repositório para acessar a lista ToDo,
e ele não deve expor nenhum detalhe de implementação sobre como eles são armazenados.

Internamente, o `TodoRepository` usa o `DatabaseService`,
que implementa o acesso ao banco de dados SQL usando o pacote `sqflite`.
Você pode implementar o mesmo `DatabaseService` usando outros pacotes de armazenamento
como `sqlite3`, `drift` ou mesmo soluções de armazenamento em nuvem como `firebase_database`.

O `TodoRepository` verifica se o banco de dados está aberto
antes de cada solicitação e o abre se necessário.

Ele implementa os métodos `fetchTodos()`, `createTodo()` e `deleteTodo()`.

<?code-excerpt "lib/data/repositories/todo_repository.dart (TodoRepository)"?>
```dart
class TodoRepository {
  TodoRepository({required this._database});

  final DatabaseService _database;

  Future<Result<List<Todo>>> fetchTodos() async {
    if (!_database.isOpen()) {
      await _database.open();
    }
    return _database.getAll();
  }

  Future<Result<Todo>> createTodo(String task) async {
    if (!_database.isOpen()) {
      await _database.open();
    }
    return _database.insert(task);
  }

  Future<Result<void>> deleteTodo(int id) async {
    if (!_database.isOpen()) {
      await _database.open();
    }
    return _database.delete(id);
  }
}
```

O `DatabaseService` implementa o acesso ao banco de dados SQLite
usando o pacote `sqflite`.

É uma boa ideia definir a tabela e os nomes das colunas como constantes
para evitar erros de digitação ao escrever código SQL.

<?code-excerpt "lib/data/services/database_service.dart (Table)"?>
```dart
static const String _todoTableName = 'todo';
static const String _idColumnName = '_id';
static const String _taskColumnName = 'task';
```

O método `open()` abre o banco de dados existente,
ou cria um novo se ele não existir.

<?code-excerpt "lib/data/services/database_service.dart (Open)"?>
```dart
Future<void> open() async {
  _database = await databaseFactory.openDatabase(
    join(await databaseFactory.getDatabasesPath(), 'app_database.db'),
    options: OpenDatabaseOptions(
      onCreate: (db, version) {
        return db.execute(
          'CREATE TABLE $_todoTableName($_idColumnName INTEGER PRIMARY KEY AUTOINCREMENT, $_taskColumnName TEXT)',
        );
      },
      version: 1,
    ),
  );
}
```

Observe que a coluna `id` é definida como `chave primária` e `autoincremento`;
isso significa que a cada item recém-inserido
é atribuído um novo valor para a coluna `id`.

O método `insert()` cria um novo item ToDo no banco de dados,
e retorna uma instância ToDo recém-criada.
O `id` é gerado como mencionado anteriormente.

<?code-excerpt "lib/data/services/database_service.dart (Insert)"?>
```dart
Future<Result<Todo>> insert(String task) async {
  try {
    final id = await _database!.insert(_todoTableName, {
      _taskColumnName: task,
    });
    return Result.ok(Todo(id: id, task: task));
  } on Exception catch (e) {
    return Result.error(e);
  }
}
```

Todas as operações `DatabaseService` usam a classe `Result` para retornar um valor,
conforme recomendado pelas [recomendações de arquitetura do Flutter][Flutter architecture recommendations].
Isso facilita o tratamento de erros em etapas posteriores no código do aplicativo.

O método `getAll()` executa uma consulta de banco de dados,
obtendo todos os valores nas colunas `id` e `task`.
Para cada entrada, ele cria uma instância da classe `Todo`.

<?code-excerpt "lib/data/services/database_service.dart (GetAll)"?>
```dart
Future<Result<List<Todo>>> getAll() async {
  try {
    final entries = await _database!.query(
      _todoTableName,
      columns: [_idColumnName, _taskColumnName],
    );
    final list = entries
        .map(
          (element) => Todo(
            id: element[_idColumnName] as int,
            task: element[_taskColumnName] as String,
          ),
        )
        .toList();
    return Result.ok(list);
  } on Exception catch (e) {
    return Result.error(e);
  }
}
```

O método `delete()` executa uma operação de exclusão de banco de dados
com base no `id` do item ToDo.

Neste caso, se nenhum item foi excluído, um erro é retornado,
indicando que algo deu errado.

<?code-excerpt "lib/data/services/database_service.dart (Delete)"?>
```dart
Future<Result<void>> delete(int id) async {
  try {
    final rowsDeleted = await _database!.delete(
      _todoTableName,
      where: '$_idColumnName = ?',
      whereArgs: [id],
    );
    if (rowsDeleted == 0) {
      return Result.error(Exception('No todo found with id $id'));
    }
    return Result.ok(null);
  } on Exception catch (e) {
    return Result.error(e);
  }
}
```

:::note
Em alguns casos, você pode querer fechar o banco de dados quando terminar de usá-lo.
Por exemplo, quando o usuário sai da tela,
ou depois que um determinado tempo se passou.

Isso depende da implementação do banco de dados
assim como os requisitos do seu aplicativo.
É recomendável que você verifique com os autores do pacote do banco de dados
para obter recomendações.
:::

## Juntando tudo {:#putting-it-all-together}

No método `main()` do seu aplicativo,
primeiro inicialize o `DatabaseService`,
que requer um código de inicialização diferente em diferentes plataformas.
Em seguida, passe o `DatabaseService` recém-criado para o `TodoRepository`
que é ele próprio passado para o `MainApp` como uma dependência de argumento do construtor.

<?code-excerpt "lib/main.dart (MainTodo)"?>
```dart
void main() {
  final DatabaseService databaseService;
  if (kIsWeb) {
    throw UnsupportedError('Platform not supported');
  } else if (Platform.isLinux || Platform.isWindows || Platform.isMacOS) {
    // Initialize the FFI-based SQLite.
    sqfliteFfiInit();
    databaseService = DatabaseService(databaseFactory: databaseFactoryFfi);
  } else {
    // Use the default native SQLite.
    databaseService = DatabaseService(databaseFactory: databaseFactory);
  }

  runApp(
    MainApp(
      // ···
      todoRepository: TodoRepository(database: databaseService),
    ),
  );
}
```

Então, quando o `TodoListScreen` é criado,
também crie o `TodoListViewModel`
e passe o `TodoRepository` para ele como dependência.

<?code-excerpt "lib/main.dart (TodoListScreen)" replace="/body: //g;/^\),$/)/g"?>
```dart
TodoListScreen(
  viewModel: TodoListViewModel(todoRepository: widget.todoRepository),
)
```

[Flutter Architecture design]:/app-architecture
[Flutter architecture recommendations]:/app-architecture
[MVVM pattern]:/app-architecture/guide#mvvm
[Persist data with SQLite]:/cookbook/persistence/sqlite
[Persistent storage architecture: Key-value data]:/app-architecture/design-patterns/key-value-data
[`/examples/app-architecture/todo_data_service/`]: {{site.repo.this}}/tree/main/examples/app-architecture/todo_data_service/
[`sqflite_common_ffi_web`]:{{site.pub}}/packages/sqflite_common_ffi_web
[`sqflite_common_ffi`]:{{site.pub}}/packages/sqflite_common_ffi
[`sqflite`]:{{site.pub}}/packages/sqflite

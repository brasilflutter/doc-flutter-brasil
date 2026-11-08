---
title: Integração de funcionalidades
description: >
  Como integrar com outros recursos do Flutter.
prev:
  title: Experiência do usuário
  path: /ai/ai-toolkit/user-experience
next:
  title: Provedores de LLM personalizados
  path: /ai/ai-toolkit/custom-llm-providers
ia-translate: true
---

Além dos recursos que são fornecidos automaticamente pelo
[`LlmChatView`][], vários pontos de integração permitem que seu aplicativo
se misture perfeitamente com outros recursos para fornecer
funcionalidades adicionais:

* **Mensagens de boas-vindas**: Exiba uma saudação inicial aos usuários.
* **Sugestões de prompts**: Ofereça aos usuários prompts predefinidos para guiar as interações.
* **Instruções do sistema**: Forneça ao LLM entradas específicas para influenciar
  suas respostas.
* **Desativar anexos e entrada de áudio**: Remova partes opcionais da UI do chat.
* **Gerenciar o comportamento de cancelamento ou erro**: Altere o comportamento
  quando o usuário cancela ou quando ocorre um erro do LLM.
* **Gerenciamento do histórico**: Todo provedor de LLM permite o gerenciamento do
  histórico de chat, o que é útil para limpá-lo, alterá-lo dinamicamente e
  armazená-lo entre as sessões.
* **Serialização/desserialização de chat**: Armazene e recupere conversas entre
  sessões do aplicativo.
* **Widgets de resposta personalizados**: Introduza componentes de UI especializados
  para apresentar respostas de LLM.
* **Estilo personalizado**: Defina estilos visuais únicos para combinar a aparência
  do chat com o aplicativo geral.
* **Chat sem UI**: Interaja diretamente com os provedores de LLM sem afetar a sessão
  de chat atual do usuário.
* **Provedores de LLM personalizados**: Crie seu próprio provedor de LLM para
  integração do chat com seu próprio backend de modelo.
* **Redirecionamento de prompts**: Depure, registre ou redirecione mensagens
  destinadas ao provedor para rastrear problemas ou rotear prompts dinamicamente.

[`LlmChatView`]:
    {{site.pub-api}}/flutter_ai_toolkit/latest/flutter_ai_toolkit/LlmChatView-class.html

## Mensagens de boas-vindas {:#welcome-messages}

A visualização de chat permite que você forneça uma mensagem de boas-vindas
personalizada para definir o contexto para o usuário:

![Exemplo de mensagem de
boas-vindas](/assets/images/docs/ai-toolkit/example-of-welcome-message.png)

Você pode inicializar o `LlmChatView` com uma mensagem de boas-vindas
definindo o parâmetro `welcomeMessage`:

```dart
class ChatPage extends StatelessWidget {
 const ChatPage({super.key});

 @override
 Widget build(BuildContext context) => Scaffold(
       appBar: AppBar(title: const Text(App.title)),
       body: LlmChatView(
         welcomeMessage: 'Hello and welcome to the Flutter AI Toolkit!',
         provider: FirebaseProvider(
          model: FirebaseAI.geminiAI().generativeModel(
             model: 'gemini-2.5-flash',
           ),
         ),
       ),
     );
}
```

Para ver um exemplo completo de como definir a mensagem de boas-vindas,
consulte o [exemplo de boas-vindas][welcome example].

[welcome example]:
    https://github.com/flutter/ai/blob/main/example/lib/welcome/welcome.dart

## Sugestões de prompts {:#suggested-prompts}

Você pode fornecer um conjunto de sugestões de prompts para dar ao usuário uma
ideia do objetivo para o qual a sessão de chat foi otimizada:

![Exemplo de sugestões de
prompts](/assets/images/docs/ai-toolkit/example-of-suggested-prompts.png)

As sugestões são mostradas apenas quando não há histórico de chat existente.
Clicar em uma delas a envia imediatamente como uma solicitação ao LLM
subjacente. Para definir a lista de sugestões, construa o `LlmChatView` com o
parâmetro `suggestions`:

```dart
class ChatPage extends StatelessWidget {
 const ChatPage({super.key});

 @override
 Widget build(BuildContext context) => Scaffold(
       appBar: AppBar(title: const Text(App.title)),
       body: LlmChatView(
         suggestions: [
           'I\'m a Star Wars fan. What should I wear for Halloween?',
           'I\'m allergic to peanuts. What candy should I avoid at Halloween?',
           'What\'s the difference between a pumpkin and a squash?',
         ],
         provider: FirebaseProvider(
          model: FirebaseAI.geminiAI().generativeModel(
             model: 'gemini-2.5-flash',
           ),
         ),
       ),
     );
}
```

Para ver um exemplo completo de como configurar sugestões para o usuário, dê uma
olhada no [exemplo de sugestões][suggestions example].

[suggestions example]:
    https://github.com/flutter/ai/blob/main/example/lib/suggestions/suggestions.dart

## Instruções de LLM {:#llm-instructions}

Para otimizar as respostas de um LLM com base nas necessidades do seu
aplicativo, você vai querer fornecer instruções a ele. Por exemplo, o
[aplicativo de exemplo de receitas][recipes example app] usa o parâmetro
`systemInstructions` da classe `GenerativeModel` para adaptar o LLM para se
concentrar na entrega de receitas com base nas instruções do usuário:

```dart
class _HomePageState extends State<HomePage> {
  ...
  // cria um novo provedor com o histórico fornecido e as configurações atuais
  LlmProvider _createProvider([List<ChatMessage>? history]) => FirebaseProvider(
      history: history,
        ...,
        model: FirebaseAI.geminiAI().generativeModel(
          model: 'gemini-2.5-flash',
          ...,
          systemInstruction: Content.system('''
You are a helpful assistant that generates recipes based on the ingredients and
instructions provided as well as my food preferences, which are as follows:
${Settings.foodPreferences.isEmpty ? 'I don\'t have any food preferences' : Settings.foodPreferences}

You should keep things casual and friendly. You may generate multiple recipes in a single response, but only if asked. ...
''',
          ),
        ),
      );
  ...
}
```

Definir instruções do sistema é exclusivo para cada provedor; o
`FirebaseProvider` permite que você as forneça por meio do parâmetro
`systemInstruction`.

Observe que, neste caso, estamos trazendo as preferências do usuário como parte
da criação do provedor de LLM passado para o construtor `LlmChatView`.
Definimos as instruções como parte do processo de criação cada vez que o
usuário altera suas preferências. O aplicativo de receitas permite que o
usuário altere suas preferências alimentares usando um drawer no scaffold:

![Exemplo de refinamento de
prompt](/assets/images/docs/ai-toolkit/setting-food-preferences.png)

Sempre que o usuário altera suas preferências alimentares, o aplicativo de
receitas cria um novo modelo para usar as novas preferências:

```dart
class _HomePageState extends State<HomePage> {
  ...
  void _onSettingsSave() => setState(() {
        // move o histórico do provedor antigo para o novo
        final history = _provider.history.toList();
        _provider = _createProvider(history);
      });
}
```

## Chamada de funções {:#function-calling}

Para permitir que o LLM execute ações em nome do usuário, você pode fornecer um
conjunto de ferramentas (funções) que o LLM pode chamar. O `FirebaseProvider`
oferece suporte a chamada de funções nativamente. Ele cuida do ciclo de enviar
o prompt do usuário, receber uma solicitação de chamada de função do LLM,
executar a função e enviar o resultado de volta ao LLM até que uma resposta de
texto final seja gerada.

Para usar a chamada de funções, você precisa definir suas ferramentas e
passá-las para o `FirebaseProvider`. Confira o
[exemplo de chamada de funções][function calling example] para mais detalhes.

[function calling example]:
    https://github.com/flutter/ai/blob/main/example/lib/function_calls/function_calls.dart

## Desativar anexos e entrada de áudio {:#disable-attachments-and-audio-input}

Se você quiser desativar os anexos (o botão **+**) ou a entrada de áudio (o
botão de microfone), você pode fazer isso com os parâmetros `enableAttachments`
e `enableVoiceNotes` do construtor `LlmChatView`:

```dart
class ChatPage extends StatelessWidget {
  const ChatPage({super.key});

  @override
  Widget build(BuildContext context) {
    // ...

    return Scaffold(
      appBar: AppBar(title: const Text('Restricted Chat')),
      body: LlmChatView(
        // ...
        enableAttachments: false,
        enableVoiceNotes: false,
      ),
    );
  }
}
```

Ambas as flags têm `true` como padrão.

## Speech-to-text personalizado {:#custom-speech-to-text}

Por padrão, o AI Toolkit usa o `LlmProvider` passado para o `LlmChatView` para
fornecer a implementação de speech-to-text (conversão de fala em texto). Se
você quiser fornecer sua própria implementação, por exemplo, para usar um
serviço específico do dispositivo, você pode fazer isso implementando a
interface `SpeechToText` e passando-a para o construtor `LlmChatView`:

```dart
LlmChatView(
  // ...
  speechToText: MyCustomSpeechToText(),
)
```

Confira o [exemplo de STT personalizado][custom STT example] para mais detalhes.

[custom STT example]:
    https://github.com/flutter/ai/tree/main/example/lib/custom_stt

## Gerenciar o comportamento de cancelamento ou erro {:#manage-cancel-or-error-behavior}

Por padrão, quando o usuário cancela uma solicitação ao LLM, a string "CANCEL"
será anexada à resposta do LLM e uma mensagem aparecerá informando que o
usuário cancelou a solicitação. Da mesma forma, no caso de um erro do LLM, como
uma queda na conexão de rede, a string "ERROR" será anexada à resposta do LLM e
uma caixa de diálogo de alerta aparecerá com os detalhes do erro.

Você pode substituir o comportamento de cancelamento e de erro com os
parâmetros `cancelMessage`, `errorMessage`, `onCancelCallback` e
`onErrorCallback` do `LlmChatView`. Por exemplo, o código a seguir substitui o
tratamento padrão de cancelamento:

```dart
class ChatPage extends StatelessWidget {
  // ...

  void _onCancel(BuildContext context) {
    ScaffoldMessenger.of(
      context,
    ).showSnackBar(const SnackBar(content: Text('Chat cancelled')));
  }

  @override
  Widget build(BuildContext context) => Scaffold(
    appBar: AppBar(title: const Text(App.title)),
    body: LlmChatView(
      // ...
      onCancelCallback: _onCancel,
      cancelMessage: 'Request cancelled',
    ),
  );
}
```

Você pode substituir qualquer um desses parâmetros, ou todos eles, e o
`LlmChatView` usará seus padrões para tudo o que você não substituir.

## Gerenciando o histórico {:#manage-history}

A [interface padrão que define todos os provedores de LLM][providerIF] que podem
ser conectados à visualização de chat inclui a capacidade de obter e definir o
histórico do provedor:

```dart
abstract class LlmProvider implements Listenable {
  Stream<String> generateStream(
    String prompt, {
    Iterable<Attachment> attachments,
  });

  Stream<String> sendMessageStream(
    String prompt, {
    Iterable<Attachment> attachments,
  });

  Iterable<ChatMessage> get history;
  set history(Iterable<ChatMessage> history);
}
```

[providerIF]:
    {{site.pub-api}}/flutter_ai_toolkit/latest/flutter_ai_toolkit/LlmProvider-class.html

Quando o histórico de um provedor muda, ele chama o método `notifyListener`
exposto pela classe base `Listenable`. Isso significa que você se
inscreve/cancela a inscrição manualmente com os métodos `add` e `remove` ou o
usa para construir uma instância da classe `ListenableBuilder`.

O método `generateStream` chama o LLM subjacente sem afetar o histórico. Chamar
o método `sendMessageStream` altera o histórico adicionando duas novas mensagens
ao histórico do provedor — uma para a mensagem do usuário e uma para a resposta
do LLM — quando a resposta é concluída. A visualização de chat usa
`sendMessageStream` quando processa um prompt de chat do usuário e
`generateStream` quando está processando a entrada de voz do usuário.

Para ver ou definir o histórico, você pode acessar a propriedade `history`:

```dart
void _clearHistory() => _provider.history = [];
```

A capacidade de acessar o histórico de um provedor também é útil quando se
trata de recriar um provedor, mantendo o histórico:

```dart
class _HomePageState extends State<HomePage> {
  ...
  void _onSettingsSave() => setState(() {
        // move o histórico do provedor antigo para o novo
        final history = _provider.history.toList();
        _provider = _createProvider(history);
      });
}
```

O método `_createProvider` cria um novo provedor com o histórico do provedor
anterior _e_ as novas preferências do usuário. É transparente para o usuário;
ele pode continuar conversando, mas agora o LLM fornece respostas levando em
consideração suas novas preferências alimentares. Por exemplo:


```dart
class _HomePageState extends State<HomePage> {
  ...
  // cria um novo provedor com o histórico fornecido e as configurações atuais
  LlmProvider _createProvider([List<ChatMessage>? history]) =>
    FirebaseProvider(
      history: history,
      ...
    );
  ...
}
```

Para ver o histórico em ação, confira o
[aplicativo de exemplo de receitas][recipes example app] e o
[aplicativo de exemplo de histórico][history example app].

[history example app]:
    https://github.com/flutter/ai/blob/main/example/lib/history/history.dart
[recipes example app]: https://github.com/flutter/ai/tree/main/example/lib/recipes

## Serialização/desserialização de chat {:#chat-serializationdeserialization}

Para salvar e restaurar o histórico de chat entre sessões de um aplicativo, é
necessária a capacidade de serializar e desserializar cada prompt do usuário,
incluindo os anexos, e cada resposta do LLM. Ambos os tipos de mensagens (os
prompts do usuário e as respostas do LLM) são expostos na classe `ChatMessage`.
A serialização pode ser realizada usando o método `toJson` de cada instância de
`ChatMessage`.

```dart
Future<void> _saveHistory() async {
  // obtém o histórico mais recente
  final history = _provider.history.toList();

  // escreve as novas mensagens
  for (var i = 0; i != history.length; ++i) {
    // pula se o arquivo já existir
    final file = await _messageFile(i);
    if (file.existsSync()) continue;

    // escreve a nova mensagem no disco
    final map = history[i].toJson();
    final json = JsonEncoder.withIndent('  ').convert(map);
    await file.writeAsString(json);
  }
}
```

Da mesma forma, para desserializar, use o método estático `fromJson` da classe
`ChatMessage`:

```dart
Future<void> _loadHistory() async {
  // lê o histórico do disco
  final history = <ChatMessage>[];
  for (var i = 0;; ++i) {
    final file = await _messageFile(i);
    if (!file.existsSync()) break;

    final map = jsonDecode(await file.readAsString());
    history.add(ChatMessage.fromJson(map));
  }

  // define o histórico no controlador
  _provider.history = history;
}
```

Para garantir um retorno rápido ao serializar, recomendamos escrever cada
mensagem do usuário apenas uma vez. Caso contrário, o usuário deve esperar que
seu aplicativo escreva todas as mensagens todas as vezes e, diante de anexos
binários, isso pode levar um tempo.

Para ver isso em ação, consulte o
[aplicativo de exemplo de histórico][history example app].

[history example app]:
    https://github.com/flutter/ai/blob/main/example/lib/history/history.dart

## Widgets de resposta personalizados {:#custom-response-widgets}

Por padrão, a resposta do LLM exibida pela visualização de chat é formatada em
Markdown. No entanto, em alguns casos, você deseja criar um widget
personalizado para mostrar a resposta do LLM que seja específica e integrada ao
seu aplicativo. Por exemplo, quando o usuário solicita uma receita no
[aplicativo de exemplo de receitas][recipes example app], a resposta do LLM é
usada para criar um widget específico para exibir receitas, como o resto do
aplicativo, e para fornecer um botão **Adicionar** caso o usuário queira
adicionar a receita ao seu banco de dados:

![Botão Adicionar receita](/assets/images/docs/ai-toolkit/add-recipe-button.png)

Isso é realizado definindo o parâmetro `responseBuilder` do construtor
`LlmChatView`:

```dart
LlmChatView(
  provider: _provider,
  welcomeMessage: _welcomeMessage,
  responseBuilder: (context, response) => RecipeResponseView(
    response,
  ),
),
```

Neste exemplo específico, o widget `RecipeResponseView` é construído com o
texto de resposta do provedor de LLM e o usa para implementar seu método
`build`:

```dart
class RecipeResponseView extends StatelessWidget {
  const RecipeResponseView(this.response, {super.key});
  final String response;

  @override
  Widget build(BuildContext context) {
    final children = <Widget>[];
    String? finalText;

    // criado com a resposta do LLM à medida que as respostas chegam, então
    // pode não ser uma resposta completa ainda
    try {
      final map = jsonDecode(response);
      final recipesWithText = map['recipes'] as List<dynamic>;
      finalText = map['text'] as String?;

      for (final recipeWithText in recipesWithText) {
        // extrai o texto antes da receita
        final text = recipeWithText['text'] as String?;
        if (text != null && text.isNotEmpty) {
          children.add(MarkdownBody(data: text));
        }

        // extrai a receita
        final json = recipeWithText['recipe'] as Map<String, dynamic>;
        final recipe = Recipe.fromJson(json);
        children.add(const Gap(16));
        children.add(Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(recipe.title, style: Theme.of(context).textTheme.titleLarge),
            Text(recipe.description),
            RecipeContentView(recipe: recipe),
          ],
        ));

        // adiciona um botão para adicionar a receita à lista
        children.add(const Gap(16));
        children.add(OutlinedButton(
          onPressed: () => RecipeRepository.addNewRecipe(recipe),
          child: const Text('Add Recipe'),
        ));
        children.add(const Gap(16));
      }
    } catch (e) {
      debugPrint('Error parsing response: $e');
    }

    ...

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: children,
    );
  }
}
```

Este código analisa o texto para extrair o texto introdutório e a receita do
LLM, agrupando-os com um botão **Adicionar Receita** para exibir no lugar do
Markdown.

Observe que estamos analisando a resposta do LLM como JSON. É comum definir o
provedor no modo JSON e fornecer um esquema para restringir o formato de suas
respostas para garantir que temos algo que podemos analisar. Cada provedor
expõe essa funcionalidade de sua própria maneira, mas a classe
`FirebaseProvider` habilita isso com um objeto `GenerationConfig` que o exemplo
de receitas usa da seguinte forma:

```dart
class _HomePageState extends State<HomePage> {
  ...

  // cria um novo provedor com o histórico fornecido e as configurações atuais
  LlmProvider _createProvider([List<ChatMessage>? history]) => FirebaseProvider(
        ...
        model: FirebaseAI.geminiAI().generativeModel(
          ...
          generationConfig: GenerationConfig(
            responseMimeType: 'application/json',
            responseSchema: Schema(...),
          systemInstruction: Content.system('''
...
Generate each response in JSON format
with the following schema, including one or more "text" and "recipe" pairs as
well as any trailing text commentary you care to provide:

{
  "recipes": [
    {
      "text": "Any commentary you care to provide about the recipe.",
      "recipe":
      {
        "title": "Recipe Title",
        "description": "Recipe Description",
        "ingredients": ["Ingredient 1", "Ingredient 2", "Ingredient 3"],
        "instructions": ["Instruction 1", "Instruction 2", "Instruction 3"]
      }
    }
  ],
  "text": "any final commentary you care to provide",
}
''',
          ),
        ),
      );
  ...
}
```

Este código inicializa o objeto `GenerationConfig` definindo o parâmetro
`responseMimeType` para `'application/json'` e o parâmetro `responseSchema`
para uma instância da classe `Schema` que define a estrutura do JSON que você
está preparado para analisar. Além disso, é uma boa prática também pedir em
JSON e fornecer uma descrição desse esquema JSON nas instruções do sistema, o
que fizemos aqui.

Para ver isso em ação, confira o
[aplicativo de exemplo de receitas][recipes example app].

## Estilo personalizado {:#custom-styling}

A visualização de chat vem pronta com um conjunto de estilos padrão para o
fundo, o campo de texto, os botões, os ícones, as sugestões e assim por diante.
Você pode personalizar totalmente esses estilos definindo os seus próprios
usando o parâmetro `style` no construtor `LlmChatView`:

```dart
LlmChatView(
  provider: FirebaseProvider(...),
  style: LlmChatViewStyle(...),
),
```

Por exemplo, o [aplicativo de exemplo de estilos personalizados][custom-ex] usa
esse recurso para implementar um aplicativo com um tema de Halloween:

![Aplicativo de demonstração com tema de Halloween](/assets/images/docs/ai-toolkit/demo-app.png)

Para obter uma lista completa dos estilos disponíveis na classe
`LlmChatViewStyle`, consulte a
[documentação de referência][reference documentation]. Você também pode
personalizar a aparência do gravador de voz usando o parâmetro
`voiceNoteRecorderStyle` da classe `LlmChatViewStyle`, o que é demonstrado no
[exemplo de estilos][styles-ex].

Para ver estilos personalizados em ação, além do
[exemplo de estilos personalizados][custom-ex] e do
[exemplo de estilos][styles-ex], confira o
[exemplo de modo escuro][dark mode example] e o
[aplicativo de demonstração][demo app].

[custom-ex]:
    https://github.com/flutter/ai/blob/main/example/lib/custom_styles/custom_styles.dart
[styles-ex]: https://github.com/flutter/ai/blob/main/example/lib/styles/styles.dart
[dark mode example]:
    https://github.com/flutter/ai/blob/main/example/lib/dark_mode/dark_mode.dart
[demo app]: https://github.com/flutter/ai#online-demo
[reference documentation]:
    {{site.pub-api}}/flutter_ai_toolkit/latest/flutter_ai_toolkit/LlmChatViewStyle-class.html

## Chat sem UI {:#chat-without-ui}

Você não precisa usar a visualização de chat para acessar a funcionalidade do
provedor subjacente. Além de poder simplesmente chamá-lo com qualquer interface
proprietária que ele forneça, você também pode usá-lo com a
[interface LlmProvider][LlmProvider interface].

[LlmProvider interface]:
    {{site.pub-api}}/flutter_ai_toolkit/latest/flutter_ai_toolkit/LlmProvider-class.html

Como exemplo, o aplicativo de exemplo de receitas fornece um botão Mágico na
página para editar receitas. O propósito desse botão é atualizar uma receita
existente em seu banco de dados com suas preferências alimentares atuais.
Pressionar o botão permite que você visualize as alterações recomendadas e
decida se deseja aplicá-las ou não:

![Usuário decide se atualiza a receita no banco de
dados](/assets/images/docs/ai-toolkit/apply-changes-decision.png)

Em vez de usar o mesmo provedor que a parte de chat do aplicativo usa, o que
inseriria mensagens de usuário espúrias e respostas de LLM no histórico de chat
do usuário, a página Editar Receita cria seu próprio provedor e o usa
diretamente:

```dart
class _EditRecipePageState extends State<EditRecipePage> {
  ...
  final _provider = FirebaseProvider(...);
  ...
  Future<void> _onMagic() async {
    final stream = _provider.sendMessageStream(
      'Generate a modified version of this recipe based on my food preferences: '
      '${_ingredientsController.text}\n\n${_instructionsController.text}',
    );
    var response = await stream.join();
    final json = jsonDecode(response);

    try {
      final modifications = json['modifications'];
      final recipe = Recipe.fromJson(json['recipe']);

      if (!context.mounted) return;
      final accept = await showDialog<bool>(
        context: context,
        builder: (context) => AlertDialog(
          title: Text(recipe.title),
          content: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text('Modifications:'),
              const Gap(16),
              Text(_wrapText(modifications)),
            ],
          ),
          actions: [
            TextButton(
              onPressed: () => context.pop(true),
              child: const Text('Accept'),
            ),
            TextButton(
              onPressed: () => context.pop(false),
              child: const Text('Reject'),
            ),
          ],
        ),
      );
      ...
    } catch (ex) {
      ...
      }
    }
  }
}
```

A chamada para `sendMessageStream` cria entradas no histórico do provedor, mas
como não está associada a uma visualização de chat, elas não serão exibidas. Se
for conveniente, você também pode realizar a mesma coisa chamando
`generateStream`, o que permite reutilizar um provedor existente sem afetar o
histórico de chat.

Para ver isso em ação, confira a [página Editar Receita][Edit Recipe page] do
exemplo de receitas.

[Edit Recipe page]:
    https://github.com/flutter/ai/blob/main/example/lib/recipes/pages/edit_recipe_page.dart

## Redirecionamento de prompts {:#rerouting-prompts}

Se você quiser depurar, registrar ou manipular a conexão entre a visualização
de chat e o provedor subjacente, você pode fazer isso com uma implementação de
uma função [`LlmStreamGenerator`][]. Em seguida, você passa essa função para o
`LlmChatView` no parâmetro `messageSender`:

[`LlmStreamGenerator`]:
    {{site.pub-api}}/flutter_ai_toolkit/latest/flutter_ai_toolkit/LlmStreamGenerator.html

```dart
class ChatPage extends StatelessWidget {
  final _provider = FirebaseProvider(...);

  @override
  Widget build(BuildContext context) => Scaffold(
      appBar: AppBar(title: const Text(App.title)),
      body: LlmChatView(
        provider: _provider,
        messageSender: _logMessage,
      ),
    );

  Stream<String> _logMessage(
    String prompt, {
    required Iterable<Attachment> attachments,
  }) async* {
    // registra a mensagem e os anexos
    debugPrint('# Sending Message');
    debugPrint('## Prompt\n$prompt');
    debugPrint('## Attachments\n${attachments.map((a) => a.toString())}');

    // encaminha a mensagem para o provedor
    final response = _provider.sendMessageStream(
      prompt,
      attachments: attachments,
    );

    // registra a resposta
    final text = await response.join();
    debugPrint('## Response\n$text');

    // retorna
    yield text;
  }
}
```

Este exemplo registra os prompts do usuário e as respostas do LLM conforme eles
vão e voltam. Ao fornecer uma função como `messageSender`, é sua
responsabilidade chamar o provedor subjacente. Se você não o fizer, ele não
receberá a mensagem. Essa capacidade permite que você faça coisas avançadas
como rotear para um provedor dinamicamente ou Geração Aumentada por Recuperação
(RAG, Retrieval Augmented Generation).

Para ver isso em ação, consulte o
[aplicativo de exemplo de registro][logging example app].

[logging example app]:
    https://github.com/flutter/ai/blob/main/example/lib/logging/logging.dart

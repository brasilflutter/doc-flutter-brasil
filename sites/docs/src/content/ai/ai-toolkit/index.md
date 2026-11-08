---
title: Flutter AI Toolkit
shortTitle: AI Toolkit
description: >
  Aprenda como adicionar o chatbot AI Toolkit
  ao seu aplicativo Flutter.
next:
  title: Experiência do usuário
  path: /ai/ai-toolkit/user-experience
ia-translate: true
---

Olá e bem-vindo ao Flutter AI Toolkit!

O AI Toolkit é um conjunto de widgets relacionados ao chat de IA que facilitam
a adição de uma janela de chat de IA ao seu aplicativo Flutter. O AI Toolkit
é organizado em torno de uma API abstrata de provedor de LLM para facilitar
a troca do provedor de LLM que você gostaria que seu provedor de chat usasse.
Ele já vem com suporte para o
[Firebase AI Logic][].

[Firebase AI Logic]: https://firebase.google.com/docs/ai-logic

## Principais recursos {:#key-features}

* **Chat multiturno**: Mantém o contexto em várias interações.
* **Respostas de streaming**: Exibe respostas de IA em tempo real à medida que
  são geradas.
* **Exibição de rich text**: Suporta texto formatado em mensagens de chat.
* **Entrada de voz**: Permite que os usuários insiram prompts usando a fala.
* **Anexos multimídia**: Permite o envio e o recebimento de vários tipos de mídia.
* **Chamada de funções**: Suporta chamadas de ferramentas (tool calls) para o provedor de LLM.
* **Estilo personalizado**: Oferece ampla personalização para corresponder ao design do seu aplicativo.
* **Serialização/desserialização de chat**: Armazene e recupere conversas
  entre sessões de aplicativos.
* **Widgets de resposta personalizados**: Introduza componentes de UI especializados para
  apresentar respostas de LLM.
* **Suporte LLM plugável**: Implemente uma interface simples para conectar seu próprio
  LLM.
* **Suporte multiplataforma**: Compatível com as plataformas Android, iOS, web e
  macOS.

## Demonstração {:#demo}

Veja como fica o exemplo de demonstração hospedando o AI Toolkit:

<img src="/assets/images/docs/ai-toolkit/ai-toolkit-app.png" alt="Aplicativo de demonstração de IA">

O [código-fonte desta demonstração][src-code] está disponível no repositório no GitHub.

[src-code]: https://github.com/flutter/ai/blob/main/example/lib/demo/demo.dart

## Começar {:#get-started}

<ol>
<li><b>Instalação</b>

Adicione as seguintes dependências ao seu arquivo `pubspec.yaml`:

```yaml
dependencies:
  flutter_ai_toolkit: ^latest_version
  firebase_ai: ^latest_version
  firebase_core: ^latest_version
```
</li>

<li><b>Configuração</b>

O AI Toolkit oferece suporte tanto à Gemini Developer API (para prototipagem) quanto ao
endpoint de produção do Firebase AI Logic. Ambos exigem um projeto Firebase e que o
pacote `firebase_core` seja inicializado, conforme descrito na documentação [Começar com
a API Gemini usando os SDKs do Firebase AI Logic][firebase_ai].

[firebase_ai]:
    https://firebase.google.com/docs/ai-logic/get-started?platform=flutter

Depois de concluir, integre o novo projeto Firebase ao seu aplicativo Flutter
usando a ferramenta `flutterfire CLI`, conforme descrito na documentação [Adicionar o
Firebase ao seu aplicativo Flutter][firebase].

[firebase]: https://firebase.google.com/docs/flutter/setup

Depois de seguir estas instruções, você está pronto para usar o Firebase para integrar IA
no seu aplicativo Flutter. Comece inicializando o Firebase:

```dart
import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_ai/firebase_ai.dart';
import 'package:flutter_ai_toolkit/flutter_ai_toolkit.dart';

// ... other imports

import 'firebase_options.dart'; // from `flutterfire config`

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp(options: DefaultFirebaseOptions.currentPlatform);
  runApp(const App());
}

// ...app stuff here
```

Com o Firebase inicializado corretamente no seu aplicativo Flutter, você agora está pronto para
criar uma instância do provedor Firebase. Você pode fazer isso de duas maneiras. Para
prototipagem, considere o endpoint do Gemini AI:

```dart
import 'package:firebase_ai/firebase_ai.dart';
import 'package:flutter_ai_toolkit/flutter_ai_toolkit.dart';

// ... app stuff here

class ChatPage extends StatelessWidget {
  const ChatPage({super.key});

  @override
  Widget build(BuildContext context) => Scaffold(
        appBar: AppBar(title: const Text(App.title)),
        // create the chat view, passing in the Firebase provider
        body: LlmChatView(
          provider: FirebaseProvider(
            // Use the Google AI endpoint
            model: FirebaseAI.googleAI().generativeModel(
              model: 'gemini-2.5-flash',
            ),
          ),
        ),
      );
}
```

A classe `FirebaseProvider` expõe o SDK do Firebase AI Logic ao
`LlmChatView`. Observe que você fornece um nome de modelo ([você tem várias
opções][options] para escolher), mas não fornece uma chave de API. Tudo
isso é tratado como parte do projeto Firebase.

Para cargas de trabalho de produção, é fácil trocar para o endpoint de produção
do Firebase AI Logic:

```dart
class ChatPage extends StatelessWidget {
  const ChatPage({super.key});

  @override
  Widget build(BuildContext context) => Scaffold(
        appBar: AppBar(title: const Text(App.title)),
        body: LlmChatView(
          provider: FirebaseProvider(
            // Use the production endpoint
            model: FirebaseAI.vertexAI().generativeModel(
              model: 'gemini-2.5-flash',
            ),
          ),
        ),
      );
}
```


Para um exemplo completo, confira os exemplos [gemini.dart] e
[vertex.dart][].

[options]:
    https://firebase.google.com/docs/ai-logic/models
[gemini.dart]:
    https://github.com/flutter/ai/blob/main/example/lib/gemini/gemini.dart
[vertex.dart]:
    https://github.com/flutter/ai/blob/main/example/lib/vertex/vertex.dart
</li>

<li><b>Configurar permissões do dispositivo</b>

Para permitir que seus usuários aproveitem recursos como entrada de voz e anexos
de mídia, certifique-se de que seu aplicativo tenha as permissões necessárias:

* **Acesso à rede:** Para habilitar o acesso à rede no macOS, adicione o seguinte aos
  seus arquivos `*.entitlements`:

  ```xml
  <plist version="1.0">
    <dict>
      ...
      <key>com.apple.security.network.client</key>
      <true/>
    </dict>
  </plist>
  ```

  Para habilitar o acesso à rede no Android, certifique-se de que seu arquivo
  `AndroidManifest.xml` contenha o seguinte:

  ```xml
  <manifest xmlns:android="http://schemas.android.com/apk/res/android">
      ...
      <uses-permission android:name="android.permission.INTERNET"/>
  </manifest>
  ```

* **Acesso ao microfone**: Configure de acordo com as [instruções de configuração de
  permissão do pacote record][record].
* **Seleção de arquivo**: Siga as [instruções do plugin file_selector][file].
* **Seleção de imagem**: Para tirar uma foto _ou_ selecionar uma foto do seu
  dispositivo, consulte as [instruções de instalação do plugin
  image_picker][image_picker].
* **Foto da web**: Para tirar uma foto na web, configure o aplicativo de acordo com
  as [instruções de configuração do plugin camera][camera].

[camera]: {{site.pub-pkg}}/camera#setup
[file]: {{site.pub-pkg}}/file_selector#usage
[image_picker]: {{site.pub-pkg}}/image_picker#installation
[record]: {{site.pub-pkg}}/record#setup-permissions-and-others
</li>
</ol>

## Exemplos {:#examples}

**firebase_options.dart**

Para usar o [aplicativo de exemplo do Firebase AI Logic][vertex-ex],
coloque os detalhes de configuração do Firebase no
arquivo `example/lib/firebase_options.dart`.
Você pode fazer isso com a ferramenta `flutterfire CLI` conforme descrito na
documentação [Adicionar o Firebase ao seu aplicativo Flutter][add-fb]
**de dentro do diretório `example`**.

:::note Considerações de segurança para `firebase_options.dart`

Se o seu aplicativo Flutter chama as APIs do Gemini diretamente do cliente,
não faça commit do `firebase_options.dart` em um repositório público.
Qualquer pessoa poderia reutilizar a configuração do seu aplicativo para enviar solicitações ao seu endpoint de IA,
consumindo cota e potencialmente gerando custos de faturamento.

Embora este guia mostre chamadas diretas do lado do cliente por simplicidade, em aplicativos
de produção você deve encaminhar as solicitações de IA por meio de um serviço de backend (por exemplo, [Cloud
Functions for Firebase](https://firebase.google.com/docs/functions), [Cloud
Run](https://cloud.google.com/run) ou seu próprio servidor). Nessa configuração, o
backend — e não o cliente — controla o acesso, e incluir o
`firebase_options.dart` no seu repositório é seguro.

Você também deve revisar e seguir a [lista de verificação de segurança do Firebase](https://firebase.google.com/support/guides/security-checklist).
:::

## Feedback

Ao longo do caminho, ao usar este pacote, por favor, [registre problemas e solicitações
de recursos][file-issues], bem como envie qualquer [código que você gostaria de
contribuir][submit]. Queremos seu feedback e suas contribuições para garantir que
o AI Toolkit seja o mais robusto e útil possível para seus aplicativos
do mundo real.

[add-fb]: https://firebase.google.com/docs/flutter/setup
[example apps]: https://github.com/flutter/ai/tree/main/example/lib
[file-issues]: https://github.com/flutter/ai/issues
[submit]: https://github.com/flutter/ai/pulls
[vertex-ex]: https://github.com/flutter/ai/blob/main/example/lib/vertex/vertex.dart

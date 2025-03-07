---
ia-translate: true
title: Depure seu módulo add-to-app
short-title: Depuração
description: Como executar, depurar e hot reload seu módulo Flutter add-to-app.
---

Uma vez que você tenha integrado o módulo Flutter ao seu projeto e usado
as APIs de plataforma do Flutter para executar o engine (motor) e/ou UI (interface do usuário) do Flutter,
você pode então construir e executar seu app Android ou iOS da mesma forma
que você executa apps Android ou iOS normais.

O Flutter agora alimenta a UI onde quer que seu código inclua
`FlutterActivity` ou `FlutterViewController`.

## Overview (Visão Geral)

Você pode estar acostumado a ter seu conjunto de ferramentas de depuração Flutter favoritas
disponíveis ao executar `flutter run` ou um comando equivalente de uma IDE (ambiente de desenvolvimento integrado).
Mas você também pode usar todas as suas [funcionalidades de depuração][] do Flutter, como
hot reload, *performance overlays* (sobreposições de desempenho), DevTools e definição de *breakpoints* (pontos de interrupção) em
cenários *add-to-app*.

O comando `flutter attach` fornece essas funcionalidades.
Para executar este comando, você pode usar as ferramentas de CLI (interface de linha de comando) do SDK (kit de desenvolvimento de software), VS Code
ou IntelliJ IDEA ou Android Studio.

O comando `flutter attach` se conecta assim que você executa seu `FlutterEngine`.
Ele permanece conectado até que você descarte seu `FlutterEngine`.
Você pode invocar `flutter attach` antes de iniciar seu *engine*.
O comando `flutter attach` aguarda pela próxima Dart VM (máquina virtual Dart) disponível que
seu *engine* hospeda.

## Debug from the Terminal (Depurar pelo Terminal)

Para conectar-se pelo terminal, execute `flutter attach`.
Para selecionar um dispositivo alvo específico, adicione `-d <deviceId>`.

```console
$ flutter attach
```

O comando deve imprimir uma saída semelhante à seguinte:

```console
Syncing files to device iPhone 15 Pro...
 7,738ms (!)

To hot reload the changes while running, press "r".
To hot restart (and rebuild state). press "R".
An Observatory debugger and profiler on iPhone 15 Pro is available at:
http://127.0.0.1:65525/EXmCgco5zjo=/
For a more detailed help message, press "h".
To detach, press "d"; to quit, press "q".
```

## Debug iOS extension in Xcode and VS Code (Depurar extensão iOS no Xcode e VS Code)

{% include docs/debug/debug-flow-ios.md add='launch' %}

## Debug Android extension in Android Studio (Depurar extensão Android no Android Studio)

{% include docs/debug/debug-flow-androidstudio-as-start.md %}

[debugging functionalities]: /testing/debugging

## Debug without USB connection {:#wireless-debugging}

Para depurar seu app via Wi-Fi em um dispositivo iOS ou Android,
use `flutter attach`.

### Debug over Wi-Fi on iOS devices (Depurar via Wi-Fi em dispositivos iOS)

Para um alvo iOS, complete os seguintes passos:

1. Verifique se seu dispositivo se conecta ao Xcode via Wi-Fi
   como descrito no [guia de configuração do iOS][].

1. Na sua máquina de desenvolvimento macOS,
   abra o **Xcode** <span aria-label="e então">></span>
   **Product** (Produto) <span aria-label="e então">></span>
   **Scheme** (Esquema) <span aria-label="e então">></span>
   **Edit Scheme...** (Editar Esquema...).

   Você também pode pressionar <kbd>Cmd</kbd> + <kbd><</kbd>.

1. Clique em **Run** (Executar).

1. Clique em **Arguments** (Argumentos).

1. Em **Arguments Passed On Launch** (Argumentos Passados na Inicialização), Clique em **+**.

   {:type="a"}
   1. Se sua máquina de desenvolvimento usa IPv4, adicione `--vm-service-host=0.0.0.0`.

   1. Se sua máquina de desenvolvimento usa IPv6, adicione `--vm-service-host=::0`.

   {% render docs/app-figure.md, img-class:"site-mobile-screenshot border", image:"development/add-to-app/debugging/wireless-port.png",
   caption:"Arguments Passed On Launch com uma rede IPv4 adicionada", width:"100%" %}

#### To determine if you're on an IPv6 network (Para determinar se você está em uma rede IPv6)

1. Abra **Settings** (Ajustes) <span aria-label="e então">></span> **Wi-Fi**.

1. Clique na sua rede conectada.

1. Clique em **Details...** (Detalhes...).

1. Clique em **TCP/IP**.

1. Verifique se há uma seção **IPv6 address** (endereço IPv6).

   {% render docs/app-figure.md, img-class:"site-mobile-screenshot border", image:"development/add-to-app/ipv6.png", caption:"Caixa de diálogo WiFi para Ajustes de Sistema do macOS", width:"60%" %}

### Debug over Wi-Fi on Android devices (Depurar via Wi-Fi em dispositivos Android)

Verifique se seu dispositivo se conecta ao Android Studio via Wi-Fi
como descrito no [guia de configuração do Android][].

[iOS setup guide]: /get-started/install/macos/mobile-ios
[Android setup guide]: /get-started/install/macos/mobile-android?tab=physical#configure-your-target-android-device

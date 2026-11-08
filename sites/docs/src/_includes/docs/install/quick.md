<!-- ia-translate: true -->

Aprenda a usar o [Visual Studio Code (VS Code)][VS Code] ou qualquer editor compatível
baseado no Code OSS para instalar e configurar rapidamente seu
ambiente de desenvolvimento Flutter.

Se você prefere outro editor ou IDE,
pode [instalar o Flutter manualmente][install Flutter manually].

[VS Code]: https://code.visualstudio.com
[install Flutter manually]: /install/manual

## Confirme sua plataforma de desenvolvimento {: #dev-platform}

Estas instruções estão configuradas para **Windows**{:.selected-os-text}.
Se você usa outro sistema operacional,
selecione-o entre as opções a seguir:

<OSSelector />

## Baixe os softwares necessários {: #download-prerequisites}

Para uma configuração do Flutter mais tranquila,
instale primeiro as ferramentas a seguir.

 1. <h3>Configure o suporte a Linux</h3>

    Se você ainda não configurou o suporte a Linux no seu Chromebook,
    [ative o suporte a Linux][chromeos-linux].

    Se você já ativou o suporte a Linux,
    confira se ele está atualizado seguindo as instruções de
    [Corrigir problemas com o Linux][chromeos-linux-update].

 1. <h3>Baixe e instale os pacotes necessários</h3>

    Usando o `apt-get` ou o mecanismo de instalação de sua preferência,
    instale as versões mais recentes dos seguintes pacotes:

    - `curl`
    - `git`
    - `unzip`
    - `xz-utils`
    - `zip`
    - `libglu1-mesa`

    Se você quiser usar o `apt-get`,
    instale esses pacotes com os seguintes comandos:

    ```console
    $ sudo apt-get update -y && sudo apt-get upgrade -y
    $ sudo apt-get install -y curl git unzip xz-utils zip libglu1-mesa
    ```

 1. <h3>Baixe e instale o Visual Studio Code</h3>

    Para instalar o Flutter rapidamente e depois editar e depurar seus apps,
    [instale e configure o Visual Studio Code][vscode-install]
    (ou o editor baseado no Code OSS de sua preferência).

{: .steps .chromeos-only}

<div class="macos-only">

:::warning
**Observação para Macs com Intel:**
O Flutter está descontinuando o suporte a Macs com processador Intel (x64).
Versões futuras do Flutter vão exigir Apple Silicon.
Para mais detalhes, confira a
[estratégia de descontinuação do macOS Intel](https://docs.google.com/document/d/1ty3js_Eg2sNIbDuyYS_aV7h4jYdx1hEpX_mV135gO4s/edit?tab=t.0#heading=h.cx7d8y57ce6p).
:::

</div>

 1. <h3>Instale as ferramentas de linha de comando do Xcode</h3>

    **Se você já tem o Git instalado,**
    pode pular para a próxima etapa: Baixe e instale o Visual Studio Code.

    Baixe as ferramentas de linha de comando do Xcode para ter acesso às
    ferramentas de linha de comando das quais o Flutter depende, incluindo o Git.
    Elas também são necessárias quando você gera builds para iOS ou macOS.

    Para baixar as ferramentas, execute o seguinte comando no terminal de sua preferência:

    ```console
    $ xcode-select --install
    ```

    Se você ainda não instalou as ferramentas,
    deve abrir uma caixa de diálogo pedindo para confirmar a instalação.
    Clique em **Install** e, quando a instalação terminar, clique em **Done**.

 1. <h3>Baixe e instale o Visual Studio Code</h3>

    Para instalar o Flutter rapidamente e depois editar e depurar seus apps,
    [instale e configure o Visual Studio Code][vscode-install]
    (ou o editor baseado no Code OSS de sua preferência).

{: .steps .macos-only}

 1. <h3>Instale o Git for Windows</h3>

    Baixe e instale a versão mais recente do [Git for Windows][].

    Para obter ajuda com a instalação ou resolver problemas do Git,
    consulte a [documentação do Git][git-install].

 1. <h3>Baixe e instale o Visual Studio Code</h3>

    Para instalar o Flutter rapidamente e depois editar e depurar seus apps,
    [instale e configure o Visual Studio Code][vscode-install]
    (ou o editor baseado no Code OSS de sua preferência).

{: .steps .windows-only}

 1. <h3>Baixe e instale os pacotes necessários</h3>

    Usando o gerenciador de pacotes ou o mecanismo de sua preferência,
    instale as versões mais recentes dos seguintes pacotes:

    - `curl`
    - `git`
    - `unzip`
    - `xz-utils`
    - `zip`
    - `libglu1-mesa`

    Em distribuições baseadas em Debian com `apt-get`, como o Ubuntu,
    instale esses pacotes com os seguintes comandos:

    ```console
    $ sudo apt-get update -y && sudo apt-get upgrade -y
    $ sudo apt-get install -y curl git unzip xz-utils zip libglu1-mesa
    ```

 1. <h3>Baixe e instale o Visual Studio Code</h3>

    Para instalar o Flutter rapidamente e depois editar e depurar seus apps,
    [instale e configure o Visual Studio Code][vscode-install]
    (ou o editor baseado no Code OSS de sua preferência).

{: .steps .linux-only}

[chromeos-linux]: https://support.google.com/chromebook/answer/9145439
[chromeos-linux-update]: https://support.google.com/chromebook/answer/9145439?hl=en#:~:text=Fix%20problems%20with%20Linux
[Git for Windows]: https://git-scm.com/downloads/win
[git-install]: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git
[vscode-install]: https://code.visualstudio.com/docs/setup/setup-overview

<a id="install-flutter" aria-hidden="true"></a>

## Instale e configure o Flutter {: #install}

Agora que você instalou os pré-requisitos,
use o VS Code para baixar e configurar o Flutter SDK:

 1. <h3>Instale a extensão do Flutter</h3>

    Abra o VS Code e instale a
    [extensão do Flutter pelo VS Code Marketplace][flutter-vscode]
    ou pressione <kbd class="special-key">Cmd/Ctrl</kbd> +
    <kbd>Shift</kbd> + <kbd>X</kbd> para abrir a visualização **Extensions**,
    pesquise por `Flutter` e clique em **Install**.
    Instalar a extensão do Flutter também instala a extensão do Dart.

 1. <h3>Instale o Flutter com o VS Code</h3>

    1. Abra a Command Palette (paleta de comandos) no VS Code.

       Vá em **View** <span aria-label="e depois">></span> **Command Palette**
       ou pressione <kbd class="special-key">Cmd/Ctrl</kbd> +
       <kbd>Shift</kbd> + <kbd>P</kbd>.

    1. Na Command Palette, digite `flutter` e selecione
       **Flutter: New Project**.

    1. O VS Code pede que você localize o Flutter SDK no seu computador.
       Selecione **Download SDK**.

    1. Quando a caixa de diálogo **Select Folder for Flutter SDK** aparecer,
       escolha onde você quer instalar o Flutter e clique em **Clone Flutter**.

       Enquanto baixa o Flutter, o VS Code exibe esta notificação:

       ```console
       Downloading the Flutter SDK. This may take a few minutes.
       ```

       Esse download leva alguns minutos.
       Se você suspeitar que o download travou, clique em **Cancel** e
       comece a instalação de novo.

    1. Quando o download terminar, clique em **Add SDK to PATH**.

       Se der certo, uma notificação é exibida:

       ```console
       The Flutter SDK was added to your PATH
       ```

    1. O VS Code pode exibir um aviso sobre o Google Analytics.
       Se você concordar, clique em **OK**.

    1. Para garantir que o Flutter esteja disponível em todos os terminais:

       1. Feche e abra de novo todas as janelas de terminal.
       1. Reinicie o VS Code.

       {:type="a"}

 1. <h3>Valide sua configuração</h3>

    Para verificar sua instalação, abra a Command Palette
    (<kbd class="special-key">Cmd/Ctrl</kbd> +
    <kbd>Shift</kbd> + <kbd>P</kbd>) e selecione
    **Flutter: Run Flutter Doctor**, ou execute `flutter doctor`
    no seu terminal.

    Na saída, você só precisa de marcações de sucesso (`[✓]`) para o **Flutter**
    e para as plataformas que pretende usar como destino
    (por exemplo, o **Chrome** permite criar para a web imediatamente).
    Você pode ignorar com segurança os avisos `[!]` ou `[✗]` de ferramentas como
    Android Studio ou Xcode até estar pronto para usar essas plataformas.

    Se encontrar algum problema durante a instalação,
    consulte [Solução de problemas na instalação do Flutter][troubleshoot].

{:.steps}

[flutter-vscode]: https://marketplace.visualstudio.com/items?itemName=Dart-Code.flutter
[troubleshoot]: /install/troubleshoot

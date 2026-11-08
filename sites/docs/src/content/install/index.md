---
title: Instale e configure o Flutter
shortTitle: Instalar
description: >-
  Baixe e instale o Flutter SDK, configure sua IDE e as plataformas de
  destino, ou atualize e resolva problemas de uma instalação existente do Flutter.
ia-translate: true
---

<a id="get-started" aria-hidden="true"></a>

## Escolha um método de instalação {: #install}

Para começar a criar apps multiplataforma a partir de uma única base de código,
escolha como você quer instalar o Flutter SDK:

<div class="card-grid wide">
  <div class="card filled-card outlined-card">
    <div class="card-header">
      <span class="card-title">
        <Icon id="rocket_launch" filled="true" size="1.675rem" />
        <span>Instalar com o VS Code</span>
      </span>
      <span class="card-subtitle" style="margin-top: 0.1rem;">Recomendado</span>
    </div>
    <div class="card-content" style="flex-direction: column; align-items: flex-start; justify-content: space-between; flex: 1;">
      <p>Use a extensão do Flutter no VS Code ou em outro editor baseado no Code OSS
        para baixar e instalar o Flutter SDK, adicioná-lo ao seu
        <code>PATH</code> e validar sua configuração.</p>
      <a class="filled-button" style="padding: 0.55rem 1.15rem; margin-top: 0.5rem;" href="/install/with-vs-code">Instalar com o VS Code</a>
    </div>
  </div>
  <div class="card outlined-card">
    <div class="card-header">
      <span class="card-title">
        <Icon id="download" filled="true" size="1.675rem" />
        <span>Baixar e instalar manualmente</span>
      </span>
      <span class="card-subtitle" style="margin-top: 0.1rem;">Configurar sem o VS Code</span>
    </div>
    <div class="card-content" style="flex-direction: column; align-items: flex-start; justify-content: space-between; flex: 1;">
      <p>Baixe o pacote mais recente do Flutter SDK estável para o seu sistema
        operacional, extraia o arquivo e adicione o Flutter ao seu
        <code>PATH</code>.</p>
      <a class="outlined-button" style="padding: 0.55rem 1.15rem; margin-top: 0.5rem;" href="/install/manual">Baixar o SDK e instalar</a>
    </div>
  </div>
</div>

<a id="editor" aria-hidden="true"></a>

## Configure as plataformas de destino e os editores {: #target-platform}

Depois de instalar o Flutter SDK,
configure as ferramentas para suas plataformas de destino e o seu editor preferido:

- **Plataformas de destino:** configure as ferramentas de desenvolvimento para [Android][], [iOS][],
  [web][] (requer apenas um navegador compatível), [Windows][], [macOS][] ou
  [Linux][].
- **IDEs e editores:** configure o suporte ao Flutter no [VS Code][] ou no
  [Android Studio e IntelliJ][Android Studio and IntelliJ].

[Android]: /platform-integration/android/setup
[iOS]: /platform-integration/ios/setup
[web]: /platform-integration/web/setup
[Windows]: /platform-integration/windows/setup
[macOS]: /platform-integration/macos/setup
[Linux]: /platform-integration/linux/setup
[VS Code]: /tools/vs-code#setup
[Android Studio and IntelliJ]: /tools/android-studio#setup

<a id="try" aria-hidden="true"></a>
<a id="update" aria-hidden="true"></a>
<a id="previous-releases" aria-hidden="true"></a>

<a id="uninstall" aria-hidden="true"></a>

## Gerencie ou resolva problemas da sua instalação {: #manage}

Se você já tem o Flutter instalado,
use os guias a seguir para atualizar, configurar,
resolver problemas ou remover sua instalação:

<div class="card-grid">
  <Card title="Atualizar o Flutter" link="/install/upgrade" outlined="true">
    Atualize o Flutter SDK para a versão mais recente ou troque de canal de release.
  </Card>
  <Card title="Arquivo do SDK" link="/install/archive" outlined="true">
    Baixe e instale versões anteriores do Flutter SDK.
  </Card>
  <Card title="Adicionar o Flutter ao PATH" link="/install/add-to-path" outlined="true">
    Configure a variável de ambiente PATH do seu sistema para executar
    o Flutter na linha de comando.
  </Card>
  <Card title="Resolver problemas do SDK" link="/install/troubleshoot" outlined="true">
    Resolva problemas comuns do seu ambiente de desenvolvimento Flutter.
  </Card>
  <Card title="Desinstalar o SDK" link="/install/uninstall" outlined="true">
    Remova o Flutter SDK e os arquivos de configuração relacionados do seu sistema.
  </Card>
</div>

<a id="next-steps" aria-hidden="true"></a>

:::tip Pronto para começar a criar?
Depois de configurar seu ambiente,
siga a [trilha de aprendizado do Flutter][Flutter learning pathway] para criar seu primeiro app Flutter.
:::

[Flutter learning pathway]: /learn/pathway

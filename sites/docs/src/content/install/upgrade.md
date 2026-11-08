---
title: Atualize o Flutter
shortTitle: Atualizar
description: Aprenda a atualizar o Flutter e a trocar de canal.
ia-translate: true
---

Não importa qual canal de release do Flutter
você acompanha, é possível usar o comando `flutter` para atualizar seu
Flutter SDK ou os packages dos quais seu app depende.

<a id="upgrading-the-flutter-sdk" aria-hidden="true"></a>

## Atualize o Flutter SDK {:#upgrade-the-flutter-sdk}

Para atualizar o Flutter SDK, use o comando `flutter upgrade`:

```console
$ flutter upgrade
```

Esse comando obtém a versão mais recente do Flutter SDK
disponível no seu canal atual do Flutter.

Se você usa o canal **stable**
e quer uma versão ainda mais recente do Flutter SDK,
mude para o canal **beta** com `flutter channel beta`
e depois execute `flutter upgrade`.

<a id="keep-informed" aria-hidden="true"></a>

### Mantenha-se informado {:#keep-informed}

A equipe do Flutter publica [guias de migração][migration guides] para breaking changes conhecidas.

Os anúncios sobre essas mudanças são enviados para a
[lista de e-mails de anúncios do Flutter][flutter-announce].

Para evitar que versões futuras do Flutter quebrem seu código,
considere enviar seus testes para o [registro de testes][test registry].


## Trocando de canal do Flutter {:#switching-flutter-channels}

O Flutter tem dois canais de release:
**stable** e **beta**.

### O canal **stable** {:#the-stable-channel}

O canal **stable** é o recomendado para novos usuários
e para releases de apps em produção.
A equipe atualiza esse canal aproximadamente a cada três meses.
O canal pode receber hot fixes ocasionais
para problemas de alta gravidade ou de alto impacto.

A integração contínua dos plugins e packages da equipe do Flutter
inclui testes com a release **stable** mais recente.

A documentação mais recente da branch **stable**
fica em: <https://api.flutter.dev>

### O canal **beta** {:#the-beta-channel}

O canal **beta** tem a release estável mais recente.
É a versão mais recente do Flutter que passou por testes intensivos.
Esse canal passou por todos os testes públicos,
foi verificado com as suítes de teste de produtos do Google que usam Flutter
e foi avaliado com [suítes de teste privadas enviadas pela comunidade][test registry].
O canal **beta** recebe hot fixes regulares
para corrigir problemas importantes recém-descobertos.

O canal **beta** é essencialmente igual ao canal **stable**,
mas é atualizado mensalmente em vez de trimestralmente.
Na verdade, quando o canal **stable** é atualizado,
ele passa a apontar para a release **beta** mais recente.

### Outros canais {:#other-channels}

Atualmente existe mais um canal, o **main** (antes chamado de **master**).
Quem [contribui com o Flutter][contribute to Flutter] usa esse canal.

Esse canal não é testado tão a fundo quanto
os canais **beta** e **stable**.

Não é recomendado usar esse canal, porque
ele tem mais chances de conter regressões graves.

A documentação mais recente da branch **main**
fica em: <https://main-api.flutter.dev>

<a id="changing-channels" aria-hidden="true"></a>

### Troque de canal {:#change-channels}

Para ver seu canal atual, use o seguinte comando:

```console
$ flutter channel
```

Para mudar para outro canal, use `flutter channel <channel-name>`.
Depois de trocar de canal, use `flutter upgrade`
para baixar o Flutter SDK mais recente e os packages dependentes desse canal.
Por exemplo:

```console
$ flutter channel beta
$ flutter upgrade
```

<a id="switching-to-a-specific-flutter-version" aria-hidden="true"></a>

## Mude para uma versão específica do Flutter {:#switch-to-a-specific-flutter-version}

Para mudar para uma versão específica do Flutter:

1. Encontre a **versão do Flutter** desejada no [arquivo do Flutter SDK][Flutter SDK archive].

1. Navegue até o Flutter SDK:

   ```console
   $ cd /path/to/flutter
   ```

   :::tip
   Você pode encontrar o caminho do Flutter SDK usando `flutter doctor --verbose`.
   :::

1. Use `git checkout` para mudar para a **versão do Flutter** desejada:

   ```console
   $ git checkout <Flutter version>
   ```

<a id="upgrading-packages" aria-hidden="true"></a>

## Atualize os packages {:#upgrade-packages}

Se você modificou seu arquivo `pubspec.yaml` ou quer atualizar
apenas os packages dos quais seu app depende
(em vez dos packages e do próprio Flutter),
use um dos comandos `flutter pub`.

Para atualizar para as _versões compatíveis mais recentes_ de
todas as dependências listadas no arquivo `pubspec.yaml`,
use o comando `upgrade`:

```console
$ flutter pub upgrade
```

Para atualizar para a _versão mais recente possível_ de
todas as dependências listadas no arquivo `pubspec.yaml`,
use o comando `upgrade --major-versions`:

```console
$ flutter pub upgrade --major-versions
```

Isso também atualiza automaticamente as restrições de versão
no arquivo `pubspec.yaml`.

Para identificar dependências de packages desatualizadas e receber orientações
sobre como atualizá-las, use o comando `outdated`. Para mais detalhes, consulte
a [documentação do `pub outdated`]({{site.dart-site}}/tools/pub/cmd/pub-outdated).

```console
$ flutter pub outdated
```

## Solução de problemas {:#troubleshooting}

### Windows: erro "Filename too long" {:#windows-filename-too-long-error}

Ao executar `flutter upgrade` no Windows,
você pode encontrar um erro como o seguinte:

```text
error: unable to create file ...: Filename too long
```

Isso acontece porque o caminho de um arquivo no Flutter SDK excede o limite
padrão de comprimento máximo de caminho no Windows.

Para resolver esse problema, considere instalar o Flutter SDK
em um caminho mais curto. Por exemplo, instale o Flutter em
`C:\Flutter` em vez de algo mais longo como
`C:\Users\<user name>\Documents\flutter`.

Caso contrário, faça o seguinte:

1. Ative o suporte a caminhos longos no Git:

   ```console
   $ git config --system core.longpaths true
   ```
   
   Se o comando falhar com um erro de permissão,
   tente executar o terminal como administrador.

1. Ative caminhos longos no Windows:
   
   ```console
   New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force
   ```
   
   Esse comando exige privilégios de administrador.

[Flutter SDK archive]: /install/archive
[flutter-announce]: {{site.groups.flutter-announce}}
[pubspec.yaml]: {{site.dart-site}}/tools/pub/pubspec
[test registry]: {{site.repo.organization}}/tests
[contribute to Flutter]: {{site.repo.flutter}}/blob/main/CONTRIBUTING.md
[migration guides]: /release/breaking-changes

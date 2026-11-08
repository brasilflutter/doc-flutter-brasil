# TODO de tradução — Flutter Brasil

> Arquivo gerado por `python3 tool/traducao/gerar_todo.py`.
> Para mudar este cabeçalho, edite `tool/traducao/todo_cabecalho.md`.

Uma página conta como traduzida quando o frontmatter tem `ia-translate: true`.
Upstream: [flutter/website](https://github.com/flutter/website). Para
sincronizar: `git fetch upstream main && git merge upstream/main`.

## Infraestrutura (portar do Eleventy para Jaspr)

Em 2025 o upstream trocou o Eleventy pelo [Jaspr](https://jaspr.site) e moveu o
conteúdo de `src/content/` para `sites/docs/src/content/`. As personalizações
abaixo existiam na versão Eleventy (último commit: `d1a053d`) e ainda precisam
ser refeitas na estrutura nova:

- [ ] Aviso "Página ainda não traduzida." nas páginas sem `ia-translate: true`
      (antes ficava em `src/_layouts/base.html`; agora seria um componente em
      `sites/docs/lib/src/`). Mostrar o aviso só dentro da página, sem cobrir
      o menu lateral (item do antigo `todo.md`).
- [ ] Logo do Flutter Brasil (`src/assets/images/logo/flutter_brasil_logo.{svg,png}`
      no commit `d1a053d`) no header.
- [ ] Ajustes de header, footer e banner (`src/_includes/*.html` no commit `d1a053d`).
- [ ] `site.yml`: título "Flutter Brasil" e URL `https://flutterbrasil.dev`
      (agora em `sites/docs/src/data/site.yml`).
- [ ] Traduzir o menu lateral (antes `src/_data/sidenav.yml`, agora
      `sites/docs/src/data/sidenav/default.yml`) e os cards da home.
- [ ] Deploy: `.firebaserc` com o projeto `docs-flutterbrasil`/`transliteradu`,
      `"site": "docs-flutterbrasil"` no `firebase.json` e o job
      `firebase-deploy` do antigo `.github/workflows/test.yml` (agora o site
      fica em `sites/docs/firebase.json` e o CI em `.github/workflows/docs.yml`).
- [ ] Remover ou adaptar os workflows do upstream que não fazem sentido no fork.
- [ ] Traduzir `README.md`.

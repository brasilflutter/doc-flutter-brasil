#!/usr/bin/env python3
"""Gera TODO-TRADUCAO.md com o status de tradução das páginas de docs.

Uma página é considerada traduzida quando o frontmatter contém
`ia-translate: true`. Parciais em `_includes/` (sem frontmatter) são
marcados com `<!-- ia-translate: true -->` na primeira linha. Execute a partir da raiz do repositório:

    python3 tool/traducao/gerar_todo.py
"""
from collections import defaultdict
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
CONTENT = ROOT / 'sites' / 'docs' / 'src' / 'content'
INCLUDES = ROOT / 'sites' / 'docs' / 'src' / '_includes'
SAIDA = ROOT / 'TODO-TRADUCAO.md'
CABECALHO = ROOT / 'tool' / 'traducao' / 'todo_cabecalho.md'

# Seções de baixa prioridade (conteúdo histórico/de referência que muda pouco
# de valor para o leitor brasileiro). Ficam no fim da lista.
BAIXA_PRIORIDADE = (
    'release/breaking-changes', 'release/release-notes',
    'tools/devtools/release-notes',
)


def frontmatter(texto: str) -> str:
    m = re.match(r'^---\n(.*?)\n---', texto, re.S)
    return m.group(1) if m else ''


def traduzida(texto: str) -> bool:
    if re.search(r'^ia-translate:\s*true\s*$', frontmatter(texto), re.M):
        return True
    return texto.lstrip().startswith('<!-- ia-translate: true -->')


def arquivos():
    for md in sorted(CONTENT.rglob('*.md')):
        yield md.relative_to(CONTENT).as_posix(), md
    for md in sorted(INCLUDES.rglob('*.md')):
        yield '_includes/' + md.relative_to(INCLUDES).as_posix(), md


def main() -> None:
    secoes = defaultdict(list)
    total = traduzidas = linhas_pendentes = 0
    for rel, md in arquivos():
        texto = md.read_text(encoding='utf-8')
        ok = traduzida(texto)
        n = texto.count('\n')
        total += 1
        if ok:
            traduzidas += 1
        else:
            linhas_pendentes += n
        secao = rel.split('/')[0] if '/' in rel else '(raiz)'
        for bp in BAIXA_PRIORIDADE:
            if rel.startswith(bp + '/'):
                secao = bp
        secoes[secao].append((rel, bool(ok), n))

    def chave(s):
        return (s in BAIXA_PRIORIDADE, s)

    out = [CABECALHO.read_text(encoding='utf-8').rstrip(), '']
    pct = 100 * traduzidas / total if total else 0
    out += ['## Progresso', '',
            f'- Páginas traduzidas: **{traduzidas} / {total}** ({pct:.1f}%)',
            f'- Linhas pendentes (aprox.): {linhas_pendentes}', '',
            '| Seção | Traduzidas | Total |', '|---|---:|---:|']
    for s in sorted(secoes, key=chave):
        itens = secoes[s]
        out.append(f'| `{s}` | {sum(i[1] for i in itens)} | {len(itens)} |')
    out += ['', '## Páginas por seção', '']
    for s in sorted(secoes, key=chave):
        itens = secoes[s]
        feitas = sum(i[1] for i in itens)
        out += [f'### `{s}` ({feitas}/{len(itens)})', '']
        for rel, ok, n in itens:
            out.append(f'- [{"x" if ok else " "}] `{rel}` ({n} linhas)')
        out.append('')
    SAIDA.write_text('\n'.join(out), encoding='utf-8')
    print(f'{SAIDA.name}: {traduzidas}/{total} traduzidas')


if __name__ == '__main__':
    main()

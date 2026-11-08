#!/usr/bin/env python3
"""Compara a estrutura de páginas traduzidas com o original em inglês.

Para cada arquivo marcado com ia-translate, busca a versão em inglês em
`upstream/main` (ou na ref passada em --ref) e confere se a quantidade de
cercas de código, code-excerpts, tags Liquid, admonitions, definições de
links de referência e âncoras {:#id} é a mesma. Também avisa sobre
rótulos de link de referência usados sem definição.

    python3 tool/traducao/verificar.py [--ref upstream/main] [arquivos...]
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PADROES = {
    'cercas ```': re.compile(r'^\s*```', re.M),
    'code-excerpt': re.compile(r'<\?code-excerpt'),
    'tags {% %}': re.compile(r'\{%'),
    'admonitions :::': re.compile(r'^\s*:::', re.M),
    'defs de link': re.compile(r'^\s*\[[^\]]+\]:\s', re.M),
    'âncoras {:#}': re.compile(r'\{:\s*#'),
}


def sem_codigo(texto):
    return re.sub(r'```.*?```', '', texto, flags=re.S)


def rotulos(texto):
    t = sem_codigo(texto)
    defs = {m.lower() for m in re.findall(r'^\s*\[([^\]]+)\]:\s', t, re.M)}
    usados = set()
    for txt, lab in re.findall(r'\[([^\]]+)\]\[([^\]]*)\]', t):
        usados.add((lab or txt).lower())
    return usados - defs


def original(ref, caminho):
    r = subprocess.run(['git', '-C', str(ROOT), 'show', f'{ref}:{caminho}'],
                       capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def marcados():
    r = subprocess.run(['git', '-C', str(ROOT), 'grep', '-lE',
                        r'^(ia-translate: true|<!-- ia-translate: true -->)',
                        '--', 'sites/docs/src'], capture_output=True, text=True)
    return r.stdout.split()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ref', default='upstream/main')
    ap.add_argument('arquivos', nargs='*')
    a = ap.parse_args()
    problemas = 0
    for caminho in a.arquivos or marcados():
        caminho = str(Path(caminho).resolve().relative_to(ROOT)) \
            if Path(caminho).is_absolute() or Path(caminho).exists() else caminho
        pt = (ROOT / caminho).read_text(encoding='utf-8')
        en = original(a.ref, caminho)
        erros = []
        if en is None:
            erros.append(f'sem original em {a.ref}')
        else:
            for nome, rx in PADROES.items():
                ne, np_ = len(rx.findall(en)), len(rx.findall(pt))
                # Âncoras explícitas a mais são permitidas: servem para manter
                # o slug em inglês de títulos traduzidos.
                if ne != np_ and not (nome == 'âncoras {:#}' and np_ > ne):
                    erros.append(f'{nome}: en={ne} pt={np_}')
            faltando = rotulos(pt) - rotulos(en)
            if faltando:
                erros.append('rótulos sem definição: ' + ', '.join(sorted(faltando)))
        if erros:
            problemas += 1
            print(f'✗ {caminho}')
            for e in erros:
                print(f'    {e}')
    print(f'{problemas} arquivo(s) com problemas.')
    sys.exit(1 if problemas else 0)


if __name__ == '__main__':
    main()

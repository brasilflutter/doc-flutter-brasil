#!/usr/bin/env python3
"""Adiciona âncoras explícitas `{:#slug}` aos títulos traduzidos, usando o
slug gerado a partir do título correspondente em inglês (mesma posição).

Assim os links `#ancora` vindos de outras páginas (e do próprio upstream)
continuam funcionando depois da tradução.

    python3 tool/traducao/ancorar_titulos.py [--ref upstream/main] arquivos...
"""
import argparse
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TITULO = re.compile(r'^(#{2,6})\s+(.*?)\s*$')
ANCORA = re.compile(r'\{:\s*#[^}]*\}\s*$')


def titulos(texto):
    """Retorna [(índice_da_linha, nível, texto)] fora de blocos de código."""
    res, em_codigo = [], False
    for i, linha in enumerate(texto.split('\n')):
        if re.match(r'^\s*```', linha):
            em_codigo = not em_codigo
            continue
        if not em_codigo:
            m = TITULO.match(linha)
            if m:
                res.append((i, len(m.group(1)), m.group(2)))
    return res


def slug(texto):
    """Mesmo algoritmo de packages/site_shared/lib/src/utils/slugify.dart,
    aplicado ao texto visível do título (sem markdown/HTML)."""
    t = re.sub(r'<[^>]+>', '', texto)
    t = re.sub(r'\[([^\]]*)\]\[[^\]]*\]|\[([^\]]*)\]\([^)]*\)',
               lambda m: m.group(1) or m.group(2) or '', t)
    t = re.sub(r'[*`]', '', t)
    t = t.lower().strip()
    t = re.sub(r'[:._]', '-', t)
    t = ''.join(c for c in t if c.isalnum() or c.isspace() or c in ':.-')
    t = re.sub(r'[\s-]+', '-', t)
    return t.strip('-')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ref', default='upstream/main')
    ap.add_argument('arquivos', nargs='+')
    a = ap.parse_args()
    for arq in a.arquivos:
        caminho = Path(arq).resolve().relative_to(ROOT).as_posix()
        en = subprocess.run(['git', '-C', str(ROOT), 'show', f'{a.ref}:{caminho}'],
                            capture_output=True, text=True, check=True).stdout
        pt = (ROOT / caminho).read_text(encoding='utf-8')
        te, tp = titulos(en), titulos(pt)
        if [n for _, n, _ in te] != [n for _, n, _ in tp]:
            print(f'✗ {caminho}: títulos não correspondem ({len(te)} en, {len(tp)} pt); ignorado')
            continue
        linhas = pt.split('\n')
        n = 0
        for (_, _, txt_en), (i, _, txt_pt) in zip(te, tp):
            if ANCORA.search(txt_en):
                continue
            s_en = slug(txt_en)
            base = ANCORA.sub('', linhas[i]).rstrip()
            sem_ancora = ANCORA.sub('', txt_pt).strip()
            novo = base if s_en == slug(sem_ancora) else f'{base} {{:#{s_en}}}'
            if s_en and novo != linhas[i]:
                linhas[i] = novo
                n += 1
        if n:
            (ROOT / caminho).write_text('\n'.join(linhas), encoding='utf-8')
        print(f'✓ {caminho}: {n} título(s) ajustado(s)')


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Restaura, a partir do original em inglês, o conteúdo dos blocos de código
precedidos por `<?code-excerpt ...?>` em páginas traduzidas.

Esses blocos são sincronizados com os arquivos de `examples/` pela ferramenta
de excerpts do upstream; se forem traduzidos, a checagem do CI falha.

    python3 tool/traducao/restaurar_excerpts.py [--ref upstream/main] arquivos...
"""
import argparse
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BLOCO = re.compile(r'(<\?code-excerpt[^\n]*\?>\n(?:[ \t]*\n)*)([ \t]*```[^\n]*\n.*?\n[ \t]*```)', re.S)


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
        blocos_en = [m.group(2) for m in BLOCO.finditer(en)]
        blocos_pt = list(BLOCO.finditer(pt))
        if len(blocos_en) != len(blocos_pt):
            print(f'✗ {caminho}: en={len(blocos_en)} pt={len(blocos_pt)} blocos; ignorado')
            continue
        it = iter(blocos_en)
        novo = BLOCO.sub(lambda m: m.group(1) + next(it), pt)
        if novo != pt:
            (ROOT / caminho).write_text(novo, encoding='utf-8')
            n = sum(1 for x, y in zip(blocos_en, blocos_pt) if x != y.group(2))
            print(f'✓ {caminho}: {n} bloco(s) restaurado(s)')


if __name__ == '__main__':
    main()

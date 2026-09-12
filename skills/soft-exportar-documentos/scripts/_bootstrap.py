"""Resolve o pacote `office/` a partir de qualquer subpasta de scripts/.

Os scripts de formato moram em scripts/docx/, scripts/pptx/, scripts/xlsx/ e
scripts/pdf/, e o pacote compartilhado `office` mora em scripts/office/. O
Python so poe no caminho a pasta do proprio script, entao sem este bootstrap o
`from office.helpers import ...` falharia. Importe-o antes de qualquer import de
`office`. Nenhum caminho aqui e absoluto: tudo sai do arquivo em si.
"""

import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
for _p in (str(_SCRIPTS), str(_SCRIPTS / "office")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

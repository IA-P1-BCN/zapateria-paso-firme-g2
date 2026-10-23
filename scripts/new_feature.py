# SCOPE: infraestructura-agentes (NO tocar backend/frontend/automation)
"""Crea la carpeta de una feature SDD desde las plantillas de specs/_templates/.

Uso:
  python scripts/new_feature.py 006 venta-grande --hu HU-09 --titulo "Venta grande"
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLANTILLAS = ROOT / "specs" / "_templates"
FEATURES = ROOT / "specs" / "features"


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("id", help="número de 3 dígitos, p. ej. 006")
    parser.add_argument("slug", help="nombre corto en kebab-case, p. ej. venta-grande")
    parser.add_argument("--hu", default="<<PENDIENTE: HU>>", help="historia de usuario, p. ej. HU-09")
    parser.add_argument("--titulo", help="título legible (por defecto, el slug)")
    args = parser.parse_args()

    if not re.fullmatch(r"\d{3}", args.id):
        parser.error("id debe tener 3 dígitos")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", args.slug):
        parser.error("slug debe ser kebab-case en minúsculas")
    existentes = [p.name for p in FEATURES.glob(f"{args.id}-*")]
    if existentes:
        print(f"✗ Ya existe una feature con el número {args.id}: {existentes[0]}")
        return 1

    destino = FEATURES / f"{args.id}-{args.slug}"
    destino.mkdir(parents=True)
    valores = {
        "{{ID}}": args.id,
        "{{SLUG}}": args.slug,
        "{{HU}}": args.hu,
        "{{TITULO}}": args.titulo or args.slug.replace("-", " ").capitalize(),
        "{{FECHA}}": date.today().isoformat(),
    }
    for plantilla in sorted(PLANTILLAS.glob("*.md")):
        texto = plantilla.read_text(encoding="utf-8")
        for marcador, valor in valores.items():
            texto = texto.replace(marcador, valor)
        (destino / plantilla.name).write_text(texto, encoding="utf-8", newline="\n")
        print(f"creado  {(destino / plantilla.name).relative_to(ROOT).as_posix()}")
    print("Siguiente paso: /sdd-spec " + args.id + "  (y añadir la fila en specs/backlog.md)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

# SCOPE: infraestructura-agentes (NO tocar backend/frontend/workflows)
"""Validate exported n8n workflow JSONs.

Usage: python scripts/validate_workflows.py [directory] [--estricto]   (default: workflows)

Checks per file:
  - valid JSON
  - top-level structure: nodes (list), connections (object), name (string)
  - every node has name, type, typeVersion, position
  - no obvious credentials leaked inside the JSON (API keys, tokens, secrets)
  --estricto (ADR-0002): also "active": false and file name NNN-slug.json
"""

import json
import re
import sys
from pathlib import Path

# Patterns that must never appear in an exported workflow (credentials live in n8n, not in JSON)
LEAK_PATTERNS = [
    re.compile(r'"apiKey"\s*:\s*"[A-Za-z0-9_\-]{16,}"'),
    re.compile(r'"api_key"\s*:\s*"[A-Za-z0-9_\-]{16,}"'),
    re.compile(r'"token"\s*:\s*"[A-Za-z0-9_\-]{16,}"'),
    re.compile(r'"password"\s*:\s*"[^"]+"'),
    re.compile(r"sk-[A-Za-z0-9_\-]{20,}"),
    re.compile(r"AIza[A-Za-z0-9_\-]{35}"),
]


NOMBRE_ARCHIVO = re.compile(r"^\d{3}-[a-z0-9]+(-[a-z0-9]+)*\.json$")


def validate(path: Path, estricto: bool = False) -> list[str]:
    errors: list[str] = []
    try:
        raw = path.read_text(encoding="utf-8")
        data = json.loads(raw)
    except (OSError, json.JSONDecodeError) as exc:
        return [f"no es un JSON válido: {exc}"]

    if not isinstance(data, dict):
        return ["el JSON raíz debe ser un objeto"]

    if not isinstance(data.get("name"), str) or not data.get("name"):
        errors.append("falta el campo 'name' (nombre del flujo)")

    nodes = data.get("nodes")
    if not isinstance(nodes, list) or not nodes:
        errors.append("falta 'nodes' o está vacío")
    else:
        for i, node in enumerate(nodes):
            if not isinstance(node, dict):
                errors.append(f"nodes[{i}] no es un objeto")
                continue
            label = node.get("name", f"nodes[{i}]")
            for field in ("name", "type", "typeVersion", "position"):
                if field not in node:
                    errors.append(f"nodo '{label}': falta '{field}'")

    if not isinstance(data.get("connections"), dict):
        errors.append("falta 'connections' (debe ser un objeto)")

    for pattern in LEAK_PATTERNS:
        match = pattern.search(raw)
        if match:
            errors.append(f"posible credencial en el JSON: …{match.group(0)[:40]}…")

    if estricto:
        if data.get("active") is not False:
            errors.append('"active" debe ser false: los flujos se exportan desactivados (AGENTS.md, regla 3)')
        if not NOMBRE_ARCHIVO.match(path.name):
            errors.append("el archivo debe llamarse NNN-slug.json con el número de 3 dígitos de su spec (ADR-0002)")

    return errors


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):  # consola de Windows
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    args = [a for a in sys.argv[1:] if a != "--estricto"]
    estricto = "--estricto" in sys.argv[1:]
    if len(args) > 1:
        print("Uso: python scripts/validate_workflows.py [carpeta] [--estricto]   (por defecto: workflows)")
        return 2

    directory = Path(args[0] if args else "workflows")
    if not directory.is_dir():
        print(f"Sin carpeta {directory}/ todavía, nada que validar")
        return 0

    files = sorted(directory.glob("*.json"))
    if not files:
        print(f"{directory}/ no contiene JSON, nada que validar")
        return 0

    failed = 0
    for path in files:
        errors = validate(path, estricto)
        if errors:
            failed += 1
            print(f"ERROR {path}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"OK    {path}")

    print(f"\n{len(files) - failed}/{len(files)} flujos válidos")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

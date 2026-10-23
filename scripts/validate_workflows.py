"""Validate exported n8n workflow JSONs.

Usage: python3 scripts/validate_workflows.py <directory>

Checks per file:
  - valid JSON
  - top-level structure: nodes (list), connections (object), name (string)
  - every node has name, type, typeVersion, position
  - no obvious credentials leaked inside the JSON (API keys, tokens, secrets)
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


def validate(path: Path) -> list[str]:
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

    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("Uso: python3 scripts/validate_workflows.py <directory>")
        return 2

    directory = Path(sys.argv[1])
    if not directory.is_dir():
        print(f"Sin carpeta {directory}/ todavía, nada que validar")
        return 0

    files = sorted(directory.glob("*.json"))
    if not files:
        print(f"{directory}/ no contiene JSON, nada que validar")
        return 0

    failed = 0
    for path in files:
        errors = validate(path)
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

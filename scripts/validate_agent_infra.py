# SCOPE: infraestructura-agentes (NO tocar backend/frontend/automation)
"""Valida la capa de agentes antes de una PR.

Comprueba:
  1. Skills: frontmatter con name (igual a la carpeta, formato kebab-case) y description (1-1024 caracteres).
  2. Cabecera SCOPE en todos los archivos de la capa de agentes (con las excepciones documentadas).
  3. Subagentes, comandos y skills sincronizados (scripts/sync_agents.py --check).
  4. Cada feature de specs/features/ tiene spec.md, plan.md y tasks.md, y spec.md declara su Estado.
  5. (--alcance) Que la rama no toca backend/, frontend/ ni automation/ respecto a la rama base.
  Informa además de cuántos <<PENDIENTE>> quedan.

Uso:
  python scripts/validate_agent_infra.py
  python scripts/validate_agent_infra.py --alcance --base develop
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sync_agents  # noqa: E402

ROOT = sync_agents.ROOT
SCOPE = sync_agents.SCOPE
CARPETAS_INFRA = [".agents", ".claude", ".opencode", "specs", "scripts"]
ARCHIVOS_RAIZ = ["AGENTS.md", "CLAUDE.md", "ontology.md"]
SIN_SCOPE = {".claude/settings.json", ".claude/settings.local.json"}  # JSON no admite comentarios (ADR-0001 D5)
PROTEGIDAS = ("backend/", "frontend/", "automation/")
EXTENSIONES = {".md", ".py", ".json", ".jsonc", ".yml", ".yaml", ".txt"}
NOMBRE_SKILL = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
ESTADOS = {"Borrador", "Aprobada", "En construcción", "En revisión", "Hecha"}


def _rel(ruta: Path) -> str:
    return ruta.relative_to(ROOT).as_posix()


def _frontmatter(texto: str) -> dict[str, str] | None:
    lineas = texto.splitlines()
    if not lineas or lineas[0].strip() != "---":
        return None
    datos = {}
    for linea in lineas[1:]:
        if linea.strip() == "---":
            return datos
        if linea.startswith((" ", "#")) or ":" not in linea:
            continue
        clave, valor = linea.split(":", 1)
        datos[clave.strip()] = valor.strip().strip('"')
    return None


def validar_skills() -> list[str]:
    errores = []
    carpeta = ROOT / ".claude" / "skills"
    skills = sorted(p for p in carpeta.iterdir() if p.is_dir()) if carpeta.exists() else []
    if not skills:
        errores.append("No hay skills en .claude/skills/")
    for skill in skills:
        archivo = skill / "SKILL.md"
        if not archivo.exists():
            errores.append(f"{_rel(skill)}: falta SKILL.md")
            continue
        fm = _frontmatter(archivo.read_text(encoding="utf-8"))
        if fm is None:
            errores.append(f"{_rel(archivo)}: el frontmatter YAML debe empezar en la línea 1")
            continue
        nombre, descripcion = fm.get("name", ""), fm.get("description", "")
        if nombre != skill.name:
            errores.append(f"{_rel(archivo)}: name '{nombre}' no coincide con la carpeta '{skill.name}'")
        if not NOMBRE_SKILL.match(nombre):
            errores.append(f"{_rel(archivo)}: name debe ser kebab-case en minúsculas")
        if not 1 <= len(descripcion) <= 1024:
            errores.append(f"{_rel(archivo)}: description debe tener entre 1 y 1024 caracteres")
    return errores


def _tiene_scope(ruta: Path) -> bool:
    lineas = ruta.read_text(encoding="utf-8").splitlines()[:3]
    if not lineas:
        return False
    if lineas[0].strip() in (SCOPE, "// " + SCOPE[2:]):  # JSONC: // SCOPE: ...
        return True
    return lineas[0].strip() == "---" and len(lineas) > 1 and lineas[1].strip() == SCOPE


def validar_scope() -> list[str]:
    archivos = [ROOT / a for a in ARCHIVOS_RAIZ]
    for carpeta in CARPETAS_INFRA:
        archivos += [p for p in (ROOT / carpeta).rglob("*")
                     if p.is_file() and p.suffix in EXTENSIONES and "__pycache__" not in p.parts]
    errores = []
    for ruta in archivos:
        if not ruta.exists():
            errores.append(f"Falta {_rel(ruta)}")
        elif _rel(ruta) not in SIN_SCOPE and not _tiene_scope(ruta):
            errores.append(f"{_rel(ruta)}: falta la cabecera SCOPE")
    return errores


def validar_specs() -> list[str]:
    errores = []
    for feature in sorted((ROOT / "specs" / "features").glob("*")):
        if not feature.is_dir():
            continue
        if not re.match(r"^\d{3}-[a-z0-9-]+$", feature.name):
            errores.append(f"{_rel(feature)}: el nombre debe ser NNN-slug")
        for nombre in ("spec.md", "plan.md", "tasks.md"):
            if not (feature / nombre).exists():
                errores.append(f"{_rel(feature)}: falta {nombre}")
        spec = feature / "spec.md"
        if spec.exists():
            m = re.search(r"\*\*Estado:\*\*\s*(.+)", spec.read_text(encoding="utf-8"))
            if not m or m.group(1).strip() not in ESTADOS:
                errores.append(f"{_rel(spec)}: 'Estado:' ausente o no es uno de {sorted(ESTADOS)}")
    return errores


def validar_alcance(base: str) -> list[str]:
    def git(*args: str) -> list[str]:
        r = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
        if r.returncode != 0:
            raise RuntimeError(r.stderr.strip())
        return [l for l in r.stdout.splitlines() if l.strip()]

    try:
        cambiados = set(git("diff", "--name-only", f"{base}...HEAD"))
        cambiados |= {l[3:].strip().strip('"') for l in git("status", "--porcelain")}
    except (RuntimeError, FileNotFoundError) as e:
        return [f"No se pudo consultar git: {e}"]
    return [f"Cambio fuera de alcance: {c}" for c in sorted(cambiados) if c.startswith(PROTEGIDAS)]


def contar_pendientes() -> int:
    total = 0
    for ruta in [ROOT / a for a in ARCHIVOS_RAIZ] + [p for c in CARPETAS_INFRA for p in (ROOT / c).rglob("*.md")]:
        if sync_agents.SKILLS_DESTINO in ruta.parents:  # copias de skills: ya se cuentan en .claude/skills/
            continue
        if ruta.exists():
            total += ruta.read_text(encoding="utf-8").count("<<PENDIENTE")
    return total


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--alcance", action="store_true", help="falla si la rama toca backend/frontend/automation")
    parser.add_argument("--base", default="develop", help="rama base para --alcance (por defecto: develop)")
    args = parser.parse_args()

    bloques = [
        ("Skills", validar_skills()),
        ("Cabecera SCOPE", validar_scope()),
        ("Sincronización de subagentes, comandos y skills", sync_agents.check()),
        ("Specs", validar_specs()),
    ]
    if args.alcance:
        bloques.append((f"Alcance respecto a {args.base}", validar_alcance(args.base)))

    fallos = 0
    for titulo, errores in bloques:
        print(f"{'✓' if not errores else '✗'} {titulo}")
        for e in errores:
            print(f"    - {e}")
        fallos += len(errores)
    print(f"ℹ Quedan {contar_pendientes()} marcadores <<PENDIENTE>> por resolver")
    print("OK" if not fallos else f"{fallos} problema(s)")
    return 1 if fallos else 0


if __name__ == "__main__":
    sys.exit(main())

# SCOPE: infraestructura-agentes (NO tocar backend/frontend/workflows)
"""Valida la capa de agentes antes de una PR.

Comprueba:
  1. Skills: frontmatter con name (igual a la carpeta, formato kebab-case) y description (1-1024 caracteres).
  2. Cabecera SCOPE en todos los archivos de la capa de agentes (con las excepciones documentadas).
  3. Subagentes, comandos y skills sincronizados (scripts/sync_agents.py --check).
  4. Cada feature de specs/features/ tiene spec.md, plan.md y tasks.md, y spec.md declara su Estado
     y su «Flujo enunciado» (ADR-0002, D4).
  5. Estructura de skills (ADR-0002, D7-D9): fuente única .claude/skills/, .opencode/skills/ solo con copias
     generadas, sin .agents/skills/, y las externas de skills-lock.json con la nota de precedencia.
  6. Subagentes: description que dice cuándo usarlo, skills declaradas que existen y se citan en el cuerpo,
     revisores en solo lectura y regla «primero la spec» en flow-builder.
  7. Terminología: «subagente», nunca «miniagente».
  8. (--alcance) Que una rama de infraestructura no toca backend/, frontend/ ni workflows/ respecto a la rama base.
  Informa además de cuántos <<PENDIENTE>> quedan.

Uso:
  python scripts/validate_agent_infra.py
  python scripts/validate_agent_infra.py --alcance --base develop
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sync_agents  # noqa: E402

ROOT = sync_agents.ROOT
SCOPE = sync_agents.SCOPE
SCOPES = sync_agents.SCOPES
CARPETAS_INFRA = [".agents", ".claude", ".opencode", "specs", "scripts"]
ARCHIVOS_RAIZ = ["AGENTS.md", "CLAUDE.md", "ontology.md"]
SIN_SCOPE = {".claude/settings.json", ".claude/settings.local.json"}  # JSON no admite comentarios (ADR-0001 D5)
PROTEGIDAS = ("backend/", "frontend/", "workflows/")  # workflows/: solo flow-builder, en su propia rama
EXTENSIONES = {".md", ".py", ".json", ".jsonc", ".yml", ".yaml", ".txt"}
NOMBRE_SKILL = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
ESTADOS = {"Borrador", "Aprobada", "En construcción", "En revisión", "Hecha"}
NOTA_EXTERNA = "prevalecen sobre esta skill externa"
SOLO_LECTURA = {"flow-reviewer", "api-contract-checker"}
HERRAMIENTAS_LECTURA = {"Read", "Grep", "Glob"}
MINIAGENTE = re.compile(r"mini[- ]?agente", re.IGNORECASE)


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
    primera = lineas[0].strip()
    if primera in SCOPES or primera in ["// " + s[2:] for s in SCOPES]:  # JSONC: // SCOPE: ...
        return True
    return primera == "---" and len(lineas) > 1 and lineas[1].strip() in SCOPES


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
            if not re.search(r"\*\*Flujo enunciado:\*\*\s*\S", spec.read_text(encoding="utf-8")):
                errores.append(f"{_rel(spec)}: falta '- **Flujo enunciado:** FL-XX' (o '—') en la cabecera")
    return errores


def validar_estructura_skills() -> list[str]:
    errores = []
    if (ROOT / ".agents" / "skills").exists():
        errores.append(".agents/skills/ no debe existir: la fuente de skills es .claude/skills/ (ADR-0002, D7)")
    destino = sync_agents.SKILLS_DESTINO
    if destino.exists():
        for ruta in sorted(destino.rglob("*")):
            if (ruta.is_file() and ruta.suffix in sync_agents.EXT_SKILLS
                    and "GENERADO por scripts/sync_agents.py" not in ruta.read_text(encoding="utf-8")):
                errores.append(f"{_rel(ruta)}: no es una copia generada; edita la skill en .claude/skills/")
    lock = ROOT / "skills-lock.json"
    if lock.exists():
        for nombre in json.loads(lock.read_text(encoding="utf-8")).get("skills", {}):
            skill = sync_agents.SKILLS_FUENTE / nombre / "SKILL.md"
            if not skill.exists():
                errores.append(f"skills-lock.json cita '{nombre}', que no está en .claude/skills/")
            elif NOTA_EXTERNA not in skill.read_text(encoding="utf-8"):
                errores.append(f"{_rel(skill)}: skill externa sin la nota de precedencia de AGENTS.md")
    return errores


def validar_subagentes() -> list[str]:
    errores = []
    existentes = {p.name for p in sync_agents.SKILLS_FUENTE.iterdir() if p.is_dir()}
    for nombre, meta in sync_agents.AGENTS.items():
        if "Úsalo" not in meta["description"]:
            errores.append(f"{nombre}: la description debe decir cuándo usarlo («Úsalo …»)")
        cuerpo = (ROOT / ".agents" / "agents" / f"{nombre}.md").read_text(encoding="utf-8")
        skills = [s.strip() for s in (meta["claude"].get("skills") or "").split(",") if s.strip()]
        if not skills:
            errores.append(f"{nombre}: no declara skills")
        for skill in skills:
            if skill not in existentes:
                errores.append(f"{nombre}: declara la skill '{skill}', que no existe en .claude/skills/")
            elif f"`{skill}`" not in cuerpo:
                errores.append(f"{nombre}: el cuerpo no cita la skill `{skill}` (OpenCode no lee el campo skills)")
        if nombre in SOLO_LECTURA:
            herramientas = {h.strip() for h in (meta["claude"]["tools"] or "*").split(",")}
            if not herramientas <= HERRAMIENTAS_LECTURA:
                errores.append(f"{nombre}: debe ser de solo lectura (Read, Grep, Glob); tiene {sorted(herramientas)}")
            if meta["opencode"].get("edit") != "deny":
                errores.append(f"{nombre}: en OpenCode 'edit' debe ser 'deny'")
    fb = (ROOT / ".agents" / "agents" / "flow-builder.md").read_text(encoding="utf-8")
    if not all(x in fb for x in ("spec.md", "plan.md", "tasks.md", "spec-writer")):
        errores.append("flow-builder: falta la regla dura de leer spec.md, plan.md y tasks.md y, si no existen, "
                       "pedir usar spec-writer")
    return errores


def validar_terminologia() -> list[str]:
    errores = []
    archivos = [ROOT / a for a in ARCHIVOS_RAIZ]
    for carpeta in CARPETAS_INFRA:
        archivos += [p for p in (ROOT / carpeta).rglob("*")
                     if p.is_file() and p.suffix in EXTENSIONES and "__pycache__" not in p.parts]
    for ruta in archivos:
        if ruta.exists() and ruta.name != "validate_agent_infra.py":
            for n, linea in enumerate(ruta.read_text(encoding="utf-8").splitlines(), 1):
                if MINIAGENTE.search(linea):
                    errores.append(f"{_rel(ruta)}:{n}: usa «subagente», no «miniagente»")
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
    parser.add_argument("--alcance", action="store_true", help="falla si la rama toca backend/, frontend/ o workflows/")
    parser.add_argument("--base", default="develop", help="rama base para --alcance (por defecto: develop)")
    args = parser.parse_args()

    bloques = [
        ("Skills", validar_skills()),
        ("Cabecera SCOPE", validar_scope()),
        ("Sincronización de subagentes, comandos y skills", sync_agents.check()),
        ("Specs", validar_specs()),
        ("Estructura de skills", validar_estructura_skills()),
        ("Subagentes", validar_subagentes()),
        ("Terminología", validar_terminologia()),
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

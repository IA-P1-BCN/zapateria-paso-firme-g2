# SCOPE: infraestructura-agentes (NO tocar backend/frontend/workflows)
"""Genera subagentes, comandos y skills de Claude Code y OpenCode desde una sola fuente.

Fuente:
  .agents/agents/<nombre>.md     cuerpo (prompt) de cada subagente
  .agents/commands/<nombre>.md   cuerpo de cada comando
  AGENTS / COMMANDS (abajo)      metadatos por herramienta
  .claude/skills/<nombre>/       skills (se editan aquí; Claude Code las lee directamente)

Destino (no editar a mano):
  .claude/agents/  .claude/commands/  .opencode/agents/  .opencode/commands/  .opencode/skills/

Uso:
  python scripts/sync_agents.py           # regenera
  python scripts/sync_agents.py --check   # sale con 1 si algo está desactualizado
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCOPE = "# SCOPE: infraestructura-agentes (NO tocar backend/frontend/workflows)"
SCOPE_FLOW_BUILDER = "# SCOPE: infraestructura-agentes (NO tocar backend/frontend; workflows/ solo flow-builder)"
SCOPES = (SCOPE, SCOPE_FLOW_BUILDER)  # ADR-0002, D10
MARCA = "# GENERADO por scripts/sync_agents.py desde {fuente}. No editar a mano."
MARCA_MD = "<!-- GENERADO por scripts/sync_agents.py desde {fuente}. No editar a mano. -->"
SKILLS_FUENTE = ROOT / ".claude" / "skills"
SKILLS_DESTINO = ROOT / ".opencode" / "skills"
EXT_SKILLS = {".md", ".txt", ".json", ".yml", ".yaml", ".py"}

SOLO_LECTURA = {"edit": "deny", "bash": "deny", "webfetch": "deny"}
ESCRIBE_CON_PERMISO = {"edit": "ask", "bash": "deny", "webfetch": "deny"}
CONSTRUYE = {"edit": "ask", "bash": "ask", "webfetch": "deny"}  # necesita validar JSON con python

# --- Subagentes -----------------------------------------------------------------------------
# claude.tools: None = hereda todas las herramientas (incluidas las del MCP n8n-mcp).
AGENTS: dict[str, dict] = {
    "spec-writer": {
        "description": "Redacta specs SDD (spec.md) de automatizaciones n8n a partir de una historia de usuario. "
                       "Úsalo para crear o actualizar specs/features/NNN-*/spec.md. Nunca aprueba ni construye.",
        "claude": {"tools": "Read, Grep, Glob, Write, Edit",
                   "skills": "sdd-workflow, dominio-apartados, n8n-convenciones, tienda-api"},
        "opencode": ESCRIBE_CON_PERMISO,
    },
    "flow-builder": {
        "description": "Genera el JSON de un flujo n8n desde una feature con spec aprobada, plan y tareas. "
                       "Úsalo para construir o modificar flujos en workflows/. Nunca activa flujos ni escribe secretos.",
        "claude": {"tools": None,
                   "skills": "n8n-convenciones, tienda-api, dominio-apartados, n8n-import-export"},
        "opencode": CONSTRUYE,
        "scope": SCOPE_FLOW_BUILDER,
    },
    "flow-reviewer": {
        "description": "Revisa (solo lectura) un flujo n8n: secretos, datos personales, reglas de negocio, errores y "
                       "convenciones. Úsalo antes de abrir una PR con flujos. Devuelve veredicto y hallazgos.",
        "claude": {"tools": "Read, Grep, Glob",
                   "skills": "revision-seguridad-flujos, n8n-convenciones, tienda-api, dominio-apartados"},
        "opencode": SOLO_LECTURA,
    },
    "api-contract-checker": {
        "description": "Verifica (solo lectura) que specs, planes y flujos usan endpoints, campos y eventos que existen "
                       "en el backend. Úsalo tras escribir un plan o un flujo con llamadas a la API.",
        "claude": {"tools": "Read, Grep, Glob", "skills": "tienda-api"},
        "opencode": SOLO_LECTURA,
    },
    "test-designer": {
        "description": "Diseña datos de prueba (fixtures.md) con un caso por criterio de aceptación, usando la forma "
                       "real de eventos y respuestas. Úsalo antes de construir o probar un flujo.",
        "claude": {"tools": "Read, Grep, Glob, Write, Edit", "skills": "datos-de-prueba, tienda-api"},
        "opencode": ESCRIBE_CON_PERMISO,
    },
    "ai-scribe": {
        "description": "Añade entradas a la bitácora de IA (docs/ai-log.md): modelo, prompts clave, alucinaciones y "
                       "decisiones. Úsalo al cerrar una tarea hecha con IA.",
        "claude": {"tools": "Read, Grep, Glob, Write, Edit", "skills": "trazabilidad-ia"},
        "opencode": ESCRIBE_CON_PERMISO,
    },
}

# --- Comandos -------------------------------------------------------------------------------
COMMANDS: dict[str, dict] = {
    "sdd-spec": {"description": "Redacta la spec SDD de una historia de usuario (delegando en spec-writer)",
                 "argument_hint": "<HU-XX | NNN | descripción>"},
    "sdd-plan": {"description": "Escribe el plan técnico de una feature con spec aprobada y lo valida contra la API",
                 "argument_hint": "<NNN>"},
    "sdd-tasks": {"description": "Descompone el plan de una feature en tareas atómicas asignables",
                  "argument_hint": "<NNN>"},
    "construir-flujo": {"description": "Genera el JSON del flujo n8n de una feature (delegando en flow-builder)",
                        "argument_hint": "<NNN> [T-NNN-k]"},
    "revisar-flujo": {"description": "Revisa un flujo antes de la PR (flow-reviewer + api-contract-checker)",
                      "argument_hint": "<NNN | ruta del JSON>"},
    "bitacora": {"description": "Registra en docs/ai-log.md lo hecho con IA (delegando en ai-scribe)",
                 "argument_hint": "<feature, tarea o descripción>"},
    # Comandos que solo envuelven una skill: en Claude Code la skill ya es el comando /<nombre>,
    # así que se generan solo para OpenCode (evita dos entradas con el mismo nombre).
    "paso-firme-review": {"description": "Revisa un diff de Paso Firme contra las reglas de negocio del briefing",
                          "argument_hint": "<rama | PR | ruta>", "herramientas": ("opencode",)},
    "paso-firme-verify": {"description": "Verifica la entrega de Paso Firme con evidencia de validador de flujos y tests",
                          "argument_hint": "<issue | rama>", "herramientas": ("opencode",)},
}


def _yaml_valor(valor) -> str:
    if isinstance(valor, bool):
        return "true" if valor else "false"
    texto = str(valor)
    if any(c in texto for c in ':#"\'{}[],&*!|>%@`') or texto != texto.strip():
        return '"' + texto.replace("\\", "\\\\").replace('"', '\\"') + '"'
    return texto


def _yaml(datos: dict, sangria: int = 0) -> list[str]:
    lineas = []
    for clave, valor in datos.items():
        if valor is None:
            continue
        if isinstance(valor, dict):
            lineas.append(" " * sangria + f"{clave}:")
            lineas.extend(_yaml(valor, sangria + 2))
        else:
            lineas.append(" " * sangria + f"{clave}: {_yaml_valor(valor)}")
    return lineas


def _cuerpo(ruta: Path) -> str:
    """Contenido de la fuente sin la línea SCOPE inicial (ya va en el frontmatter)."""
    lineas = ruta.read_text(encoding="utf-8").splitlines()
    if lineas and lineas[0].strip() in SCOPES:
        lineas = lineas[1:]
    while lineas and not lineas[0].strip():
        lineas = lineas[1:]
    return "\n".join(lineas).rstrip() + "\n"


def _documento(frontmatter: dict, fuente: str, cuerpo: str, scope: str = SCOPE) -> str:
    cabecera = ["---", scope, MARCA.format(fuente=fuente), *_yaml(frontmatter), "---", ""]
    return "\n".join(cabecera) + "\n" + cuerpo


def _copia_skill(ruta: Path) -> str:
    """Copia de un archivo de skill con la marca GENERADO justo debajo de la línea SCOPE."""
    fuente = ruta.relative_to(ROOT).as_posix()
    lineas = ruta.read_text(encoding="utf-8").splitlines()
    if len(lineas) > 1 and lineas[0].strip() == "---" and lineas[1].strip() == SCOPE:
        lineas.insert(2, MARCA.format(fuente=fuente))  # comentario YAML dentro del frontmatter
    elif lineas and lineas[0].strip() == SCOPE:
        lineas.insert(1, MARCA_MD.format(fuente=fuente))
    else:
        lineas.insert(0, MARCA_MD.format(fuente=fuente))
    return "\n".join(lineas).rstrip() + "\n"


def _archivos_skills() -> list[Path]:
    if not SKILLS_FUENTE.exists():
        return []
    return sorted(p for p in SKILLS_FUENTE.rglob("*")
                  if p.is_file() and p.suffix in EXT_SKILLS and "__pycache__" not in p.parts)


def generar() -> dict[Path, str]:
    """Devuelve {ruta_destino: contenido} de todo lo que debe existir."""
    salida: dict[Path, str] = {}
    for nombre, meta in AGENTS.items():
        fuente = f".agents/agents/{nombre}.md"
        cuerpo = _cuerpo(ROOT / fuente)
        claude = {"name": nombre, "description": meta["description"],
                  "tools": meta["claude"]["tools"], "model": "inherit", "skills": meta["claude"]["skills"]}
        scope = meta.get("scope", SCOPE)
        salida[ROOT / ".claude" / "agents" / f"{nombre}.md"] = _documento(claude, fuente, cuerpo, scope)
        opencode = {"description": meta["description"], "mode": "subagent", "permission": meta["opencode"]}
        salida[ROOT / ".opencode" / "agents" / f"{nombre}.md"] = _documento(opencode, fuente, cuerpo, scope)
    for nombre, meta in COMMANDS.items():
        fuente = f".agents/commands/{nombre}.md"
        cuerpo = _cuerpo(ROOT / fuente)
        herramientas = meta.get("herramientas", ("claude", "opencode"))
        if "claude" in herramientas:
            claude = {"description": meta["description"], "argument-hint": meta["argument_hint"]}
            salida[ROOT / ".claude" / "commands" / f"{nombre}.md"] = _documento(claude, fuente, cuerpo)
        if "opencode" in herramientas:
            opencode = {"description": meta["description"]}
            salida[ROOT / ".opencode" / "commands" / f"{nombre}.md"] = _documento(opencode, fuente, cuerpo)
    for ruta in _archivos_skills():
        salida[SKILLS_DESTINO / ruta.relative_to(SKILLS_FUENTE)] = _copia_skill(ruta)
    return salida


def _huerfanos(esperados: dict[Path, str]) -> list[Path]:
    """Archivos generados antes cuya fuente ya no existe."""
    huerfanos = []
    for carpeta in (".claude/agents", ".claude/commands", ".opencode/agents", ".opencode/commands"):
        for ruta in (ROOT / carpeta).glob("*.md"):
            if ruta not in esperados and "GENERADO por scripts/sync_agents.py" in ruta.read_text(encoding="utf-8"):
                huerfanos.append(ruta)
    if SKILLS_DESTINO.exists():
        for ruta in SKILLS_DESTINO.rglob("*"):
            if (ruta.is_file() and ruta.suffix in EXT_SKILLS and ruta not in esperados
                    and "GENERADO por scripts/sync_agents.py" in ruta.read_text(encoding="utf-8")):
                huerfanos.append(ruta)
    return huerfanos


def comprobar_fuentes() -> list[str]:
    errores = []
    for nombre in AGENTS:
        if not (ROOT / ".agents" / "agents" / f"{nombre}.md").exists():
            errores.append(f"Falta la fuente .agents/agents/{nombre}.md")
    for nombre in COMMANDS:
        if not (ROOT / ".agents" / "commands" / f"{nombre}.md").exists():
            errores.append(f"Falta la fuente .agents/commands/{nombre}.md")
    for ruta in (ROOT / ".agents" / "agents").glob("*.md"):
        if ruta.stem not in AGENTS:
            errores.append(f"{ruta.relative_to(ROOT)} no tiene metadatos en AGENTS (scripts/sync_agents.py)")
    for ruta in (ROOT / ".agents" / "commands").glob("*.md"):
        if ruta.stem not in COMMANDS:
            errores.append(f"{ruta.relative_to(ROOT)} no tiene metadatos en COMMANDS (scripts/sync_agents.py)")
    return errores


def check() -> list[str]:
    """Lista de problemas (vacía si todo está sincronizado)."""
    problemas = comprobar_fuentes()
    if problemas:
        return problemas
    esperados = generar()
    for ruta, contenido in esperados.items():
        if not ruta.exists():
            problemas.append(f"Falta {ruta.relative_to(ROOT)}")
        elif ruta.read_text(encoding="utf-8") != contenido:
            problemas.append(f"Desactualizado {ruta.relative_to(ROOT)}")
    problemas += [f"Huérfano {r.relative_to(ROOT)}" for r in _huerfanos(esperados)]
    return problemas


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):  # consola de Windows
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true", help="solo comprobar, sin escribir")
    args = parser.parse_args()

    if args.check:
        problemas = check()
        for p in problemas:
            print(f"✗ {p}")
        print("✓ Subagentes, comandos y skills sincronizados" if not problemas else
              "Ejecuta: python scripts/sync_agents.py")
        return 1 if problemas else 0

    errores = comprobar_fuentes()
    if errores:
        for e in errores:
            print(f"✗ {e}")
        return 1
    esperados = generar()
    for ruta, contenido in esperados.items():
        ruta.parent.mkdir(parents=True, exist_ok=True)
        if not ruta.exists() or ruta.read_text(encoding="utf-8") != contenido:
            ruta.write_text(contenido, encoding="utf-8", newline="\n")
            print(f"escrito  {ruta.relative_to(ROOT)}")
    for ruta in _huerfanos(esperados):
        ruta.unlink()
        print(f"borrado  {ruta.relative_to(ROOT)} (sin fuente)")
        if ruta.parent != SKILLS_DESTINO and ruta.parent.is_relative_to(SKILLS_DESTINO) and not any(ruta.parent.iterdir()):
            ruta.parent.rmdir()
    n_skills = len([p for p in SKILLS_FUENTE.iterdir() if p.is_dir()]) if SKILLS_FUENTE.exists() else 0
    print(f"✓ {len(AGENTS)} subagentes, {len(COMMANDS)} comandos y {n_skills} skills para Claude Code y OpenCode")
    return 0


if __name__ == "__main__":
    sys.exit(main())

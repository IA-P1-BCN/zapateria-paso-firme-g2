# SCOPE: infraestructura-agentes (NO tocar backend/frontend/workflows)

# CLAUDE.md

Las instrucciones del proyecto son las mismas para todas las herramientas y viven en `AGENTS.md`:

@AGENTS.md

## Solo para Claude Code

- **Skills**: `.claude/skills/` es la fuente. Tras editar una, ejecuta `python scripts/sync_agents.py` para copiarla a `.opencode/skills/` (la usa el resto del equipo con OpenCode). Se cargan solas cuando son relevantes o con `/<nombre>`.
- **Subagentes y comandos**: `.claude/agents/` y `.claude/commands/` son **generados**. Edita `.agents/agents/` o `.agents/commands/` y ejecuta `python scripts/sync_agents.py`.
- **Permisos**: `.claude/settings.json` bloquea editar `backend/` y `frontend/` y leer `.env`, y pide confirmación para tocar `workflows/`, hacer commit o push. Tus ajustes personales van en `.claude/settings.local.json` (no se sube).
- **n8n-mcp** (opcional, lo recomienda el enunciado). Se añade en ámbito *local* para que la clave no llegue al repo:

  ```bash
  claude mcp add n8n-mcp --scope local \
    -e MCP_MODE=stdio -e LOG_LEVEL=error -e DISABLE_CONSOLE_OUTPUT=true \
    -e N8N_API_URL=http://localhost:5678 -e N8N_API_KEY=<tu-clave-de-n8n> \
    -- npx -y n8n-mcp
  ```

  Con el MCP conectado puedes consultar nodos y validar flujos. **No** lo uses para activar flujos ni para borrar nada en la instancia.

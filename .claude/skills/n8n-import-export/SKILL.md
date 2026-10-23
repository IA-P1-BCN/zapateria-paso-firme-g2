---
# SCOPE: infraestructura-agentes (NO tocar backend/frontend/automation)
name: n8n-import-export
description: Cómo exportar flujos de n8n a JSON para versionarlos en Git y cómo importarlos en otra instancia (CLI de n8n dentro de Docker, UI o n8n-mcp), y cómo limpiar el JSON antes de una PR. Úsala cuando haya que subir, bajar, sincronizar o compartir un flujo.
---

# Importar y exportar flujos

La carpeta de flujos es `automation/` <<PENDIENTE: o `workflows/`, como pide el enunciado>>. El contenedor de n8n **no** monta el repositorio, así que se copia con `docker compose cp`.

## Exportar (n8n → repo)

```bash
# 1. Ver ids
docker compose exec n8n n8n list:workflow
# 2. Exportar uno, legible
docker compose exec n8n n8n export:workflow --id=<ID> --pretty --output=/tmp/flujo.json
# 3. Copiarlo al repo con el nombre de su spec
docker compose cp n8n:/tmp/flujo.json automation/003-abonos-a-distancia.json
```

Alternativa: en el editor, menú `…` → *Download*.

## Importar (repo → n8n)

```bash
docker compose cp automation/003-abonos-a-distancia.json n8n:/tmp/flujo.json
docker compose exec n8n n8n import:workflow --input=/tmp/flujo.json
```

Alternativa: en el editor, *Import from File*. Tras importar: **asignar las credenciales** en cada nodo (las referencias no traen la credencial a otra instancia) y comprobar el Error Workflow.

## Con n8n-mcp (opcional)

Si el MCP `n8n-mcp` está configurado (ver `CLAUDE.md` o `.opencode/opencode.jsonc`), el agente puede consultar la documentación de nodos y validar un JSON. **Permitido**: buscar nodos, validar, crear un flujo **inactivo** en la instancia local. **Prohibido**: activar/publicar, borrar flujos, tocar credenciales.

## Limpieza antes de la PR (checklist)

- [ ] `"active": false`.
- [ ] Sin valores secretos (busca: `apiKey`, `X-API-Key`, `Bearer`, `password`, `token`, `secret`).
- [ ] `pinData` vacío o solo con datos ficticios (`@example.com`).
- [ ] `settings.errorWorkflow` asignado (salvo el propio `[ERR]`).
- [ ] Nombre del flujo y del archivo coinciden con la spec.
- [ ] El JSON es válido: `python -m json.tool automation/<archivo>.json > /dev/null`.

## Nunca

- Subir la carpeta de datos de n8n (`n8n_data`) ni exportar credenciales (`export:credentials`).
- Importar sobre la instancia de otra persona sin avisar.

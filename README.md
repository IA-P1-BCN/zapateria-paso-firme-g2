# Zapatería Paso Firme · Automatizaciones con n8n

Sistema de **apartados** de una zapatería de barrio: el cliente deja un abono inicial y paga el resto a plazos.
La app (FastAPI + HTML/JS) ya guarda apartados, abonos, ventas y vales y avisa a **n8n** por webhook. Este
repositorio añade las **automatizaciones en n8n** (confirmaciones, recibos, abonos por Bizum, cierre diario,
avisos de error…) y la capa de agentes de IA con la que se construyen.

- Enunciado: [`docs/BRIEFING_zapateria.md`](docs/BRIEFING_zapateria.md)
- Cómo funciona la app (endpoints, webhook, errores): [`docs/guia-de-la-app.md`](docs/guia-de-la-app.md)
- Producto y flujos: [`docs/prd-nivel-medio.md`](docs/prd-nivel-medio.md), [`docs/diagramas/`](docs/diagramas/)
- Cómo colaborar (ramas, commits, PR): [`CONTRIBUTING.md`](CONTRIBUTING.md)
- Reglas para agentes de IA: [`AGENTS.md`](AGENTS.md)

## Arrancar el entorno

Requisitos: Docker y Docker Compose.

```bash
cp .env.example .env          # rellena tu API_KEY y el resto de valores
docker compose up -d          # app en http://localhost:8000 · n8n en http://localhost:5678
docker compose logs tienda    # comprobar si fallan los avisos a n8n
```

Dentro de n8n la app es `http://tienda:8000` (no `localhost`) y la app avisa a `http://n8n:5678/webhook/tienda`.

## Importar los flujos en n8n

Los flujos están en [`workflows/`](workflows/) como `NNN-slug.json`, con el número de su spec
(tabla de equivalencias con el enunciado en [`workflows/README.md`](workflows/README.md)).

1. **Desde la UI**: en n8n, *Workflows → Import from File* y elige el JSON.
2. **Desde la terminal** (el contenedor de n8n no monta el repositorio):

   ```bash
   docker compose cp workflows/001-confirmacion-apartado.json n8n:/tmp/flujo.json
   docker compose exec n8n n8n import:workflow --input=/tmp/flujo.json
   ```

3. **Crea las credenciales en la UI** (los JSON solo las nombran, nunca llevan claves):
   - `API tienda` → *Header Auth*, Name `X-API-Key`, Value = la `API_KEY` de tu `.env`.
   - Gmail → la cuenta de la tienda (canal único de avisos a clientes y a Marisa).
4. Asigna el Error Workflow `[ERR] Avisos de error` en *Settings* de cada flujo.
5. Prueba con la *Test URL* y los casos de `specs/features/NNN-*/fixtures.md`.
6. **Activa** el flujo solo cuando lo haya revisado una persona. Los JSON del repo se guardan con `"active": false`.

Para exportar un flujo de vuelta al repo, limpiar el JSON y validarlo: skill
[`n8n-import-export`](.claude/skills/n8n-import-export/SKILL.md) y `python scripts/validate_workflows.py workflows --estricto`.

## Estructura

| Ruta | Qué es |
|---|---|
| `backend/`, `frontend/` | La app (no se modifica en este proyecto) |
| `workflows/` | Flujos n8n exportados (`NNN-slug.json`) |
| `specs/` | Spec-Driven Development: constitución, backlog y una carpeta por feature (spec, plan, tasks, fixtures) |
| `data/` | Datos de prueba del enunciado (CSV del Excel antiguo y correos del banco) |
| `docs/` | Enunciado, guía de la app, PRD, diagramas y bitácora de IA (`docs/ai-log.md`) |
| `.agents/`, `.claude/`, `.opencode/`, `scripts/` | Capa de agentes de IA (ver [`.agents/README.md`](.agents/README.md)) |

## Comprobaciones antes de una PR

```bash
cd backend && python -m pytest                 # tests de la app (no se modifican)
python scripts/validate_workflows.py workflows --estricto
python scripts/sync_agents.py --check          # si tocaste la capa de agentes
python scripts/validate_agent_infra.py
```

# SCOPE: infraestructura-agentes (NO tocar backend/frontend/workflows)

# AGENTS.md · Zapatería Paso Firme

Punto de entrada **común** para cualquier agente de IA (OpenCode, Claude Code, Aider, Cline…).
Léelo entero antes de hacer nada. Es corto a propósito: el detalle está en las skills y en `specs/`, que se cargan cuando hacen falta.

## 1. Qué es este proyecto

Zapatería de barrio con un **sistema de apartados**: el cliente deja un abono inicial y paga el resto a plazos.
Ya existe una **app** (FastAPI + HTML/JS) que guarda apartados, abonos, ventas y vales, aplica las reglas del negocio y avisa a **n8n** por webhook.
**Nuestro trabajo NO es programar la app**: es construir automatizaciones en **n8n** (avisos, recibos, cierres, vencimientos, informes, abonos por Bizum) que hablen con ella.

- Enunciado completo: `docs/BRIEFING_zapateria.md`
- Cómo funciona la app (endpoints, webhook, errores): `docs/guia-de-la-app.md`
- Modelo conceptual del dominio: `ontology.md`
- Principios no negociables: `specs/constitution.md`

## 2. Mapa del repositorio

| Ruta | Qué es | ¿Puede tocarla un agente? |
|---|---|---|
| `backend/` | API FastAPI (MVC: models, schemas, routes, controllers, middleware, services) | ❌ **Nunca.** Solo lectura, como fuente de verdad |
| `frontend/` | Interfaz HTML/CSS/JS plano (no es React) | ❌ **Nunca.** Solo lectura |
| `workflows/` | Flujos n8n exportados en JSON (`NNN-slug.json`, ver `workflows/README.md`) | ⚠️ Solo el subagente `flow-builder`, con spec **Aprobada** y confirmación humana (ADR-0002) |
| `data/` | CSV del Excel antiguo y correos del banco (`data/correos/*.eml`) | ❌ Solo lectura. Son datos de prueba del enunciado |
| `docs/` | Enunciado, guía de la app y bitácora de IA (`docs/ai-log.md`) | ⚠️ Solo `ai-scribe` puede añadir entradas a `docs/ai-log.md` |
| `specs/` | Spec-Driven Development: constitución, specs, planes, tareas | ✅ Sí, siguiendo `specs/README.md` |
| `.agents/` | Fuente única de subagentes (`agents/`), comandos (`commands/`), plantilla de bitácora y decisiones (ADR). Ya no contiene skills | ✅ Sí; después ejecuta `python scripts/sync_agents.py` |
| `.claude/` | Config de Claude Code + **skills** (`.claude/skills/` es la **única fuente** de skills; Claude Code solo lee esta carpeta) | ✅ Skills sí; `agents/` y `commands/` son **generados** |
| `.opencode/` | Config de OpenCode (`opencode.jsonc`; `agents/`, `commands/` y `skills/` **generados**). OpenCode lee `.opencode/skills/` y, por compatibilidad, `.claude/skills/` | ✅ Solo `opencode.jsonc` |
| `scripts/` | Utilidades de la capa de agentes (sync, validación, nueva feature) | ✅ Sí |

## 3. Reglas duras (lo que un agente NO hace nunca)

1. **No modifica `backend/` ni `frontend/`.** Si una automatización necesita algo que la app no tiene, se anota como `<<PENDIENTE>>` en la spec y decide un humano.
2. **No escribe credenciales, claves, tokens ni contraseñas** en ningún archivo (JSON de flujos incluido). En n8n las credenciales se crean en la UI y los flujos solo las referencian por nombre. Nunca lee `.env`.
3. **No activa ni publica flujos** en n8n, ni toca la instancia de producción. Los JSON se exportan con `"active": false`.
4. **No hace `git commit`, `git push`, merge ni abre PRs** por su cuenta. Prepara los cambios; los confirma un humano.
5. **No recalcula importes que da la app** (`abonado`, `pendiente`, `estado`, `fecha_limite`, importe del vale). Usa los que llegan en el webhook o la API.
6. **La IA extrae, el flujo decide.** Un modelo de lenguaje puede sacar datos de un texto (ordenante, importe, concepto), pero la decisión de registrar, rechazar o preguntar a Marisa la toma el flujo con IF/Switch y la API.
7. **No inventa endpoints, campos ni eventos.** Si no está en `backend/routes/`, `backend/schemas/` o `docs/guia-de-la-app.md`, no existe. Usa `<<PENDIENTE: confirmar en backend/...>>`.
8. **No construye nada sin spec aprobada** (`specs/features/NNN-*/spec.md` con `Estado: Aprobada`).
9. **No cambia una prueba para que pase.** Si falla, se arregla el flujo.
10. **No envía a modelos externos más datos personales de los imprescindibles** (RGPD).

## 4. El dominio en 10 líneas (detalle en `ontology.md`)

- **Apartado** = un par de zapatos (producto + talla) reservado por un cliente. Estados: `activo` → `liquidado` | `vencido`.
- Abono inicial **≥ 5 €** y ≤ precio. Plazo: `fecha_limite` = fecha + **90 días**.
- **Abonos** de cualquier importe, **nunca más de lo pendiente**, solo si el apartado está `activo` y no ha pasado `fecha_limite`.
- `liquidado` lo pone la app sola cuando lo pendiente llega a 0.
- `vencido` **no** lo pone la app sola: n8n llama a `POST /api/apartados/{id}/vencer` cuando ya pasó el plazo; la app genera un **vale** con lo abonado.
- Formas de pago válidas en la app: `efectivo`, `tarjeta`, `bizum` (no existe `transferencia`).
- **Cliente** no es una tabla: son campos de texto del apartado (`cliente`, `telefono`, `email`). No hay catálogo de productos ni inventario.
- Cifras de Marisa: ventas del día (ventas + abonos), recaudación mensual (separando ventas y abonos), total pendiente (suma de `pendiente` de los activos).

## 5. Integración app ↔ n8n (lo mínimo para no equivocarse)

- Desde **dentro de n8n** la app es `http://tienda:8000` (no `localhost`). Desde tu máquina, `http://localhost:8000`.
- Toda llamada a `/api/...` lleva la cabecera `X-API-Key`. En n8n: credencial **Header Auth** creada en la UI, nunca el valor en el nodo.
- La app envía **un único webhook** `POST http://n8n:5678/webhook/tienda` con `{"evento": "...", "datos": {...}}`. Eventos: `apartado.creado`, `abono.registrado`, `venta.registrada`, `apartado.vencido`.
- En n8n el cuerpo llega dentro de `body`: `{{ $json.body.evento }}`, `{{ $json.body.datos.estado }}`.
- El aviso se envía **una vez y sin reintentos**. Los flujos programados consultan la API, no dependen de los avisos.
- Errores de la API: `401` (clave), `404` (no existe), `422` (regla del negocio) con `{"detail": "..."}`. Para tratarlos: *On Error → Continue (using error output)*.
- Detalle completo: skill `tienda-api`.

## 6. Convenciones (resumen; detalle en la skill `n8n-convenciones`)

- Nombre de flujo: `[NNN] Nombre en español`, con el **número de su spec** (`[001] Confirmación de apartado`), no el número de flujo del enunciado. Sub-flujos: `[SUB] …`. Error Workflow: `[ERR] Avisos de error`. Enrutador: `[000] Enrutador de eventos`.
- Nombre de nodo: verbo + objeto (`Pedir apartado a la API`, `Enviar recibo al cliente`); IF/Switch como pregunta (`¿Liquidado?`).
- Archivo exportado: `workflows/NNN-slug.json` (3 dígitos), numerado igual que su spec. El nº de flujo del enunciado (`FL-XX`) va en la cabecera de la spec (ADR-0002).
- Rama: `feature/HU-XX-slug`. Una tarea del Kanban = un flujo (o parte) = una rama = una PR.
- Variables configurables (umbral de venta grande, hora del cierre…) en variables de n8n, no fijas en el nodo.

## 7. Forma de trabajo (Spec-Driven Development)

```
HU del enunciado ──▶ /sdd-spec ──▶ spec.md (Borrador) ──▶ revisión humana ──▶ Aprobada
      ──▶ /sdd-plan ──▶ plan.md ──▶ /sdd-tasks ──▶ tasks.md (asignables a agente o humano)
      ──▶ /construir-flujo ──▶ JSON en workflows/ ──▶ importar y probar en n8n (humano)
      ──▶ /revisar-flujo ──▶ PR con revisión humana ──▶ /bitacora
```

Ver `specs/README.md`. Plantillas en `specs/_templates/`. Nueva feature: `python scripts/new_feature.py <NNN> <slug> --hu HU-XX --fl FL-XX`.

## 8. Subagentes y skills disponibles

**Subagentes** (contexto aislado, devuelven un resumen). Fuente: `.agents/agents/`.

| Subagente | Para qué | Escribe en |
|---|---|---|
| `spec-writer` | Redactar `spec.md` desde una HU | `specs/features/**` |
| `flow-builder` | Generar el JSON del flujo desde spec+plan+tasks aprobados | `workflows/**` y casillas de `tasks.md` |
| `flow-reviewer` | Revisar un flujo: seguridad, datos personales, reglas, errores | Nada (solo lectura) |
| `api-contract-checker` | Comprobar que specs/flujos usan endpoints y campos que existen | Nada (solo lectura) |
| `test-designer` | Diseñar payloads y casos de prueba (fixtures) | `specs/features/**/fixtures.md` |
| `ai-scribe` | Registrar prompts y decisiones en la bitácora | `docs/ai-log.md` |

**Skills** (se cargan bajo demanda; se editan **solo** en `.claude/skills/` y `python scripts/sync_agents.py` las copia a `.opencode/skills/`):
- Del proyecto: `sdd-workflow`, `dominio-apartados`, `tienda-api`, `n8n-convenciones`, `n8n-import-export`, `revision-seguridad-flujos`, `datos-de-prueba`, `trazabilidad-ia`.
- Del equipo: `paso-firme-review`, `paso-firme-verify`.
- Externas adaptadas (ADR-0002, D8): `n8n-expression-syntax`, `n8n-code-javascript`, `n8n-workflow-patterns`. Si contradicen este archivo o una skill del proyecto, **prevalece el proyecto**.

**Comandos**: `/sdd-spec`, `/sdd-plan`, `/sdd-tasks`, `/construir-flujo`, `/revisar-flujo`, `/bitacora` y, en OpenCode, `/paso-firme-review` y `/paso-firme-verify` (en Claude Code son skills y se invocan igual).

**Orquestación**: los subagentes **no se llaman entre sí**. El agente principal (o el comando) orquesta `spec-writer` → aprobación humana → `/sdd-plan` y `/sdd-tasks` → `flow-builder` → `flow-reviewer` + `api-contract-checker` → `ai-scribe`, con revisión humana entre pasos. Detalle en `.agents/README.md`.

## 9. Comandos útiles

```bash
cp .env.example .env && docker compose up -d     # levantar app (8000) y n8n (5678)
docker compose logs tienda                       # ver si fallan los avisos a n8n
python scripts/sync_agents.py                    # regenerar subagentes/comandos tras editar .agents/
python scripts/validate_agent_infra.py           # validar la capa de agentes antes de una PR
```

Los tests de la app (`cd backend && pytest`) solo se ejecutan para comprobar que no se ha roto nada; nunca se modifican.

## 10. Marcadores

`<<PENDIENTE: ...>>` = dato que un humano debe confirmar. Un agente nunca lo sustituye por una suposición; lo deja y lo menciona en su resumen.

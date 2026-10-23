---
# SCOPE: infraestructura-agentes (NO tocar backend/frontend/automation)
# GENERADO por scripts/sync_agents.py desde .claude/skills/sdd-workflow/SKILL.md. No editar a mano.
name: sdd-workflow
description: Ciclo Spec-Driven Development del proyecto (spec → plan → tasks → flujo → revisión). Úsala al crear o editar cualquier archivo de specs/, al pasar una feature de estado o cuando alguien pida "hacer la spec", "el plan" o "las tareas" de una historia de usuario.
---

# Spec-Driven Development en Paso Firme

## Dónde está todo

- Principios: `specs/constitution.md` (manda sobre todo lo demás).
- Proceso y estados: `specs/README.md`.
- Mapa HU → feature: `specs/backlog.md`.
- Plantillas: `specs/_templates/{spec,plan,tasks}.md`.
- Crear carpeta nueva: `python scripts/new_feature.py <NNN> <slug> --hu HU-XX [--titulo "…"]`.

## Gates (no te los saltes)

| Para escribir… | Requisito |
|---|---|
| `spec.md` | Existe la HU en `docs/BRIEFING_zapateria.md` o un requisito explícito |
| `plan.md` | `spec.md` con `Estado: Aprobada` (puesto por una persona) |
| `tasks.md` | `plan.md` existe y sus endpoints han pasado `api-contract-checker` |
| JSON del flujo | Las tres cosas anteriores + la tarea asignada |

Si un gate no se cumple: **para**, dilo en tu resumen y propone el paso que falta. No cambies tú el `Estado:` a `Aprobada`.

## Cómo escribir una buena spec

1. Copia los criterios de aceptación de la HU **literalmente** (CA-1, CA-2…). Puedes añadir, no quitar.
2. Cada entrada debe existir en `backend/schemas/` o en `docs/guia-de-la-app.md`. Si no, `<<PENDIENTE: confirmar en backend/...>>`.
3. Rellena §7 (errores y bordes) con al menos: dato opcional ausente, error 4xx de la API, fallo del canal de envío.
4. §9 «Datos personales»: qué sale hacia terceros (IA, correo, Telegram).
5. Las decisiones que no te corresponden (canal, hora, carpeta) van a §11 como `<<PENDIENTE>>`.

## Cómo escribir un buen plan

- Nodos en orden con nombre según la skill `n8n-convenciones`.
- Tabla de llamadas a la API con método, ruta, parámetros y campos de respuesta usados.
- Credenciales **solo por nombre**.
- Una fila en «Riesgos y decisiones» por cada alternativa descartada.

## Cómo escribir buenas tareas

- Atómicas (una sesión), con tipo `agente` o `humano`, agente sugerido, responsable, dependencia y «hecho cuando» comprobable.
- Todo lo que exige la UI de n8n (credenciales, publicar, probar con la app) es `humano`.
- La última tarea siempre es la bitácora (`ai-scribe`).

## Definición de hecho de una feature

- [ ] Spec aprobada, plan y tareas al día con lo construido.
- [ ] JSON exportado con `"active": false`, sin secretos.
- [ ] Todos los casos de `fixtures.md` comprobados (evidencia en la PR).
- [ ] `flow-reviewer` → APROBADO y PR aprobada por otra persona.
- [ ] Entrada en `docs/ai-log.md`.

---
# SCOPE: infraestructura-agentes (NO tocar backend/frontend/workflows)
name: trazabilidad-ia
description: Cómo registrar en docs/ai-log.md (bitácora de IA, entregable del proyecto) la herramienta y el modelo usados, los prompts clave, las alucinaciones o errores del agente y las decisiones aceptadas o rechazadas. Úsala al cerrar una tarea hecha con IA, al detectar una alucinación o al comparar modelos.
---

# Trazabilidad de IA

Entregable: `docs/ai-log.md`. Plantilla de entrada: `.agents/templates/ai-log-entry.md`.

## Qué se registra (y qué no)

| Sí | No |
|---|---|
| Herramienta y modelo exactos (p. ej. OpenCode + modelo gratuito de Zen) | Conversaciones enteras |
| El prompt que funcionó (resumido si es largo) | Claves, tokens, `.env` |
| Errores y alucinaciones: qué inventó, cómo se detectó, cómo se corrigió | Datos personales de clientes |
| Decisiones: aceptado / rechazado / modificado y por qué | Opiniones sin evidencia |
| Enlace a la spec, la PR y la tarea | |

## Reglas

- Una entrada por tarea relevante, **añadida al final** (nunca reescribir entradas anteriores).
- Fecha absoluta (`2026-10-23`), autor humano responsable y agente/subagente usado.
- Si un agente inventó un endpoint, campo o nodo, regístralo siempre: es la evidencia más valiosa.
- Comparativa de modelos (nivel medio): misma tarea, misma entrada; tabla con calidad, velocidad y errores.

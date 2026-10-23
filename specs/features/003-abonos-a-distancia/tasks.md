# SCOPE: infraestructura-agentes (NO tocar backend/frontend/automation)

# 003 · Abonos a distancia — Tareas

| ID | Tarea | Tipo | Agente sugerido | Responsable | Depende de | Hecho cuando |
|---|---|---|---|---|---|---|
| T-003-01 | Resolver preguntas abiertas (transferencia, canal, duplicados) y aprobar la spec | humano | — | <<PENDIENTE>> | — | `Estado: Aprobada` |
| T-003-02 | Verificar los 9 casos esperados contra los datos de ejemplo de la app | agente | `test-designer` | <<PENDIENTE>> | 01 | Tabla de `fixtures.md` confirmada |
| T-003-03 | Diseñar prompt y esquema de extracción (solo extrae) | agente | `flow-builder` | <<PENDIENTE>> | 01 | Prompt en el plan; esquema JSON fijo |
| T-003-04 | Code «Buscar candidatos» con normalización de nombres | agente | `flow-builder` | <<PENDIENTE>> | 02 | Pasa los 9 casos en pinned data |
| T-003-05 | Generar el JSON completo del flujo | agente | `flow-builder` | <<PENDIENTE>> | 03, 04 | JSON válido, `"active": false` |
| T-003-06 | Crear credenciales (buzón, IA, API) en n8n | humano | — | <<PENDIENTE>> | 01 | Credenciales en la UI |
| T-003-07 | Probar los 9 correos con Form Trigger | humano | — | <<PENDIENTE>> | 05, 06 | CA-6 |
| T-003-08 | Revisión de seguridad y API | agente | `flow-reviewer`, `api-contract-checker` | <<PENDIENTE>> | 07 | APROBADO |
| T-003-09 | PR y revisión humana | humano | — | <<PENDIENTE>> | 08 | PR aprobada |
| T-003-10 | Bitácora (prompt de extracción y alucinaciones vistas) | agente | `ai-scribe` | <<PENDIENTE>> | 09 | Entrada en `docs/ai-log.md` |

## Seguimiento

- [ ] T-003-01
- [ ] T-003-02
- [ ] T-003-03
- [ ] T-003-04
- [ ] T-003-05
- [ ] T-003-06
- [ ] T-003-07
- [ ] T-003-08
- [ ] T-003-09
- [ ] T-003-10

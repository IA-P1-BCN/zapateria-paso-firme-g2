# SCOPE: infraestructura-agentes (NO tocar backend/frontend/automation)

# 002 · Recibo de abono — Tareas

| ID | Tarea | Tipo | Agente sugerido | Responsable | Depende de | Hecho cuando |
|---|---|---|---|---|---|---|
| T-002-01 | Aprobar la spec | humano | — | <<PENDIENTE>> | — | `Estado: Aprobada` |
| T-002-02 | Completar fixtures | agente | `test-designer` | <<PENDIENTE>> | 01 | Un caso por CA |
| T-002-03 | Generar el JSON del flujo | agente | `flow-builder` | <<PENDIENTE>> | 02, 000 | JSON válido, `"active": false` |
| T-002-04 | Importar y probar (fixtures + abono real en la app) | humano | — | <<PENDIENTE>> | 03 | CA-1…CA-4 |
| T-002-05 | Revisión automática | agente | `flow-reviewer` | <<PENDIENTE>> | 04 | APROBADO |
| T-002-06 | PR y revisión humana | humano | — | <<PENDIENTE>> | 05 | PR aprobada |
| T-002-07 | Bitácora | agente | `ai-scribe` | <<PENDIENTE>> | 06 | Entrada en `docs/ai-log.md` |

## Seguimiento

- [ ] T-002-01
- [ ] T-002-02
- [ ] T-002-03
- [ ] T-002-04
- [ ] T-002-05
- [ ] T-002-06
- [ ] T-002-07

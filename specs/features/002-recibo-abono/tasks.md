# SCOPE: infraestructura-agentes (NO tocar backend/frontend/workflows)

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

- [x] T-002-01 · Spec aprobada por levifvy el 2026-10-26
- [x] T-002-02 · fixtures.md: F-002-1…F-002-12, cobertura CA-1…CA-4
- [ ] T-002-03 · JSON generado y validado (`validate_workflows.py --estricto` OK); integración con 000 pendiente
- [x] T-002-04 · Probado por levifvy el 2026-10-26: CA-1…CA-4 OK con fixtures (E2E con la app pendiente de 000)
- [x] T-002-05 · flow-reviewer: APROBADO (0 bloqueantes) · api-contract-checker: CONTRATO OK (2026-10-26)
- [ ] T-002-06
- [x] T-002-07 · Entrada «2026-10-26 · HU-02 · #11» en `docs/ai-log.md`

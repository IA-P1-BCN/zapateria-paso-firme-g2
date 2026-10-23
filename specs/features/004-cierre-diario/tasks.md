# SCOPE: infraestructura-agentes (NO tocar backend/frontend/automation)

# 004 · Cierre diario — Tareas

| ID | Tarea | Tipo | Agente sugerido | Responsable | Depende de | Hecho cuando |
|---|---|---|---|---|---|---|
| T-004-01 | Decidir hora, histórico y canal; aprobar la spec | humano | — | <<PENDIENTE>> | — | `Estado: Aprobada` |
| T-004-02 | Completar fixtures con totales esperados | agente | `test-designer` | <<PENDIENTE>> | 01 | Totales calculados a mano en los casos |
| T-004-03 | Generar el JSON del flujo | agente | `flow-builder` | <<PENDIENTE>> | 02 | JSON válido, `"active": false` |
| T-004-04 | Crear credenciales (Sheets, canal) y la hoja | humano | — | <<PENDIENTE>> | 01 | Hoja creada, credenciales en la UI |
| T-004-05 | Probar con datos de ejemplo y comparar con la app | humano | — | <<PENDIENTE>> | 03, 04 | CA-1…CA-5 |
| T-004-06 | Revisión automática | agente | `flow-reviewer`, `api-contract-checker` | <<PENDIENTE>> | 05 | APROBADO |
| T-004-07 | PR y revisión humana | humano | — | <<PENDIENTE>> | 06 | PR aprobada |
| T-004-08 | Bitácora | agente | `ai-scribe` | <<PENDIENTE>> | 07 | Entrada en `docs/ai-log.md` |

## Seguimiento

- [ ] T-004-01
- [ ] T-004-02
- [ ] T-004-03
- [ ] T-004-04
- [ ] T-004-05
- [ ] T-004-06
- [ ] T-004-07
- [ ] T-004-08

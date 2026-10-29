# SCOPE: infraestructura-agentes (NO tocar backend/frontend/workflows)

# 005 · Avisos de error — Tareas

| ID | Tarea | Tipo | Agente sugerido | Responsable | Depende de | Hecho cuando |
|---|---|---|---|---|---|---|
| T-005-01 | Aprobar la spec | humano | — | <<PENDIENTE>> | — | `Estado: Aprobada` |
| T-005-02 | Fixtures: flujo que falla con secreto falso | agente | `test-designer` | <<PENDIENTE>> | 01 | Caso documentado |
| T-005-03 | Generar el JSON del Error Workflow | agente | `flow-builder` | <<PENDIENTE>> | 02 | JSON válido, `"active": false` |
| T-005-04 | Importar, asignarlo en todos los flujos y probar | humano | — | <<PENDIENTE>> | 03 | CA-1, CA-2 |
| T-005-05 | Revisión automática | agente | `flow-reviewer` | <<PENDIENTE>> | 04 | APROBADO y CA-3 comprobado |
| T-005-06 | PR y revisión humana | humano | — | <<PENDIENTE>> | 05 | PR aprobada |
| T-005-07 | Bitácora | agente | `ai-scribe` | <<PENDIENTE>> | 06 | Entrada en `docs/ai-log.md` |

## Seguimiento

- [ ] T-005-01
- [ ] T-005-02
- [x] T-005-03
- [ ] T-005-04
- [ ] T-005-05
- [ ] T-005-06
- [ ] T-005-07

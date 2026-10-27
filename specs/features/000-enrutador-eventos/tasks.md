# SCOPE: infraestructura-agentes (NO tocar backend/frontend/workflows)

# 000 · Enrutador de eventos — Tareas

| ID | Tarea | Tipo | Agente sugerido | Responsable | Depende de | Hecho cuando |
|---|---|---|---|---|---|---|
| T-000-01 | Aprobar la spec y resolver la pregunta abierta | humano | — | Levi | — | `Estado: Aprobada` |
| T-000-02 | Revisar fixtures de eventos y casos de borde | agente | `test-designer` | Brian | 01 | `fixtures.md` cubre CA-1…CA-4 |
| T-000-03 | Generar el JSON del enrutador | agente | `flow-builder` | Brian | 02 | JSON válido, `"active": false`, nombres según convención |
| T-000-04 | Importar, publicar en local y probar con la app real | humano | — | Brian | 03 | Crear un apartado en la app genera una ejecución por la rama correcta |
| T-000-05 | Revisión automática | agente | `flow-reviewer` | Brian | 04 | Veredicto APROBADO |
| T-000-06 | PR y revisión humana | humano | — | <<PENDIENTE>> | 05 | PR aprobada |
| T-000-07 | Entrada en la bitácora | agente | `ai-scribe` | <<PENDIENTE>> | 06 | Entrada en `docs/ai-log.md` |
| T-000-08 | Cablear Execute Workflow a 001/002 y asignar el Error Workflow 005 cuando existan | humano | — | Brian | 001, 002, 005 | El enrutador ejecuta los hijos y el Error Workflow está asignado |

## Seguimiento

- [x] T-000-01
- [x] T-000-02
- [x] T-000-03
- [x] T-000-04
- [x] T-000-05
- [ ] T-000-06
- [ ] T-000-07
- [ ] T-000-08

## Notas de revisión

- T-000-05: `flow-reviewer` devolvió **APROBADO CON OBSERVACIONES**, sin bloqueantes. La única observación es la ausencia de `settings.errorWorkflow`, aplazada a T-000-08 hasta que exista `005`.

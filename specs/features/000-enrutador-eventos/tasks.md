# SCOPE: infraestructura-agentes (NO tocar backend/frontend/workflows)

# 000 · Enrutador de eventos — Tareas

| ID | Tarea | Tipo | Agente sugerido | Responsable | Depende de | Hecho cuando |
|---|---|---|---|---|---|---|
| T-000-01 | Aprobar la spec y resolver la pregunta abierta | humano | — | <<PENDIENTE>> | — | `Estado: Aprobada` |
| T-000-02 | Revisar fixtures de los 4 eventos | agente | `test-designer` | <<PENDIENTE>> | 01 | `fixtures.md` cubre CA-1…CA-4 |
| T-000-03 | Generar el JSON del enrutador | agente | `flow-builder` | <<PENDIENTE>> | 02 | JSON válido, `"active": false`, nombres según convención |
| T-000-04 | Importar, publicar en local y probar con la app real | humano | — | <<PENDIENTE>> | 03 | Crear un apartado en la app genera una ejecución por la rama correcta |
| T-000-05 | Revisión automática | agente | `flow-reviewer` | <<PENDIENTE>> | 04 | Veredicto APROBADO |
| T-000-06 | PR y revisión humana | humano | — | <<PENDIENTE>> | 05 | PR aprobada |
| T-000-07 | Entrada en la bitácora | agente | `ai-scribe` | <<PENDIENTE>> | 06 | Entrada en `docs/ai-log.md` |

## Seguimiento

- [ ] T-000-01
- [ ] T-000-02
- [ ] T-000-03
- [ ] T-000-04
- [ ] T-000-05
- [ ] T-000-06
- [ ] T-000-07

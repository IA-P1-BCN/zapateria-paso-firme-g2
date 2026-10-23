# SCOPE: infraestructura-agentes (NO tocar backend/frontend/automation)

# 001 · Confirmación de apartado — Tareas

| ID | Tarea | Tipo | Agente sugerido | Responsable | Depende de | Hecho cuando |
|---|---|---|---|---|---|---|
| T-001-01 | Decidir canal y aprobar la spec | humano | — | <<PENDIENTE>> | — | `Estado: Aprobada`, preguntas abiertas resueltas |
| T-001-02 | Completar fixtures | agente | `test-designer` | <<PENDIENTE>> | 01 | Un caso por CA |
| T-001-03 | Crear credencial de envío en n8n | humano | — | <<PENDIENTE>> | 01 | Credencial creada en la UI (nunca en el repo) |
| T-001-04 | Generar el JSON del flujo | agente | `flow-builder` | <<PENDIENTE>> | 02, 000 | JSON válido, `"active": false` |
| T-001-05 | Importar y probar con fixtures y con la app | humano | — | <<PENDIENTE>> | 03, 04 | CA-1…CA-4 comprobados |
| T-001-06 | Revisión automática | agente | `flow-reviewer` | <<PENDIENTE>> | 05 | APROBADO |
| T-001-07 | PR y revisión humana | humano | — | <<PENDIENTE>> | 06 | PR aprobada |
| T-001-08 | Bitácora | agente | `ai-scribe` | <<PENDIENTE>> | 07 | Entrada en `docs/ai-log.md` |

## Seguimiento

- [ ] T-001-01
- [ ] T-001-02
- [ ] T-001-03
- [ ] T-001-04
- [ ] T-001-05
- [ ] T-001-06
- [ ] T-001-07
- [ ] T-001-08

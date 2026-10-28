# SCOPE: infraestructura-agentes (NO tocar backend/frontend/workflows)

# 001 · Confirmación de apartado — Tareas

| ID | Tarea | Tipo | Agente sugerido | Responsable | Depende de | Hecho cuando |
|---|---|---|---|---|---|---|
| T-001-01 | Decidir canal y aprobar la spec | humano | — | Brian Hañari | — | `Estado: Aprobada`, preguntas abiertas resueltas |
| T-001-02 | Completar fixtures | agente | `test-designer` | Brian Hañari | 01 | Un caso por CA |
| T-001-03 | Crear credencial de envío en n8n | humano | — | Brian Hañari | 01 | Credencial `Gmail tienda` creada en la UI (nunca en el repo) |
| T-001-04 | Generar el JSON del flujo | agente | `flow-builder` | Brian Hañari | 02, 000 | JSON válido, `"active": false` |
| T-001-05 | Importar y probar con fixtures y con la app | humano | — | Brian Hañari | 03, 04 | CA-1…CA-4 comprobados |
| T-001-06 | Revisión automática | agente | `flow-reviewer` | Brian Hañari | 05 | APROBADO |
| T-001-07 | PR y revisión humana | humano | — | Miguel Matesanz | 06 | PR aprobada |
| T-001-08 | Bitácora | agente | `ai-scribe` | Brian Hañari | 07 | Entrada en `docs/ai-log.md` |

## Seguimiento

- [x] T-001-01
- [x] T-001-02
- [ ] T-001-03
- [x] T-001-04
- [ ] T-001-05
- [ ] T-001-06
- [ ] T-001-07
- [ ] T-001-08

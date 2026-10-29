# SCOPE: infraestructura-agentes (NO tocar backend/frontend/workflows)

# 004 · Cierre diario — Tareas

| ID | Tarea | Tipo | Agente sugerido | Responsable | Depende de | Hecho cuando |
|---|---|---|---|---|---|---|
| T-004-01 | Decidir hora (21:30), histórico (Google Sheets `Cierres`) y canal (Gmail); aprobar la spec | humano | — | Miguel Matesanz / Levi Flores | — | `Estado: Aprobada` en `spec.md` |
| T-004-02 | Completar fixtures con totales esperados | agente | `test-designer` | Miguel Matesanz | T-004-01 | Totales calculados a mano en los casos (`F-004-1` a `F-004-3`) |
| T-004-03 | Generar el JSON del flujo `workflows/004-cierre-diario.json` | agente | `flow-builder` | Miguel Matesanz | T-004-02 | JSON válido, `"active": false`, sin secretos |
| T-004-04 | Crear credenciales (`API tienda`, Google Sheets, Gmail) y hoja `Cierres` en n8n | humano | — | Miguel Matesanz | T-004-01 | Credenciales en la UI y hoja creada con cabeceras |
| T-004-05 | Probar con datos de ejemplo y comparar con la app | humano | — | Miguel Matesanz | T-004-03, T-004-04 | CA-1 a CA-5 verificados en n8n |
| T-004-06 | Revisión automática | agente | `flow-reviewer`, `api-contract-checker` | Levi Flores | T-004-03 | Veredicto APROBADO |
| T-004-07 | PR y revisión humana | humano | — | Levi Flores | T-004-05, T-004-06 | PR aprobada |
| T-004-08 | Bitácora | agente | `ai-scribe` | Miguel Matesanz | T-004-06 | Entrada en `docs/ai-log.md` |

## Seguimiento

- [x] T-004-01
- [x] T-004-02
- [x] T-004-03
- [ ] T-004-04
- [ ] T-004-05
- [x] T-004-06
- [ ] T-004-07
- [x] T-004-08

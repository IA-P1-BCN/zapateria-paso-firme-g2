# SCOPE: infraestructura-agentes (NO tocar backend/frontend/workflows)

# 008 · Informe mensual — Tareas

Reglas: cada tarea cabe en una sesión, tiene un responsable y un criterio de hecho comprobable.
Tipo: `agente` (lo hace un subagente y lo revisa una persona) o `humano` (requiere la UI de n8n, credenciales o decisión).

| ID | Tarea | Tipo | Agente sugerido | Responsable | Depende de | Hecho cuando |
|---|---|---|---|---|---|---|
| T-008-01 | Aprobar la spec (cambiar `Estado: Aprobada`) | humano | — | <<PENDIENTE>> | — | `Estado: Aprobada` en `spec.md` |
| T-008-02 | Escribir fixtures con totales esperados | agente | `test-designer` | <<PENDIENTE>> | T-008-01 | `fixtures.md` cubre CA-1 a CA-5 |
| T-008-03 | Generar el JSON del flujo `workflows/008-informe-mensual.json` | agente | `flow-builder` | <<PENDIENTE>> | T-008-02 | JSON válido, `"active": false`, sin secretos |
| T-008-04 | Importar, asignar credenciales y probar | humano | — | <<PENDIENTE>> | T-008-03 | Todos los casos de `fixtures.md` pasan en n8n |
| T-008-05 | Revisión automática | agente | `flow-reviewer`, `api-contract-checker` | <<PENDIENTE>> | T-008-03 | Veredicto APROBADO |
| T-008-06 | PR y revisión humana | humano | — | <<PENDIENTE>> | T-008-04, T-008-05 | PR aprobada por otra persona |
| T-008-07 | Entrada en la bitácora | agente | `ai-scribe` | <<PENDIENTE>> | T-008-05 | Entrada en `docs/ai-log.md` |

## Seguimiento

- [x] T-008-01
- [x] T-008-02
- [x] T-008-03
- [ ] T-008-04
- [x] T-008-05
- [ ] T-008-06
- [ ] T-008-07
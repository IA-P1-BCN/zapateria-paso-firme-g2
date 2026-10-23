# SCOPE: infraestructura-agentes (NO tocar backend/frontend/automation)

# {{ID}} · {{TITULO}} — Tareas

Reglas: cada tarea cabe en una sesión, tiene un responsable y un criterio de hecho comprobable.
Tipo: `agente` (lo hace un subagente y lo revisa una persona) o `humano` (requiere la UI de n8n, credenciales o decisión).

| ID | Tarea | Tipo | Agente sugerido | Responsable | Depende de | Hecho cuando |
|---|---|---|---|---|---|---|
| T-{{ID}}-01 | Aprobar la spec | humano | — | <<PENDIENTE>> | — | `Estado: Aprobada` |
| T-{{ID}}-02 | Escribir fixtures | agente | `test-designer` | <<PENDIENTE>> | 01 | `fixtures.md` cubre todos los CA |
| T-{{ID}}-03 | Generar el JSON del flujo | agente | `flow-builder` | <<PENDIENTE>> | 02 | JSON válido con `"active": false` |
| T-{{ID}}-04 | Importar, asignar credenciales y probar | humano | — | <<PENDIENTE>> | 03 | Todos los casos de `fixtures.md` pasan |
| T-{{ID}}-05 | Revisión automática | agente | `flow-reviewer` | <<PENDIENTE>> | 04 | Veredicto APROBADO |
| T-{{ID}}-06 | PR y revisión humana | humano | — | <<PENDIENTE>> | 05 | PR aprobada por otra persona |
| T-{{ID}}-07 | Entrada en la bitácora | agente | `ai-scribe` | <<PENDIENTE>> | 06 | Entrada en `docs/ai-log.md` |

## Seguimiento

- [ ] T-{{ID}}-01
- [ ] T-{{ID}}-02
- [ ] T-{{ID}}-03
- [ ] T-{{ID}}-04
- [ ] T-{{ID}}-05
- [ ] T-{{ID}}-06
- [ ] T-{{ID}}-07

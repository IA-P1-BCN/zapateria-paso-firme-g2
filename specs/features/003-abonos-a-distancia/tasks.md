# SCOPE: infraestructura-agentes (NO tocar backend/frontend/workflows)

# 003 · Abonos a distancia — Tareas

| ID | Tarea | Tipo | Agente sugerido | Responsable | Depende de | Hecho cuando |
|---|---|---|---|---|---|---|
| T-003-01 | Resolver preguntas abiertas (duplicados, respuesta de Marisa) y aprobar la spec | humano | — | <<PENDIENTE>> | — | `Estado: Aprobada` |
| T-003-02 | Verificar los 9 casos esperados contra los datos de ejemplo de la app | agente | `test-designer` | <<PENDIENTE>> | 01 | Tabla de `fixtures.md` confirmada |
| T-003-03 | Diseñar prompt y esquema de extracción (solo extrae) | agente | `flow-builder` | <<PENDIENTE>> | 01 | Prompt en el plan; esquema JSON fijo |
| T-003-04 | Code «Buscar candidatos» con normalización de nombres | agente | `flow-builder` | <<PENDIENTE>> | 02 | Pasa los 9 casos en pinned data |
| T-003-05 | Generar el JSON completo del flujo | agente | `flow-builder` | <<PENDIENTE>> | 03, 04 | JSON válido, `"active": false` |
| T-003-06 | Crear credenciales (buzón, IA, API) en n8n | humano | — | <<PENDIENTE>> | 01 | Credenciales en la UI |
| T-003-07 | Probar los 9 correos con Form Trigger | humano | — | <<PENDIENTE>> | 05, 06 | CA-6 |
| T-003-08 | Revisión de seguridad y API | agente | `flow-reviewer`, `api-contract-checker` | <<PENDIENTE>> | 07 | APROBADO |
| T-003-09 | PR y revisión humana | humano | — | <<PENDIENTE>> | 08 | PR aprobada |
| T-003-10 | Bitácora (prompt de extracción y alucinaciones vistas) | agente | `ai-scribe` | <<PENDIENTE>> | 09 | Entrada en `docs/ai-log.md` |

## Seguimiento

- [x] T-003-01 · Spec aprobada por el responsable humano en sesión el 2026-10-27 (decisiones: Data Table `Emails`, etiqueta `Banco` + `BANCO_REMITENTES`, Marisa registra a mano, `[TEST]` aparte, `referencia_apartado` en el esquema, transferencia → `bizum`). Queda `<<PENDIENTE>>` el modelo de IA y `Aprueba:`
- [x] T-003-02 · `fixtures.md` confirmado contra la API tras reiniciar los datos el 2026-10-27 (ids 1, 2, 3, 11, 12, 16 y 24; `q=Antonio` y `q=Silvia Cortes` vacíos). Añade F-003-10 (duplicado), F-003-11 (la IA no decide) y F-003-12 (remitente ajeno)
- [x] T-003-03 · Prompt y esquema en `plan.md` §7. Modelo elegido el 2026-10-29: `models/gemini-3.5-flash-lite`; probado en T-003-07 (extracción obtenida en `plan.md` §7.6)
- [x] T-003-04 · `Buscar candidatos` validado con los 9 correos reales en n8n (2026-10-29): resuelve por nombre (01, 03, 06, 09, con tildes), por referencia (02), por nombre abreviado + concepto (04) y marca dudoso/desconocido en 05 y 07. No se usó *pinned data*
- [x] T-003-05 · JSON en `workflows/003-abonos-a-distancia.json`; ajustado tras la prueba en n8n (sin `Detener por error de la API`, `errorWorkflow` = `<<ASIGNAR_EN_N8N>>`, modelo fijado; commit `0674949`)
- [x] T-003-06 · Credenciales creadas en n8n local el 2026-10-28/29: Gmail OAuth2 (cuenta común de la tienda), Gemini (API key de AI Studio), `API tienda` (Header Auth `X-API-Key`). Data Table `Emails` creada. Pendiente: renombrarlas a `Gmail tienda` e `IA extracción` en la UI
- [x] T-003-07 · Probado el 2026-10-29 con **Gmail real** en lugar del Form Trigger: los 9 correos dan el resultado esperado (ejecuciones 14–22) y F-003-10 (duplicado) no registra nada (ejecución 23). F-003-11a/b y F-003-12 quedan pendientes: no los exige el briefing (solo «los correos de `data/correos/`»). Ver evidencias en la PR #70
- [ ] T-003-08
- [ ] T-003-09
- [ ] T-003-10

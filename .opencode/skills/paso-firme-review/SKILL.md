---
# SCOPE: infraestructura-agentes (NO tocar backend/frontend/workflows)
# GENERADO por scripts/sync_agents.py desde .claude/skills/paso-firme-review/SKILL.md. No editar a mano.
name: paso-firme-review
description: Revisa un diff de Paso Firme frente a las reglas de negocio del briefing (IA extrae y el flujo decide, importes solo desde la app, credenciales solo en n8n, webhook correcto) y devuelve hallazgos concretos con archivo, impacto y comprobación sugerida. Úsala antes del push, antes de la revisión humana o cuando se solicite revisar una PR.
---

# Revisar cambios de Paso Firme

Leer `docs/BRIEFING_zapateria.md`, `docs/guia-de-la-app.md` y, si existe,
`AGENTS.md`. Identificar la rama o PR solicitada, el diff completo
(`git diff develop...HEAD` y `git status`) y los archivos que permitan
comprobar un posible defecto. Incluir archivos nuevos y cambios sin commit
cuando formen parte del alcance.

## Reglas que no se negocian

1. **La IA extrae, el flujo decide.** En nodos de IA el modelo solo saca
   datos (ordenante, importe, concepto). Qué apartado es y si se puede
   registrar lo deciden IF/Switch y la API. Que un modelo clasifique o
   decida un pago es un defecto de severidad alta.
2. **Los importes los da la app.** `abonado`, `pendiente`, importes de vales
   y totales vienen de la API. Nunca se recalculan en n8n, en una plantilla
   ni en un modelo. Sumas del cierre diario y del informe mensual: nodo Code
   sobre los movimientos que devuelve la API, sin inventar importes y sin
   redondear cada sumando; solo el **total** se redondea a 2 decimales para
   quitar el error de coma flotante (ADR-0002, D6).
3. **Credenciales solo en n8n.** Ninguna clave, token ni contraseña en JSON,
   código ni repo. Los nodos referencian credenciales por nombre (`API
   tienda`, Header Auth `X-API-Key`). Los JSON exportados se revisan
   con `python scripts/validate_workflows.py`.
4. **Sin datos personales reales** en el repo ni en el pinned data; solo los
   ejemplos de la app (`@example.com`).
5. **Pruebas como contrato.** Si una prueba falla, se arregla el flujo; nunca
   se cambia la prueba ni el resultado esperado.

## Convenciones a revisar en flujos n8n

- Webhook de la app: se lee `{{ $json.body.evento }}` y
  `{{ $json.body.datos... }}` (no `$json.evento`).
- Dentro de n8n la app es `http://tienda:8000`; `localhost` solo desde el
  navegador. Nombres de ficheros: `workflows/NNN-slug.json`.
- Nodos Code en JavaScript corto y comentado; sin llamadas HTTP (para eso
  está HTTP Request). Salida de IA con Structured Output Parser; al modelo
  solo asunto y cuerpo del correo (RGPD), nunca datos de la app.
- Manejo de errores: Error Workflow, salidas de error y reintentos donde
  tenga sentido.
- Backend: Python/FastAPI con pytest; los importes de la API tal cual los da
  (sin traducir campos).
- Código, scripts y commits en inglés; mensajes a persona usuaria en español.

## Cómo entregar la revisión

Priorizar defectos demostrables introducidos por el diff. Cada hallazgo
indica archivo/línea, condición que lo dispara, impacto y una forma de
comprobarlo. Separar una limitación ya documentada de un defecto nuevo. Si
no hay hallazgos, decirlo e indicar qué no se pudo comprobar; no inventar
problemas para completar una lista. La revisión automática no sustituye la
aprobación humana y no edita, publica, aprueba ni mergea nada salvo que se
haya autorizado por separado.

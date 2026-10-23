---
# SCOPE: infraestructura-agentes (NO tocar backend/frontend/automation)
# GENERADO por scripts/sync_agents.py desde .claude/skills/revision-seguridad-flujos/SKILL.md. No editar a mano.
name: revision-seguridad-flujos
description: Checklist de revisión de un flujo n8n antes de mergear (credenciales, datos personales y RGPD, webhooks expuestos, reglas de negocio, manejo de errores, convenciones). Úsala al revisar un JSON de flujo, una PR con flujos o al preparar la revisión humana.
---

# Revisión de flujos

Salida esperada: **veredicto** (`APROBADO` / `CAMBIOS NECESARIOS`) + lista de hallazgos `archivo · nodo · problema · cómo arreglarlo`, de más grave a menos.

## 1. Secretos (bloqueante)

- [ ] Ningún valor de clave, token o contraseña en `parameters` (busca `apiKey`, `X-API-Key`, `Authorization`, `Bearer `, `password`, `token`, `secret`, `sk-`, `AIza`).
- [ ] Las llamadas a la API usan la credencial Header Auth, no cabeceras escritas a mano.
- [ ] Ninguna URL con usuario/contraseña embebidos.
- [ ] El Error Workflow enmascara secretos en los mensajes.

## 2. Datos personales (bloqueante)

- [ ] `pinData` y fixtures sin datos reales (solo `@example.com`, teléfonos ficticios).
- [ ] A la IA solo se envía el texto imprescindible; nunca listas de clientes, teléfonos ni emails.
- [ ] Los mensajes a un cliente solo contienen **sus** datos.
- [ ] La spec documenta qué datos salen (§9).

## 3. Reglas de negocio

- [ ] Importes y estados salen del webhook o de la API; no se recalculan `abonado`/`pendiente`/`estado`.
- [ ] La IA no decide: el registro/rechazo depende de IF/Switch/Code + API.
- [ ] Los 422 de la API se tratan (rama de error → aviso a Marisa con `detail`).
- [ ] Ante ambigüedad (varios candidatos, sin concepto) **no se registra nada**.

## 4. Robustez

- [ ] `settings.errorWorkflow` asignado.
- [ ] Retry On Fail en envíos e IA.
- [ ] Listas vacías no rompen el flujo (Always Output Data donde haga falta).
- [ ] URLs internas `http://tienda:8000`, no `localhost`.
- [ ] Expresiones del webhook con `$json.body.…`.

## 5. Webhooks expuestos

- [ ] Solo existe el webhook `tienda` del enrutador (más los que pida una spec aprobada).
- [ ] Si un webhook es público (formulario, Telegram), la spec lo justifica y valida la entrada.
- [ ] Nota: la app no envía autenticación al webhook (`backend/services/n8n.py`); no se puede exigir sin tocar el backend.

## 6. Convenciones y contrato

- [ ] `"active": false`; nombres de flujo/nodos según `n8n-convenciones`.
- [ ] Cada endpoint usado existe (`api-contract-checker`).
- [ ] Hay un caso de `fixtures.md` por criterio de aceptación.

## Búsqueda rápida de secretos

```bash
grep -nEi '"(apiKey|password|token|secret|authorization)"\s*:\s*"[^"{=]' automation/*.json
grep -nE 'Bearer [A-Za-z0-9._-]{8,}|X-API-Key"?\s*:\s*"[^"{=]' automation/*.json
```

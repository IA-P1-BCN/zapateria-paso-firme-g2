# SCOPE: infraestructura-agentes (NO tocar backend/frontend/workflows)

# 005 · Avisos de error — Fixtures

La entrada es el item del **Error Trigger** de n8n, no un webhook de la tienda. Los campos que usa el aviso son los de la spec §4: `workflow` (nombre e id), `execution.url`, `lastNodeExecuted` y `execution.error` (mensaje y, si lo hay, stack).

```json
{"workflow": {"id": 101, "name": "[TEST] Falla a propósito"}, "execution": {"id": 4032, "url": "http://localhost:5678/execution/4032", "error": {"message": "Fallo de prueba", "stack": "…"}}, "lastNodeExecuted": "Fallar a propósito"}
```

> **Nota (PENDIENTE §4):** la forma exacta del item del Error Trigger varía entre versiones de n8n. Este bloque refleja los datos que fija la spec, **no** la estructura literal. Confirmar la forma real con el primer aviso recibido al importar y, si difiere, actualizar este bloque (ahí queda cerrado el `<<PENDIENTE>>` de la spec).

Los flujos `[TEST]` viven solo en la instancia de pruebas de n8n.

**Importante (igual que F-002-12 de la feature 002):** n8n **no lanza el Error Workflow en ejecuciones manuales**. Para cada caso, el flujo `[TEST]` se **activa** (publica) con su Error Workflow asignado en *Settings → Error workflow* y se provoca desde fuera (curl al webhook de producción o al producirse el fallo real). El mensaje del error lo genera el nodo que falla; el texto exacto del error técnico (p. ej. el texto de `ECONNREFUSED`) depende de la versión — lo que se exige está en la tabla.

Destinatario de referencia: `tienda@pasofirme.example` (buzón de prueba en la instancia local; el real es `<<PENDIENTE: dirección de la tienda, la crea Levi con el OAuth>>`). Datos ficticios: nombres inventados, emails `@example.com`, teléfonos `6xx 000 xxx`.

## Casos

| Caso | Cómo se provoca | Resultado esperado |
|---|---|---|
| F-005-1 Error simple (CA-1) | Flujo `[TEST] Falla a propósito`: Webhook (ruta `falla-test`, POST) → *Stop and Error* `Fallar a propósito` con mensaje «Fallo de prueba». Asignar el Error Workflow en *Settings* del flujo, **activarlo** y `curl -X POST http://localhost:5678/webhook/falla-test -H "Content-Type: application/json" -d '{}'` | Correo a `tienda@pasofirme.example` con los 5 datos: nombre del flujo `[TEST] Falla a propósito` (con su id), nodo `Fallar a propósito`, mensaje `Fallo de prueba`, fecha y hora del fallo y enlace a la ejecución (`http://localhost:5678/execution/{id}`). Ver [T-1](#t-1) para el formato de referencia |
| F-005-2 Secreto en el mensaje (CA-2) | Como F-005-1, cambiando el mensaje del *Stop and Error* a «X-API-Key: clave-falsa-123 Bearer abc.def». **JWT con puntos** (variante): mensaje «Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NSJ9.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c». Otra variante: el mismo JWT pegado **sin** etiqueta `Bearer`, dentro de un mensaje de más de 600 caracteres para forzar el recorte | El aviso lleva flujo, nodo, fecha y enlace como siempre. En el texto del error: `X-API-Key: ***` y `Bearer ***`. **Nunca** `clave-falsa-123` ni `abc.def`; si se incluye el stack, tampoco los contiene. Variante JWT: `Bearer ***` (el token completo nunca en claro, ni decodificable por mitades tras el recorte; el enmascarado se aplica antes del recorte de 600). JWT sin `Bearer`: el token también sale como `***` |
| F-005-3 API caída (CA-1, hoy) | Flujo `[TEST] Falla por API`: Webhook (ruta `falla-api-test`) → HTTP Request `Pedir apartados a la API` (GET `http://tienda:8000/api/apartados`, credencial `API tienda`). Asignar y activar. `docker compose stop tienda` y `curl -X POST http://localhost:5678/webhook/falla-api-test -d '{}'` | El aviso lleva flujo `[TEST] Falla por API`, nodo `Pedir apartados a la API`, fecha y enlace a la ejecución; el mensaje técnico muestra el error de conexión (`ECONNREFUSED` / «connect ECONNREFUSED»). *Variante rápida sin parar la tienda:* sin credencial en el nodo HTTP → error 401 con el `detail` de la app «Falta la cabecera X-API-Key o no es válida» |
| F-005-4 Datos personales en el error (CA-2, §7) | Como F-005-1, mensaje del *Stop and Error*: «Error al registrar a Carmen Ruiz (carmen@example.com, tel. 612 000 001): apartado duplicado» | El aviso lleva la información de diagnóstico completa: flujo `[TEST] Falla a propósito`, nodo `Fallar a propósito`, error técnico, fecha y enlace a la ejecución. **No contiene** el email `carmen@example.com`, el teléfono `612 000 001` ni el nombre `Carmen Ruiz` completos: aparecen enmascarados (p. ej. `***@example.com`, `612 *** ***`) o ausentes del mensaje. El detalle con los datos queda en el enlace a la ejecución de n8n |
| F-005-5 Falla el propio aviso (§7) | Con el flujo `[ERR] Avisos de error` construido: romper su envío (revocar/desfogar la credencial `Gmail tienda`, o cambiar temporalmente el destinatario a «no-es-un-correo») y provocar F-005-1 | **No llega ningún correo** (n8n no encadena Error Workflows). La ejecución del `[ERR]` queda registrada como fallida en *Executions* de n8n. Restaurar la credencial/destinatario después |
| F-005-6 Errores seguidos (§7) | Como F-005-1: lanzar el webhook `falla-test` 3 veces seguidas | Llegan **3 correos independientes**, uno por ejecución fallida, sin agrupar (cada uno con su id de ejecución y su enlace). Nada de «resumen de 3 errores» |

### T-1 · Formato de referencia del aviso

(F-005-1 y resto de casos) El nodo `Enviar aviso` no existe todavía: el texto exacto lo fija su construcción. **Lo exigible en todos los casos** son los 5 datos; a título de referencia:

```text
⚠️ Fallo en [TEST] Falla a propósito
Nodo: Fallar a propósito
Fecha: 29/10/2026 12:34
Error: Fallo de prueba
Detalle: http://localhost:5678/execution/4032
```

## Cómo probar

1. Crear los flujos `[TEST]` **solo en la instancia de pruebas** (no se exportan): cada uno con su Webhook de producción, el nodo que falla y el Error Workflow asignado en *Settings → Error workflow*.
2. Activar el `[TEST]` y provocar con `curl` (arriba). Comprobar el correo contra la tabla y el enlace a la ejecución.
3. F-005-5: provocarlo con el flujo `[ERR]` ya construido (rompe su envío de forma controlada) y verificar en *Executions* la ejecución fallida; luego restaurar.
4. Al recibir el primer aviso, comparar el item real del Error Trigger con el bloque del principio y actualizarlo (cierra el `<<PENDIENTE>>` de la spec §4); confirmar también la forma concreta de las máscaras de F-005-2 y F-005-4 y anotarla aquí.
5. Para F-002-12 (feature 002) ya quedó constatado el mismo comportamiento: en ejecución manual del `[TEST]` **no** se dispara el Error Workflow; el paso del test no debe depender de eso.

## Generalización

- Cuando existan los flujos 001 y 004, repetir F-005-3 con sus nodos reales (p. ej. `Pedir apartado a la API` del 001; el del cierre diario según su spec) y con el evento real de la app. Los avisos deben salir igual con cualquier flujo que tenga el Error Workflow asignado (CA-1).
- CA-3 (todos los flujos con el Error Workflow asignado) **no lleva fixture**: es una revisión de repositorio, la hace `flow-reviewer` al revisar cada PR (Constitución VIII). No se fuerza su provocación aquí.

Los flujos `[TEST]` son locales y no se exportan al repositorio.

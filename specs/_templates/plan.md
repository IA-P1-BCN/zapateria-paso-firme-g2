# SCOPE: infraestructura-agentes (NO tocar backend/frontend/automation)

# {{ID}} · {{TITULO}} — Plan

- **Spec:** `spec.md` (debe estar `Aprobada`)
- **Flujo n8n:** `[{{ID}}] {{TITULO}}` → `automation/{{ID}}-{{SLUG}}.json` <<PENDIENTE: confirmar carpeta>>
- **Fecha:** {{FECHA}}

## 1. Diseño del flujo

Lista ordenada de nodos (nombre según `n8n-convenciones`, tipo de nodo, qué hace).

| # | Nodo | Tipo n8n | Qué hace |
|---|---|---|---|

## 2. Llamadas a la API de la tienda

| Método y ruta | Cuándo | Cuerpo / parámetros | Campos de respuesta que se usan |
|---|---|---|---|

Comprobado con `api-contract-checker`: <<PENDIENTE: sí/no y fecha>>

## 3. Credenciales y variables (solo nombres, nunca valores)

| Nombre en n8n | Tipo | Para qué |
|---|---|---|

## 4. Manejo de errores

- Error Workflow asignado: `[ERR] Avisos de error`.
- Ramas de error (On Error → Continue using error output) en: …
- Reintentos: …

## 5. Datos de prueba

Ver `fixtures.md`. Casos mínimos: camino feliz, cada caso de error de la spec, datos vacíos.

## 6. Riesgos y decisiones

| Decisión | Alternativas | Por qué |
|---|---|---|

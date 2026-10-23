---
# SCOPE: infraestructura-agentes (NO tocar backend/frontend/automation)
name: datos-de-prueba
description: Cómo diseñar y usar datos de prueba para los flujos (fixtures.md, pinned data, payloads del webhook, correos del banco de data/correos, reinicio de datos de ejemplo, curl contra la Test URL). Úsala al escribir fixtures, preparar pruebas de un flujo o reproducir un fallo.
---

# Datos de prueba

**Las pruebas son el contrato** (Constitución V): si falla, se arregla el flujo, no la prueba.

## Formato de `fixtures.md`

Una tabla por feature: `Caso (F-NNN-k) | Entrada | Resultado esperado`, con un caso por cada criterio de aceptación y por cada borde de la spec (§7). Los payloads largos van debajo en bloques ```json```. Resultados esperados **concretos** (textos e importes exactos), no «funciona bien».

## Fuentes permitidas

| Fuente | Uso |
|---|---|
| Ejemplos de `docs/guia-de-la-app.md` §6 / skill `tienda-api` | Forma exacta de los eventos |
| `data/correos/*.eml` | 9 avisos del banco con su resultado esperado (tabla del enunciado) |
| `data/excel_actual_*.csv` | Migración (HU-10) |
| Datos de ejemplo de la app (`backend/seed.py`) | Pruebas de extremo a extremo. Fechas relativas al día de arranque |

Datos inventados: nombres ficticios, emails `@example.com`, teléfonos `6xx 000 xxx`. Nunca datos reales.

## Ejecutar

```bash
# Enviar un evento a la Test URL (con "Listen for test event" pulsado)
curl -X POST http://localhost:5678/webhook-test/tienda -H "Content-Type: application/json" -d @evento.json
# Provocar un evento real desde la app (la app avisa a la Production URL si el flujo está publicado)
curl -X POST http://localhost:8000/api/ventas -H "X-API-Key: $API_KEY" -H "Content-Type: application/json" -d '{"concepto":"Prueba","importe":4.5}'
# Volver a los datos de ejemplo de hoy
docker compose down -v && docker compose up -d
```

En el editor: fija la salida de un nodo (*Pin data*) para probar los siguientes sin repetir el disparador. Quita el pin data con datos reales antes de exportar.

## Correos del banco sin Gmail

Form Trigger con campos `asunto` y `cuerpo`, pegando el texto del `.eml`. Mismo flujo a partir del nodo de extracción.

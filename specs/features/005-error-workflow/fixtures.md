# SCOPE: infraestructura-agentes (NO tocar backend/frontend/automation)

# 005 · Avisos de error — Fixtures

| Caso | Cómo se provoca | Resultado esperado |
|---|---|---|
| F-005-1 Error simple | Flujo `[TEST] Falla a propósito` con nodo *Stop and Error* «Fallo de prueba», con este Error Workflow asignado | Aviso con «[TEST] Falla a propósito», nodo «Stop and Error», «Fallo de prueba» y enlace a la ejecución |
| F-005-2 Secreto en el mensaje | *Stop and Error* con «X-API-Key: clave-falsa-123 Bearer abc.def» | El aviso muestra `X-API-Key: ***` y `Bearer ***`; nunca `clave-falsa-123` |
| F-005-3 API caída | `docker compose stop tienda` y ejecutar el cierre diario | Aviso con el nodo `Pedir ventas del día` y el error de conexión |

El flujo `[TEST]` es local y no se exporta al repositorio.

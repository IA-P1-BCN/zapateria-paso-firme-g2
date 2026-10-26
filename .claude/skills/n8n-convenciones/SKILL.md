---
# SCOPE: infraestructura-agentes (NO tocar backend/frontend/workflows)
name: n8n-convenciones
description: Convenciones del equipo para construir flujos n8n (nombres de flujos y nodos, estructura con enrutador y sub-flujos, credenciales, variables, manejo de errores, nodos Code, exportación con active false). Úsala al generar, modificar o revisar el JSON de un flujo o al escribir un plan.md.
---

# Convenciones n8n

## Nombres

| Elemento | Convención | Ejemplo |
|---|---|---|
| Flujo | `[NNN] Nombre` con el nº de su spec | `[003] Abonos a distancia` |
| Sub-flujo reutilizable | `[SUB] Nombre` | `[SUB] Buscar apartado` |
| Error Workflow | `[ERR] Avisos de error` | |
| Flujo de prueba local (no se exporta) | `[TEST] …` | |
| Nodo de acción | Verbo + objeto, en español | `Pedir apartados activos`, `Enviar recibo al cliente` |
| Nodo IF / Switch | Pregunta | `¿Liquidado?`, `¿Qué evento es?` |
| Archivo | `workflows/NNN-slug.json` (3 dígitos = nº de spec) | `workflows/003-abonos-a-distancia.json` |

## Estructura

- **Un único Webhook** (`[000] Enrutador de eventos`, path `tienda`) + Switch sobre `{{ $json.body.evento }}` → Execute Workflow hacia cada flujo.
- Cada flujo de evento empieza con **Execute Workflow Trigger** y recibe `datos`.
- Lógica repetida (buscar apartado, enviar notificación) → sub-flujo `[SUB]`.
- Flujos programados: Schedule Trigger y **consultan la API** (los avisos pueden perderse).

## Llamadas a la API

- URL base `http://tienda:8000` (nunca `localhost` dentro de n8n).
- Autenticación: credencial **Header Auth** `API tienda`. Nunca la cabecera escrita a mano en el nodo.
- Errores de negocio (404/422): *Settings → On Error → Continue (using error output)* y rama que avisa a Marisa con `{{ $json.error... }}` / `detail`.
- Consultas sin `pagina` para recibir la lista entera (un item por elemento).
- Listas que pueden venir vacías: activar **Always Output Data** si el flujo debe seguir.

## Credenciales y variables

- Se crean **en la UI de n8n**. El JSON solo lleva la referencia (`credentials: {tipo: {id, name}}`); nunca valores.
- Umbrales y parámetros (importe de venta grande, hora del cierre, chat de Marisa) en **variables de n8n** (`$vars.NOMBRE`) o en un nodo Set inicial `Configuración`, nunca repartidos por los nodos. <<PENDIENTE: confirmar si la instancia permite Variables; si no, nodo Set `Configuración`>>.

## Errores

- Todo flujo exportado: `settings.errorWorkflow` apuntando a `[ERR] Avisos de error`.
- Retry On Fail (2 intentos) en nodos de envío y de IA.

## Nodos Code

- Pequeños, una responsabilidad, con un comentario arriba que diga qué hacen.
- Sin secretos, sin llamadas HTTP (para eso está HTTP Request).
- No recalculan `abonado`/`pendiente`/`estado`. Sí pueden sumar movimientos y formatear.
- Formato español: `new Intl.NumberFormat('es-ES', {style: 'currency', currency: 'EUR'}).format(x)`; fechas con `DateTime.fromISO(f).toFormat('dd/MM/yyyy')`.

## IA dentro de n8n

- Solo extrae o redacta. Salida estructurada (JSON con esquema) y validada en un Code después.
- Las cifras de cualquier mensaje las inserta el flujo, no el modelo.
- Al modelo solo el texto imprescindible (Constitución IX).

## Exportación

- `"active": false` siempre.
- Sin `pinData` con datos personales reales.
- Ver la skill `n8n-import-export`.

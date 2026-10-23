# SCOPE: infraestructura-agentes (NO tocar backend/frontend/automation)
<!-- GENERADO por scripts/sync_agents.py desde .claude/skills/tienda-api/webhook-eventos.md. No editar a mano. -->

# Eventos del webhook

Origen: `backend/controllers/apartados.py` y `backend/controllers/ventas.py` (llamadas a `n8n.avisar`). Ejemplos de `docs/guia-de-la-app.md` §6.

| Evento | Se envía en | `datos` |
|---|---|---|
| `apartado.creado` | `POST /api/apartados` | Apartado nuevo |
| `abono.registrado` | `POST /api/apartados/{id}/abonos` | Apartado actualizado `| {"importe": <abono>}` |
| `venta.registrada` | `POST /api/ventas` | Venta |
| `apartado.vencido` | `POST /api/apartados/{id}/vencer` | `{"apartado": …, "vale": …}` |

`datos.estado` es el estado **después** de la acción.

```json
{"evento": "apartado.creado", "datos": {"id": 25, "fecha": "2026-10-20", "cliente": "Carmen Ruiz", "telefono": "612 345 001", "email": "carmen@example.com", "producto": "Botín piel marrón", "talla": "38", "precio": 89.9, "fecha_limite": "2027-01-18", "estado": "activo", "abonado": 10.0, "pendiente": 79.9}}
```

```json
{"evento": "abono.registrado", "datos": {"id": 25, "fecha": "2026-10-20", "cliente": "Carmen Ruiz", "telefono": "612 345 001", "email": "carmen@example.com", "producto": "Botín piel marrón", "talla": "38", "precio": 89.9, "fecha_limite": "2027-01-18", "estado": "activo", "abonado": 30.0, "pendiente": 59.9, "importe": 20.0}}
```

```json
{"evento": "venta.registrada", "datos": {"id": 257, "fecha": "2026-10-20", "concepto": "Crema calzado", "importe": 4.5, "forma_pago": "efectivo"}}
```

```json
{"evento": "apartado.vencido", "datos": {"apartado": {"id": 16, "cliente": "Paula Ramos", "email": "paula16@example.com", "producto": "Zapatilla running azul", "precio": 64.5, "abonado": 5.0, "pendiente": 59.5, "estado": "vencido"}, "vale": {"id": 2, "codigo": "VALE-00016", "apartado_id": 16, "fecha": "2026-10-20", "importe": 5.0, "usado": 0}}}
```

Expresiones en n8n (nodo justo después del Webhook): `{{ $json.body.evento }}`, `{{ $json.body.datos.pendiente }}`, `{{ $json.body.datos.vale.codigo }}`.

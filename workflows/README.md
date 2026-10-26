# Flujos de n8n

Aquí viven los flujos exportados desde n8n, versionados en JSON. Convenciones en
[ADR-0002](../.agents/decisions/ADR-0002-convenciones-flujos.md) y en la skill `n8n-convenciones`.

## Convención de nombres

```
NNN-slug.json        →  flujo en n8n: [NNN] Nombre
```

`NNN` es el número de **3 dígitos de su spec** (`specs/features/NNN-slug/`), no el número del
[briefing](../docs/BRIEFING_zapateria.md). El número del enunciado (`FL-XX`) se apunta en la cabecera de
cada spec (`Flujo enunciado: FL-XX`) para no perder la trazabilidad.

| Archivo | Flujo en n8n | Flujo del enunciado |
| ------- | ------------ | ------------------- |
| `000-enrutador-eventos.json` | `[000] Enrutador de eventos` | — (webhook único + Switch) |
| `001-confirmacion-apartado.json` | `[001] Confirmación de apartado` | FL-01 · Confirmación de apartado |
| `002-recibo-abono.json` | `[002] Recibo de abono` | FL-02 · Recibo de abono |
| `003-abonos-a-distancia.json` | `[003] Abonos a distancia` | FL-03 · Abonos a distancia |
| `004-cierre-diario.json` | `[004] Cierre diario` | FL-05 · Cierre diario |
| `005-error-workflow.json` | `[ERR] Avisos de error` | FL-08 · Error Workflow |
| `006-venta-grande.json` | `[006] Venta grande` | FL-04 · Venta grande |
| `007-recordatorios-vencimientos.json` | `[007] Recordatorios y vencimientos` | FL-06 · Recordatorios y vencimientos |
| `008-informe-mensual.json` | `[008] Informe mensual` | FL-07 · Informe mensual |

Los números 006 en adelante siguen [`specs/backlog.md`](../specs/backlog.md) y aún no tienen spec.

## Importar un flujo en n8n

1. Arranca el entorno: `docker compose up -d` (n8n en <http://localhost:5678>).
2. En n8n: **Workflows → Import from File** y elige el JSON. También por CLI (el contenedor no monta el repo):

   ```bash
   docker compose cp workflows/003-abonos-a-distancia.json n8n:/tmp/flujo.json
   docker compose exec n8n n8n import:workflow --input=/tmp/flujo.json
   ```

3. Crea en la UI las credenciales que el flujo referencia por nombre (p. ej. **`API tienda`**, Header Auth con
   la cabecera `X-API-Key`). Los JSON nunca llevan el valor.
4. Prueba con la *Test URL* y los casos de `specs/features/NNN-*/fixtures.md`. **No** lo actives desde un agente:
   activar es decisión humana.

Más detalle en la skill `n8n-import-export`.

## Reglas antes de subir un JSON

1. **Exportar** desde n8n: *Workflow → Export → Download* (JSON de todo el flujo), con `"active": false`.
2. **Revisar credenciales**: ninguna API key, contraseña, token ni URL con clave puede ir dentro del JSON.
   Las credenciales se crean en la UI de n8n y el flujo solo las referencia por nombre.
3. **Sin datos personales**: quita nombres, correos o teléfonos reales de los nodos.
4. Comprueba en local: `python scripts/validate_workflows.py workflows`. La CI valida el JSON en cada PR.

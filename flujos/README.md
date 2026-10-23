# Flujos de n8n

Aquí viven los flujos exportados desde n8n, versionados en JSON.

## Convención de nombres

```
NN-nombre-del-flujo.json
```

Donde `NN` es el número del flujo según el
[briefing](../docs/BRIEFING_zapateria.md) (`## 🔄 Automatizaciones a construir`):

| # | Flujo |
| - | ----- |
| 1 | Confirmación al apartar |
| 2 | Recibo de cada abono |
| 3 | Abonos por Bizum/transferencia |
| 4 | Aviso de nuevo apartado |
| 5 | Cierre diario |
| 6 | Recordatorios y vencimientos |
| 7 | Informe mensual |
| 8 | Error Workflow |

Ejemplo: `01-confirmacion-apartado.json`.

## Reglas antes de subir un JSON

1. **Exportar** desde n8n: *Workflow → Export → Download* (JSON de todo el flujo).
2. **Revisar credenciales**: ninguna API key, contraseña, token ni URL con clave puede ir
   dentro del JSON. Usa variables de entorno en n8n para lo sensible.
3. **Sin datos personales**: quita nombres, correos o teléfonos reales de los nodos.
4. La CI de GitHub valida que el JSON sea correcto en cada PR.

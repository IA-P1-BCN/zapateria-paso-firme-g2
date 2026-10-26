# SCOPE: infraestructura-agentes (NO tocar backend/frontend/workflows)

# Backlog · HU del enunciado → features

Fuente: `docs/BRIEFING_zapateria.md` (sección «Historias de usuario» y «Automatizaciones a construir»).
Responsables: `<<PENDIENTE: asignar en el Kanban>>`.

| Feature | HU | Flujo del enunciado | Nivel | Estado |
|---|---|---|---|---|
| `000-enrutador-eventos` | (requisito esencial: webhook único + Switch) | — | 🟢 Esencial | Borrador |
| `001-confirmacion-apartado` | HU-01 | FL-01 · Confirmación de apartado | 🟢 Esencial | Borrador |
| `002-recibo-abono` | HU-02 | FL-02 · Recibo de abono | 🟢 Esencial | Borrador |
| `003-abonos-a-distancia` | HU-03 | FL-03 · Abonos a distancia | 🟢 Esencial | Borrador |
| `004-cierre-diario` | HU-04 | FL-05 · Cierre diario | 🟢 Esencial | Borrador |
| `005-error-workflow` | HU-05 | FL-08 · Error Workflow | 🟢 Esencial | Borrador |
| `006-venta-grande` | HU-09 | FL-04 · Venta grande | 🟡 Medio | Sin spec |
| `007-recordatorios-vencimientos` | HU-06, HU-07 | FL-06 · Recordatorios y vencimientos | 🟡 Medio | Sin spec |
| `008-informe-mensual` | HU-08 | FL-07 · Informe mensual | 🟡 Medio | Sin spec |
| `009-migracion-excel` | HU-10 | Migración | 🟡 Medio | Sin spec |
| `010-sub-buscar-apartado` | (sub-workflow reutilizable) | — | 🟡 Medio | Sin spec |
| `011-sub-enviar-notificacion` | (sub-workflow reutilizable) | — | 🟡 Medio | Sin spec |
| `012-asistente-telegram-cliente` | HU-11 | Asistente IA | 🟠 Avanzado | Sin spec |
| `013-asistente-telegram-marisa` | HU-12 | Asistente IA | 🟠 Avanzado | Sin spec |
| `014-entrada-automatica` | HU-13 | Apartados desde casa / datáfono | 🟠 Avanzado | Sin spec |
| `015-datos-personales` | HU-14 | Transversal | 🟠 Avanzado | Sin spec |
| `016-panel-marisa` | HU-15 | Panel | 🔴 Experto | Sin spec |
| `017-funcionar-siempre` | HU-16 | Despliegue, backups, CI | 🔴 Experto | Sin spec |

## Bloqueos conocidos (necesitan decisión humana)

| Tema | Afecta a | Por qué |
|---|---|---|
| La app no tiene forma de pago `transferencia` | 003 | `FORMAS_PAGO = efectivo, tarjeta, bizum` en `backend/config.py` |
| La app envía el webhook sin cabecera de autenticación | 000, 015 | `backend/services/n8n.py` solo manda `Content-Type`; proteger el webhook (HU-14) exigiría tocar el backend |
| No hay endpoint para marcar un vale como usado | 007 | La tabla `vales` tiene `usado`, pero no hay ruta |
| No hay registro de consentimiento ni de recordatorios enviados | 007, 015 | La app no los guarda; hay que guardarlos en n8n / Google Sheets |

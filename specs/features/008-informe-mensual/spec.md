# SCOPE: infraestructura-agentes (NO tocar backend/frontend/workflows)

# 008 · Informe mensual — Spec

- **Estado:** Aprobada
- **HU:** HU-08 · Informe mensual (flujo 7)
- **Flujo enunciado:** FL-07 · Informe mensual
- **Nivel:** 🟡 Medio
- **Redacta:** <<PENDIENTE>> · **Aprueba:** <<PENDIENTE: otra persona del equipo>>
- **Fecha:** 2026-10-29

## 1. Objetivo

El día 1 de cada mes a las 08:00 (zona `Europe/Madrid`) enviar a Marisa un informe del mes anterior con la recaudación (ventas directas y abonos por separado), el total pendiente de cobro y el número de apartados nuevos, liquidados y vencidos, para que sepa cómo va el negocio sin hacer cuentas.

## 2. Historia de usuario

> Como **Marisa**, quiero un informe a principios de mes con lo recaudado y lo que me deben, para saber cómo va el negocio sin hacer cuentas.

## 3. Disparador

| Tipo | Detalle |
|---|---|
| Schedule Trigger | Día 1 de cada mes a las `08:00`, zona `Europe/Madrid` (`ZONA_HORARIA`). El informe debe llegar antes de las 10:00 (OE-06, KPI-06) |

## 4. Entradas

| Campo | Origen | Obligatorio | Notas |
|---|---|---|---|
| Ventas del mes anterior | `GET /api/ventas?desde=YYYY-MM-DD&hasta=YYYY-MM-DD` | Sí | `importe`, `forma_pago`, `fecha`, `concepto`. Sin `pagina` para recibir todas |
| Abonos del mes anterior | `GET /api/abonos?desde=YYYY-MM-DD&hasta=YYYY-MM-DD` | Sí | `importe`, `forma_pago`, `fecha`, `apartado_id`. Ambas fechas incluidas |
| Apartados activos | `GET /api/apartados?estado=activo` (sin `pagina`) | Sí | Se suma `pendiente` de cada item para el total pendiente de cobro |
| Apartados (sin filtro) | `GET /api/apartados` (sin `pagina`) | Sí | Se filtra por `fecha` dentro del mes anterior para contar apartados nuevos |
| Vales | `GET /api/vales` (sin filtro) | Sí | Se filtra por `fecha` dentro del mes anterior para contar vencidos |
| Detalle de apartado liquidado | `GET /api/apartados/{id}` | Sí | Solo para apartados con `estado = liquidado`; se usan sus `abonos[]` para aproximar la fecha de liquidación (último abono) |
| Mes anterior | Calculado por n8n a partir de la fecha de ejecución y `ZONA_HORARIA` | Sí | Rango `desde` = primer día del mes anterior; `hasta` = último día del mes anterior, formato `AAAA-MM-DD` |

No depende de los avisos del webhook: consulta la API (Constitución X / RNF-10).

## 5. Salidas

| Salida | Destinatario | Canal | Contenido |
|---|---|---|---|
| Informe mensual | Marisa (`MARISA_EMAIL`) | Gmail (`PF · Gmail`) | Tabla HTML con: recaudación (ventas directas, abonos, total), total pendiente de cobro, conteos de apartados nuevos, liquidados y vencidos del mes |
| Informe de mes sin datos | Marisa (`MARISA_EMAIL`) | Gmail | Mismas secciones con ceros y una nota de que no hubo movimientos |

No se guarda histórico en Google Sheets ni en ningún otro almacén (fuera de alcance).

## 6. Reglas de negocio aplicables

- Métrica «Recaudación mensual» (`ontology.md` §7): ventas directas + abonos del mes, por separado.
- Total pendiente de cobro (`ontology.md` §7): suma de `pendiente` de los apartados `activo`.
- Los importes de la app (`abonado`, `pendiente`, `estado`, `fecha_limite`, importe del vale) se usan tal cual (Constitución I). n8n solo suma movimientos y redondea **solo los totales** a 2 decimales; **no se redondean los sumandos** (ADR-0002, D6; RNF-14).
- Un apartado con el plazo pasado sigue `activo` hasta que se venza (R-10); el informe de vencidos se basa en los vales generados (`fecha` del vale), no en `fecha_limite`.
- `liquidado` lo pone la app sola cuando `pendiente` llega a 0 (R-09). No existe fecha de liquidación en la app (dependencia §5.3 del PRD); se aproxima por el último abono.
- Formas de pago válidas: `efectivo`, `tarjeta`, `bizum` (R-08). Este informe no desglosa por forma de pago (fuera de alcance).
- No se recalculan `abonado`/`pendiente`/`estado` de ningún apartado.

## 7. Casos de error y bordes

| Caso | Comportamiento esperado |
|---|---|
| Mes sin datos | Enviar el informe con ceros en todas las secciones y una nota («Sin movimientos en el mes»). No fallar |
| Lista vacía de la API (0 ventas, 0 abonos, 0 activos, 0 vales) | Activar «Always Output Data» en los nodos HTTP Request para que el flujo continúe y no se detenga por 0 items |
| API no responde / timeout | Retry On Fail (2 intentos) en los nodos HTTP Request y Error Workflow `[ERR] Avisos de error` (`005`) si persiste |
| Error 401 (clave) | Error de configuración; aviso inmediato por el Error Workflow, sin reintentar en bucle |
| Error 404 (recurso inexistente) | Aviso a Marisa con `detail`; continuar con el resto del informe si es posible |
| Error 422 (regla de negocio) | En las consultas de listas, propagar al Error Workflow; en el nodo de detalle (N+1) tratar con `On Error → Continue (using error output)` y avisar a Marisa con `detail` |
| Reejecución el mismo día | No hay idempotencia estricta: se envía otro email. No se guarda histórico, por lo que no se duplican filas |
| Apartado liquidado sin abonos o con detalle inaccesible | Se contabiliza como liquidado del mes solo si su último abono cae en el mes; si `GET /api/apartados/{id}` falla (404/422), se avisa a Marisa con el motivo y se continúa con el resto; el conteo de liquidados puede quedar incompleto (aproximación documentada) |
| Apartado con fecha `fecha` fuera del mes pero abono en el mes | Los «nuevos» se cuentan por `fecha` del apartado, no por abonos |
| Vales con `fecha` en el mes | Se cuentan como vencidos del mes; un vale por apartado (como mucho uno) |
| Redondeo | Solo los totales (recaudación de ventas, recaudación de abonos, recaudación total, pendiente total) se redondean a 2 decimales; los sumandos individuales no |
| Zona horaria | El cálculo del mes anterior y de «hoy» se hace en `Europe/Madrid` (`ZONA_HORARIA`), no en UTC |
| Error de Gmail al enviar | Reintento con espera; si persiste, Error Workflow |

## 8. Criterios de aceptación

- [ ] CA-1 (RF-37) El día 1, antes de las 10:00, llega un informe con la recaudación del mes anterior separada en ventas directas y abonos.
- [ ] CA-2 (RF-38) El informe incluye el total pendiente de cobro de los apartados activos.
- [ ] CA-3 (RF-39) El informe incluye el número de apartados nuevos, liquidados y vencidos del mes anterior.
- [ ] CA-4 (RF-40) Los importes del informe coinciden con las consultas a la API (ventas, abonos y pendiente).
- [ ] CA-5 (RF-41) Un mes sin datos genera un informe con ceros y una nota, sin fallar.

## 9. Datos personales

- Las consultas a la API devuelven `ApartadoOut`/`AbonoOut`/`VentaOut`/`ValeOut`, que pueden incluir `cliente`, `telefono` y `email` en los apartados, pero el flujo **solo agrega conteos e importes**; no incluye datos de clientes en el correo ni los envía a ningún modelo externo (no se usa IA en este flujo).
- El correo se envía únicamente a Marisa (`MARISA_EMAIL`). No se envía a clientes ni a terceros.
- Cumple RGPD: mensajes transaccionales internos; sin datos personales de clientes en la salida.

## 10. Fuera de alcance

- Generación de PDF (solo tabla HTML en el correo).
- Histórico en Google Sheets u otro almacén (no se guarda; el informe solo se envía por correo).
- Desglose de la recaudación por forma de pago (efectivo/tarjeta/bizum).
- Fecha exacta de liquidación (la app no la guarda); se aproxima por el último abono.
- Idempotencia estricta en la reejecución (se envía otro email).
- Cambios en la app (Constitución VII).

## 11. Preguntas abiertas

- <<PENDIENTE: confirmar si el desglose por forma de pago debe añadirse al informe (afecta al alcance futuro)>>
- <<PENDIENTE: confirmar que la aproximación de liquidados por último abono es aceptable para Marisa; si no, proponer añadir fecha de liquidación a la app>>
- <<PENDIENTE: confirmar el formato de la tabla HTML (columnas, orden, estilo) con Marisa>>
- <<PENDIENTE: confirmar si se quiere una copia del informe en Google Sheets para histórico>>
- <<PENDIENTE: confirmar el valor/nombre de la variable `MARISA_EMAIL` y que la instancia permite Variables de n8n; si no, usar nodo Set `Configuración`>>
- (Resuelto) Credenciales con los nombres usados en el proyecto: `API tienda` (Header Auth) y `Gmail tienda` (Gmail OAuth2).

## 12. Credenciales y variables

| Nombre en n8n | Tipo | Para qué |
|---|---|---|
| `API tienda` (Header Auth, `X-API-Key`) | Credencial | Autenticación en todos los HTTP Request a `http://tienda:8000` |
| `Gmail tienda` (OAuth2) | Credencial | Envío del correo a Marisa |
| `MARISA_EMAIL` | Variable n8n | Destinatario del informe |
| `ZONA_HORARIA` | Variable n8n | `Europe/Madrid` (cálculo del mes anterior y de la hora de disparo) |

Sin Google Sheets: este flujo no usa credencial de Sheets.

## 13. Errores y observabilidad

- Todo flujo exportado lleva `settings.errorWorkflow` apuntando a `[ERR] Avisos de error`.
- Retry On Fail (2 intentos) en los nodos HTTP Request y en el nodo de envío de Gmail.
- `On Error → Continue (using error output)` en los HTTP Request para tratar 4xx sin romper el flujo.
- El Error Workflow avisa a Marisa con flujo, nodo, mensaje de error y enlace a la ejecución, sin secretos.

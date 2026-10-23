# SCOPE: infraestructura-agentes (NO tocar backend/frontend/automation)

# {{ID}} · {{TITULO}} — Spec

- **Estado:** Borrador
- **HU:** {{HU}}
- **Nivel:** <<PENDIENTE: Esencial | Medio | Avanzado | Experto>>
- **Redacta:** <<PENDIENTE>> · **Aprueba:** <<PENDIENTE: otra persona del equipo>>
- **Fecha:** {{FECHA}}

## 1. Objetivo

Una o dos frases: qué problema de Marisa, la dependienta o el cliente resuelve.

## 2. Historia de usuario

> Como **…**, quiero **…**, para **…**.

## 3. Disparador

| Tipo | Detalle |
|---|---|
| Evento de la app / Schedule / Correo / Formulario / Error | Evento exacto, cron, buzón… |

## 4. Entradas

Campos que usa el flujo, con su origen (evento, API, correo). Solo campos que existan en `backend/schemas/` o en `docs/guia-de-la-app.md`.

| Campo | Origen | Obligatorio | Notas |
|---|---|---|---|

## 5. Salidas

| Salida | Destinatario | Canal | Contenido |
|---|---|---|---|

## 6. Reglas de negocio aplicables

Referencias a `ontology.md` §6 (R-01…R-13) y a la constitución.

## 7. Casos de error y bordes

| Caso | Comportamiento esperado |
|---|---|

## 8. Criterios de aceptación

Copiados del enunciado (se pueden ampliar, nunca recortar). Cada uno debe poder comprobarse con un caso de `fixtures.md`.

- [ ] CA-1 …

## 9. Datos personales

Qué datos personales toca el flujo y cuáles salen a terceros (modelo de IA, correo, Telegram).

## 10. Fuera de alcance

## 11. Preguntas abiertas

- <<PENDIENTE: …>>

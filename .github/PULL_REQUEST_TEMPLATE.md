## 📋 Descripción

<!-- ¿Qué hace este PR? ¿Qué flujo o parte de la app toca? -->

**Flujo / tarea (issue):** Closes #
**Feature:** `NNN-slug` · HU-XX · Flujo enunciado FL-XX · flujo en n8n `[NNN] Nombre`

## 🔄 Tipo de cambio

- [ ] Nuevo flujo n8n
- [ ] Mejora de un flujo existente
- [ ] Arreglo de un bug
- [ ] Cambio en la app (backend/frontend)
- [ ] Documentación / specs / capa de agentes
- [ ] Configuración / CI / repo

## 🧪 Cómo probarlo

<!-- Para flujos: importar `workflows/NNN-slug.json` (ver workflows/README.md), asignar las credenciales
     por nombre (p. ej. `API tienda`) y ejecutar los casos de `specs/features/NNN-slug/fixtures.md`. -->

1.
2.

## ✅ Definition of Done

- [ ] Spec `Aprobada`; `plan.md` y `tasks.md` al día (`specs/features/NNN-slug/`)
- [ ] JSON exportado en `workflows/NNN-slug.json` con `"active": false`, **sin credenciales ni datos personales** (tampoco en `pinData`)
- [ ] `python scripts/validate_workflows.py workflows --estricto` sin errores
- [ ] Error Workflow asignado (`[ERR] Avisos de error`)
- [ ] Probado con los datos de ejemplo (casos de `fixtures.md` en Evidencias)
- [ ] Los importes vienen de la app (sin recalcular en n8n ni plantillas)
- [ ] `/revisar-flujo` → APROBADO (pega el veredicto en Notas)
- [ ] Tests pasando en local: `cd backend && python -m pytest`
- [ ] Entrada en la bitácora de IA `docs/ai-log.md` si se usó IA (`/bitacora`)
- [ ] Título del PR en formato Conventional Commits (`feat(f03): …`)

## 📸 Evidencias

<!-- Capturas del flujo funcionando, respuesta del webhook, logs, etc. -->

| Caso | Resultado | Captura / ejecución |
|---|---|---|
| F-NNN-1 | | |

## ❓ Notas para el reviewer

<!-- Dónde mirar, dudas abiertas, qué probar en local, veredicto de /revisar-flujo -->

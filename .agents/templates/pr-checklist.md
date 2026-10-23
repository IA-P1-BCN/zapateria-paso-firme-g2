# SCOPE: infraestructura-agentes (NO tocar backend/frontend/automation)

<!-- Plantilla de descripción de PR para un flujo n8n. -->

## Qué hace

Feature `NNN-slug` · HU-XX · flujo `[NNN] Nombre`.

## Archivos

- `automation/NNN-slug.json`
- `specs/features/NNN-slug/{spec,plan,tasks,fixtures}.md`

## Cómo probarlo

1. Importar el JSON (skill `n8n-import-export`) y asignar credenciales: <lista de nombres>.
2. Ejecutar los casos de `fixtures.md`.

## Evidencias

| Caso | Resultado | Captura / ejecución |
|---|---|---|

## Checklist

- [ ] Spec `Aprobada`; plan y tareas al día.
- [ ] `"active": false`, sin secretos, sin datos personales reales en `pinData`.
- [ ] Error Workflow asignado.
- [ ] `/revisar-flujo` → APROBADO (pegar el veredicto).
- [ ] No se ha tocado `backend/` ni `frontend/`.
- [ ] Entrada en `docs/ai-log.md`.

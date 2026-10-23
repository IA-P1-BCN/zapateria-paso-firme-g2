# SCOPE: infraestructura-agentes (NO tocar backend/frontend/automation)

# specs/ · Spec-Driven Development

Cada automatización se define aquí **antes** de pedirle nada a un agente.

```
specs/
├── constitution.md          principios no negociables
├── backlog.md               HU del enunciado → feature, nivel y estado
├── _templates/              plantillas de spec, plan y tareas
└── features/
    └── NNN-slug/
        ├── spec.md          QUÉ: disparador, entradas, salidas, errores, criterios de aceptación
        ├── plan.md          CÓMO: nodos de n8n, endpoints, credenciales, manejo de errores
        ├── tasks.md         EJECUCIÓN: tareas atómicas asignables a agente o persona
        └── fixtures.md      DATOS DE PRUEBA: payloads y resultado esperado (opcional hasta el plan)
```

## Estados de una feature (campo `Estado:` de `spec.md`)

| Estado | Quién lo pone | Qué permite |
|---|---|---|
| `Borrador` | `spec-writer` o persona | Discutir, preguntar, corregir |
| `Aprobada` | **Solo una persona** del equipo, distinta de quien la redactó | Escribir plan y tareas, construir |
| `En construcción` | Quien construye | `flow-builder` trabaja sobre `tasks.md` |
| `En revisión` | Quien abre la PR | `flow-reviewer` + revisión humana |
| `Hecha` | Quien mergea | Flujo en `develop`, evidencias en la PR |

## Ciclo

1. `python scripts/new_feature.py 006 venta-grande --hu HU-09` (o `/sdd-spec HU-09`).
2. `/sdd-spec` → `spec.md` en `Borrador`. Revisarla en equipo y pasarla a `Aprobada`.
3. `/sdd-plan NNN` → `plan.md`. El agente pasa `api-contract-checker` sobre el plan.
4. `/sdd-tasks NNN` → `tasks.md`. Asignar responsable a cada tarea.
5. `/construir-flujo NNN` → JSON del flujo. Importar en n8n y probar con `fixtures.md`.
6. `/revisar-flujo NNN` → informe de revisión. Abrir PR (persona).
7. `/bitacora` → entrada en `docs/ai-log.md`.

## Reglas

- Numeración de 3 dígitos, sin reutilizar números. El JSON del flujo lleva el mismo número.
- Lo desconocido se marca `<<PENDIENTE: ...>>`; nunca se inventa.
- Los criterios de aceptación copian los del enunciado (HU) y se pueden ampliar, nunca recortar.
- Ver `specs/constitution.md` y la skill `sdd-workflow`.

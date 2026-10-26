---
# SCOPE: infraestructura-agentes (NO tocar backend/frontend/workflows)
# GENERADO por scripts/sync_agents.py desde .claude/skills/paso-firme-verify/SKILL.md. No editar a mano.
name: paso-firme-verify
description: Verifica una entrega de Paso Firme contra su issue, el validador de flujos y los tests del backend, e informa la evidencia real antes de preparar una PR. Úsala para comprobar cambios, diagnosticar verificaciones fallidas o preparar el checklist de la PR.
---

# Verificar una entrega de Paso Firme

Trabajar desde la raíz del repositorio. Leer `docs/BRIEFING_zapateria.md` y,
si existe, `AGENTS.md`; identificar la issue y el alcance del cambio.
Identificar rama, diff y archivos nuevos con `git status --short --branch`,
`git diff` y `git diff --cached`. Si el trabajo está commiteado, comparar
contra la base de la PR (`git diff develop...HEAD`); no confundir un árbol
limpio con la ausencia de cambios.

## Comprobaciones

Ejecutar en este orden y reportar el resultado real de cada una:

1. **Flujos n8n**: `python scripts/validate_workflows.py`
   (estructura y ausencia de credenciales). Un flujo sin exportar a
   `workflows/` se señala como pendiente, no como aprobado.
2. **Tests del backend**: `cd backend && python -m pytest -v`. Informar
   nº de aprobados, fallidos y saltados. Un test saltado no equivale a
   aprobado; no afirmar cobertura si no se midió.
3. **Formato**: `git diff --check` para detectar problemas de whitespace.
4. **Credenciales y datos**: revisar el diff en busca de claves, tokens o
   datos personales; nunca leer ni mostrar `.env`.

No añadir tests que solo reproduzcan la implementación, no eliminar tests
que fallen y no cambiar el resultado esperado para que pase la suite.

## Reglas de evidencia

- Reutilizar evidencia de una ejecución previa solo si no hubo cambios de
  código posteriores, indicando su procedencia; nunca fingir una ejecución
  nueva.
- Entregar comandos ejecutados, resultado y qué criterio sigue sin
  verificar. Si algo no se pudo ejecutar (entorno, dependencias), decirlo
  explícitamente.
- Preparar el resumen de la PR (qué cambia, cómo se probó) con la evidencia
  real; la skill no publica ni aprueba PRs por sí sola.

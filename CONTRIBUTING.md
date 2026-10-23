# Contribuir en Zapatería Paso Firme

Guía rápida para trabajar en equipo en este repo. El enunciado completo está en
[`docs/BRIEFING_zapateria.md`](docs/BRIEFING_zapateria.md) y la app en
[`docs/guia-de-la-app.md`](docs/guia-de-la-app.md).

## 🌳 Ramas

La rama por defecto (producción del equipo) es **`develop`**. `main` queda como copia estable.

Nunca se trabaja directamente sobre `develop`. Cada cambio vive en su rama:

| Tipo | Prefijo | Ejemplo |
| --- | --- | --- |
| Flujo nuevo o cambio en un flujo | `flujo/` | `flujo/confirmacion-apartado` |
| Arreglo de un bug | `fix/` | `fix/webhook-bizum-formato-importe` |
| Documentación | `docs/` | `docs/setup-colaboracion` |
| Cambio en backend/frontend | `feat/` | `feat/nuevo-endpoint-abonos` |
| Configuración del repo/CI | `docs/` o `ci/` | `ci/validar-json-flujos` |

```bash
git switch develop
git pull
git switch -c flujo/confirmacion-apartado
# ... trabajar y commitear ...
git push -u origin flujo/confirmacion-apartado
```

## 🔀 Flujo de Pull Request

1. Abre una **issue** antes de empezar (usa las plantillas: "👟 Flujo n8n" o "🐛 Bug").
2. Crea la rama desde `develop`.
3. Haz el cambio con commits claros.
4. Abre el PR hacia `develop` — la plantilla te guía. Escribe `Closes #N` para cerrar la issue al mergear.
5. Pide review al equipo (mínimo 1 aprobación) y espera a que la **CI pase** (tests + validación de JSON).
6. Al mergear, borra la rama.

## ✍️ Commits

Convención estándar, en **español** y en imperativo:

```
feat: añade flujo de confirmación de apartado
fix: corrige importe del Bizum con símbolo €
docs: actualiza la guía de endpoints
test: cubre el webhook de abonos
```

Tipos: `feat`, `fix`, `docs`, `test`, `refactor`, `ci`, `chore`.

## 🤖 Flujos de n8n

- Cada flujo se exporta desde n8n (**Workflow → Export** en formato JSON) y se guarda en
  [`flujos/`](flujos/) con el número y nombre del flujo, p. ej. `01-confirmacion-apartado.json`.
- **Antes de subir, revisa el JSON**: no puede contener credenciales, API keys, correos reales
  ni IDs personales de n8n. La CI valida que el JSON sea correcto, pero el contenido lo revisáis vosotros.
- El PR debe decir en qué flujo del briefing está basado y qué HU cierra.

## 🧪 Tests y app local

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m pytest          # los mismos tests que corren en la CI
uvicorn main:app --reload # levantar la API en local
```

La CI se ejecuta en cada PR contra `develop` y debe estar en verde antes del merge.

## 🧠 Trabajo con agentes de IA

Usad agentes de IA para diseñar y depolar flujos, pero recordad (del briefing): *el agente
propone, la responsabilidad de los flujos es vuestra*. Todo lo que genere un agente pasa por
review humana igual que cualquier PR — y el review automático de IA en el PR es una ayuda extra,
no un sello de calidad.

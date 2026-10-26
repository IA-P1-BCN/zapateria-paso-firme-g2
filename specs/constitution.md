# SCOPE: infraestructura-agentes (NO tocar backend/frontend/workflows)

# Constitución del proyecto

Principios **no negociables**. Toda spec, plan, tarea, flujo y PR debe cumplirlos. Un agente que detecte que una petición los viola se detiene y lo dice.

| Versión | Fecha | Cambio |
|---|---|---|
| 1.0 | 2026-10-23 | Versión inicial |

---

## I. La app es la fuente de verdad

Los importes y estados que calcula la app (`abonado`, `pendiente`, `estado`, `fecha_limite`, importe y código del vale) **se usan tal cual llegan**. n8n puede formatearlos (`79,90 €`, `18/01/2027`) y sumar movimientos para los cierres, pero nunca recalcular lo que ya da la app.

## II. La IA extrae, el flujo decide

Los modelos de lenguaje solo transforman texto en datos estructurados (o redactan el tono de un mensaje). Las decisiones (qué apartado es, si se registra, si se pregunta a Marisa) las toman nodos deterministas (IF, Switch, Code) apoyados en la API. Las cifras de un mensaje redactado por IA las inserta el flujo, no el modelo.

## III. Cero secretos en el repositorio

Ninguna clave, token, contraseña ni URL con credenciales en JSON, specs, fixtures ni logs. Las credenciales viven en n8n (UI) y en `.env` (que no se sube). Los flujos las referencian por nombre.

## IV. Spec antes que flujo

No se construye ni se modifica un flujo sin `spec.md` con `Estado: Aprobada` por un humano. El plan y las tareas derivan de la spec; si la realidad obliga a cambiarlos, se actualiza primero la spec.

## V. Las pruebas son el contrato

Cada flujo tiene datos de prueba (`fixtures.md`, pinned data) y un resultado esperado por caso. Si una prueba falla, se arregla el flujo, **no la prueba**. Los datos de prueba no contienen datos personales reales (correos `@example.com`).

## VI. Revisión humana obligatoria

Ningún agente activa o publica flujos, hace commit, push, merge ni abre PRs. Todo flujo generado se importa, se ejecuta con datos de ejemplo y se revisa en una PR con al menos **una aprobación de otra persona del equipo**.

## VII. El código de la app no se toca

`backend/` y `frontend/` son de solo lectura. Si un flujo necesita algo que la app no ofrece, se documenta como `<<PENDIENTE>>` y lo decide un humano (y, si hace falta, la profesora).

## VIII. Los fallos se ven

Todo flujo tiene asignado el Error Workflow `[ERR] Avisos de error`. Los `4xx` de la API que forman parte del negocio (422 por pagar de más, plazo vencido…) se tratan con rama de error y aviso a Marisa, no rompiendo el flujo. Ningún aviso de error incluye secretos.

## IX. Mínimos datos personales (RGPD)

A un modelo externo solo se le envía el texto imprescindible para la tarea. Se documenta qué datos salen en cada flujo (sección «Datos personales» de la spec). Solo se escribe a clientes con un medio de contacto informado y `<<PENDIENTE: consentimiento, HU-14>>`.

## X. Trazabilidad

Los prompts relevantes, las alucinaciones detectadas y las decisiones (aceptado / rechazado y por qué) se registran en `docs/ai-log.md`.

---

## Gobierno

- Cambiar esta constitución requiere una PR propia con la aprobación de **las 3 personas del equipo**.
- En caso de conflicto: constitución > spec aprobada > plan > tareas > instrucciones puntuales a un agente.

# SCOPE: infraestructura-agentes (NO tocar backend/frontend/workflows)

# 002 · Recibo de abono — Fixtures

Entrada = `datos` del evento `abono.registrado` (forma real: `ApartadoOut` + `importe`, `backend/controllers/apartados.py:40`).
El sub-flujo lo recibe **en la raíz** (Execute Workflow Trigger desde `[000]`), no dentro de `body`.
`id` es el id del **apartado**. El evento no trae `forma_pago` ni id del abono.
Datos ficticios: nombres inventados, emails `@example.com`, teléfonos `6xx 000 xxx`.
`tienda_email` = `tienda@pasofirme.example` (nodo Set `Configuración`).

Los importes esperados son los del payload **formateados** (`20,00 €`); nunca se recalculan.
Los saltos de línea de los cuerpos siguen los textos de la spec §5.

## Base

```json
{"id": 25, "fecha": "2026-10-20", "cliente": "Carmen Ruiz", "telefono": "612 000 001", "email": "carmen@example.com", "producto": "Botín piel marrón", "talla": "38", "precio": 89.9, "fecha_limite": "2027-01-18", "estado": "activo", "abonado": 30.0, "pendiente": 59.9, "importe": 20.0}
```

## Casos

| Caso | Entrada (cambios sobre la base) | Resultado esperado |
|---|---|---|
| F-002-1 Recibo con `activo` (CA-1) | Base | Se ejecuta **`Enviar recibo al cliente`** (no los otros dos). Para: `carmen@example.com`. Asunto: `Recibo de tu abono · Apartado nº 25`. Cuerpo: [R-1](#r-1) |
| F-002-2 Liquida (CA-2, §7 «pendiente = 0 y liquidado») | `"importe": 59.9, "abonado": 89.9, "pendiente": 0.0, "estado": "liquidado"` | Se ejecuta **`Enviar aviso de recogida`** (no `Enviar recibo al cliente`). Para: `carmen@example.com`. Asunto: `¡Ya puedes recoger tus zapatos! · Apartado nº 25`. Cuerpo: [R-2](#r-2) |
| F-002-3 Trampa A: `pendiente` 0 con `activo` (CA-3) · **sintético: no lo produce la app; prueba la regla** | `"importe": 59.9, "abonado": 89.9, "pendiente": 0.0, "estado": "activo"` | Se ejecuta **`Enviar recibo al cliente`** (decide `estado`, no `pendiente`). Para: `carmen@example.com`. Asunto: `Recibo de tu abono · Apartado nº 25`. Cuerpo: [R-3](#r-3) |
| F-002-4 Trampa B: `pendiente` > 0 con `liquidado` (CA-3) · **sintético: no lo produce la app; prueba la regla** | `"estado": "liquidado"` (resto como base: `pendiente: 59.9`) | Se ejecuta **`Enviar aviso de recogida`**. Para: `carmen@example.com`. Asunto: `¡Ya puedes recoger tus zapatos! · Apartado nº 25`. Cuerpo: [R-4](#r-4) |
| F-002-5 Sin email `null` (CA-4, §7) | `"email": null` | Ejecución **sin error**. Se ejecuta **`Avisar a la tienda: sin correo`**; no se ejecuta ningún envío al cliente. Para: `tienda@pasofirme.example`. Asunto: `Recibo no enviado · Apartado nº 25`. Cuerpo: [R-5](#r-5) (sin línea de liquidado) |
| F-002-6 Email vacío (§7) | `"email": ""` | Igual que F-002-5: `Avisar a la tienda: sin correo`, mismo asunto y cuerpo [R-5](#r-5) |
| F-002-7 Email solo espacios (§7) | `"email": "   "` | Igual que F-002-5: `Avisar a la tienda: sin correo`, mismo asunto y cuerpo [R-5](#r-5). No se intenta enviar a `"   "` |
| F-002-8 Sin email y liquidado (CA-4, §7) | `"email": null, "importe": 59.9, "abonado": 89.9, "pendiente": 0.0, "estado": "liquidado"` | Ejecución sin error. Se ejecuta **`Avisar a la tienda: sin correo`** (no `Enviar aviso de recogida`). Para: `tienda@pasofirme.example`. Asunto: `Recibo no enviado · Apartado nº 25`. Cuerpo: [R-8](#r-8) (con la línea de liquidado) |
| F-002-9 Talla nula (§7) | `"talla": null` | `Enviar recibo al cliente` a `carmen@example.com`, asunto `Recibo de tu abono · Apartado nº 25`. Cuerpo: [R-9](#r-9): «(Botín piel marrón)» sin «, talla», y en ningún sitio aparece `null`, `undefined` ni `, talla )` |
| F-002-10 Decimales (§7) | `"importe": 0.1, "abonado": 30.0, "pendiente": 59.9` (abono previo 29.9; coherente con la app) | `Enviar recibo al cliente` a `carmen@example.com`, asunto `Recibo de tu abono · Apartado nº 25`. Cuerpo: [R-10](#r-10): `0,10 €`, `30,00 €`, `59,90 €` (nunca `0.1`, `0,1 €` ni `59,9 €`). Los valores numéricos de los datos no cambian |
| F-002-11 Fecha límite sin desfase (§7) | Base (`"fecha_limite": "2027-01-18"`). Ejecutar también con la zona horaria de la instancia en `America/New_York` (o cualquier UTC−) | En el cuerpo aparece `Fecha límite para completar el pago: 18/01/2027.` en ambas ejecuciones (nunca `17/01/2027` ni `2027-01-18`). Cuerpo completo: [R-1](#r-1) |
| F-002-12 Fallo del envío (§7) | `"email": "no-es-un-correo"` (pasa `¿Tiene correo?` pero Gmail lo rechaza con error de cabecera `To`). Ver «Cómo probar» | `Enviar recibo al cliente` falla; el nodo muestra **2 intentos** (Retry On Fail, *Max Tries* = 2) y la ejecución termina en error. Se ejecuta el Error Workflow **`[ERR] Avisos de error`** con el nombre del flujo `[002] Recibo de abono` y el nodo `Enviar recibo al cliente`. No se envía ningún otro correo (ni a la tienda) |

## Cuerpos esperados

Remitente en todos: «Zapatería Paso Firme».

### R-1
(F-002-1, F-002-11)
```text
Hola Carmen Ruiz: hemos recibido tu abono de 20,00 € para el apartado nº 25 (Botín piel marrón, talla 38).
Total abonado: 30,00 €. Pendiente: 59,90 €. Fecha límite para completar el pago: 18/01/2027.
Gracias por tu confianza. Zapatería Paso Firme
```

### R-2
(F-002-2)
```text
Hola Carmen Ruiz: hemos recibido tu abono de 59,90 € y tu apartado nº 25 (Botín piel marrón, talla 38)
está pagado por completo (89,90 €). Ya puedes pasar por la tienda a recogerlos. Zapatería Paso Firme
```

### R-3
(F-002-3, sintético)
```text
Hola Carmen Ruiz: hemos recibido tu abono de 59,90 € para el apartado nº 25 (Botín piel marrón, talla 38).
Total abonado: 89,90 €. Pendiente: 0,00 €. Fecha límite para completar el pago: 18/01/2027.
Gracias por tu confianza. Zapatería Paso Firme
```

### R-4
(F-002-4, sintético; el aviso de recogida no muestra `pendiente`)
```text
Hola Carmen Ruiz: hemos recibido tu abono de 20,00 € y tu apartado nº 25 (Botín piel marrón, talla 38)
está pagado por completo (30,00 €). Ya puedes pasar por la tienda a recogerlos. Zapatería Paso Firme
```

### R-5
(F-002-5, F-002-6, F-002-7)
```text
No se pudo enviar el recibo del abono de 20,00 € del apartado nº 25 (Carmen Ruiz): el cliente no tiene correo.
```

### R-8
(F-002-8)
```text
No se pudo enviar el recibo del abono de 59,90 € del apartado nº 25 (Carmen Ruiz): el cliente no tiene correo.
El apartado ha quedado liquidado: avisadle para que recoja los zapatos.
```

### R-9
(F-002-9)
```text
Hola Carmen Ruiz: hemos recibido tu abono de 20,00 € para el apartado nº 25 (Botín piel marrón).
Total abonado: 30,00 €. Pendiente: 59,90 €. Fecha límite para completar el pago: 18/01/2027.
Gracias por tu confianza. Zapatería Paso Firme
```

### R-10
(F-002-10)
```text
Hola Carmen Ruiz: hemos recibido tu abono de 0,10 € para el apartado nº 25 (Botín piel marrón, talla 38).
Total abonado: 30,00 €. Pendiente: 59,90 €. Fecha límite para completar el pago: 18/01/2027.
Gracias por tu confianza. Zapatería Paso Firme
```

## Cómo probar

El webhook es de `[000]`; este sub-flujo se prueba **sin curl**:

1. Abrir `[002] Recibo de abono` en el editor, nodo `Recibir abono registrado` → *Pin data* → pegar la Base con los cambios del caso (un objeto en la raíz, **sin** `body` ni `evento`):
   ```json
   [{"id": 25, "fecha": "2026-10-20", "cliente": "Carmen Ruiz", "telefono": "612 000 001", "email": null, "producto": "Botín piel marrón", "talla": "38", "precio": 89.9, "fecha_limite": "2027-01-18", "estado": "liquidado", "abonado": 89.9, "pendiente": 0.0, "importe": 59.9}]
   ```
   (ejemplo = F-002-8).
2. *Test workflow* y comprobar qué nodo de envío se ejecuta, su `To`, `Subject` y `Message` contra la tabla. Para no escribir a nadie, se puede desactivar (*Deactivate*) el nodo Gmail y revisar su entrada, o apuntar `tienda_email` a un buzón de pruebas `@example.com`.
3. F-002-11: repetir con *Settings → Timezone* del flujo en `America/New_York`.
4. F-002-12: n8n **no lanza el Error Workflow en ejecuciones manuales**. Probarlo de extremo a extremo: con `[000]`, `[002]` y `[ERR]` importados (y `[000]` publicado en la instancia de pruebas, decisión humana), crear un apartado con email `no-es-un-correo` y abonar (`POST /api/apartados/{id}/abonos`). En manual solo se verifica el reintento (2 intentos) y el error del nodo.
5. **Quitar el pin data antes de exportar** el JSON.

Pruebas de extremo a extremo con los datos de ejemplo de la app (`backend/seed.py`): los ids, nombres y fechas cambian con el día de arranque, así que los textos esperados se recalculan formateando la respuesta del `POST .../abonos`, no los de esta tabla. Reiniciar: `docker compose down -v && docker compose up -d`.

## Cobertura

CA-1 → F-002-1, F-002-3, F-002-9, F-002-10, F-002-11 · CA-2 → F-002-2 · CA-3 → F-002-3, F-002-4 · CA-4 → F-002-5, F-002-6, F-002-7, F-002-8 · Fallo del envío (§7) → F-002-12.

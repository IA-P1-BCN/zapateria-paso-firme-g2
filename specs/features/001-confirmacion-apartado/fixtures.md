# SCOPE: infraestructura-agentes (NO tocar backend/frontend/automation)

# 001 · Confirmación de apartado — Fixtures

Entrada = `datos` del evento `apartado.creado` (lo que pasa el enrutador). Datos ficticios.

| Caso | Entrada | Resultado esperado |
|---|---|---|
| F-001-1 Camino feliz | `{"id": 25, "fecha": "2026-10-20", "cliente": "Carmen Ruiz", "telefono": "612 345 001", "email": "carmen@example.com", "producto": "Botín piel marrón", "talla": "38", "precio": 89.9, "fecha_limite": "2027-01-18", "estado": "activo", "abonado": 10.0, "pendiente": 79.9}` | Correo a carmen@example.com con «Botín piel marrón», «38», «89,90 €», «10,00 €», «79,90 €», «18/01/2027» |
| F-001-2 Sin correo | Igual que F-001-1 con `"email": null` | No se envía nada al cliente; la tienda recibe «sin correo» con #25 y Carmen Ruiz; ejecución sin error |
| F-001-3 Sin talla | Igual que F-001-1 con `"talla": null` | El mensaje no contiene «null» |
| F-001-4 Liquidado al alta | `"abonado": 89.9, "pendiente": 0.0, "estado": "liquidado"` | Mensaje de «pagado, puede recogerlos» <<PENDIENTE: texto>> |
| F-001-5 Con la app | Crear un apartado real desde http://localhost:8000 | Mensaje recibido en < 1 min (CA-1) |

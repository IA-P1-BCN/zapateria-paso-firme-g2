# HU-13 · Solicitud de apartado por Gmail + Importación datáfono (FL-12, FL-13)

**Disparador:** Gmail Trigger sobre `PF/Solicitudes` y `PF/Datáfono` + Schedule  
**Resultado:** Solicitud registrada / Ventas con tarjeta importadas

```mermaid
sequenceDiagram
    actor Cliente
    participant GT as Gmail Trigger
    participant FL12 as FL-12 Solicitud
    participant IA as Modelo IA
    participant SHEETS as Google Sheets
    participant GM as Gmail
    actor Marisa
    participant DEP as Dependienta
    participant APP as App

    Cliente->>GT: Correo solicitud de apartado
    GT->>FL12: Procesar
    FL12->>IA: Extraer nombre/producto/talla/teléfono
    IA-->>FL12: Datos
    FL12->>FL12: Validar mínimos
    FL12->>SHEETS: Guardar en Solicitudes (pendiente)
    FL12->>GM: Avisar a Marisa con checklist
    FL12->>GM: Responder al cliente (recibida)
    Marisa->>DEP: Confirma disponibilidad
    Cliente->>DEP: Paga abono inicial
    DEP->>APP: Crea apartado en app
    FL12->>SHEETS: Marcar como convertida
```

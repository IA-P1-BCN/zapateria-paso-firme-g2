# HU-15 · Panel de Marisa (FL-14)

**Disparador:** Consulta  
**Resultado:** Panel con ventas, recaudación, pendiente y vencimientos

```mermaid
sequenceDiagram
    actor Marisa
    participant PANEL as Panel de Marisa
    participant API as API
    participant SHEETS as Google Sheets
    participant N8N as n8n

    Marisa->>PANEL: Acceder (autenticado)
    PANEL->>API: GET /api/ventas, /api/abonos, /api/apartados
    PANEL->>SHEETS: Obtener cierres y estado flujos
    PANEL->>N8N: Consultar últimas ejecuciones
    API-->>PANEL: Datos actualizados
    SHEETS-->>PANEL: Datos auxiliares
    N8N-->>PANEL: Estado
    PANEL->>Marisa: Mostrar métricas clave
```

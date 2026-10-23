# HU-08 · Error Workflow (FL-08)

**Disparador:** Error Trigger en cualquier workflow  
**Resultado:** Email de error a Marisa sin secretos

```mermaid
sequenceDiagram
    participant WF as Cualquier workflow
    participant ERR as Error Trigger
    participant FL08 as FL-08 Error Workflow
    participant GM as Gmail
    actor Marisa

    WF-->>ERR: Error en nodo/ejecución
    ERR->>FL08: Datos del error (workflow, nodo, mensaje, executionId)
    FL08->>GM: Email a Marisa con contexto y enlace (sin credenciales)
```

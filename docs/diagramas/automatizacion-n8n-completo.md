# Automatización n8n · Proyecto completo

**Proyecto:** Automatizaciones n8n · Zapatería Paso Firme  
**Alcance:** Niveles Esencial, Medio, Avanzado y Experto  
**Canal:** Gmail  
**PRD asociado:** [PRD del proyecto completo](../prd-completo.md)  
**Flujo de usuario:** [Flujo de usuario · Proyecto completo](flujo-usuario-completo.md)

Este documento muestra la automatización completa: el núcleo del Nivel Medio, las extensiones de autoservicio y las piezas de operación (PostgreSQL, backups, CI, panel y MCP).

---

## 1. Núcleo Esencial + Medio

```mermaid
flowchart LR
    APP["App de la tienda"] -- "eventos" --> WH["Webhook /tienda + Switch"]
    WH --> F1["FL-01, FL-02 y FL-04"]
    F1 --> GM["Gmail"]

    CRON["Schedule Trigger"] --> F2["FL-05, FL-06 y FL-07"]
    F2 --> API["API de la tienda"]
    F2 --> GM
    F2 --> SH["Google Sheets"]

    BANK["Banco por Gmail"] --> F3["FL-03 Abonos a distancia"]
    F3 --> API
    F3 --> GM
    F3 --> SH

    MAN["Ejecución manual"] --> F9["FL-09 Migración"]
    F9 --> API
    F9 --> SH
    F9 --> GM

    F1 -. "error" .-> ERR["FL-08 Error Workflow"]
    F2 -. "error" .-> ERR
    F3 -. "error" .-> ERR
    F9 -. "error" .-> ERR
    ERR --> GM
```

Los detalles de nodos, sub-workflows e idempotencia del núcleo están en [Automatización n8n · Nivel Medio](automatizacion-n8n-nivel-medio.md).

---

## 2. Extensiones Avanzado + Experto

```mermaid
flowchart TB
    subgraph ENTRADA["Gmail"]
        G1["PF/Consultas"]
        G2["PF/Marisa"]
        G3["PF/Solicitudes"]
        G4["PF/Datáfono"]
        G5["PF/Banco"]
        G6["PF/Errores"]
    end

    subgraph N8N["n8n"]
        F10["FL-10 Asistente de saldo"]
        F11["FL-11 Consultas de Marisa"]
        F12["FL-12 Solicitud de apartado"]
        F13["FL-13 Importación del datáfono"]
        F03["FL-03 Abonos a distancia"]
        IA["IA: intención, extracción y redacción"]
        SUB["SUB · Consultar apartados por email"]
        REC["Reconciliación diaria"]
        ERR["FL-08 Error Workflow"]
    end

    subgraph APP["App de la tienda"]
        API["API REST"]
        DB[("Datos")]
    end

    subgraph DATOS["Datos auxiliares"]
        SH["Google Sheets"]
        CONS["Consentimientos"]
        SOL["Solicitudes"]
        DAT["Datáfono"]
    end

    subgraph SALIDAS["Salidas"]
        CL["Email al cliente"]
        MA["Email a Marisa"]
    end

    G1 --> F10
    G2 --> F11
    G3 --> F12
    G4 --> F13
    G5 --> F03
    G6 --> ERR

    F10 --> CONS
    CONS --> SH
    CONS -- "sin consentimiento" --> MA
    CONS -- "con consentimiento" --> SUB
    SUB --> API
    API --> DB
    F10 --> IA
    IA --> F10
    F10 --> CL

    F11 --> API
    F11 --> IA
    IA --> F11
    F11 --> MA

    F12 --> IA
    IA --> F12
    F12 --> SOL
    F12 --> MA
    F12 --> CL

    F13 --> DAT
    F13 --> API
    F13 --> MA

    F03 --> API
    F03 --> SH

    REC --> API
    REC --> SH
    REC --> MA

    F10 -. "error" .-> ERR
    F11 -. "error" .-> ERR
    F12 -. "error" .-> ERR
    F13 -. "error" .-> ERR
    F03 -. "error" .-> ERR
    ERR --> MA
```

---

## 3. Workflows

| ID | Workflow | Disparador | Núcleo | Salidas |
|---|---|---|---|---|
| FL-01 | Confirmación de apartado | Webhook | Webhook + Switch | Gmail |
| FL-02 | Recibo de abono | Webhook | Webhook + Switch | Gmail |
| FL-03 | Abonos a distancia | Gmail Trigger | IA + API | API, Gmail, Sheets |
| FL-04 | Venta grande | Webhook | Webhook + Switch | Gmail |
| FL-05 | Cierre diario | Schedule 21:30 | API + Sheets | Gmail, Sheets |
| FL-06 | Recordatorios y vencimientos | Schedule 08:00 | API + Sheets | Gmail, Sheets |
| FL-07 | Informe mensual | Schedule día 1 | API | Gmail |
| FL-08 | Error Workflow | Error Trigger | — | Gmail |
| FL-09 | Migración del Excel | Manual | CSV + API | API, Sheets, Gmail |
| FL-10 | Asistente de saldo | Gmail Trigger | IA + API + consentimiento | Gmail |
| FL-11 | Consultas de Marisa | Gmail Trigger | IA + API | Gmail |
| FL-12 | Solicitud de apartado | Gmail Trigger | IA + Sheets | Gmail, Sheets |
| FL-13 | Importación del datáfono | Schedule 23:00 + Gmail | CSV + API | API, Sheets, Gmail |
| FL-14 | Panel de Marisa | Consulta | API + Sheets | Panel |
| FL-15 | CI de flujos | Pull Request | GitHub Actions | Check |
| FL-16 | Servidor MCP | Consulta | API | MCP |

---

## 4. Flujo 10 en secuencia

```mermaid
sequenceDiagram
    actor Cliente
    participant Gmail
    participant FL10 as n8n FL-10
    participant CONS as Consentimientos
    participant API as App API
    participant IA

    Cliente->>Gmail: Consulta de saldo
    Gmail->>FL10: Trigger PF/Consultas
    FL10->>FL10: Verificar message_id y auto-respuesta
    FL10->>CONS: ¿Consentimiento del email?
    alt Sin consentimiento
        CONS-->>FL10: No
        FL10->>Cliente: Aviso de contactar con la tienda
        FL10->>FL10: Registrar consulta
    else Con consentimiento
        CONS-->>FL10: Sí
        FL10->>API: GET /api/apartados
        API-->>FL10: Apartados
        FL10->>FL10: Filtrar por email remitente
        alt Sin coincidencias
            FL10->>Cliente: Respuesta genérica
        else Con coincidencias
            FL10->>IA: Intención y datos filtrados
            IA-->>FL10: Respuesta redactada
            FL10->>Cliente: Saldo y fecha límite
        end
    end
```

**Claves:**

- La IA no recibe la lista completa de clientes.
- Las cifras salen de la API.
- Sin consentimiento no se responde con datos.
- Una respuesta por `message_id`.

---

## 5. Flujo 13 en secuencia

```mermaid
sequenceDiagram
    participant Gmail
    participant FL13 as n8n FL-13
    participant SH as Google Sheets
    participant API as App API
    actor Marisa

    Gmail->>FL13: Trigger PF/Datáfono
    FL13->>Gmail: Descargar CSV adjunto
    FL13->>FL13: Parsear y normalizar
    FL13->>SH: Consultar hashes importados
    SH-->>FL13: Hashes existentes
    loop Cada cobro nuevo
        FL13->>API: POST /api/ventas con tarjeta
        API-->>FL13: Venta creada
        FL13->>SH: Guardar hash
    end
    FL13->>Marisa: Reporte de importados, omitidos y errores
```

**Reglas:**

- Solo cobros con tarjeta.
- No se importan devoluciones ni negativos.
- Si no hay CSV, se avisa sin fallar.
- La clave `hash_cobro` evita duplicados.

---

## 6. Infraestructura y operación

```mermaid
flowchart TB
    subgraph CLOUD["Cloud"]
        LB["HTTPS y proxy inverso"]
        N8N["n8n"]
        APP["App de la tienda"]
        PG[("PostgreSQL")]
        VOL[("Volumen de datos")]
    end

    subgraph GOBIERNO["Gobierno"]
        CI["GitHub Actions"]
        MCP["Servidor MCP"]
        PANEL["Panel de Marisa"]
    end

    subgraph CONTINUIDAD["Continuidad"]
        BK["Backups diarios"]
        MON["Monitorización"]
        REC["Reconciliación diaria"]
    end

    LB --> N8N
    LB --> APP
    N8N --> PG
    APP --> VOL
    PG --> BK
    N8N --> REC
    REC --> PG
    CI --> N8N
    MON --> N8N
    MON --> APP
    PANEL --> APP
    PANEL --> N8N
    MCP --> APP
```

### 6.1 Despliegue

| Elemento | Configuración |
|---|---|
| n8n | Contenedor con HTTPS, `WEBHOOK_URL` pública y `N8N_ENCRYPTION_KEY` |
| App | Contenedor con `API_KEY` y `N8N_WEBHOOK_URL` |
| PostgreSQL | Base de datos de n8n |
| Volumen | Datos de la app y de n8n |
| Proxy | TLS, redirección HTTPS y límites de tasa |
| Secretos | Variables del proveedor, nunca en Git |

### 6.2 Backups

- `pg_dump` diario de PostgreSQL.
- Copia de la clave de cifrado de n8n.
- Copia del volumen de la app.
- Retención propuesta: 30 días.
- Restauración de prueba mensual.
- Almacenamiento fuera del servidor principal.

### 6.3 Reconciliación

1. Comparar los abonos del día en la app con `Emails` y los recibos enviados.
2. Reenviar recibos que falten.
3. Registrar eventos no recibidos.
4. Comprobar cierres y avisos.
5. Enviar resumen a Marisa.
6. No duplicar: claves de idempotencia.

### 6.4 Webhook en producción

El webhook no puede quedar abierto. Opciones:

1. **Basic Auth en n8n** y credenciales en la URL de `N8N_WEBHOOK_URL`.
2. **Cabecera de autenticación** enviada por la app, con un cambio mínimo en `backend/services/n8n.py`.
3. **Proxy inverso** que valide una cabecera o un token.

Además:

- Validar el esquema del cuerpo en n8n.
- Rechazar eventos desconocidos.
- Limitar el tamaño del payload.
- Rate limiting en el proxy.
- No exponer el editor de n8n sin autenticación.

---

## 7. CI de flujos

```mermaid
flowchart LR
    PR["Pull Request con workflows/**"] --> J["Job de validación"]
    J --> P["JSON parseable"]
    J --> S["Sin secretos"]
    J --> N["Nombres y convención"]
    J --> W["Webhook esperado"]
    J --> E["Error Workflow configurado"]
    P --> R{"¿Todo OK?"}
    S --> R
    N --> R
    W --> R
    E --> R
    R -- "Sí" --> M["Merge permitido"]
    R -- "No" --> F["PR bloqueada"]
```

**Comprobaciones mínimas:**

- `JSON.parse` correcto.
- Campos `name`, `nodes`, `connections`, `settings`.
- Nombres únicos y prefijo `PF · FL-0X`.
- Sin `credentials` con valores.
- Sin tokens, claves ni contraseñas.
- Path de webhook `tienda`.
- Error Workflow configurado.
- Tags permitidos.

---

## 8. Panel y MCP

### 8.1 Panel

| Fuente | Datos |
|---|---|
| API de la app | Ventas, abonos, apartados activos, pendiente |
| Google Sheets | Cierres, avisos, solicitudes |
| n8n | Última ejecución y errores |

**Herramienta propuesta:** Looker Studio sobre Google Sheets, o una web sencilla que consuma la API. Requisitos: móvil, autenticación y actualización diaria como mínimo.

### 8.2 MCP

```mermaid
flowchart LR
    AG["Agente externo"] -- "token" --> MCP["Servidor MCP n8n"]
    MCP --> T1["consultar_apartado"]
    MCP --> T2["listar_vencimientos"]
    MCP --> T3["resumen_negocio"]
    T1 --> API["API de la tienda"]
    T2 --> API
    T3 --> API
    MCP --> AUD["Auditoría"]
```

- Solo lectura.
- Token obligatorio.
- Datos mínimos.
- Auditoría de consultas.
- Sin acceso directo a la base de datos.

---

## 9. Datos auxiliares

| Hoja | Clave | Flujos |
|---|---|---|
| `Cierres` | `fecha` | FL-05 |
| `Avisos` | `apartado_id + tipo + fecha_limite` | FL-06 |
| `Emails` | `message_id` | FL-03 |
| `Migracion` | `hash_fila` | FL-09 |
| `Consentimientos` | `email` | FL-10, FL-12 |
| `Solicitudes` | `message_id` | FL-12 |
| `Consultas` | `message_id` | FL-10, FL-11 |
| `Datáfono` | `hash_cobro` | FL-13 |
| `Reconciliacion` | `fecha` | Reconciliación |

---

## 10. Credenciales y variables

| Tipo | Nombre | Uso |
|---|---|---|
| Header Auth | `PF · API tienda` | API |
| OAuth2 | `PF · Gmail` | Correo |
| OAuth2 | `PF · Google Sheets` | Hojas |
| API Key | `PF · IA` | Modelo |
| Postgres | `PF · PostgreSQL` | n8n |
| Variable | `MARISA_EMAIL` | Consultas y avisos |
| Variable | `TIENDA_EMAIL` | Remitente |
| Variable | `VENTA_GRANDE_UMBRAL` | FL-04 |
| Variable | `BANCO_REMITENTES` | FL-03 |
| Variable | `ZONA_HORARIA` | Schedule |
| Variable | `PANEL_URL` | Panel |
| Variable | `MCP_TOKEN` | MCP |

---

## 11. Errores, alertas y límites

| Situación | Tratamiento |
|---|---|
| Error de cualquier workflow | FL-08 envía email a Marisa |
| Gmail con cuota | Reintento y aviso |
| IA con límite | Cola, reintento y fallback |
| API 401 | Error de configuración |
| API 422 | Regla de negocio; aviso |
| Webhook sin autenticación | Rechazo y alerta |
| Backup fallido | Alerta |
| Restauración fallida | Incidencia crítica |
| CI rojo | PR bloqueada |
| MCP sin token | Rechazo y registro |
| Consulta de cliente sin consentimiento | Sin datos y aviso |

---

## 12. Orden de construcción

| Fase | Contenido |
|---|---|
| 1 | Webhook, Switch, sub-workflows y FL-01/FL-02 |
| 2 | FL-03, FL-05 y FL-08 |
| 3 | FL-04, FL-06, FL-07 y FL-09 |
| 4 | FL-10, FL-11, FL-12, FL-13 |
| 5 | Reconciliación, webhook protegido y consentimientos |
| 6 | PostgreSQL, backups, despliegue y monitorización |
| 7 | Panel, CI y MCP |
| 8 | Pruebas, evidencias y documentación |

Cada fase se prueba con datos de ejemplo y se revisa en una PR antes de avanzar.

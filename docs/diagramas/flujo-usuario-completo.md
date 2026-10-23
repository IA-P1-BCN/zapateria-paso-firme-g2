# Flujo de usuario · Proyecto completo

**Proyecto:** Automatizaciones n8n · Zapatería Paso Firme  
**Alcance:** Niveles Esencial, Medio, Avanzado y Experto  
**Canal:** Gmail  
**PRD asociado:** [PRD del proyecto completo](../prd-completo.md)  
**Diagrama de automatización:** [Automatización n8n · Proyecto completo](automatizacion-n8n-completo.md)

Este documento une el recorrido del [Nivel Medio](flujo-usuario-nivel-medio.md) con las funciones avanzadas: consultas por correo, solicitudes de apartado, importación del datáfono, panel de Marisa y operación cloud.

---

## 1. Recorrido completo de un vistazo

```mermaid
flowchart TD
    subgraph CLIENTE["Cliente"]
        C1["Aparta en tienda"]
        C2["Paga abonos"]
        C3["Paga por Bizum o transferencia"]
        C4["Pregunta su saldo por email"]
        C5["Pide apartar por email"]
        C6["Recibe confirmación, recibo, recordatorio o vale"]
        C7["Recibe respuesta a su consulta"]
    end

    subgraph TIENDA["Dependienta y Marisa"]
        T1["Dependienta registra apartado, abono o venta"]
        T2["Marisa revisa solo los casos dudosos"]
        T3["Marisa confirma la solicitud"]
        T4["Marisa pregunta cifras por email"]
        T5["Marisa consulta el panel"]
    end

    subgraph APP["App de la tienda"]
        A1["Valida reglas y guarda"]
        A2["API REST"]
        A3["Webhook de eventos"]
    end

    subgraph N8N["n8n"]
        N0["Webhook /tienda + Switch"]
        N1["FL-01 a FL-08"]
        N3["FL-03 Abonos a distancia"]
        N10["FL-10 Asistente de saldo"]
        N11["FL-11 Consultas de Marisa"]
        N12["FL-12 Solicitud de apartado"]
        N13["FL-13 Importación del datáfono"]
        N14["Reconciliación diaria"]
    end

    subgraph CORREO["Gmail"]
        GB["Banco"]
        GC["Consultas de clientes"]
        GM["Consultas de Marisa"]
        GS["Solicitudes"]
        GD["CSV del datáfono"]
    end

    subgraph OPS["Operación"]
        P["Panel de Marisa"]
        CLOUD["Cloud con HTTPS"]
        BK["Copias de seguridad"]
    end

    C1 --> T1
    C2 --> T1
    T1 --> A1
    A1 --> A2
    A2 --> A3
    A3 --> N0
    N0 --> N1
    N1 --> C6

    C3 --> GB
    GB --> N3
    N3 --> A2
    N3 --> C6
    N3 -. "duda" .-> T2
    T2 --> T1

    C4 --> GC
    GC --> N10
    N10 --> A2
    N10 --> C7
    N10 -. "sin consentimiento o sin coincidencia" .-> T2

    C5 --> GS
    GS --> N12
    N12 --> T3
    N12 --> C7
    T3 --> T1

    T4 --> GM
    GM --> N11
    N11 --> A2
    N11 --> T4

    GD --> N13
    N13 --> A2
    N13 --> T2

    N14 --> A2
    N14 --> T2

    A2 --> P
    N0 --> P
    CLOUD --> N0
    BK --> A2
    P --> T5
```

---

## 2. Consultas por Gmail

### 2.1 Cliente pregunta por su saldo

```mermaid
sequenceDiagram
    actor Cliente
    participant Gmail
    participant FL10 as n8n FL-10
    participant CONS as Consentimientos
    participant API as App API
    participant IA

    Cliente->>Gmail: "¿Cuánto me falta para mis zapatos?"
    Gmail->>FL10: Trigger PF/Consultas
    FL10->>FL10: Comprobar message_id y auto-respuesta
    FL10->>CONS: ¿Email con consentimiento?
    alt Sin consentimiento
        CONS-->>FL10: No
        FL10->>Cliente: Aviso de contactar con la tienda
        FL10->>FL10: Registrar consulta
    else Con consentimiento
        CONS-->>FL10: Sí
        FL10->>API: GET /api/apartados
        API-->>FL10: Lista de apartados
        FL10->>FL10: Filtrar por email remitente
        alt Sin apartados
            FL10->>Cliente: Respuesta genérica
        else Con apartados
            FL10->>IA: Intención y datos filtrados
            IA-->>FL10: Respuesta redactada
            FL10->>Cliente: Saldo, talla, pendiente y fecha límite
        end
    end
```

**Reglas:**

- Solo se muestran apartados cuyo `email` coincide con el remitente.
- Si hay varios, se listan todos los suyos.
- Las cifras salen de la API; la IA solo redacta.
- Si no hay coincidencia, no se revela nada.
- Se responde una vez por `message_id`.

### 2.2 Marisa pregunta cifras

```mermaid
sequenceDiagram
    actor Marisa
    participant Gmail
    participant FL11 as n8n FL-11
    participant API as App API
    participant IA

    Marisa->>Gmail: "¿Cuánto se recaudó esta semana?"
    Gmail->>FL11: Trigger PF/Marisa
    FL11->>FL11: Verificar remitente autorizado
    alt No autorizado
        FL11-->>Marisa: Sin datos
    else Autorizado
        FL11->>IA: Clasificar intención
        IA-->>FL11: recaudacion_semana
        FL11->>API: GET ventas y abonos del periodo
        API-->>FL11: Datos
        FL11->>IA: Redactar con cifras de la API
        IA-->>FL11: Respuesta
        FL11->>Marisa: Total, desglose y periodo
    end
```

**Intenciones:** recaudación de hoy, semana o mes; pendiente de cobro; vencimientos; apartados activos; ventas del día.

**Regla:** la IA elige una consulta permitida; no genera consultas arbitrarias ni inventa cifras.

---

## 3. Entradas automáticas

### 3.1 Solicitud de apartado por correo

```mermaid
flowchart TD
    C["Cliente escribe: quiero apartar unos zapatos"] --> G["Gmail PF/Solicitudes"]
    G --> F["FL-12 Solicitud de apartado"]
    F --> X["IA extrae producto, talla, teléfono y nombre"]
    X --> V{"¿Datos mínimos?"}
    V -- "No" --> M["Email a Marisa con lo que falta"]
    V -- "Sí" --> S["Guardar en Solicitudes"]
    S --> M
    S --> R["Respuesta al cliente: solicitud recibida"]
    M --> T["Marisa comprueba disponibilidad y precio"]
    T --> A["Cliente paga el abono inicial"]
    A --> D["Dependienta crea el apartado en la app"]
    D --> E["Solicitud marcada como convertida"]
    E --> C2["Cliente recibe confirmación del apartado"]
```

**Importante:** la solicitud **no crea** el apartado. El apartado se formaliza cuando llega el abono inicial y la dependienta lo registra. Así se evita reservar stock sin pago.

### 3.2 Importación del datáfono

```mermaid
flowchart LR
    D["Correo con CSV del datáfono"] --> S["Schedule 23:00"]
    S --> G["Buscar adjunto en Gmail"]
    G --> P["Descargar y parsear CSV"]
    P --> H["Calcular hash por cobro"]
    H --> C{"¿Ya importado?"}
    C -- "Sí" --> O["Reportar omitido"]
    C -- "No" --> V["POST /api/ventas con tarjeta"]
    V --> L["Guardar hash en Datáfono"]
    L --> E["Email a Marisa"]
    O --> E
    G -. "sin CSV" .-> E
```

**Reglas:**

- Solo cobros con tarjeta.
- No se importan devoluciones ni importes negativos; se reportan.
- La clave de idempotencia evita duplicados.
- Si no hay CSV, se avisa sin fallar.

---

## 4. Operación y panel

```mermaid
flowchart TB
    subgraph CLOUD["Cloud"]
        LB["HTTPS y proxy inverso"]
        N8N["n8n"]
        APP["App de la tienda"]
        PG[("PostgreSQL")]
        VOL[("Volumen de datos")]
    end

    subgraph GOBIERNO["Gobierno y operación"]
        CI["GitHub Actions"]
        BK["Backups diarios"]
        MON["Monitorización"]
        PANEL["Panel de Marisa"]
        MCP["Servidor MCP"]
    end

    LB --> N8N
    LB --> APP
    N8N --> PG
    APP --> VOL
    PG --> BK
    CI --> N8N
    MON --> N8N
    MON --> APP
    PANEL --> APP
    PANEL --> N8N
    MCP --> APP
```

### 4.1 Qué ve Marisa en el panel

| Bloque | Contenido |
|---|---|
| Hoy | Ventas, abonos y total |
| Mes | Recaudación y comparación |
| Pendiente | Suma de lo que falta por cobrar |
| Vencimientos | Apartados que vencen en 7 y 1 días |
| Flujos | Última ejecución y errores |
| Accesos | Enlace a la app y a los cierres |

### 4.2 Continuidad

- n8n con PostgreSQL.
- Copia diaria de base de datos y clave de cifrado.
- Restauración probada una vez al mes.
- Monitorización cada 5 minutos.
- Reconciliación diaria de abonos y eventos.
- Webhook protegido cuando se expone a Internet.

---

## 5. Adaptación de Telegram a Gmail

| Antes | Ahora | Efecto |
|---|---|---|
| Cliente pregunta por Telegram | Cliente escribe a `tienda@pasofirme.example` | Asíncrono; respuesta objetivo en 15 minutos |
| Marisa pregunta por Telegram | Marisa escribe desde su correo autorizado | Copia y trazabilidad en la bandeja |
| Cliente pide apartar por Telegram | Cliente envía correo a `PF/Solicitudes` | La tienda confirma y crea el apartado al cobrar |
| Datáfono se sube a mano | CSV adjunto en Gmail | Importación nocturna |
| Avisos internos por Telegram | Avisos por Gmail | Menos inmediatez, menos credenciales |

**Consecuencia de producto:** Gmail no es un chat. El asistente es útil para consultas no urgentes. Si Marisa necesita inmediatez, se reevalúa un canal adicional en el futuro.

---

## 6. Journey completo *(recorrido del usuario a lo largo de la experiencia)*

| Etapa | Cliente | Dependienta | Marisa | Sistema |
|---|---|---|---|---|
| Descubrimiento | Elige zapatos | Atiende | — | — |
| Alta | Deja abono inicial | Registra apartado | — | App valida y avisa |
| Seguimiento | Paga abonos | Registra | — | Recibos y saldos |
| Pago remoto | Bizum o transferencia | — | Decide dudas | n8n registra o pregunta |
| Vencimiento | Recibe aviso | — | Recibe lista | n8n vence y genera vale |
| Cierre | — | — | Recibe cierre | n8n suma y guarda |
| Informe | — | — | Recibe informe | n8n consulta y envía |
| Consulta | Pregunta por correo | — | — | Asistente responde |
| Solicitud | Pide apartar | Crea al cobrar | Confirma | n8n registra solicitud |
| Operación | — | — | Ve el panel | Cloud, backups y CI |

---

## 7. Momentos de verdad del proyecto completo

1. **El cliente pregunta y recibe sus datos, no los de otro.** La identidad se verifica por email.
2. **Marisa pregunta y recibe cifras reales.** La IA no calcula.
3. **Una solicitud no reserva stock sin pago.** Se confirma con el abono inicial.
4. **El datáfono no duplica ventas.** Hash y reporte.
5. **El webhook público no acepta cualquiera.** Autenticación y validación.
6. **El sistema sobrevive a una caída.** Backups, monitorización y reconciliación.
7. **Un cambio de flujo no rompe main.** CI valida el JSON.
8. **Los datos personales se tratan con cuidado.** Consentimiento, minimización y retención.

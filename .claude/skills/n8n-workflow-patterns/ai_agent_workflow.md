# SCOPE: infraestructura-agentes (NO tocar backend/frontend/workflows)

# AI Extraction Workflow Pattern (project adaptation)

> Archivo de referencia de una skill externa adaptada. Prevalecen `AGENTS.md` y la nota de su `SKILL.md`.

**Use Case**: a language model reads unstructured text (for example a bank email about a Bizum) and **extracts**
fields. The **workflow decides** what to do with them, using IF/Switch nodes and the app's API (AGENTS.md rule 6).

> The upstream file described an agent that "decides and acts" with tools. That contradicts rule 6 of this project,
> so it was rewritten. An AI node here never registers, rejects or chooses an apartado by itself.

---

## Pattern Structure

```
Trigger → (filter: is it a payment?) → LLM Chain / Information Extractor + Structured Output Parser
        → IF/Switch (all fields present? amount ≤ pendiente? apartado activo?) → HTTP Request (API)
                                                                          └─ else → ask Marisa
```

- The model receives **only what it needs** (subject and body of the email), never data from the app (rule 10, RGPD).
- Output is forced to JSON with a **Structured Output Parser** (`ordenante`, `importe`, `concepto`, `confianza`).
- Searching the apartado, checking the amount against `pendiente` and registering the abono are done by
  **HTTP Request nodes** against the API (`tienda-api`). If anything is unclear: **register nothing** and ask Marisa.

---

## Core AI Connection Types

Sub-nodes connect with dedicated `ai_*` connection types, **not** `main`. A sub-node wired to `main` is
disconnected (and `validate_workflow` flags it).

| Connection type | Wires in | Into slot |
|---|---|---|
| `ai_languageModel` | The LLM (OpenAI, Anthropic, Gemini, Ollama…) | model (required) |
| `ai_outputParser` | Structured-output parser | output parser |
| `ai_memory` | Conversation context store | memory (only for the advanced Telegram assistants) |
| `ai_tool` | A node the model can call | tools — **avoid here**: tools let the model act |

**Wiring direction**: a sub-node connects FROM itself TO the chain/agent, and the connection lives on the
sub-node keyed by its `ai_*` type. Edit it in the n8n UI or in the exported JSON, never in the live instance from an agent.

**Output fact**: an AI Agent node puts its answer in `$json.output`; with a Structured Output Parser the fields are
under `$json.output.<campo>`.

---

## Checklist for AI Extraction Workflows

- [ ] The model only **extracts**; every decision is an IF/Switch or an API response
- [ ] Model wired via `ai_languageModel`; parser via `ai_outputParser`
- [ ] No `ai_tool` that registers, changes or deletes data
- [ ] Only the minimum text is sent to the model (no names, phones or emails from the app)
- [ ] Missing or low-confidence fields go to the "ask Marisa" branch
- [ ] Validated (`python scripts/validate_workflows.py`) and exported with `"active": false`; activation is human

---

**Related**:
- [webhook_processing.md](webhook_processing.md) — receiving events
- [http_api_integration.md](http_api_integration.md) — calling the API
- Project skills `dominio-apartados`, `tienda-api`, `revision-seguridad-flujos`

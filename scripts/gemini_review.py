# SCOPE: infraestructura-agentes (NO tocar backend/frontend/workflows)
"""Ask Gemini to review a pull request diff against the project rules.

Reads (env vars):
  GEMINI_API_KEY            required; if missing, writes a notice and exits 0
  GEMINI_MODEL              optional, defaults to gemini-flash-lite-latest (best free quota)
  GEMINI_FALLBACK_MODEL     optional, tried when the main model keeps failing
  DIFF_FILE                 path to the PR diff
  CI_REPORT_FILE            path to the tests/validation output (optional)
  REVIEW_FILE               where to write the Markdown review
  AGENTS_FILE               path to AGENTS.md (optional extra context for the rules)
"""

import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

API_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
MAX_DIFF_CHARS = 120_000
REQUEST_TIMEOUT_SECONDS = 90
RETRY_WAITS_SECONDS = [15]
RETRYABLE_STATUS = {429, 500, 502, 503, 504}

BASE_RULES = """You are a strict but helpful code reviewer for a student team building n8n
automations for a shoe shop (Zapateria Paso Firme). Review the pull request diff.

Focus, in this order:
1. Security: credentials, API keys, tokens or real personal data in workflow JSONs, code or docs.
   Exported n8n workflows must never contain secrets; nodes reference credentials by name.
2. Business rules: the AI node only extracts data; IF/Switch and the API decide. Amounts
   (abonado, pendiente, vale) must come from the app, never recalculated in n8n or templates.
3. Correctness: webhook data read from $json.body..., app called at http://tienda:8000 inside
   n8n (never localhost), error handling (Error Workflow, error outputs, retries).
4. Conventions: backend is Python/FastAPI with pytest; n8n flow JSONs live in workflows/ as
   NNN-slug.json (3-digit spec number, see ADR-0002); commits and PR titles follow Conventional Commits.
5. If a CI report is attached, explain likely causes of failures and the minimal fix.

Do not invent n8n nodes or parameters. If unsure, say so.
Answer in Spanish, in Markdown, with sections: "Resumen", "Problemas" (each with file and
severity: alta / media / baja) and "Sugerencias". Be concise. If there is nothing relevant,
say so in one line."""


def build_system_prompt() -> str:
    agents = os.environ.get("AGENTS_FILE", "AGENTS.md")
    path = Path(agents)
    prompt = BASE_RULES
    if path.is_file():
        rules = path.read_text(encoding="utf-8")[:20_000]
        prompt += f"\n\nProject rules from {agents}:\n{rules}"
    else:
        prompt += f"\n\n({agents} not found in this PR; review only against the base rules above.)"
    return prompt


def call_gemini(model: str, api_key: str, system_prompt: str, user_content: str) -> str:
    url = API_URL.format(model=model)
    body = json.dumps(
        {
            "system_instruction": {"parts": [{"text": system_prompt}]},
            "contents": [{"parts": [{"text": user_content}]}],
            "generationConfig": {"temperature": 0.2, "maxOutputTokens": 2048},
        }
    ).encode("utf-8")

    last_error: Exception | None = None
    models = [model]
    fallback = os.environ.get("GEMINI_FALLBACK_MODEL")
    if fallback and fallback != model:
        models.append(fallback)

    for candidate in models:
        for attempt in range(len(RETRY_WAITS_SECONDS) + 1):
            request = urllib.request.Request(
                url.format(model=candidate),
                data=body,
                headers={"Content-Type": "application/json", "x-goog-api-key": api_key},
                method="POST",
            )
            try:
                with urllib.request.urlopen(request, timeout=REQUEST_TIMEOUT_SECONDS) as response:
                    payload = json.loads(response.read().decode("utf-8"))
                return payload["candidates"][0]["content"]["parts"][0]["text"]
            except urllib.error.HTTPError as exc:
                last_error = exc
                if exc.code not in RETRYABLE_STATUS:
                    break
            except Exception as exc:  # noqa: BLE001 - report any transport failure
                last_error = exc
            if attempt < len(RETRY_WAITS_SECONDS):
                time.sleep(RETRY_WAITS_SECONDS[attempt])

    raise RuntimeError(f"Gemini falló con todos los modelos: {last_error}")


def main() -> int:
    review_file = Path(os.environ.get("REVIEW_FILE", "review.md"))
    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        review_file.write_text(
            "## 🤖 Review IA\n\n⚠️ No hay `GEMINI_API_KEY` configurada en los secrets del repo; "
            "se omite la review automática.\n",
            encoding="utf-8",
        )
        print("GEMINI_API_KEY ausente; review omitida")
        return 0

    diff_path = Path(os.environ.get("DIFF_FILE", "pr.diff"))
    diff = diff_path.read_text(encoding="utf-8") if diff_path.is_file() else ""
    if len(diff) > MAX_DIFF_CHARS:
        diff = diff[:MAX_DIFF_CHARS] + "\n… [diff truncado por longitud]"

    user_content = f"Diff del PR:\n```diff\n{diff}\n```"

    ci_report = os.environ.get("CI_REPORT_FILE")
    if ci_report and Path(ci_report).is_file():
        report = Path(ci_report).read_text(encoding="utf-8")[:8_000]
        user_content += f"\n\nSalida de la CI (tests / validación de flujos):\n```\n{report}\n```"

    if not diff.strip():
        user_content += "\n\n(El diff está vacío: el PR no cambia código.)"

    model = os.environ.get("GEMINI_MODEL") or "gemini-flash-lite-latest"
    try:
        text = call_gemini(model, api_key, build_system_prompt(), user_content)
        review_file.write_text(f"## 🤖 Review IA ({model})\n\n{text}\n", encoding="utf-8")
    except Exception as exc:  # noqa: BLE001 - never break the workflow for a review failure
        review_file.write_text(
            "## 🤖 Review IA\n\n⚠️ La review automática falló: "
            f"`{exc}`. El PR se puede revisar manualmente.\n",
            encoding="utf-8",
        )
        print(f"Review fallida: {exc}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

# SCOPE: infraestructura-agentes (NO tocar backend/frontend/workflows)

# 003 · Abonos a distancia — Fixtures

Los correos están en `data/correos/` (no se copian aquí). El resultado esperado sale del enunciado (`docs/BRIEFING_zapateria.md`, tabla de correos) y está pensado para los **apartados de ejemplo** que carga la app al arrancar (`backend/seed.py`).

| Caso | Correo | Extracción esperada (IA) | Resultado esperado del flujo |
|---|---|---|---|
| F-003-1 | `01_bizum_carmen.eml` | CARMEN RUIZ GARCIA · 10,00 · «zuecos» · bizum | Un único activo de «Carmen Ruiz» → **registra** 10 € |
| F-003-2 | `02_bizum_jorge.eml` | JORGE M. · 20,00 · «apartado 2 bota» · bizum | Nº de apartado en el concepto → **registra** en ese apartado |
| F-003-3 | `03_transferencia_lucia.eml` | LUCIA GOMEZ PEREZ · 12,00 · «Liquidar mocasines» · transferencia | Paga justo lo pendiente → **registra** con `forma_pago: "bizum"`, queda **liquidado** y se avisa a Marisa de que era una transferencia |
| F-003-4 | `04_bizum_laura.eml` | LAURA O. · 15,00 · «deportivas» · bizum | Importe > pendiente → **no registra**, avisa a Marisa con el motivo |
| F-003-5 | `05_bizum_romero.eml` | ROMERO D · 10,00 · (vacío) · bizum | Solo apellido e inicial, sin concepto → **no registra**, pregunta a Marisa |
| F-003-6 | `06_bizum_paula.eml` | PAULA RAMOS LEON · 20,00 · «zapatillas running…» · bizum | Apartado fuera de plazo → **no registra**, avisa a Marisa |
| F-003-7 | `07_transferencia_desconocido.eml` | ANTONIO FERNANDEZ SOTO · 25,00 · «botas» · transferencia | Ningún cliente → **no registra**, pregunta a Marisa |
| F-003-8 | `08_publicidad_banco.eml` | `es_pago: false` | **Se ignora**, sin aviso |
| F-003-9 | `09_bizum_silvia.eml` | SILVIA CORTES · 5,00 · «abono sandalias» · bizum | Un único activo de «Silvia Cortés» (con tilde en la app) → **registra** 5 € |

Comprobaciones extra:
- Tras F-003-1, F-003-2, F-003-3 y F-003-9 llega el recibo del flujo `002` (evento `abono.registrado`).
- Procesar F-003-1 dos veces no crea dos abonos.
- En ningún caso se envía a la IA la lista de apartados.

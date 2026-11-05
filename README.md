# Token Economics — Module 1: The End of Cheap Tokens

## Lab 1 — Read Your Token Bill

Reproducible implementation of the five Taller Academy lab exercises. The course's fixed illustrative rates are **$2.00 / million uncached input, $10.00 output, $2.50 cache write and $0.20 cached input**. These are NOT actual provider invoices.

| Exercise | Deliverable |
|---|---|
| 1. Predict then count | Five reproducible samples, real `tiktoken` counts and comparison in `SUBMISSION.md` |
| 2. Price three calls | Normalized usage, actual context size, total price, output share, monthly difference |
| 3. The loop tax | A 30-turn model with 20-/30-turn totals and early-file overhead |
| 4. Cost per completed task | Expected support-ticket costs with retry and human escalation |
| 5. Own baseline | Measured one-turn Ollama task from previous public FDE lab, with the incomplete result marked honestly |

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python count_tokens.py --write
python finalize_submission.py
python -m unittest discover -s tests -v
```

No hosted API key needed. The tokenizer is **OpenAI's `o200k_base`**. This counts the *raw content* under that tokenizer; it excludes chat-message wrappers, and is not an exact billed Anthropic, OpenAI or Gemini API input amount. The course permits the local OpenAI tokenizer track as an approximation for newer models.

## Evidence and safety

All source text comes from public training practice material; the JSONL corpus is synthetic. Historical baseline measured with **Ollama qwen2.5:3b** on November 4, 2026: one call, 68 input tokens, 58 output tokens, and no verified numerical result. It is explicitly marked **NOT COMPLETED** rather than claiming an unsupported success. See `results/baseline_measured.json`.

GitHub Actions runs the tokenizer after push, updates `SUBMISSION.md` with real counts, and checks arithmetic. Until that action succeeds, do **not** treat any token-count placeholders as observations.

# Token Economics — Module 1: The End of Cheap Tokens

## Lab 1: Read Your Token Bill

A reproducible, public, privacy-safe implementation of all five Taller Academy exercises.

- Exercise 1: Predict and **actually count** tokens for an authentic one-line request, English paragraph, Spanish translation, a 201-line practice Python source file, and comparable-length JSONL logs. The `o200k_base` tokenizer is used for content-only counts, not an API bill.
- Exercise 2: Price three normalized calls with **the course's fixed illustrative price sheet**. Compare uncached, cache read, and cache write.
- Exercise 3: Quantify cumulative token resends for 20 and 30 turns, including a one-time 5,000-token file. A per-turn CSV can be opened in Excel.
- Exercise 4: Compare total cost per completed support ticket, including human escalation after two failed attempts.
- Exercise 5: Use an **actual measured model request** from a prior public Day 1 lab. Its quality bar is marked **NO** rather than inventing a completed outcome.

See [SUBMISSION.md](SUBMISSION.md) for all five written deliverables and [results/token_counts.json](results/token_counts.json) for observed tokenizer counts.

The `.github/workflows/measure.yml` workflow counts all five samples automatically on the first push, finalizes the report, and commits results to `main`. No API key needed.

### Reproduce

```bash
python -m pip install -r requirements.txt
python count_tokens.py
python finalize_submission.py
python -m unittest discover -s tests -v
```

**Safety and accuracy:** All training materials are synthetic/public. Actual observed Ollama usage is distinguished from the hypothetical dollar cost under the course price sheet. The token counts depend on the tokenizer and omit chat message wrappers; different providers can bill different totals.

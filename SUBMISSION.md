# Lab 1 — Read Your Token Bill

**Course:** The End of Cheap Tokens — Module 01

**Measurement status:** All arithmetic and the actual-model baseline are documented below. Exercise 1 exact tokenizer counts will be inserted by the `measure.yml` workflow after its first run. No unmeasured numbers are presented as observed.

## Exercise 1 — Predict, then count

Five public training samples are checked into `samples/`. `count_tokens.py` uses `tiktoken/o200k_base` to produce observed counts and ratios into `results/token_counts.json`. The workflow generates the final five-row table and both short answers after measuring.

## Exercise 2 — Price three calls

| Call | Uncached input | Cache write | Cached input | Output | Real context | Total cost | Output share |
|---|---:|---:|---:|---:|---:|---:|---:|
| Call 1 | 12,400 | 0 | 0 | 1,850 | 12,400 | $0.04330 | 42.73% |
| Call 2 | 900 | 0 | 11,500 | 1,850 | 12,400 | $0.02260 | 81.86% |
| Call 3 | 900 | 11,500 | 0 | 1,850 | 12,400 | $0.04905 | 37.72% |

Provider inclusive-input normalization: (900, 0, 11,500, 1,850). Monthly savings for 10,000 calls at Call 2 rates instead of Call 1: **$207.00**.

## Exercise 3 — The loop tax

A 20-turn agent sends **445,000 input** and 8,000 output tokens, costing **$0.970**. A 30-turn agent sends **892,500 input** and 12,000 output, costing **$1.905**. Adding a 5,000-token file at turn one of 30 turns adds **150,000 input** tokens and **$0.30**. See the 30-row `loop_tax.csv` spreadsheet. Cheapest avoidance: retrieve the file on demand rather than retaining it on all future turns.

## Exercise 4 — Cost per completed task

For 1,000 tickets: Setup A has **$5.80** API spend, **202.5** expected human escalations, and **$410.80** total. Setup B has **$11.88** API spend, **6.4** expected escalations, and **$24.68** total. Cost per attempt hides the much larger human-handling expense.

## Exercise 5 — Actual model baseline

**Task:** Estimate remaining business days on synthetic invoice #4471 without tools.

**Turns:** 1.

**Context at end:** 68 observed input tokens.

**Largest context item:** Invoice question; no tools or documents.

**Usage:** 68 input tokens and 58 output tokens, as recorded by Ollama `qwen2.5:3b`.

**Course-sheet cost:** $0.000716, hypothetical only, not an actual provider bill.

**Completed to quality bar: NO.** The model did not fabricate a missing due date, but it could not calculate a supported numerical answer.

**Source:** https://github.com/kNightRunner/taller-academy-fde-day1-foundations/blob/main/results/experiments.json (`plain_call`).

## Run

```bash
python -m pip install -r requirements.txt
python count_tokens.py
python finalize_submission.py
python -m unittest discover -s tests -v
```

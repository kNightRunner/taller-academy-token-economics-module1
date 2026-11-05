# Lab 1 — Read Your Token Bill

**Course:** The End of Cheap Tokens — Module 01. All dollar amounts use the fixed course price sheet, NOT live provider prices.

## Exercise 1 — Predict, then count

The counts below are actual tokenizer executions using `tiktoken/o200k_base` on the checked-in raw files; they exclude chat framing. They are not the Anthropic or Gemini billable token counts.

| Content | Characters | Predicted (chars / 4) | Counted | Actual / predicted |
|---|---:|---:|---:|---:|
| One-line prompt | 43 | 11 | 13 | 1.18× |
| English prose | 397 | 100 | 79 | 0.79× |
| Spanish translation | 482 | 121 | 95 | 0.79× |
| Python source (~200 lines) | 8,688 | 2,172 | 1,853 | 0.85× |
| Comparable JSONL log | 8,499 | 2,125 | 2,592 | 1.22× |

**Largest underestimate:** Comparable JSONL log had the largest measured / predicted ratio.
**Spanish vs English:** 95 vs 79 tokens, a difference of **+16 tokens** (+20.3%).

## Exercise 2 — Price three calls

| Call | Uncached input | Cache write | Cached input | Output | Real context | Total cost | Output cost share |
|---|---:|---:|---:|---:|---:|---:|---:|
| Call 1 | 12,400 | 0 | 0 | 1,850 | 12,400 | $0.04330 | 42.73% |
| Call 2 | 900 | 0 | 11,500 | 1,850 | 12,400 | $0.02260 | 81.86% |
| Call 3 | 900 | 11,500 | 0 | 1,850 | 12,400 | $0.04905 | 37.72% |

**Normalized Call 2 (inclusive-provider reporting):** 12,400 total input − 11,500 cached = **900 uncached**, **0 cache write**, **11,500 cached**, **1,850 output**.
**10,000 calls / month:** ($0.04330 − $0.02260) × 10,000 = **$207.00 saved** using Call 2 instead of Call 1.

## Exercise 3 — The loop tax

System/tool prompt: 8,000 input tokens. Every subsequent turn adds 1,500 history tokens. Each turn produces 400 output tokens. No cache.

| Turns | Total input | Total output | Input cost | Output cost | Total cost |
|---:|---:|---:|---:|---:|---:|
| 20 | 445,000 | 8,000 | $0.890 | $0.080 | **$0.970** |
| 30 | 892,500 | 12,000 | $1.785 | $0.120 | **$1.905** |

| Turn | Input tokens | Accumulated input |
|---:|---:|---:|
| 1 | 8,000 | 8,000 |
| 2 | 9,500 | 17,500 |
| 3 | 11,000 | 28,500 |
| 4 | 12,500 | 41,000 |
| 5 | 14,000 | 55,000 |
| 6 | 15,500 | 70,500 |
| 7 | 17,000 | 87,500 |
| 8 | 18,500 | 106,000 |
| 9 | 20,000 | 126,000 |
| 10 | 21,500 | 147,500 |
| 11 | 23,000 | 170,500 |
| 12 | 24,500 | 195,000 |
| 13 | 26,000 | 221,000 |
| 14 | 27,500 | 248,500 |
| 15 | 29,000 | 277,500 |
| 16 | 30,500 | 308,000 |
| 17 | 32,000 | 340,000 |
| 18 | 33,500 | 373,500 |
| 19 | 35,000 | 408,500 |
| 20 | 36,500 | 445,000 |
| 21 | 38,000 | 483,000 |
| 22 | 39,500 | 522,500 |
| 23 | 41,000 | 563,500 |
| 24 | 42,500 | 606,000 |
| 25 | 44,000 | 650,000 |
| 26 | 45,500 | 695,500 |
| 27 | 47,000 | 742,500 |
| 28 | 48,500 | 791,000 |
| 29 | 50,000 | 841,000 |
| 30 | 51,500 | 892,500 |

**One 5,000-token file added at turn 1:** 30 repetitions × 5,000 = **150,000** extra input tokens. Extra cost = **$0.30**, changing the 30-turn cost from **$1.905** to **$2.205**.
**Cheapest avoidance:** Keep one-time files out of persistent history and retrieve only necessary excerpts on demand, then remove or compact them.

## Exercise 4 — Cost per completed task

Assume the second attempt has the same independent success probability. Expected human escalation fraction is (1 − p)². Fractional ticket counts are expectations.

| Setup | Attempts | API spend | Human escalations | Human costs | Total cost |
|---|---:|---:|---:|---:|---:|
| Small model A | 1,450.0 | $5.80 | 202.5 | $405.00 | **$410.80** |
| Large model B | 1,080.0 | $11.88 | 6.4 | $12.80 | **$24.68** |

**What cost per call hid:** The higher-priced model has dramatically fewer $2.00 human escalations and saves **$386.12** per 1,000 completed tickets.

## Exercise 5 — Real-task baseline (one measured model invocation)

**Task:** Determine how many business days remain before synthetic invoice #4471 becomes overdue, without tools.
**Model:** Ollama `qwen2.5:3b` on 2026-11-04T20:24:45.097651+00:00.
**Turns:** 1.
**Context at end:** 68 observed input tokens.
**Largest context item:** Invoice question; no documents or tools attached.
**Actual usage:** 68 uncached input + 0 cache write + 0 cached input + 58 output tokens.
**Illustrative cost:** $0.000716 at course rates; this is **not** an actual Ollama charge.
**Completed to quality bar: NO.** The answer identified missing due-date evidence without inventing it, but did not complete the numerical task.
**Quality bar:** Provide a defensible numerical business-day count based on verified invoice and calendar facts.

**Recorded model answer:**

> Without specific information about the due date for the invoice related to order #4471, it's impossible to determine how many business days are left until the invoice goes overdue. You would need to know the original due date provided by the supplier or the company that issued the invoice.

**Source:** [plain_call measured Ollama experiment](https://github.com/kNightRunner/taller-academy-fde-day1-foundations/blob/main/results/experiments.json).

## Reproduce and inspect

```bash
python -m pip install -r requirements.txt
python count_tokens.py
python finalize_submission.py
python -m unittest discover -s tests -v
```

See `results/token_counts.json` and `loop_tax.csv` for measured counts and the per-turn spreadsheet-compatible table. No private customer materials or secrets were used.

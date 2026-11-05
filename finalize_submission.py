"""Publish one self-contained, measured Lab 1 written submission."""
from pathlib import Path
import json
from calculations import price, loop, tickets
ROOT=Path(__file__).resolve().parent
def main():
    measured=ROOT/"results/token_counts.json"
    if not measured.exists(): raise SystemExit("Run python count_tokens.py first: measurement absent.")
    data=json.loads(measured.read_text(encoding="utf-8"))
    rows=data["rows"]
    if len(rows)!=5 or any(not isinstance(r["counted_tokens"],int) for r in rows):
        raise SystemExit("Incomplete tokenizer measurements.")
    baseline=json.loads((ROOT/"results/baseline_measured.json").read_text())
    lines=[
    "# Lab 1 — Read Your Token Bill","",
    "**Course:** The End of Cheap Tokens — Module 01. All dollar amounts use the fixed course price sheet, NOT live provider prices.","",
    "## Exercise 1 — Predict, then count","",
    "The counts below are actual tokenizer executions using `tiktoken/o200k_base` on the checked-in raw files; they exclude chat framing. They are not the Anthropic or Gemini billable token counts.","",
    "| Content | Characters | Predicted (chars / 4) | Counted | Actual / predicted |",
    "|---|---:|---:|---:|---:|"]
    for r in rows:lines.append(f'| {r["content"]} | {r["characters"]:,} | {r["predicted_tokens"]:,} | {r["counted_tokens"]:,} | {r["ratio_counted_predicted"]:.2f}× |')
    e,s=rows[1],rows[2]
    lines+=["",f'**Largest underestimate:** {data["questions"]["largest_underestimate"]} had the largest measured / predicted ratio.',
        f'**Spanish vs English:** {s["counted_tokens"]:,} vs {e["counted_tokens"]:,} tokens, a difference of **{s["counted_tokens"]-e["counted_tokens"]:+,} tokens** ({(s["counted_tokens"]/e["counted_tokens"]-1)*100:+.1f}%).',
        "","## Exercise 2 — Price three calls","",
        "| Call | Uncached input | Cache write | Cached input | Output | Real context | Total cost | Output cost share |",
        "|---|---:|---:|---:|---:|---:|---:|---:|"]
    for label,u,w,c,o in [("Call 1",12400,0,0,1850),("Call 2",900,0,11500,1850),("Call 3",900,11500,0,1850)]:
        total=price(u,w,c,o)
        lines.append(f"| {label} | {u:,} | {w:,} | {c:,} | {o:,} | {u+w+c:,} | ${total:.5f} | {1850*10/1e6/total:.2%} |")
    lines+=["","**Normalized Call 2 (inclusive-provider reporting):** 12,400 total input − 11,500 cached = **900 uncached**, **0 cache write**, **11,500 cached**, **1,850 output**.",
       f'**10,000 calls / month:** (${price(12400,0,0,1850):.5f} − ${price(900,0,11500,1850):.5f}) × 10,000 = **$207.00 saved** using Call 2 instead of Call 1.',
       "","## Exercise 3 — The loop tax","",
       "System/tool prompt: 8,000 input tokens. Every subsequent turn adds 1,500 history tokens. Each turn produces 400 output tokens. No cache.",
       "","| Turns | Total input | Total output | Input cost | Output cost | Total cost |",
       "|---:|---:|---:|---:|---:|---:|"]
    for n in (20,30):
        x=loop(n)
        lines.append(f'| {n} | {x["input"]:,} | {x["output"]:,} | ${x["input"]*2/1e6:.3f} | ${x["output"]*10/1e6:.3f} | **${x["total_usd"]:.3f}** |')
    lines+=["","| Turn | Input tokens | Accumulated input |","|---:|---:|---:|"]
    cumulative=0
    for n in range(1,31):
        inp=8000+1500*(n-1);cumulative+=inp
        lines.append(f"| {n} | {inp:,} | {cumulative:,} |")
    lines+=["","**One 5,000-token file added at turn 1:** 30 repetitions × 5,000 = **150,000** extra input tokens. Extra cost = **$0.30**, changing the 30-turn cost from **$1.905** to **$2.205**.",
      "**Cheapest avoidance:** Keep one-time files out of persistent history and retrieve only necessary excerpts on demand, then remove or compact them.",
      "","## Exercise 4 — Cost per completed task","",
      "Assume the second attempt has the same independent success probability. Expected human escalation fraction is (1 − p)². Fractional ticket counts are expectations.","",
      "| Setup | Attempts | API spend | Human escalations | Human costs | Total cost |",
      "|---|---:|---:|---:|---:|---:|"]
    a=tickets(0.004,0.55);b=tickets(0.011,0.92)
    for label,x in [("Small model A",a),("Large model B",b)]:
        lines.append(f'| {label} | {x["attempts"]:,.1f} | ${x["api_usd"]:.2f} | {x["human_tickets"]:.1f} | ${x["human_usd"]:.2f} | **${x["total_usd"]:.2f}** |')
    lines+=["","**What cost per call hid:** The higher-priced model has dramatically fewer $2.00 human escalations and saves **$386.12** per 1,000 completed tickets.",
      "","## Exercise 5 — Real-task baseline (one measured model invocation)","",
      f'**Task:** {baseline["task"]}',
      f'**Model:** {baseline["provider"]} `{baseline["model"]}` on {baseline["observed_utc"]}.',
      f'**Turns:** {baseline["turns"]}.',
      f'**Context at end:** {baseline["context_at_end_input_tokens"]} observed input tokens.',
      f'**Largest context item:** {baseline["biggest_context_item"]}',
      f'**Actual usage:** {baseline["total_uncached_input_tokens"]} uncached input + {baseline["total_cache_write_tokens"]} cache write + {baseline["total_cached_input_tokens"]} cached input + {baseline["total_output_tokens"]} output tokens.',
      f'**Illustrative cost:** ${baseline["course_sheet_illustrative_cost_usd"]:.6f} at course rates; this is **not** an actual Ollama charge.',
      '**Completed to quality bar: NO.** The answer identified missing due-date evidence without inventing it, but did not complete the numerical task.',
      f'**Quality bar:** {baseline["quality_bar"]}',"",
      "**Recorded model answer:**","","> "+baseline["actual_response"],"",
      f'**Source:** [{baseline["source_experiment"]} measured Ollama experiment]({baseline["source"]}).',
      "","## Reproduce and inspect","",
      "```bash","python -m pip install -r requirements.txt","python count_tokens.py","python finalize_submission.py","python -m unittest discover -s tests -v","```","",
      "See `results/token_counts.json` and `loop_tax.csv` for measured counts and the per-turn spreadsheet-compatible table. No private customer materials or secrets were used."]
    (ROOT/"SUBMISSION.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
    print("Created SUBMISSION.md from measured counts")
if __name__=="__main__":main()

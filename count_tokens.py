"""Measure five actual sample files with OpenAI o200k_base, not estimated API billing."""
import json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parent
SAMPLES=[("One-line prompt","samples/prompt.txt"),("English prose","samples/english_paragraph.txt"),("Spanish translation","samples/spanish_paragraph.txt"),("Python source (~200 lines)","samples/source_201_lines.py"),("Comparable JSONL log","samples/log_comparable_size.jsonl")]
def main():
    import tiktoken
    codec=tiktoken.get_encoding("o200k_base")
    rows=[]
    for label,name in SAMPLES:
        body=(ROOT/name).read_text(encoding="utf-8")
        predicted=math.ceil(len(body)/4)
        actual=len(codec.encode(body))
        rows.append(dict(content=label,file=name,characters=len(body),predicted_tokens=predicted,counted_tokens=actual,ratio_counted_predicted=round(actual/predicted,4)))
    questions=dict(largest_underestimate=max(rows,key=lambda row:row["ratio_counted_predicted"])["content"],spanish_minus_english=rows[2]["counted_tokens"]-rows[1]["counted_tokens"],spanish_vs_english_percent=round(100*(rows[2]["counted_tokens"]/rows[1]["counted_tokens"]-1),2))
    output={"tokenizer":"o200k_base","method":"tiktoken.encode(raw_text)","scope":"Content tokens only, excludes API message framing","rows":rows,"questions":questions}
    target=ROOT/"results/token_counts.json";target.parent.mkdir(exist_ok=True)
    target.write_text(json.dumps(output,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(output,indent=2,ensure_ascii=False))
if __name__=="__main__":main()

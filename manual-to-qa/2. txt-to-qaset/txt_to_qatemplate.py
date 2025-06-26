import json
from pathlib import Path
import os

input_txt_dir = Path("YOUR_TXT_PATH")
output_qa_dir = Path("YOUR_QaTemplate_PATH")
output_qa_dir.mkdir(parents=True, exist_ok=True)

category = "YOUR_CATEGORY"

def process_txt_file(txt_path: Path):
    product_name = "YOUR_PRODUCT_NAME"
    with open(txt_path, "r", encoding="utf-8") as f:
        raw_text = f.read()

    paragraphs = [p.strip() for p in raw_text.split("=== Page ===") if p.strip()]

    qa_dataset = []
    for para in paragraphs:
        qa_dataset.append({
            "question": "",
            "answer": "",
            "category": category,
            "product_name": product_name,
            "context": para
        })

    output_file = output_qa_dir / f"{txt_path.stem}_qa_template.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(qa_dataset, f, ensure_ascii=False, indent=4)
    print(f"저장 완료: {output_file}")

for txt_file in input_txt_dir.glob("*.txt"):
    process_txt_file(txt_file)

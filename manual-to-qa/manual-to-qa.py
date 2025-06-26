# unified_manual_to_qa_pipeline.py

import os
import json
import time
from pathlib import Path
import openai
from pypdf import PdfReader
import fitz
import pdfplumber
from pdf2image import convert_from_path
import pytesseract

### CONFIGURATION ###
INPUT_PDF_DIR = "YOUR_PDF_DIRECTORY"
OUTPUT_TXT_DIR = "YOUR_TXT_DIRECTORY"
OUTPUT_TEMPLATE_DIR = "YOUR_TEMPLATE_DIRECTORY"
OUTPUT_QA_DIR = "YOUR_QA_DIRECTORY"
TESSERACT_PATH = "YOUR_TESSERACT_EXE_PATH"
PDF_EXTRACTION_METHOD = "mupdf"  # one of ['mupdf', 'pypdf', 'pdfplumber', 'ocr']
CATEGORY = "YOUR_CATEGORY"
PRODUCT_NAME = "YOUR_PRODUCT_NAME"
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"

openai.api_key = OPENAI_API_KEY
pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

### PDF → TXT FUNCTIONS ###
def save_text_to_file(text, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)

def extract_text_from_pdf_mupdf(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = ""
    for page in doc:
        full_text += f"\n\n=== Page ===\n\n" + page.get_text()
    return full_text

def extract_text_from_pdf_pypdf(pdf_path):
    full_text = ""
    try:
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            full_text += f"\n\n=== Page ===\n\n"
            full_text += page.extract_text()
    except Exception as e:
        print(f"오류 발생: {e}")
    return full_text

def extract_text_from_pdf_pdfplumber(pdf_path):
    full_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            full_text += f"\n\n=== Page ===\n\n"
            full_text += page.extract_text()
    return full_text

def extract_text_from_pdf_ocr(pdf_path, lang='kor+eng', dpi=300):
    images = convert_from_path(pdf_path, dpi=dpi)
    full_text = ""
    for img in images:
        text = pytesseract.image_to_string(img, lang=lang, config='--psm 6')
        full_text += f"\n\n=== Page ===\n\n" + text
    return full_text

def process_pdfs_to_txt():
    Path(OUTPUT_TXT_DIR).mkdir(parents=True, exist_ok=True)
    for root, _, files in os.walk(INPUT_PDF_DIR):
        for file in files:
            if file.lower().endswith(".pdf"):
                pdf_path = os.path.join(root, file)
                if PDF_EXTRACTION_METHOD == 'mupdf':
                    text = extract_text_from_pdf_mupdf(pdf_path)
                    suffix = "_MuPDF.txt"
                elif PDF_EXTRACTION_METHOD == 'pypdf':
                    text = extract_text_from_pdf_pypdf(pdf_path)
                    suffix = "_pypdf.txt"
                elif PDF_EXTRACTION_METHOD == 'pdfplumber':
                    text = extract_text_from_pdf_pdfplumber(pdf_path)
                    suffix = "_pdfplumber.txt"
                elif PDF_EXTRACTION_METHOD == 'ocr':
                    text = extract_text_from_pdf_ocr(pdf_path)
                    suffix = "_pytesseract.txt"
                else:
                    raise ValueError("Invalid extraction method")

                relative_path = os.path.relpath(pdf_path, INPUT_PDF_DIR)
                txt_filename = os.path.splitext(relative_path)[0] + suffix
                output_path = os.path.join(OUTPUT_TXT_DIR, txt_filename)
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                save_text_to_file(text, output_path)
                print(f"TXT 저장 완료: {output_path}")

### TXT → QA TEMPLATE ###
def generate_templates():
    Path(OUTPUT_TEMPLATE_DIR).mkdir(parents=True, exist_ok=True)
    for txt_path in Path(OUTPUT_TXT_DIR).glob("*.txt"):
        with open(txt_path, "r", encoding="utf-8") as f:
            raw_text = f.read()

        paragraphs = [p.strip() for p in raw_text.split("=== Page ===") if p.strip()]
        qa_dataset = [{
            "question": "",
            "answer": "",
            "category": CATEGORY,
            "product_name": PRODUCT_NAME,
            "context": para
        } for para in paragraphs]

        out_path = Path(OUTPUT_TEMPLATE_DIR) / f"{txt_path.stem}_qa_template.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(qa_dataset, f, ensure_ascii=False, indent=4)
        print(f"QA 템플릿 저장 완료: {out_path}")

### TEMPLATE → FINAL QA SET ###
def build_prompt(context):
    return f"""아래는 자동차 매뉴얼의 일부입니다. 이 내용을 바탕으로 사용자가 실제로 궁금해할 만한 질문과 그에 대한 답변을 2개 생성해 주세요.

[매뉴얼 발췌 내용]
{context}

아래 JSON 형식으로 출력해 주세요:

[
  {{
    \"question\": \"사용자 질문 1\",
    \"answer\": \"질문에 대한 명확한 답변 1\"
  }},
  {{
    \"question\": \"사용자 질문 2\",
    \"answer\": \"질문에 대한 명확한 답변 2\"
  }}
]"""

def generate_final_qa():
    Path(OUTPUT_QA_DIR).mkdir(parents=True, exist_ok=True)
    for template_path in Path(OUTPUT_TEMPLATE_DIR).glob("*.json"):
        output_path = Path(OUTPUT_QA_DIR) / f"{template_path.stem}.jsonl"
        with open(template_path, "r", encoding="utf-8") as f:
            template = json.load(f)

        with open(output_path, "w", encoding="utf-8") as f_out:
            for idx, entry in enumerate(template):
                print(f"  🔹 chunk_index {idx}")
                try:
                    messages = [
                        {"role": "system", "content": "당신은 제품 매뉴얼을 분석해 QA를 생성하는 전문가입니다."},
                        {"role": "user", "content": build_prompt(entry["context"])}
                    ]
                    response = openai.ChatCompletion.create(
                        model="gpt-4",
                        messages=messages,
                        temperature=0.7
                    )
                    content = response.choices[0].message.content
                    qas = json.loads(content)
                except Exception as e:
                    print(f"[오류] GPT 응답 실패: {e}")
                    qas = []

                record = {
                    "product_name": PRODUCT_NAME,
                    "chunk_index": idx,
                    "qas": qas
                }
                f_out.write(json.dumps(record, ensure_ascii=False) + "\n")
                time.sleep(1.1)

        print(f"QA 결과 저장 완료: {output_path}")

### MAIN ENTRY POINT ###
if __name__ == "__main__":
    process_pdfs_to_txt()
    generate_templates()
    generate_final_qa()

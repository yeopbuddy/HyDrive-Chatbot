# pip install pymupdf
import fitz  # PyMuPDF
import os

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = ""

    for page in doc:
        full_text += f"\n\n=== Page ===\n\n"  # 페이지 구분자 추가 : 추후 context 구분을 위함
        full_text += page.get_text()
    
    return full_text

def save_text_to_file(text, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)

def process_all_pdfs(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith(".pdf"):
                pdf_path = os.path.join(root, file)
                text = extract_text_from_pdf(pdf_path)

                relative_path = os.path.relpath(pdf_path, input_dir)
                txt_filename = os.path.splitext(relative_path)[0] + "_MuPDF.txt"
                output_path = os.path.join(output_dir, txt_filename)

                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                save_text_to_file(text, output_path)
                print(f"저장 완료: {output_path}")

input_folder = "YOUR_INPUT_PATH"
output_folder = "YOUR_OUTPUT_PATH"

process_all_pdfs(input_folder, output_folder)
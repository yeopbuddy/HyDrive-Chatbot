# pip install pypdf
import os
from pypdf import PdfReader

def extract_text_pypdf(pdf_path):
    full_text = ""
    try:
        reader = PdfReader(pdf_path)
        num_pages = len(reader.pages)

        for i in range(num_pages):
            page = reader.pages[i] 
            text = page.extract_text() 
            full_text += f"\n\n=== Page ===\n\n"  # 페이지 구분자 추가 : 추후 context 구분을 위함
    except Exception as e:
        print(f"오류 발생 ({pdf_path}): {e}")
        full_text += f"\n\n=== 텍스트 추출 오류 ===\n\n" 

    return full_text

def save_text_to_file(text, output_path):
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"저장 완료: {output_path}")
    except Exception as e:
        print(f"텍스트 파일 저장 중 오류 발생 ({output_path}): {e}")

def process_all_pdfs(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith(".pdf"):
                pdf_path = os.path.join(root, file)
                text = extract_text_pypdf(pdf_path)
                relative_path = os.path.relpath(pdf_path, input_dir)
                txt_filename = os.path.splitext(relative_path)[0] + "_pypdf.txt"
                output_path = os.path.join(output_dir, txt_filename)
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                save_text_to_file(text, output_path)
                print(f"저장 완료: {output_path}")

input_folder = "YOUR_INPUT_PATH"
output_folder = "YOUR_OUTPUT_PATH"

process_all_pdfs(input_folder, output_folder)

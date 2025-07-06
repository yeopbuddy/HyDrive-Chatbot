# pip install pdf2image pytesseract pillow
# window : download tesseract-OCR AT "https://github.com/UB-Mannheim/tesseract/wiki" and set Individual Path(Line 9)

from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import os

pytesseract.pytesseract.tesseract_cmd = r'YOUR_tesseract.exe_PATH'

def ocr_pdf_to_text(pdf_path, lang='kor+eng', dpi=300):
    images = convert_from_path(pdf_path, dpi=dpi)

    all_text = ""
    for i, img in enumerate(images):
        text = pytesseract.image_to_string(img, lang=lang, config='--psm 6')
        full_text += f"\n\n=== Page ===\n\n"  # 페이지 구분자 추가 : 추후 context 구분을 위함

    return all_text

def process_all_pdfs(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith(".pdf"):
                pdf_path = os.path.join(root, file)
                text = ocr_pdf_to_text(pdf_path)

                relative_path = os.path.relpath(pdf_path, input_dir)
                txt_filename = os.path.splitext(relative_path)[0] + "_pytesseract.txt"
                output_path = os.path.join(output_dir, txt_filename)

                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                save_text_to_file(text, output_path)
                print(f"저장 완료: {output_path}")

input_folder = "YOUR_INPUT_PATH"
output_folder = "YOUR_OUTPUT_PATH"

process_all_pdfs(input_folder, output_folder)

# 📰 pdf-to-txt

PDF 문서로부터 텍스트를 추출하는 코드입니다.  
**MuPDF, pdfplumber, PyPDF2, Tesseract OCR** 4가지 엔진 기반의 추출입니다.

---

## 🔧 지원 추출 방식

| 추출 방식         | 설명 |
|------------------|------|
| **MuPDF**        | 가장 정확한 레이아웃 기반 텍스트 추출. 좌표 기반 정렬 가능. (`PyMuPDF`) |
| **pdfplumber**   | 표, 정렬 등 레이아웃 분석이 뛰어난 방식. 글자 위치 정보까지 접근 가능. |
| **PyPDF2**       | 빠르고 가벼운 방식이지만 일부 레이아웃 손실 가능성 있음. |
| **Tesseract OCR**| 스캔된 이미지 PDF에 적합. OCR로 이미지에서 텍스트 추출. |


## 💡 의존 라이브러리 설치

코드 상단의 주석 처리된 pip install 실행이 필요합니다.

Tesseract OCR은 별도 설치가 필요합니다.  
설치 방법: [https://github.com/tesseract-ocr/tesseract](https://github.com/tesseract-ocr/tesseract)

---

## 📌 참고

- **MuPDF**는 `.get_text()`에 `sort=True` 또는 좌표 기반으로 정렬 가능
- **pdfplumber**는 표 형식 추출에 유리
- **OCR** 방식은 스캔 문서 및 이미지 PDF에 반드시 필요

---
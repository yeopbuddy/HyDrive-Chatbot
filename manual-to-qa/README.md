# 📚 manual-to-qa

제품 매뉴얼 PDF 파일을 입력하면, 이를 기반으로 **사용자 맞춤형 QA 데이터셋**을 자동 생성하는 end-to-end 파이프라인입니다.  
PDF → 텍스트 추출 → QA 템플릿 생성 → GPT 기반 QA 생성까지 모두 포함합니다.

---

## 🛠 구성 레포 및 모듈

### 1️⃣ `pdf-to-txt/`
PDF 문서를 텍스트(.txt)로 변환합니다.  
다양한 방식으로 텍스트를 추출할 수 있습니다:

- `PyMuPDF`
- `pdfplumber`
- `PyPDF2`
- `OCR (Tesseract)`

📂 출력 경로: `./txts/*.txt`

---

### 2️⃣ `txt-to-qaset/`
텍스트 문서를 기반으로 QA 데이터셋을 생성합니다.

#### 🔹 `txt_to_qatemplate.py`
- 페이지 또는 문단 단위로 context를 나누어 QA 템플릿(JSON)을 생성합니다.
- 📂 출력 경로: `./qaraw/*.json`

#### 🔹 `qatemplate-to-qaset.py`
- OpenAI GPT API를 호출하여 질문-답변 쌍을 생성합니다.
- 포맷: `{ "product_name", "chunk_index", "qas": [ {question, answer}, ... ] }`
- 📂 출력 경로: `./qaset/*.jsonl` or `./qaset/*.json`

---

## 🧬 파이프라인 흐름

```
📄 PDF
  ↓
📜 txts/     ← pdf-to-txt
  ↓
🧩 qaraw/    ← txt_to_qatemplate.py
  ↓
📦 qaset/    ← qatemplate-to-qaset.py
```

---

## 📌 설치

- OCR 사용 시 Tesseract 설치 필요
- GPT 사용을 위한 OpenAI API 키 필요

---

## 💡 활용 예시

이 데이터셋은 다음과 같은 분야에 사용 가능합니다:

- RAG 기반 챗봇 학습
- 고객 서비스 QA 시스템
- 제품 사용법 질의응답
- 사용자 설명서 요약

👨‍💻 Maintained by @yeopbuddy
문의: [kjohn0714@ajou.ac.kr] / GitHub Issue
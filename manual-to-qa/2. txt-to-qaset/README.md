# 🤖 txt-to-qaset

PDF로부터 추출된 텍스트(txt)를 기반으로 **제품 매뉴얼 QA 데이터셋**을 자동 생성하는 파이프라인입니다.  
GPT API를 활용하여 사용자의 질문-답변 쌍을 생성하며, 챗봇 학습이나 RAG 시스템에 활용할 수 있습니다.

---

## 📁 구성 파일

| 파일명 | 설명 |
|--------|------|
| `txt_to_qatemplate.py` | txt 파일을 페이지/문단 단위로 분할하여 QA 템플릿(JSON) 생성 |
| `qatemplate-to-qaset.py` | 템플릿(JSON)을 바탕으로 GPT API 호출하여 최종 QA 세트 생성 |

---

## 🧩 사용 흐름

1. **PDF → TXT 변환**: (다른 레포 `1. pdf-to-txt` 사용)
2. **TXT → QA 템플릿 생성**  
   → `qaraw/` 폴더에 각 페이지/문단별 context 기반 템플릿 생성

3. **QA 템플릿 → GPT 기반 QA 세트 생성**  
   → `qaset/` 폴더에 chunk별 `{"product_name", "chunk_index", "qas": [...]}` 포맷으로 저장

---

## 📦 예시 출력 포맷

```json
{
  "product_name": "Owner's Manual Poter2",
  "chunk_index": 0,
  "qas": [
    {
      "question": "겨울 모드에서 난방은 어떻게 작동하나요?",
      "answer": "겨울 모드에서는 유닛이 난방을 수행하며 냉각 모드는 비활성화됩니다."
    },
    {
      "question": "여름 모드일 때는 냉방만 가능한가요?",
      "answer": "예, 여름 모드에서는 냉방만 가능하며 난방은 중단됩니다."
    }
  ]
}
```

---

## 💡 주의사항

- OpenAI GPT API 키 필요
- OpenAI SDK 버전은 0.28 기준 (`pip install openai==0.28`)
- 초당 호출 제한을 피하기 위해 `time.sleep()` 포함됨

---
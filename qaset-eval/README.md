### 🧠 qaset-eval

**QA Set 자동 평가 도구 목록**
LLM 기반 QA 데이터셋(`.jsonl`)을 자동으로 평가하고, 정량/정성 기준에 따라 평가 결과를 저장합니다.
OpenAI GPT API와 [`DeepEval`](https://github.com/confident-ai/deepeval) 기반 평가 두 가지 방식을 모두 지원합니다.

---

## 📁 프로젝트 구성

```
qaset-eval/
├── gpt_relevancy_eval.py         # GPT API 기반 정성 평가
├── deepeval_metrics_eval.py      # DeepEval 기반 정량 평가
```

---

## 🔍 평가 방식

### ✅ 1. DeepEval 기반 평가 (`deepeval_metrics_eval.py`)

* **샘플링 방식**: `type + category` 기준 다중 기준 층화 샘플링 (총 300개 샘플)
* **사용 메트릭**:

  * `Answer Relevancy` (답변의 적절성)
  * `Toxicity` (유해성)
* **모델**: `gpt-4o-mini`

📀 *입력 조건*:

* 입력 `.jsonl` 파일은 다음 필드를 가지고 있어야 합니다:
  `question`, `answer`, `type`, `category`

📄 *출력*: `filename_eval_result.json` (JSON)

---

### ✅ 2. GPT 기반 평가 (`gpt_relevancy_eval.py`)

* **평가 항목**: 사용자가 궁금한 질문에 대한 답변이 적절한지 GPT-4o가 평가
* **응답 포맷**:

  ```json
  {
    "relevancy_result": "관련성: 매우 적절함\n이유: ..."
  }
  ```

📀 *입력 조건*:

* 입력 `.jsonl` 파일은 다음 필드를 가지고 있어야 합니다:
  `question`, `answer` (선택적으로 `qa_id`)

📄 *출력*: 동일한 이름의 `.jsonl` 파일에 평가 결과 추가

---

## 📌 주의사항

* OpenAI API 사용 시 요금이 발생할 수 있습니다.
* 평가 결과는 주관적일 수 있으며, 학습/운영 목적에 따라 threshold 조정이 필요합니다.
* DeepEval은 최소 300개의 샘플 수량이 필요합니다.

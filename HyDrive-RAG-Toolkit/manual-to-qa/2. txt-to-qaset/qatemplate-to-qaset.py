# pip install openai==0.28
import openai
import json
import time
from pathlib import Path

openai.api_key = "YOUR_OPENAI_API_KEY" 

# 경로 설정
template_dir = Path("YOUR_TEMPLATE_PATH")
output_dir = Path("YOUR_OUTPUT_PATH")
output_dir.mkdir(exist_ok=True)

# 프롬프트 생성 함수
def build_prompt(context):
    # OR YOUR CUSTOM COMMAND
    return f"""아래는 자동차 매뉴얼의 일부입니다. 이 내용을 바탕으로 사용자가 실제로 궁금해할 만한 질문과 그에 대한 답변을 2개 생성해 주세요.

[매뉴얼 발췌 내용]
{context}

아래 JSON 형식으로 출력해 주세요:

[
  {{
    "question": "사용자 질문 1",
    "answer": "질문에 대한 명확한 답변 1"
  }},
  {{
    "question": "사용자 질문 2",
    "answer": "질문에 대한 명확한 답변 2"
  }}
]

조건:
- 서로 다른 주제를 다루는 질문이어야 합니다.
- 질문은 실제 매뉴얼 독자가 가질 법한 것으로 작성해 주세요.
- 질문이 없다고 판단 될 경우, 해당 context를 pass할 수 있습니다.
"""

def generate_qa(context): # GPT API 기반
    try:
        messages = [
            {"role": "system", "content": "당신은 제품 매뉴얼을 분석해 QA를 생성하는 전문가입니다."}, # OR YOUR CUSTOM MESSAGES
            {"role": "user", "content": build_prompt(context)}
        ]
        response = openai.ChatCompletion.create( # OR YOUR CUSTOM RESPONSE OPTION
            model="gpt-4",
            messages=messages,
            temperature=0.7
        )
        content = response.choices[0].message.content
        return json.loads(content)
    except Exception as e:
        print(f"[오류] GPT 응답 실패: {e}")
        return []

for template_path in template_dir.glob("*.json"):
    product_name = "YOUR_PRODUCT_NAME"
    output_path = output_dir / f"{template_path.stem}.jsonl"

    print(f"\n처리 시작: {template_path.name}")
    with open(template_path, "r", encoding="utf-8") as f:
        template = json.load(f)

    with open(output_path, "w", encoding="utf-8") as f_out:
        for idx, entry in enumerate(template):
            print(f"  🔹 chunk_index {idx}")
            qas = generate_qa(entry["context"])
            record = {
                "product_name": product_name,
                "chunk_index": idx,
                "qas": qas
            }
            f_out.write(json.dumps(record, ensure_ascii=False) + "\n")
            time.sleep(1.1)  # Rate limit 대비

    print(f"저장 완료: {output_path}")

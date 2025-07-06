
import json
from tqdm import tqdm
from pathlib import Path
from openai import OpenAI

client = OpenAI(api_key="YOUR_API_KEY")

def evaluate_relevancy(question, answer):
    prompt = f"""다음은 고객 질문과 이에 대한 답변입니다.

[질문]
{question}

[답변]
{answer}

이 답변이 질문에 적절하게 응답하고 있나요?
- 매우 적절함 / 부분적으로 적절함 / 관련 없음 중 선택하고
- 간단한 이유도 함께 제시해 주세요.

형식:
관련성: (매우 적절함 / 부분적으로 적절함 / 관련 없음)
이유: ...
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )
    return response.choices[0].message.content

input_dir = Path("YOUR_INPUT_DIR")
output_dir = Path("YOUR_OUTPUT_DIR")
output_dir.mkdir(parents=True, exist_ok=True)

for input_file in input_dir.glob("*.jsonl"):
    output_file = output_dir / input_file.name
    results = []

    with open(input_file, "r", encoding="utf-8") as f:
        for line in tqdm(f, desc=f"평가 중: {input_file.name}"):
            item = json.loads(line)
            result = evaluate_relevancy(item["question"], item["answer"])
            results.append({
                "qa_id": item.get("qa_id", None),
                "question": item["question"],
                "answer": item["answer"],
                "relevancy_result": result
            })

    with open(output_file, "w", encoding="utf-8") as f:
        for row in results:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(f"완료: {output_file}")
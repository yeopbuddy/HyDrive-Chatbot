import json
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from deepeval.test_case import LLMTestCase
from deepeval.dataset import EvaluationDataset
from deepeval.metrics import AnswerRelevancyMetric, ToxicityMetric
from deepeval import evaluate
from tqdm import tqdm

input_dir = Path("YOUR_INPUT_DIR") # 경로 설정
output_dir = Path("YOUR_OUTPUT_DIR")
output_dir.mkdir(parents=True, exist_ok=True)

relevancy_metric = AnswerRelevancyMetric(threshold=0.5, model="gpt-4o-mini") # 메트릭 설정
toxicity_metric = ToxicityMetric(threshold=0.5, model="gpt-4o-mini")

for input_file in input_dir.glob("*.jsonl"):
    print(f"평가 시작: {input_file.name}")

    with open(input_file, "r", encoding="utf-8") as f:
        data = [json.loads(line.strip()) for line in f]

    if len(data) < 300:
        print(f"샘플 수 부족: {len(data)}개 (300 미만)")
        continue

    df = pd.DataFrame(data)

    if "type" not in df.columns or "category" not in df.columns:
        print(f"필요한 열(type/category)이 누락됨. 건너뜀: {input_file.name}")
        continue

    df["stratum"] = df["type"] + "_" + df["category"] # 다중 기준 층화 샘플링
    sample_df, _ = train_test_split(
        df,
        test_size=len(df) - 300,
        stratify=df["stratum"],
        random_state=42
    )

    
    dataset = EvaluationDataset() # 평가셋 구성
    for _, row in sample_df.iterrows():
        dataset.add_test_case(
            LLMTestCase(
                input=row["question"],
                actual_output=row["answer"]
            )
        )

    results = evaluate(dataset, [relevancy_metric, toxicity_metric])

    output_path = output_dir / f"{input_file.stem}_eval_result.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results.to_dict(), f, ensure_ascii=False, indent=2)

    print(f"저장 완료: {output_path}")

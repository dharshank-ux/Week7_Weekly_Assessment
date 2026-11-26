import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RESULTS_FILE = ROOT / "Task4" / "evaluation_results.json"
OUTPUT_FILE = ROOT / "Task4" / "local_metrics.json"


def evaluate():
    with open(RESULTS_FILE, "r", encoding="utf-8") as file:
        results = json.load(file)

    total = len(results)
    faithfulness_checks = 0
    faithfulness_pass = 0
    answer_relevance_checks = 0
    answer_relevance_pass = 0
    context_precision_pass = 0
    context_recall_pass = 0

    for item in results:
        question = item["question"].lower()
        answer = item["answer"].lower()
        expected = item["expected_answer"].lower()
        sources = item.get("retrieved_sources", [])

        refused = "i don't have information" in answer

        if item["type"] == "unanswerable":
            faithfulness_checks += 1
            answer_relevance_checks += 1

            if refused:
                faithfulness_pass += 1
                answer_relevance_pass += 1

            context_precision_pass += 1 if sources else 0
            context_recall_pass += 1 if refused else 0
            continue

        faithfulness_checks += 1
        answer_relevance_checks += 1

        expected_terms = [
            word for word in expected.split()
            if len(word) > 2
        ]

        matched_terms = sum(
            1 for word in expected_terms if word in answer
        )

        if expected_terms and matched_terms / len(expected_terms) >= 0.5:
            faithfulness_pass += 1
            answer_relevance_pass += 1

        if item.get("source_match") and sources:
            context_precision_pass += 1
            context_recall_pass += 1

    metrics = {
        "evaluation_type": "Local heuristic evaluation - not official RAGAS",
        "total_questions": total,
        "faithfulness_proxy": round(
            faithfulness_pass / faithfulness_checks, 3
        ) if faithfulness_checks else 0,
        "answer_relevancy_proxy": round(
            answer_relevance_pass / answer_relevance_checks, 3
        ) if answer_relevance_checks else 0,
        "context_precision_proxy": round(
            context_precision_pass / total, 3
        ) if total else 0,
        "context_recall_proxy": round(
            context_recall_pass / total, 3
        ) if total else 0
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(metrics, file, indent=4)

    print("\n========== LOCAL EVALUATION METRICS ==========")

    for key, value in metrics.items():
        print(f"{key}: {value}")

    print("\nSaved to:", OUTPUT_FILE)


if __name__ == "__main__":
    evaluate()
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from Task1.src.rag import answer, retrieve

DATASET_PATH = ROOT / "Task4" / "data" / "golden.jsonl"


def load_dataset():
    with open(DATASET_PATH, "r", encoding="utf-8") as file:
        return [json.loads(line) for line in file if line.strip()]


def get_source(chunk):
    # Qdrant ScoredPoint stores metadata inside payload
    payload = getattr(chunk, "payload", None)

    if payload is None and isinstance(chunk, dict):
        payload = chunk.get("payload", chunk)

    if not isinstance(payload, dict):
        return ""

    return payload.get("source", "")


def is_refusal(response):
    text = str(response).lower()

    refusal_phrases = [
        "i don't have information",
        "i do not have information",
        "i don't know",
        "i do not know"
    ]

    return any(phrase in text for phrase in refusal_phrases)


def evaluate():
    dataset = load_dataset()

    total = len(dataset)
    answered = 0
    correct_sources = 0
    results = []

    print("\n========== RAG EVALUATION ==========\n")

    for item in dataset:
        question = item["question"]

        try:
            response = answer(question, k=4)
            chunks = retrieve(question, k=4)

            response_text = str(response)
            refusal = is_refusal(response_text)

            if not refusal:
                answered += 1

            retrieved_sources = {
                get_source(chunk)
                for chunk in chunks
                if get_source(chunk)
            }

            expected_sources = set(item["expected_sources"])

            if item["type"] == "unanswerable":
                source_match = refusal
            else:
                source_match = bool(
                    expected_sources.intersection(retrieved_sources)
                )

            if source_match:
                correct_sources += 1

            result = {
                "id": item["id"],
                "type": item["type"],
                "question": question,
                "answer": response_text,
                "expected_answer": item["expected_answer"],
                "retrieved_sources": list(retrieved_sources),
                "source_match": source_match,
                "refused": refusal
            }

            results.append(result)

            print(f"Question {item['id']}: {question}")
            print("Answer:", response_text)
            print("Retrieved sources:", retrieved_sources)
            print("Expected source match:", source_match)
            print("-" * 60)

        except Exception as error:
            print(f"Question {item['id']} failed: {error}")

    completed = len(results)

    print("\n========== EVALUATION SUMMARY ==========")
    print("Total questions:", total)
    print("Completed questions:", completed)
    print("Answered questions:", answered)
    print("Source matches:", correct_sources)

    if total:
        print(
            "Source Hit Rate:",
            round(correct_sources / total * 100, 2),
            "%"
        )

    output_path = ROOT / "Task4" / "evaluation_results.json"

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(results, file, indent=4, ensure_ascii=False)

    print("\nResults saved to:", output_path)


if __name__ == "__main__":
    evaluate()
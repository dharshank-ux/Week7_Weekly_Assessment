import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "Task4" / "evaluation_results.json"


def normalize_tokens(text):
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def is_answer_correct(expected, actual):
    expected_tokens = normalize_tokens(expected)
    actual_tokens = normalize_tokens(actual)

    if not expected_tokens:
        return True

    matched_tokens = expected_tokens.intersection(actual_tokens)

    coverage = len(matched_tokens) / len(expected_tokens)

    return coverage >= 0.80


def main():
    with open(RESULTS, "r", encoding="utf-8") as file:
        data = json.load(file)

    failures = []

    for item in data:
        if item["type"] == "unanswerable":
            continue

        expected = item["expected_answer"]
        actual = item["answer"]

        if not is_answer_correct(expected, actual):
            failures.append({
                "question": item["question"],
                "answer": actual,
                "expected": expected,
                "sources": item["retrieved_sources"]
            })

    print("========== FAILURE ANALYSIS ==========")

    print(f"\nTotal questions checked: {len(data)}")
    print(f"Potential failures: {len(failures)}")

    if failures:
        for index, failure in enumerate(failures, 1):
            print(f"\nFailure {index}")
            print("Question:", failure["question"])
            print("Expected:", failure["expected"])
            print("Actual:", failure["answer"])
            print("Sources:", failure["sources"])
    else:
        print("\nNo obvious failures found by the keyword coverage check.")

    print("\nNote: This is a simple local keyword check.")
    print("Manual review is still required.")


if __name__ == "__main__":
    main()
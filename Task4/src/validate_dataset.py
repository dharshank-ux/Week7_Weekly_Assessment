import json
from pathlib import Path

DATASET_PATH = Path(__file__).parent.parent / "data" / "golden.jsonl"

def load_dataset():
    records = []

    with open(DATASET_PATH, "r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            if line.strip():
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError as error:
                    print(f"Invalid JSON at line {line_number}: {error}")
                    return []

    return records


def main():
    dataset = load_dataset()

    simple = sum(item["type"] == "simple" for item in dataset)
    multi = sum(item["type"] == "multi_chunk" for item in dataset)
    unanswerable = sum(item["type"] == "unanswerable" for item in dataset)

    print("GOLDEN DATASET VALIDATION")
    print("=========================")
    print("Total questions:", len(dataset))
    print("Simple questions:", simple)
    print("Multi-chunk questions:", multi)
    print("Unanswerable questions:", unanswerable)

    if len(dataset) == 15 and simple == 8 and multi == 4 and unanswerable == 3:
        print("\nDataset validation PASSED!")
    else:
        print("\nDataset validation FAILED!")


if __name__ == "__main__":
    main()
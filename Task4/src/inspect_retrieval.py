import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from Task1.src.rag import retrieve

questions = [
    "How many casual leaves are available per year?",
    "What is the monthly salary of a software developer at ABC Technologies?"
]

for question in questions:
    print("\nQUESTION:", question)
    print("=" * 60)

    chunks = retrieve(question, k=4)

    for chunk in chunks:
        payload = chunk.payload or {}

        print("Score:", getattr(chunk, "score", "N/A"))
        print("Source:", payload.get("source", "Unknown"))
        print("Text:", payload.get("text", ""))
        print("-" * 40)
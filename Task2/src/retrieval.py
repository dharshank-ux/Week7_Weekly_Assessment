import re
from pathlib import Path

from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient

BASE_DIR = Path(__file__).resolve().parents[2]
DB_DIR = BASE_DIR / "Task1" / "qdrant_db"

COLLECTION_NAME = "company_policies"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

print("Loading retrieval components...")

model = SentenceTransformer(MODEL_NAME)
client = QdrantClient(path=str(DB_DIR))


def tokenize(text):
    return re.findall(r"\b\w+\b", text.lower())


def load_chunks():
    points, _ = client.scroll(
        collection_name=COLLECTION_NAME,
        limit=1000,
        with_payload=True,
        with_vectors=False
    )

    return [
        point for point in points
        if point.payload and point.payload.get("text")
    ]


chunks = load_chunks()

if not chunks:
    raise RuntimeError("No indexed chunks found. Run Task 1 ingestion first.")

corpus = [
    tokenize(point.payload["text"])
    for point in chunks
]

bm25 = BM25Okapi(corpus)


def bm25_search(question, limit=50):
    scores = bm25.get_scores(tokenize(question))

    ranked_indices = sorted(
        range(len(scores)),
        key=lambda i: scores[i],
        reverse=True
    )

    return [chunks[i] for i in ranked_indices[:limit]]


def vector_search(question, limit=50):
    vector = model.encode(question).tolist()

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=vector,
        limit=limit,
        with_payload=True
    ).points

    return results


def reciprocal_rank_fusion(*ranked_lists, k=60):
    scores = {}

    for ranked_list in ranked_lists:
        for rank, point in enumerate(ranked_list, start=1):
            point_id = str(point.id)

            scores[point_id] = (
                scores.get(point_id, 0)
                + 1 / (k + rank)
            )

    point_map = {
        str(point.id): point
        for point in chunks
    }

    ranked_ids = sorted(
        scores,
        key=lambda point_id: scores[point_id],
        reverse=True
    )

    return [
        point_map[point_id]
        for point_id in ranked_ids
        if point_id in point_map
    ]


def hit_at_3(results, expected_source):
    return any(
        point.payload.get("source") == expected_source
        for point in results[:3]
    )


questions = [
    # 6 exact-term questions
    ("exact", "How many casual leaves per year?", "leave_policy.txt"),
    ("exact", "How many sick leaves are available?", "leave_policy.txt"),
    ("exact", "How many earned leaves are available?", "leave_policy.txt"),
    ("exact", "What are the working hours?", "attendance_policy.txt"),
    ("exact", "When is salary paid?", "salary_policy.txt"),
    ("exact", "What is the expense reimbursement policy?", "expense_policy.txt"),

    # 6 meaning-based questions
    ("meaning", "How many days off can staff take for personal reasons?", "leave_policy.txt"),
    ("meaning", "What time off is available when an employee is ill?", "leave_policy.txt"),
    ("meaning", "What is the normal weekday work schedule?", "attendance_policy.txt"),
    ("meaning", "Can staff perform their duties from home?", "work_from_home.txt"),
    ("meaning", "How can workers get back money spent on company business?", "expense_policy.txt"),
    ("meaning", "How should employees keep private company information safe?", "security_policy.txt"),
]


def evaluate():
    bm25_hits = 0
    vector_hits = 0
    hybrid_hits = 0

    exact_results = []
    meaning_results = []

    print("\n========== RETRIEVAL EVALUATION ==========")

    for category, question, expected in questions:
        bm25_results = bm25_search(question)
        vector_results = vector_search(question)

        hybrid_results = reciprocal_rank_fusion(
            bm25_results,
            vector_results
        )

        b_hit = hit_at_3(bm25_results, expected)
        v_hit = hit_at_3(vector_results, expected)
        h_hit = hit_at_3(hybrid_results, expected)

        bm25_hits += int(b_hit)
        vector_hits += int(v_hit)
        hybrid_hits += int(h_hit)

        result = (b_hit, v_hit, h_hit)

        if category == "exact":
            exact_results.append(result)
        else:
            meaning_results.append(result)

        print(f"\nQuestion: {question}")
        print(f"Expected source: {expected}")
        print(f"BM25 Hit@3: {b_hit}")
        print(f"Vector Hit@3: {v_hit}")
        print(f"Hybrid Hit@3: {h_hit}")

    total = len(questions)

    print("\n========== FINAL HIT@3 ==========")
    print(f"BM25:   {bm25_hits}/{total} = {bm25_hits / total:.2f}")
    print(f"Vector: {vector_hits}/{total} = {vector_hits / total:.2f}")
    print(f"Hybrid: {hybrid_hits}/{total} = {hybrid_hits / total:.2f}")

    print("\n========== CATEGORY RESULTS ==========")

    for name, results in [
        ("Exact-term", exact_results),
        ("Meaning-based", meaning_results)
    ]:
        print(f"\n{name} questions:")
        for index, method in enumerate(["BM25", "Vector", "Hybrid"]):
            hits = sum(result[index] for result in results)
            print(f"{method}: {hits}/{len(results)}")


if __name__ == "__main__":
    evaluate()
    client.close()
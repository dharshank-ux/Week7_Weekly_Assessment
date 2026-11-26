from sentence_transformers import CrossEncoder

from retrieval import vector_search, client

MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L-6-v2"

print("Loading Cross-Encoder model...")
reranker = CrossEncoder(MODEL_NAME)


questions = [
    ("How many casual leaves per year?", "leave_policy.txt"),
    ("How many sick leaves are available?", "leave_policy.txt"),
    ("How many earned leaves are available?", "leave_policy.txt"),
    ("What are the working hours?", "attendance_policy.txt"),
    ("When is salary paid?", "salary_policy.txt"),
    ("How can employees work remotely?", "work_from_home.txt"),
    ("How are business expenses reimbursed?", "expense_policy.txt"),
    ("How should company information be protected?", "security_policy.txt"),
    ("Who approves business travel?", "travel_policy.txt"),
    ("What behavior is expected from employees?", "conduct_policy.txt"),
]


def rerank(question, candidates, top_k=5):
    pairs = [
        [question, point.payload["text"]]
        for point in candidates
    ]

    scores = reranker.predict(pairs)

    ranked = sorted(
        zip(candidates, scores),
        key=lambda item: item[1],
        reverse=True
    )

    return ranked[:top_k], ranked


def find_correct_rank(results, expected_source):
    for rank, item in enumerate(results, start=1):
        point = item[0] if isinstance(item, tuple) else item

        if point.payload.get("source") == expected_source:
            return rank

    return None


def evaluate():
    print("\n========== CROSS-ENCODER EVALUATION ==========")

    before_hits = 0
    after_hits = 0

    for question, expected_source in questions:

        candidates = vector_search(question, limit=50)

        before_rank = find_correct_rank(
            candidates,
            expected_source
        )

        top5, reranked_all = rerank(
            question,
            candidates,
            top_k=5
        )

        after_rank = find_correct_rank(
            reranked_all,
            expected_source
        )

        if before_rank is not None and before_rank <= 5:
            before_hits += 1

        if after_rank is not None and after_rank <= 5:
            after_hits += 1

        print(f"\nQuestion: {question}")
        print(f"Expected: {expected_source}")
        print(f"Rank before reranking: {before_rank}")
        print(f"Rank after reranking: {after_rank}")
        print("Top 5 results:")

        for rank, (point, score) in enumerate(top5, start=1):
            print(
                f"{rank}. {point.payload['source']} "
                f"| Score: {score:.4f}"
            )

    print("\n========== SUMMARY ==========")
    print(f"Before Reranking Hit@5: {before_hits}/10")
    print(f"After Reranking Hit@5: {after_hits}/10")


if __name__ == "__main__":
    try:
        evaluate()
    finally:
        client.close()
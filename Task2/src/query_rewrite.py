import time

from retrieval import (
    questions,
    vector_search,
    reciprocal_rank_fusion,
    hit_at_3,
    client
)


def rewrite_query(question):
    """Generate three alternative phrasings."""

    replacements = [
        {
            "casual leaves": "personal time off",
            "sick leaves": "medical leave days",
            "earned leaves": "annual earned time off",
            "working hours": "work schedule",
            "salary paid": "monthly payday",
            "expense reimbursement": "business expense repayment",
            "work from home": "remote working",
            "company information": "confidential company data",
        },
        {
            "casual leaves": "personal leave entitlement",
            "sick leaves": "illness absence allowance",
            "earned leaves": "annual leave entitlement",
            "working hours": "daily office timings",
            "salary paid": "employee payment date",
            "expense reimbursement": "claiming business costs",
            "work from home": "working remotely",
            "company information": "private organizational information",
        },
        {
            "casual leaves": "days off for personal reasons",
            "sick leaves": "time off when ill",
            "earned leaves": "accumulated paid leave",
            "working hours": "normal weekday schedule",
            "salary paid": "when employees receive their pay",
            "expense reimbursement": "getting business expenses refunded",
            "work from home": "performing duties from home",
            "company information": "protecting sensitive business data",
        }
    ]

    rewritten = []

    for mapping in replacements:
        new_question = question

        for original, replacement in mapping.items():
            new_question = new_question.replace(
                original,
                replacement
            )

        rewritten.append(new_question)

    return rewritten


def evaluate():
    baseline_hits = 0
    rewritten_hits = 0

    baseline_time = 0
    rewritten_time = 0

    print("\n========== QUERY REWRITING EVALUATION ==========")

    for category, question, expected in questions:

        # Original vector search
        start = time.perf_counter()

        original_results = vector_search(
            question,
            limit=50
        )

        baseline_time += time.perf_counter() - start

        # Generate 3 alternative queries
        alternatives = rewrite_query(question)

        print(f"\nQuestion: {question}")

        for index, alternative in enumerate(alternatives, 1):
            print(f"Rewrite {index}: {alternative}")

        # Search all rewritten queries
        start = time.perf_counter()

        rewritten_results = [
            vector_search(query, limit=50)
            for query in alternatives
        ]

        # Merge original and rewritten results with RRF
        merged_results = reciprocal_rank_fusion(
            original_results,
            *rewritten_results
        )

        rewritten_time += time.perf_counter() - start

        original_hit = hit_at_3(
            original_results,
            expected
        )

        rewritten_hit = hit_at_3(
            merged_results,
            expected
        )

        baseline_hits += int(original_hit)
        rewritten_hits += int(rewritten_hit)

        print(f"Expected source: {expected}")
        print(f"Original Hit@3: {original_hit}")
        print(f"Rewritten Hit@3: {rewritten_hit}")

    total = len(questions)

    print("\n========== FINAL COMPARISON ==========")

    print(
        f"Original Vector Hit@3: "
        f"{baseline_hits}/{total} "
        f"= {baseline_hits / total:.2f}"
    )

    print(
        f"Query Rewrite + RRF Hit@3: "
        f"{rewritten_hits}/{total} "
        f"= {rewritten_hits / total:.2f}"
    )

    print(f"Original latency: {baseline_time:.3f} seconds")
    print(f"Rewritten latency: {rewritten_time:.3f} seconds")


if __name__ == "__main__":
    try:
        evaluate()
    finally:
        client.close()
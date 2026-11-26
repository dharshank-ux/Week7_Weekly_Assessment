from qdrant_client import models

from retrieval import model, client, COLLECTION_NAME


def metadata_search(question, department=None, year=None, limit=10):

    vector = model.encode(question).tolist()

    conditions = []

    if department:
        conditions.append(
            models.FieldCondition(
                key="department",
                match=models.MatchValue(value=department)
            )
        )

    if year is not None:
        conditions.append(
            models.FieldCondition(
                key="year",
                match=models.MatchValue(value=year)
            )
        )

    query_filter = None

    if conditions:
        query_filter = models.Filter(must=conditions)

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=vector,
        query_filter=query_filter,
        limit=limit,
        with_payload=True
    ).points

    return results


def show_results(title, results):

    print(f"\n========== {title} ==========")

    if not results:
        print("No matching documents")
        return

    for point in results:
        payload = point.payload or {}

        print(
            f"Source: {payload.get('source')} | "
            f"Department: {payload.get('department')} | "
            f"Year: {payload.get('year')} | "
            f"Text: {payload.get('text')}"
        )


def evaluate():

    question = "How many casual leaves are available?"

    all_results = metadata_search(
        question,
        limit=10
    )

    hr_results = metadata_search(
        question,
        department="HR",
        limit=10
    )

    current_results = metadata_search(
        question,
        department="HR",
        year=2026,
        limit=10
    )

    show_results("WITHOUT METADATA FILTER", all_results)

    show_results("WITH HR FILTER", hr_results)

    show_results("WITH HR AND YEAR FILTER", current_results)

    print("\n========== OUTDATED DOCUMENT TEST ==========")

    old_text = "Casual Leave: 5 days per year."

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            models.PointStruct(
                id="00000000-0000-4000-8000-000000002024",
                vector=model.encode(old_text).tolist(),
                payload={
                    "text": old_text,
                    "source": "old_leave_policy.txt",
                    "page": 1,
                    "department": "HR",
                    "year": 2024
                }
            )
        ],
        wait=True
    )

    outdated_results = metadata_search(
        question,
        department="HR",
        limit=10
    )

    current_only_results = metadata_search(
        question,
        department="HR",
        year=2026,
        limit=10
    )

    show_results("INCLUDING OLD DOCUMENT", outdated_results)

    show_results("ONLY 2026 DOCUMENTS", current_only_results)

    old_found = any(
        p.payload.get("year") == 2024
        for p in outdated_results
    )

    old_filtered = any(
        p.payload.get("year") == 2024
        for p in current_only_results
    )

    print("\nOld document found without year filter:", old_found)
    print("Old document found with 2026 filter:", old_filtered)


if __name__ == "__main__":
    try:
        evaluate()
    finally:
        client.close()
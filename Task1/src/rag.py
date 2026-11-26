import os
import re
from pathlib import Path

from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient

BASE_DIR = Path(__file__).resolve().parents[2]
DB_DIR = BASE_DIR / "Task1" / "qdrant_db"

COLLECTION_NAME = "company_policies"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

SCORE_THRESHOLD = 0.35
CONTEXT_BUDGET = 500

print("Loading RAG components...")

model = SentenceTransformer(MODEL_NAME)
client = QdrantClient(path=str(DB_DIR))


def retrieve(question, k=4):
    vector = model.encode(question).tolist()

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=vector,
        limit=k,
        with_payload=True
    ).points

    return results


def fit_context(chunks, budget):
    selected = []
    used_tokens = 0

    for chunk in chunks:
        payload = chunk.payload or {}
        text = payload.get("text", "")

        token_count = len(
            model.tokenizer.encode(
                text,
                add_special_tokens=False
            )
        )

        if used_tokens + token_count <= budget:
            selected.append(chunk)
            used_tokens += token_count

    return selected


def check_question_support(question, context):
    q = question.lower()
    c = context.lower()

    if any(word in q for word in ["salary", "pay", "wage"]):

        if q.startswith("when "):
            return (
                "last working day" in c
                or "salary payment date" in c
            )

        amount_question = (
            "how much" in q
            or "amount" in q
            or "salary of" in q
            or "monthly salary" in q
        )

        if amount_question:
            amount_patterns = [
                r"(?:rs\.?|inr|₹|\$)\s*[\d,]+",
                r"\b\d+(?:,\d{3})+\s*(?:per month|monthly)\b",
                r"\b\d+\s*(?:rupees|lakh|lakhs)\b"
            ]

            return any(
                re.search(pattern, c)
                for pattern in amount_patterns
            )

    return True


def calculate_leave_total(question, context):
    q = question.lower()
    c = context.lower()

    if "total" in q and "casual" in q and "sick" in q:
        casual = re.search(
            r"casual leave:\s*(\d+)\s*days",
            c
        )

        sick = re.search(
            r"sick leave:\s*(\d+)\s*days",
            c
        )

        if casual and sick:
            casual_days = int(casual.group(1))
            sick_days = int(sick.group(1))
            total = casual_days + sick_days

            return (
                f"Casual Leave: {casual_days} days per year.\n"
                f"Sick Leave: {sick_days} days per year.\n"
                f"Total: {total} days per year."
            )

    return None


def generate_answer(question, context):
    """Generate concise answers using supplied context only."""

    api_key = os.getenv("OPENAI_API_KEY")

    if api_key:
        from openai import OpenAI

        llm = OpenAI(api_key=api_key)

        response = llm.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Answer ONLY using the supplied context. "
                        "Answer every part of the question. "
                        "Give concise answers. "
                        "Do not include unrelated information. "
                        "Never guess or use outside knowledge. "
                        "If unavailable, say exactly: "
                        "I don't have information on that."
                    )
                },
                {
                    "role": "user",
                    "content": (
                        f"Context:\n{context}\n\n"
                        f"Question: {question}"
                    )
                }
            ],
            temperature=0
        )

        return response.choices[0].message.content

    # Local extractive answer
    q = question.lower()

    lines = [
        line.strip()
        for line in context.splitlines()
        if line.strip()
    ]

    asks_working_days = (
        "working days" in q
        or "days per week" in q
    )

    asks_working_hours = "working hours" in q

    # Both working days and working hours
    if asks_working_days and asks_working_hours:
        days = [
            line for line in lines
            if "working days:" in line.lower()
        ]

        hours = [
            line for line in lines
            if "working hours:" in line.lower()
        ]

        result = days[:1] + hours[:1]

        if result:
            return "\n".join(result)

    # Working hours only
    if asks_working_hours:
        matches = [
            line for line in lines
            if "working hours:" in line.lower()
        ]

        if matches:
            return matches[0]

    # Working days only
    if asks_working_days:
        matches = [
            line for line in lines
            if "working days:" in line.lower()
        ]

        if matches:
            return matches[0]

    # Salary payment date
    if "when " in q and "salary" in q:
        matches = [
            line for line in lines
            if "salary is paid" in line.lower()
        ]

        if matches:
            return matches[0]

    # Combined leave calculation
    total_answer = calculate_leave_total(question, context)

    if total_answer:
        return total_answer

    return "\n".join(lines)


def answer(question, k=4):
    chunks = retrieve(question, k=k)

    if not chunks:
        return "I don't have information on that"

    best_score = max(chunk.score for chunk in chunks)

    if best_score < SCORE_THRESHOLD:
        return "I don't have information on that"

    selected = fit_context(chunks, CONTEXT_BUDGET)

    if not selected:
        return "I don't have information on that"

    context = "\n".join(
        (chunk.payload or {}).get("text", "")
        for chunk in selected
    )

    if not check_question_support(question, context):
        return "I don't have information on that"

    total_answer = calculate_leave_total(question, context)

    if total_answer:
        return total_answer

    return generate_answer(question, context)


if __name__ == "__main__":

    questions = [
        "How many casual leaves per year?",
        "How many sick leaves are available?",
        "What are the working hours?",
        "What are the working days and normal working hours?",
        "When is the monthly salary paid?",
        "What is the monthly salary of a software developer?",
        "How many casual and sick leaves are available in total per year?",
        "Who won the world cup?"
    ]

    for question in questions:
        print(f"\nQ: {question}")
        print(f"A: {answer(question)}")

    client.close()
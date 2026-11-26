PROMPTS = {
    "basic": """
Answer the user's question clearly and helpfully.
Question: {question}
Context:
{context}
""",

    "context_only": """
Answer the question using ONLY the information in the context.
Do not use outside knowledge.
Question: {question}
Context:
{context}
""",

    "context_citation": """
Answer using ONLY the information in the provided context.
Cite every factual statement using this exact format:
[Source: filename, Page number]

If the answer is not available in the context, reply:
I don't know.

Do not guess or invent information.

Question: {question}
Context:
{context}
"""
}


QUESTIONS = [
    {
        "question": "How many casual leaves are available per year?",
        "answerable": True
    },
    {
        "question": "How many sick leaves are available?",
        "answerable": True
    },
    {
        "question": "How many earned leaves are available?",
        "answerable": True
    },
    {
        "question": "What are the normal working hours?",
        "answerable": True
    },
    {
        "question": "Which days are working days?",
        "answerable": True
    },
    {
        "question": "When is salary paid?",
        "answerable": True
    },
    {
        "question": "How early should casual leave be requested?",
        "answerable": True
    },
    {
        "question": "Who won the 2026 FIFA World Cup?",
        "answerable": False
    },
    {
        "question": "Who is the current CEO of ABC Technologies?",
        "answerable": False
    },
    {
        "question": "How many employees work at ABC Technologies?",
        "answerable": False
    }
]


def show_evaluation_plan():
    print("=" * 60)
    print("HALLUCINATION EVALUATION")
    print("=" * 60)

    print("\nTotal questions:", len(QUESTIONS))
    print("Answerable questions:", sum(
        q["answerable"] for q in QUESTIONS
    ))
    print("Unanswerable questions:", sum(
        not q["answerable"] for q in QUESTIONS
    ))

    print("\nPROMPT STRATEGIES")

    for name, prompt in PROMPTS.items():
        print(f"\n--- {name.upper()} ---")
        print(prompt.strip())

    print("\nEvaluation questions:")

    for index, item in enumerate(QUESTIONS, start=1):
        status = "Answerable" if item["answerable"] else "Unanswerable"
        print(f"{index}. {item['question']} [{status}]")


if __name__ == "__main__":
    show_evaluation_plan()
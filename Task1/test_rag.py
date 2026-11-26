from src.rag import answer, retrieve, fit_context

# 6 Answerable questions
answerable_questions = [
    "How many casual leaves per year?",
    "How many sick leaves are available?",
    "How many earned leaves are available?",
    "What are the working hours?",
    "Which days are working days?",
    "When is salary paid?"
]

# 4 Unanswerable questions
unanswerable_questions = [
    "Who won the world cup?",
    "What is the company CEO name?",
    "What is the monthly salary of an employee?",
    "How many employees work in the company?"
]

print("\n========== ANSWERABLE QUESTIONS ==========")

for question in answerable_questions:
    print(f"\nQ: {question}")
    print(f"A: {answer(question)}")

print("\n========== UNANSWERABLE QUESTIONS ==========")

for question in unanswerable_questions:
    print(f"\nQ: {question}")
    print(f"A: {answer(question)}")

print("\n========== CONTEXT BUDGET TEST ==========")

for k in [2, 5, 10]:
    chunks = retrieve("What is the leave policy?", k=k)
    selected = fit_context(chunks, budget=100)

    print(
        f"k={k} | Retrieved={len(chunks)} "
        f"| Selected={len(selected)}"
    )
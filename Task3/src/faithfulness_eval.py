EVALUATIONS = [
    {
        "question": "How many casual leaves are available per year?",
        "answer": "Employees get 12 casual leaves per year.",
        "claims": [
            {
                "claim": "Employees get 12 casual leaves per year.",
                "supported": True,
                "source": "leave_policy.txt"
            }
        ]
    },
    {
        "question": "How many sick leaves are available?",
        "answer": "Employees get 10 sick leaves per year.",
        "claims": [
            {
                "claim": "Employees get 10 sick leaves per year.",
                "supported": True,
                "source": "leave_policy.txt"
            }
        ]
    },
    {
        "question": "How many earned leaves are available?",
        "answer": "Employees get 15 earned leaves per year.",
        "claims": [
            {
                "claim": "Employees get 15 earned leaves per year.",
                "supported": True,
                "source": "leave_policy.txt"
            }
        ]
    },
    {
        "question": "What are the normal working hours?",
        "answer": "Normal working hours are 9 AM to 6 PM.",
        "claims": [
            {
                "claim": "Normal working hours are 9 AM to 6 PM.",
                "supported": True,
                "source": "attendance_policy.txt"
            }
        ]
    },
    {
        "question": "When is salary paid?",
        "answer": "Salary is paid on the last working day of each month.",
        "claims": [
            {
                "claim": "Salary is paid on the last working day of each month.",
                "supported": True,
                "source": "salary_policy.txt"
            }
        ]
    }
]


def evaluate_faithfulness():
    total_claims = 0
    supported_claims = 0

    print("=" * 60)
    print("MANUAL FAITHFULNESS EVALUATION")
    print("=" * 60)

    for index, item in enumerate(EVALUATIONS, start=1):
        print(f"\nQuestion {index}: {item['question']}")
        print("Answer:", item["answer"])

        for claim in item["claims"]:
            total_claims += 1

            if claim["supported"]:
                supported_claims += 1
                status = "SUPPORTED"
            else:
                status = "NOT SUPPORTED"

            print(f"Claim: {claim['claim']}")
            print(f"Source: {claim['source']}")
            print(f"Status: {status}")

    score = supported_claims / total_claims if total_claims else 0

    print("\n" + "=" * 60)
    print("FAITHFULNESS SUMMARY")
    print("=" * 60)
    print("Total claims:", total_claims)
    print("Supported claims:", supported_claims)
    print("Faithfulness score:", round(score, 2))


if __name__ == "__main__":
    evaluate_faithfulness()
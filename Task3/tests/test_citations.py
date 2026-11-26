from types import SimpleNamespace

from Task3.src.citations import (
    format_context,
    extract_citations,
    validate_citations
)


def create_chunk(text, source, page):
    return SimpleNamespace(
        payload={
            "text": text,
            "source": source,
            "page": page
        }
    )


def test_format_context():
    chunks = [
        create_chunk("Casual Leave: 12 days per year.", "leave_policy.txt", 1)
    ]

    result = format_context(chunks)

    assert "[Source: leave_policy.txt, Page 1]" in result
    assert "Casual Leave: 12 days per year." in result


def test_extract_citations():
    answer = (
        "Employees get 12 casual leaves. "
        "[Source: leave_policy.txt, Page 1]"
    )

    citations = extract_citations(answer)

    assert len(citations) == 1
    assert citations[0]["source"] == "leave_policy.txt"
    assert citations[0]["page"] == 1


def test_valid_citation():
    chunks = [
        create_chunk("Casual Leave: 12 days.", "leave_policy.txt", 1)
    ]

    answer = "Employees get 12 days. [Source: leave_policy.txt, Page 1]"

    result = validate_citations(answer, chunks)

    assert result[0]["valid"] is True


def test_invalid_citation():
    chunks = [
        create_chunk("Casual Leave: 12 days.", "leave_policy.txt", 1)
    ]

    answer = "Employees get 20 days. [Source: fake_policy.txt, Page 5]"

    result = validate_citations(answer, chunks)

    assert result[0]["valid"] is False


def test_no_citation():
    chunks = [
        create_chunk("Casual Leave: 12 days.", "leave_policy.txt", 1)
    ]

    result = validate_citations("Employees get 12 days.", chunks)

    assert result == []
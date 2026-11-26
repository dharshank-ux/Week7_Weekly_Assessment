import re


def format_context(chunks):
    """
    Format retrieved chunks with source and page citations.
    """
    formatted = []

    for chunk in chunks:
        payload = chunk.payload or {}

        text = payload.get("text", "")
        source = payload.get("source", "Unknown")
        page = payload.get("page", 1)

        formatted.append(
            f"[Source: {source}, Page {page}]\n{text}"
        )

    return "\n\n".join(formatted)


def extract_citations(answer):
    """
    Extract citations from an answer.
    """
    pattern = r"\[Source:\s*([^,\]]+),\s*Page\s*(\d+)\]"
    matches = re.findall(pattern, answer)

    return [
        {
            "source": source.strip(),
            "page": int(page)
        }
        for source, page in matches
    ]


def validate_citations(answer, retrieved_chunks):
    """
    Check whether citations exist in retrieved chunks.
    """
    citations = extract_citations(answer)

    valid_sources = set()

    for chunk in retrieved_chunks:
        payload = chunk.payload or {}

        valid_sources.add(
            (
                payload.get("source"),
                int(payload.get("page", 1))
            )
        )

    results = []

    for citation in citations:
        key = (citation["source"], citation["page"])

        results.append({
            **citation,
            "valid": key in valid_sources
        })

    return results


if __name__ == "__main__":
    print("Citation formatting module loaded successfully.")
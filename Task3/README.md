Task 3 – Citations and Hallucination Control

Overview

This task implements citation formatting, citation validation, hallucination evaluation, manual faithfulness assessment, and a protected FastAPI endpoint.

1. Citation Formatting

- Formatted retrieved context with source filename and page number.
- Used the format: "[Source: filename, Page number]".
- Implemented citation extraction using regular expressions.

2. Citation Validation

- Extracted citations from generated answers.
- Compared citations against retrieved document sources and page numbers.
- Identified valid and invalid citations.

3. Hallucination Evaluation

Created three prompt strategies:

- Basic prompt
- Context-only prompt
- Context-only with citation and "I don't know" instruction

Prepared a 10-question evaluation dataset:

- 7 answerable questions
- 3 unanswerable questions

4. Manual Faithfulness Assessment

- Prepared five answers for manual assessment.
- Checked whether each factual claim was supported by the source document.
- Recorded supported and unsupported claims.

5. FastAPI Endpoint

Implemented a POST "/ask" endpoint with:

- API key authentication
- Question validation
- RAG answer generation
- Clear error handling when no relevant information is found

6. API Testing

Tested:

- Home endpoint
- Valid API key
- Invalid API key
- Missing API key
- No-results response
- Empty question

Result: 6 API tests passed.

Technologies Used

- Python
- FastAPI
- Qdrant
- Sentence Transformers
- Pytest
- Regular Expressions

Conclusion

Implemented citation formatting and validation, prepared hallucination and faithfulness evaluation workflows, and developed a protected RAG API endpoint.
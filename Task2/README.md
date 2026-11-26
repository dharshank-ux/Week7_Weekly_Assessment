Task 2 – Advanced Retrieval

Overview

This task implements and evaluates advanced retrieval techniques for a RAG (Retrieval-Augmented Generation) system.

1. BM25 and Vector Search

- Implemented BM25 keyword-based retrieval.
- Implemented dense vector retrieval using Sentence Transformers.
- Evaluated both methods using 12 questions:
  - 6 exact-term questions
  - 6 meaning-based questions
- Compared retrieval performance using Hit@3.

2. Reciprocal Rank Fusion (RRF)

- Combined BM25 and vector search results using Reciprocal Rank Fusion.

- Used the formula:
  
  "RRF Score = 1 / (60 + rank)"

- Compared BM25, vector search, and hybrid retrieval performance.

3. Cross-Encoder Reranking

- Retrieved the top 50 candidates using vector search.
- Applied a Cross-Encoder model to rerank the candidates.
- Selected the top 5 results.
- Evaluated the correct source rank before and after reranking using 10 questions.

4. Query Rewriting

- Generated alternative versions of user queries.
- Performed vector search using the original and rewritten queries.
- Combined results using RRF.
- Compared Hit@3 and retrieval latency.

5. Metadata Filtering

- Implemented metadata filtering using Qdrant.
- Applied department-based filtering.
- Applied year-based filtering.
- Tested outdated document exclusion.

Outdated Document Test

- Added an old HR policy document from 2024.
- Without a year filter, the old document was retrieved.
- With the HR department and 2026 year filter, the old document was excluded.

Technologies Used

- Python
- Sentence Transformers
- Qdrant
- BM25
- Cross-Encoder
- Reciprocal Rank Fusion (RRF)
- Pytest

Conclusion

Advanced retrieval techniques were implemented to improve document retrieval. BM25, vector search, hybrid retrieval, reranking, query rewriting, and metadata filtering were evaluated as part of this task.
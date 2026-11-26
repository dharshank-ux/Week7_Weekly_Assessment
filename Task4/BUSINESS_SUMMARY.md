# Business Summary – Enterprise RAG Knowledge Assistant

## Project Overview

The Enterprise RAG Knowledge Assistant helps employees retrieve accurate information from company policy documents. It uses semantic search and a Retrieval-Augmented Generation (RAG) pipeline to answer questions based on internal company information.

## Key Capabilities

- Retrieves information from company policy documents.
- Supports semantic and keyword-based retrieval.
- Uses BM25 and vector search with Reciprocal Rank Fusion.
- Applies reranking and query rewriting.
- Supports metadata filtering.
- Provides source-aware retrieval.
- Refuses questions when requested information is unavailable.
- Supports combined leave calculations.

## Evaluation Results

The system was evaluated using a golden dataset of 15 questions:

- 8 simple questions.
- 4 multi-chunk questions.
- 3 unanswerable questions.

The final evaluation completed all 15 questions and achieved a 100% source hit rate.

Local heuristic evaluation produced:

- Faithfulness proxy: 0.867
- Answer relevancy proxy: 0.867
- Context precision proxy: 1.000
- Context recall proxy: 1.000

These are local heuristic proxy scores, not official RAGAS measurements.

## Improvements

The system was improved to:
1. Prevent unsupported salary amount answers.
2. Calculate combined casual and sick leave totals.
3. Return concise answers for working hours and salary payment questions.
4. Refuse unsupported questions instead of guessing.

## Business Benefits

- Reduces time spent searching company policy documents.
- Helps employees access HR and operational information quickly.
- Improves consistency of policy-related answers.
- Reduces unsupported answers through refusal checks.
- Provides a foundation for an internal enterprise knowledge assistant.

## Conclusion

The project demonstrates an end-to-end enterprise RAG workflow, including document ingestion, retrieval, reranking, metadata filtering, evaluation, and answer improvement. Further work can improve multi-part answer generation and introduce a dedicated LLM-based evaluation model.
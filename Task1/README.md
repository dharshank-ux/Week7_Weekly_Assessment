# Task 1 - RAG Pipeline with Fallback

## Overview
Built a Retrieval-Augmented Generation (RAG) pipeline for company policy documents.

## Documents
- 8 company policy documents
- Text loading and parsing
- Chunking
- Sentence Transformer embeddings
- Qdrant vector storage
- Metadata and stable IDs

## Indexing
The indexing pipeline uses stable UUID5 IDs.
Running ingestion multiple times updates existing points instead of creating duplicates.

## Query Pipeline
1. Embed the user question.
2. Retrieve relevant chunks.
3. Check similarity score.
4. Apply fallback if score is below 0.35.
5. Fit retrieved context within a 500-token budget.
6. Generate an answer using context only.

## Context Budget
Tested retrieval with k = 2, 5, 10.

## Evaluation
- 6 answerable questions
- 4 unanswerable questions
- Fallback mechanism
- Context budget validation

## Technologies
- Python
- Sentence Transformers
- Qdrant
- OpenAI API (optional)

## Run
bash
python Task1/src/ingest.py
python Task1/test_rag.py
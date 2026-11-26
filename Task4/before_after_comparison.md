# Before and After Comparison

## Evaluation Results

| Metric | Before | After |
|---|---:|---:|
| Faithfulness Proxy | 0.933 | 0.867 |
| Answer Relevancy Proxy | 0.933 | 0.867 |
| Context Precision Proxy | 1.000 | 1.000 |
| Context Recall Proxy | 1.000 | 1.000 |
| Source Hit Rate | 1.000 | 1.000 |

Note: These are local heuristic proxy scores, not official RAGAS metrics.

## Improvements Implemented

1. Added salary amount support checking to prevent unsupported salary answers.
2. Added combined casual and sick leave calculation.
3. Improved concise answers for working hours and salary payment date.
4. Added refusal for unsupported questions.

## Remaining Limitations

1. Some simple questions still return extra context lines.
2. Multi-part questions may not return every requested detail.
3. Local extractive generation does not provide full natural-language reasoning.

## Conclusion

The RAG system completed all 15 evaluation questions and achieved a 100% source hit rate. Improvements were made to unsupported-answer handling, leave calculation, and concise response generation. Further improvements are needed for multi-part answers and evaluation accuracy.
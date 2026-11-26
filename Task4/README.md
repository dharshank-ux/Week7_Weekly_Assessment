# Task 4 – RAG Evaluation and Optimization

## 1. Overview

This task evaluates and improves the Enterprise RAG Knowledge Assistant using a golden question dataset, retrieval evaluation, local heuristic metrics, and failure analysis.

## 2. Golden Dataset

Dataset location: data/golden.jsonl

Total questions: 15

- 8 simple questions
- 4 multi-chunk questions
- 3 unanswerable questions

Each question contains an expected answer and expected source information.

## 3. Evaluation

Run the evaluation:

bash
python Task4/src/evaluate.py


Final results:

- Total questions: 15
- Completed questions: 15
- Source matches: 15
- Source Hit Rate: 100%

Results are saved in evaluation_results.json.

## 4. Local Heuristic Metrics

Run:

bash
python Task4/src/local_evaluation.py


Latest results:

| Metric | Score |
|---|---:|
| Faithfulness Proxy | 0.867 |
| Answer Relevancy Proxy | 0.867 |
| Context Precision Proxy | 1.000 |
| Context Recall Proxy | 1.000 |

Note: These are local heuristic proxy scores, not official RAGAS measurements.

## 5. Failure Analysis

Run:

bash
python Task4/src/failure_analysis.py


An identified issue was that working-hours answers included unrelated context.

### Improvement Implemented

The local answer-generation logic was updated to return the relevant working-hours sentence instead of all retrieved context.

Other improvements:

- Added salary amount support checks.
- Added combined casual and sick leave calculation.
- Improved concise salary payment answers.
- Preserved refusal behavior for unsupported questions.

## 6. Before and After Comparison

See before_after_comparison.md for the comparison table and improvement details.

## 7. Business Summary

See BUSINESS_SUMMARY.md for the project overview, business benefits, evaluation results, and conclusion.

## 8. Project Structure

text
Task4/
│
├── data/
│   └── golden.jsonl
│
├── src/
│   ├── evaluate.py
│   ├── local_evaluation.py
│   ├── failure_analysis.py
│   ├── validate_dataset.py
│   └── inspect_retrieval.py
│
├── tests/
├── evaluation_results.json
├── local_metrics.json
├── before_after_comparison.md
├── BUSINESS_SUMMARY.md
└── README.md


## 9. Conclusion

The evaluation completed all 15 golden dataset questions with a 100% source hit rate. The RAG pipeline was improved to reduce irrelevant output, calculate combined leave totals, and refuse unsupported questions.

Further improvements can include LLM-based evaluation, better multi-part answer generation, and official RAGAS metric measurement.
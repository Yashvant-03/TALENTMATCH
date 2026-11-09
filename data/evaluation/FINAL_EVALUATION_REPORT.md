# TALENTMATCH — Evaluation Report

## Dataset

- Synthetic resumes: 10
- Synthetic job descriptions: 10
- Possible resume-job pairs: 100
- Reviewed pairs: 40
- Reviewed-pair coverage: 40.0%

## Relevance labels

- Low (0): 8
- Partial (1): 21
- Strong (2): 11

## Model comparison

| model                |   precision_at_3_any |   precision_at_3_strong |   mrr_any |   mrr_strong |   ndcg_at_3 |   spearman |
|:---------------------|---------------------:|------------------------:|----------:|-------------:|------------:|-----------:|
| Hybrid               |                0.867 |                   0.367 |         1 |            1 |           1 |      0.852 |
| Sentence Transformer |                0.867 |                   0.367 |         1 |            1 |           1 |      0.852 |

## Evaluation methodology

- Precision@3 (any): labels 1 and 2 count as relevant.
- Precision@3 (strong): only label 2 counts as relevant.
- MRR (any): first result with label 1 or 2.
- MRR (strong): first result with label 2.
- nDCG@3: graded relevance using labels 0, 1 and 2.
- Spearman: correlation between model scores and reviewed relevance labels.

## Limitations

1. Only 40 of 100 possible pairs have reviewed relevance labels.
2. Unreviewed pairs are unknown, not negative examples.
3. Synthetic resumes and job descriptions do not establish real-world effectiveness.
4. The 50/50 hybrid weighting is a fixed experimental choice, not an optimized weight.
5. Exact phrase extraction can miss valid paraphrases and context.
6. Similarity and skill coverage are decision-support signals, not hiring verdicts.
7. Results should not be generalized to real candidate populations.

## Interpretation

The hybrid model must not be claimed as superior unless it demonstrates
consistent improvement on a larger, independently reviewed evaluation set.

## Result interpretation and evidence limits

The Hybrid and Sentence Transformer approaches produced identical values
on all six reported evaluation metrics:

- Precision@3 (any): 0.867
- Precision@3 (strong): 0.367
- MRR (any): 1.000
- MRR (strong): 1.000
- nDCG@3: 1.000
- Spearman: 0.852

Therefore, this evaluation does not demonstrate that adding required-skill
coverage improves ranking quality over Sentence Transformer similarity alone.
The hybrid method remains an experimental scoring approach.

These results are preliminary. They are calculated on 40 reviewed pairs
from 100 possible synthetic resume-job pairs. The 60 unreviewed pairs are
unknown, not negative examples. The metrics should not be interpreted as
evidence of performance on real resumes, real job descriptions, or actual
hiring decisions.

MRR values describe the first relevant result within the reviewed evaluation
subset. They do not establish that the first result is the best candidate
among all possible jobs or candidates.

Further evaluation should use a larger independently reviewed dataset,
clearer annotation guidelines, and comparisons on the same held-out pairs.

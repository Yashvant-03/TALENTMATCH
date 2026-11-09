# TALENTMATCH

**Transformer-based resume and job-description matching with evidence-backed skill analysis.**

TALENTMATCH is an AI/ML portfolio project that compares resume text with job descriptions, estimates semantic relevance, extracts explicit skill evidence, and displays ranked matches through a Streamlit interface.

> **Important:** This is a research and portfolio demonstration, not a hiring decision system. Scores are estimated relevance signals, not probabilities of suitability. Missing evidence does not prove a candidate lacks a skill.

## 1. Problem and intended use

Manually comparing resumes with job descriptions can be time-consuming. TALENTMATCH demonstrates how semantic text similarity and explicit skill evidence can support an initial comparison.

**Intended use:** exploratory resume/job-description comparison.

**Not intended for:** automated hiring decisions, candidate rejection, or claims about an individual's ability or suitability.

## 2. Features

- Sentence Transformer semantic matching using `sentence-transformers/all-MiniLM-L6-v2`.
- TF-IDF baseline used during model comparison.
- Rule-based skill extraction with aliases and phrase-level evidence.
- Required and preferred skill matching.
- Required-skill coverage and missing-evidence reporting.
- Experimental hybrid score combining semantic similarity and required-skill coverage.
- Streamlit interface for exploring saved ranking results.
- Reviewed-pair evaluation and per-resume metrics.

## 3. Architecture

1. Load synthetic resume and job-description text.
2. Generate sentence embeddings using Sentence Transformers.
3. Calculate semantic similarity scores.
4. Extract explicit skill evidence using patterns and aliases.
5. Calculate required-skill coverage.
6. Calculate the experimental hybrid score.
7. Evaluate rankings on reviewed pairs.
8. Display saved rankings and evidence in Streamlit.

See [architecture documentation](docs/architecture.md).

## 4. Scoring

The experimental hybrid score is:

`Hybrid Score = 0.5 × Semantic Similarity + 0.5 × Required Skill Coverage`

Required skill coverage:

`Coverage = Matched Required Skills / Total Required Skills`

The 50/50 weights are fixed experimental choices, not learned or validated optimal weights.

## 5. Dataset

The current demonstration uses:

- 10 synthetic resumes.
- 10 synthetic job descriptions.
- 100 possible resume/job pairs.
- 40 manually reviewed relevance labels.

The data is synthetic and was created for controlled project development. It is not a representative sample of real applicants or job postings.

Relevance labels:

- `0`: Low
- `1`: Partial
- `2`: Strong

The 60 unreviewed pairs are unknown, not negative examples.

## 6. Evaluation results

The current evaluation uses 40 reviewed pairs.

| Metric | Hybrid | Sentence Transformer |
|---|---:|---:|
| Precision@3 (any relevant) | 0.867 | 0.867 |
| Precision@3 (strong only) | 0.367 | 0.367 |
| MRR (any relevant) | 1.000 | 1.000 |
| MRR (strong only) | 1.000 | 1.000 |
| nDCG@3 | 1.000 | 1.000 |
| Spearman correlation | 0.852 | 0.852 |

**Interpretation:** Hybrid and Sentence Transformer produced identical reported metrics. This evaluation does not demonstrate that adding required-skill coverage improves ranking quality.

These are preliminary results on a small, partially judged synthetic dataset. MRR is calculated within the reviewed evaluation subset. The results do not establish generalization to real resumes, real job markets, or hiring outcomes.

Detailed results:

- [Evaluation report](data/evaluation/FINAL_EVALUATION_REPORT.md)
- [Per-resume metrics](data/evaluation/final_per_resume_metrics.csv)
- [Model summary](data/evaluation/final_model_summary.csv)

## 7. Project structure

```text
TALENTMATCH/
├── app/
│   └── streamlit_app.py
├── data/
│   ├── synthetic/
│   └── evaluation/
├── docs/
│   └── architecture.md
├── tests/
│   └── test_artifacts.py
├── TALENTMATCH.ipynb
├── TALENTMATCH_CLEAN.ipynb
├── requirements.txt
├── README.md
└── .gitignore
TALENTMATCH.ipynb is the preserved original notebook. TALENTMATCH_CLEAN.ipynb removes an exact duplicate cell and clears historical error outputs. A fresh end-to-end rerun of either notebook has not yet been verified.
8. Setup
Python 3.10 or later is recommended.

Clone the repository:
git clone <YOUR_REPOSITORY_URL>
cd TALENTMATCH


Create and activate a virtual environment.

Windows PowerShell:
python -m venv .venv
.venv\Scripts\Activate.ps1


Install dependencies:
python -m pip install --upgrade pip
pip install -r requirements.txt


Run the tests:
python -m pytest -q tests


Launch the Streamlit app:
streamlit run app/streamlit_app.py


The app reads the saved CSV artifacts in data/. It does not regenerate embeddings when launched. The Sentence Transformer model is needed for reproducing the embedding pipeline in the notebook.
9. Reproducibility status
- Saved datasets and evaluation artifacts are included.
- Notebook source and execution history are included.
- Streamlit app and artifact tests are included.
- The current test suite has passed in the development environment.
- A fresh end-to-end notebook rerun has not yet been verified.
- Model weights are not committed; the Sentence Transformer model may need to be downloaded when reproducing the pipeline.
10. Limitations and responsible use
1. Only 40 of 100 possible pairs have reviewed relevance labels.
2. Unreviewed pairs are unknown, not negative examples.
3. Synthetic resumes and job descriptions do not establish real-world effectiveness.
4. The hybrid weighting is not optimized.
5. Exact phrase extraction can miss valid paraphrases and context.
6. Similarity and skill coverage are decision-support signals, not hiring verdicts.
7. Missing evidence is not proof that a person lacks a skill.
8. Results should not be generalized to real candidate populations.
11. Future improvements
- Expand independently reviewed evaluation data.
- Improve skill extraction with contextual methods.
- Compare ranking approaches using a consistent held-out evaluation set.
- Evaluate score calibration and ranking robustness.
- Add stronger data validation and reproducibility checks.
12. Tests
Run:
python -m pytest -q tests


The current test suite checks required files, dataset dimensions, relevance labels, and ranking artifact validity.

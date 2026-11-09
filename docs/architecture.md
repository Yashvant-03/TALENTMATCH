# TALENTMATCH — System Architecture

## 1. Architecture overview

```mermaid
flowchart TD
    A[Synthetic Resumes] --> C[Text Preparation]
    B[Synthetic Job Descriptions] --> C
    C --> D[Sentence Transformer: all-MiniLM-L6-v2]
    D --> E[Semantic Similarity]
    C --> F[Rule-Based Skill Extraction]
    F --> G[Required and Preferred Skill Evidence]
    G --> H[Required Skill Coverage]
    E --> I[Hybrid Scoring]
    H --> I
    E --> J[Semantic-Only Ranking]
    I --> K[Hybrid Ranking]
    J --> L[Saved Evaluation Results]
    K --> L
    G --> L
    L --> M[Streamlit Demo]
    2. Main components
Component	Responsibility
Synthetic data	Supplies controlled resume and job-description examples
Sentence Transformer	Generates 384-dimensional text embeddings
Semantic similarity	Measures semantic closeness between resume and job text
Skill extraction	Detects configured skills and aliases in resume text
Evidence mapping	Stores matched phrases supporting detected skills
Coverage calculation	Calculates matched required skills divided by total required skills
Hybrid ranking	Combines semantic similarity and required-skill coverage
Evaluation	Compares rankings against manually reviewed relevance labels
Streamlit app	Displays saved rankings, skill coverage, and evidence

3. Scoring
Hybrid score:

0.5 × Semantic Similarity + 0.5 × Required Skill Coverage

Required-skill coverage:

Matched Required Skills / Total Required Skills

These weights are experimental choices, not learned optimal parameters.
4. Data flow
1. Load resume and job-description datasets.
2. Encode text with the Sentence Transformer.
3. Calculate semantic similarity scores.
4. Detect required and preferred skills using configured patterns.
5. Retain supporting text evidence for detected skills.
6. Calculate required-skill coverage.
7. Generate semantic-only and hybrid rankings.
8. Compare rankings against reviewed relevance labels.
9. Save evaluation artifacts for the Streamlit application.
5. Technology
- Python
- pandas and NumPy
- scikit-learn
- Sentence Transformers
- PyTorch
- Streamlit
- pytest
6. Limitations and responsible use
- Current demonstration data is synthetic.
- Only 40 of 100 possible resume/job pairs have reviewed labels.
- Unreviewed pairs are unknown, not negative.
- Evaluation metrics are preliminary and do not establish real-world effectiveness.
- Skill extraction is pattern-based and may miss paraphrases or context.
- Missing detected evidence does not prove a person lacks a skill.
- Scores are estimated relevance measures, not hiring probabilities or suitability verdicts.
- Human review is required for any consequential decision.

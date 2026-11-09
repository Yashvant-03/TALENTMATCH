
from pathlib import Path
import ast
import json

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

RESUME_FILE = DATA / "synthetic" / "resumes.csv"
JOBS_FILE = DATA / "synthetic" / "job_descriptions.csv"
HYBRID_FILE = DATA / "evaluation" / "hybrid_ranking_results.csv"
SEMANTIC_FILE = DATA / "evaluation" / "semantic_ranking_results.csv"

st.set_page_config(
    page_title="TALENTMATCH",
    page_icon="🎯",
    layout="wide"
)

@st.cache_data
def load_data():
    resumes = pd.read_csv(RESUME_FILE)
    jobs = pd.read_csv(JOBS_FILE)
    hybrid = pd.read_csv(HYBRID_FILE)
    semantic = pd.read_csv(SEMANTIC_FILE)
    return resumes, jobs, hybrid, semantic

def parse_list(value):
    if pd.isna(value) or not str(value).strip():
        return []
    try:
        parsed = json.loads(value)
        return parsed if isinstance(parsed, list) else []
    except (ValueError, TypeError):
        try:
            parsed = ast.literal_eval(value)
            return parsed if isinstance(parsed, list) else []
        except (ValueError, SyntaxError):
            return []

def parse_evidence(value):
    if pd.isna(value) or not str(value).strip():
        return {}
    try:
        parsed = json.loads(value)
        return parsed if isinstance(parsed, dict) else {}
    except (ValueError, TypeError):
        try:
            parsed = ast.literal_eval(value)
            return parsed if isinstance(parsed, dict) else {}
        except (ValueError, SyntaxError):
            return {}

st.title("🎯 TALENTMATCH")
st.subheader("Evidence-backed resume and job matching")

st.write(
    "Explore estimated relevance between synthetic resumes and job descriptions. "
    "Inspect skill coverage, missing requirements, and supporting text evidence."
)

st.warning(
    "Research/demo tool only. Scores are not hiring probabilities or suitability "
    "verdicts. Missing evidence does not prove a person lacks a skill. "
    "The dataset is synthetic and evaluation coverage is limited."
)

try:
    resumes, jobs, hybrid, semantic = load_data()
except Exception as exc:
    st.error(f"Could not load project data: {exc}")
    st.stop()

resume_options = {
    f"{row.resume_id} — {row.profile}": row.resume_id
    for row in resumes.itertuples()
}

selected_label = st.sidebar.selectbox(
    "Select synthetic resume",
    list(resume_options.keys())
)
resume_id = resume_options[selected_label]

ranking_method = st.sidebar.radio(
    "Ranking method",
    ["Hybrid", "Sentence Transformer"]
)

ranking_df = hybrid if ranking_method == "Hybrid" else semantic
score_column = "hybrid_score" if ranking_method == "Hybrid" else "semantic_score"

resume_row = resumes[resumes["resume_id"] == resume_id].iloc[0]

st.markdown("### Selected resume")
st.caption(f"Resume ID: {resume_id} | Profile: {resume_row['profile']}")
with st.expander("View synthetic resume text"):
    st.write(resume_row["resume_text"])

results = ranking_df[ranking_df["resume_id"] == resume_id].copy()
results = results.sort_values(score_column, ascending=False)

if results.empty:
    st.info("No saved ranking results are available for this resume.")
    st.stop()

st.markdown("### Ranked job matches")
st.caption(
    f"Ranking method: {ranking_method} | "
    f"Available results: {len(results)}"
)

for rank, (_, result) in enumerate(results.iterrows(), start=1):
    job_rows = jobs[jobs["job_id"] == result["job_id"]]
    if job_rows.empty:
        continue

    job = job_rows.iloc[0]
    score = float(result[score_column])
    coverage = float(result["required_coverage"])

    with st.container(border=True):
        st.markdown(f"#### {rank}. {job['job_title']}")
        st.caption(f"Job ID: {result['job_id']}")

        col1, col2 = st.columns(2)
        col1.metric("Estimated relevance score", f"{score:.3f}")
        col2.metric("Required skill coverage", f"{coverage:.0%}")

        with st.expander("Job description"):
            st.write(job["job_description"])

        matched = parse_list(result["matched_required"])
        missing = parse_list(result["missing_required"])
        preferred = parse_list(result["matched_preferred"])
        evidence = parse_evidence(result["skill_evidence"])

        left, right = st.columns(2)

        with left:
            st.markdown("**Required skills with evidence**")
            if matched:
                for skill in matched:
                    st.write(f"✓ {skill}")
            else:
                st.write("No required skills matched in the saved analysis.")

            st.markdown("**Matched preferred skills**")
            if preferred:
                for skill in preferred:
                    st.write(f"• {skill}")
            else:
                st.write("No preferred skills matched.")

        with right:
            st.markdown("**Required skills without detected evidence**")
            if missing:
                for skill in missing:
                    st.write(f"• {skill}")
            else:
                st.write("No missing required skills detected.")

        with st.expander("Inspect supporting evidence"):
            if evidence:
                for skill, phrases in evidence.items():
                    st.markdown(f"**{skill}**")
                    if isinstance(phrases, list):
                        for phrase in phrases:
                            st.write(f"- “{phrase}”")
                    else:
                        st.write(str(phrases))
            else:
                st.write("No phrase-level evidence stored for this result.")

        explanation = result.get("evidence_explanation", "")
        if pd.notna(explanation) and str(explanation).strip():
            st.caption(str(explanation))

st.divider()
st.caption(
    "TALENTMATCH | Synthetic demonstration dataset | "
    "Estimated relevance, not a hiring decision."
)

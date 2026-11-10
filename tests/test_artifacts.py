from pathlib import Path
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def test_required_project_files_exist():
    required = [
        DATA / "synthetic/resumes.csv",
        DATA / "synthetic/job_descriptions.csv",
        DATA / "evaluation/reviewed_pairs.csv",
        DATA / "evaluation/skill_matching_results.csv",
        DATA / "evaluation/hybrid_ranking_results.csv",
        DATA / "evaluation/semantic_ranking_results.csv",
    ]
    missing = [str(path) for path in required if not path.exists()]
    assert not missing, f"Missing project files: {missing}"


def test_synthetic_dataset_dimensions():
    resumes = pd.read_csv(DATA / "synthetic/resumes.csv")
    jobs = pd.read_csv(DATA / "synthetic/job_descriptions.csv")
    assert len(resumes) == 10
    assert len(jobs) == 10
    assert resumes["resume_id"].is_unique
    assert jobs["job_id"].is_unique


def test_reviewed_labels_are_valid():
    reviewed = pd.read_csv(DATA / "evaluation/reviewed_pairs.csv")
    assert len(reviewed) == 40
    assert not reviewed[["resume_id", "job_id"]].duplicated().any()
    assert reviewed["relevance_label"].notna().all()
    assert set(reviewed["relevance_label"].unique()).issubset({0, 1, 2})


def test_ranking_artifacts_have_valid_scores():
    for filename, score_column in [
        ("hybrid_ranking_results.csv", "hybrid_score"),
        ("semantic_ranking_results.csv", "semantic_score"),
    ]:
        df = pd.read_csv(DATA / "evaluation" / filename)
        assert len(df) == 40
        assert {"resume_id", "job_id", score_column}.issubset(df.columns)
        assert df[score_column].notna().all()
        assert df[score_column].between(0, 1).all()
        assert not df[["resume_id", "job_id"]].duplicated().any()


def test_skill_evidence_is_valid_json():
    df = pd.read_csv(DATA / "evaluation/skill_matching_results.csv")
    assert "skill_evidence" in df.columns
    for value in df["skill_evidence"].dropna():
        parsed = json.loads(value)
        assert isinstance(parsed, dict)


def test_coverage_is_between_zero_and_one():
    df = pd.read_csv(DATA / "evaluation/skill_matching_results.csv")
    assert df["required_coverage"].notna().all()
    assert df["required_coverage"].between(0, 1).all()

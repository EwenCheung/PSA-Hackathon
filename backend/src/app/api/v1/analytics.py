"""
API: Analytics Dashboard

Purpose:
- Provide company-wide KPIs, aggregates, and insights for the employer dashboard.
- Data pulled from 'employee_insights' table.
"""
from pathlib import Path
import sqlite3
import json
import pandas as pd
import numpy as np
import math
from pandas.errors import DatabaseError
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder

router = APIRouter(
    prefix="/api/v1/analytics",
    tags=["Analytics"],
)

# Path to your SQLite database
DB_PATH = Path(__file__).resolve().parents[2] / "data" / "database" / "app.db"
ANALYTICS_COLUMNS = [
    "id",
    "name",
    "role",
    "department_id",
    "level",
    "skills",
    "goals",
    "courses_enrolled",
    "courses_recommended_json",
    "leadership_summary",
    "years_with_company",
]


# ---------------------------
# Utility functions
# ---------------------------
def load_employee_data():
    conn = sqlite3.connect(DB_PATH)
    try:
        df = pd.read_sql_query("SELECT * FROM employee_insights", conn)
    except (sqlite3.OperationalError, DatabaseError):
        df = pd.DataFrame(columns=ANALYTICS_COLUMNS)
    finally:
        conn.close()

    missing_columns = [col for col in ANALYTICS_COLUMNS if col not in df.columns]
    for column in missing_columns:
        df[column] = pd.Series(dtype="object")
    return df


def parse_json_column(series: pd.Series):
    """Safely parse JSON fields."""
    def safe_parse(x):
        if pd.isna(x) or x in ("", "null", None):
            return []
        try:
            val = json.loads(x)
            if isinstance(val, dict):
                return list(val.keys())
            elif isinstance(val, list):
                return val
            else:
                return [val]
        except Exception:
            return []
    return series.apply(safe_parse)


def safe_float(val):
    """Convert NaN or Inf to None for JSON serialization."""
    if val is None:
        return None
    if isinstance(val, float):
        if math.isnan(val) or math.isinf(val):
            return None
    return val


def sanitize_dict(d):
    """Recursively replace NaN/Inf with None in dicts/lists."""
    if isinstance(d, dict):
        return {k: sanitize_dict(v) for k, v in d.items()}
    elif isinstance(d, list):
        return [sanitize_dict(v) for v in d]
    else:
        return safe_float(d)


# ---------------------------
# Routes
# ---------------------------

@router.get("/overview")
def get_company_overview():
    df = load_employee_data()
    df.fillna("", inplace=True)

    # ========== Basic Stats ==========
    total_employees = len(df)
    roles_count = df["role"].value_counts().to_dict()
    department_count = df["department_id"].value_counts().to_dict()
    level_count = df["level"].value_counts().to_dict()

    # ========== Skills & Goals ==========
    all_skills = parse_json_column(df["skills"]).explode().value_counts().head(15).reset_index().values.tolist()
    all_goals = parse_json_column(df["goals"]).explode().value_counts().head(30).reset_index().values.tolist()

    # ========== Courses ==========
    enrolled_courses = parse_json_column(df["courses_enrolled"]).explode().value_counts().head(10).reset_index().values.tolist()
    recommended_courses = parse_json_column(df["courses_recommended_json"]).explode().value_counts().head(20).reset_index().values.tolist()

    # ========== Leadership ==========
    def extract_leadership_score(summary):
        import re
        if isinstance(summary, str):
            match = re.search(r"(\d+(\.\d+)?)", summary)
            return float(match.group(1)) if match else np.nan
        return np.nan

    df["leadership_score"] = df["leadership_summary"].apply(extract_leadership_score)
    df["leadership_category"] = df["leadership_summary"].apply(
        lambda x: "High" if isinstance(x, str) and "high" in x.lower() else ("Low" if isinstance(x, str) and "low" in x.lower() else "Mid")
    )

    leadership_dist = df["leadership_category"].value_counts().to_dict()

    # High potential employees
    high_potential = df[df["leadership_category"] == "High"][[
        "id", "name", "role", "department_id", "level", "years_with_company", "leadership_score", "leadership_category"
    ]].to_dict(orient="records")

    # ========== Seniority ==========
    most_senior = df.sort_values(by="years_with_company", ascending=False).head(10)[[
        "id", "name", "role", "department_id", "level", "years_with_company"
    ]].to_dict(orient="records")

    # ========== Role Analytics ==========
    df["num_skills"] = parse_json_column(df["skills"]).apply(len)
    role_analytics = (
        df.groupby("role")
        .agg(
            count=("id", "count"),
            avg_skills=("num_skills", "mean"),
            avg_leadership_score=("leadership_score", "mean"),
            avg_years=("years_with_company", "mean"),
        )
        .reset_index()
        .to_dict(orient="records")
    )

    roles_lacking_skills = [r for r in role_analytics if safe_float(r["avg_skills"]) <= 3.0]

    # ========== Return Combined Insights ==========
    result = {
        "total_employees": total_employees,
        "roles_count": roles_count,
        "department_count": department_count,
        "level_count": level_count,
        "top_skills": all_skills,
        "top_goals": all_goals,
        "top_enrolled_courses": enrolled_courses,
        "top_recommended_courses": recommended_courses,
        "leadership_distribution": leadership_dist,
        "high_potential_employees": high_potential,
        "most_senior": most_senior,
        "role_analytics": role_analytics,
        "roles_lacking_skills": roles_lacking_skills
    }

    return jsonable_encoder(sanitize_dict(result))


@router.get("/roles")
def get_role_analytics():
    df = load_employee_data()
    df["num_skills"] = parse_json_column(df["skills"]).apply(len)

    result = (
        df.groupby("role")
        .agg(
            total_employees=("id", "count"),
            avg_skills=("num_skills", "mean"),
            avg_tenure=("years_with_company", "mean"),
        )
        .reset_index()
        .to_dict(orient="records")
    )

    return jsonable_encoder(sanitize_dict(result))


@router.get("/departments")
def get_department_stats():
    df = load_employee_data()
    result = (
        df.groupby("department_id")
        .agg(
            total_employees=("id", "count"),
            avg_tenure=("years_with_company", "mean"),
        )
        .reset_index()
        .to_dict(orient="records")
    )
    return jsonable_encoder(sanitize_dict(result))


@router.get("/employees")
def get_employee_details():
    df = load_employee_data()
    df["skills"] = parse_json_column(df["skills"])
    df["goals"] = parse_json_column(df["goals"])
    return jsonable_encoder(sanitize_dict(df[[
        "id", "name", "department_id", "role", "level",
        "years_with_company", "skills", "goals", "leadership_summary"
    ]].to_dict(orient="records")))

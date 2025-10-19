# dashboard.py
"""
Generate statistics & simple dashboard artifacts from employee_insights table.

Produces:
 - printed summary statistics
 - CSV exports under ./reports/
 - basic matplotlib plots saved as PNG under ./reports/plots/
 - a JSON summary file ./reports/summary.json

Usage:
    python dashboard.py
"""

import json
import sqlite3
from pathlib import Path
from collections import Counter, defaultdict
import math

import pandas as pd
import matplotlib.pyplot as plt

# -------------------------
# Configuration
# -------------------------
BASE_DIR = Path(__file__).resolve().parents[2] / "data" / "database"
DB_PATH = BASE_DIR / "app.db"
REPORT_DIR = Path(__file__).resolve().parent / "reports"
PLOTS_DIR = REPORT_DIR / "plots"
REPORT_DIR.mkdir(parents=True, exist_ok=True)
PLOTS_DIR.mkdir(parents=True, exist_ok=True)

# -------------------------
# Helpers
# -------------------------
def safe_json_load(s, default):
    if s is None:
        return default
    if isinstance(s, (dict, list)):
        return s
    try:
        return json.loads(s)
    except Exception:
        return default

def top_n(counter, n=10):
    return counter.most_common(n)

# -------------------------
# Load data from DB
# -------------------------
def load_insights_table(db_path: Path) -> pd.DataFrame:
    conn = sqlite3.connect(str(db_path))
    df = pd.read_sql_query("SELECT * FROM employee_insights", conn)
    conn.close()
    return df

# -------------------------
# Extract & normalize columns
# -------------------------
def normalize_df(df: pd.DataFrame) -> pd.DataFrame:
    # Parse JSON columns into Python structures
    df = df.copy()

    df["skills_list"] = df["skills"].apply(lambda s: safe_json_load(s, []))
    df["goals_list"] = df["goals"].apply(lambda s: safe_json_load(s, []))
    df["courses_enrolled_map"] = df["courses_enrolled"].apply(lambda s: safe_json_load(s, {}))
    df["courses_recommended"] = df["courses_recommended_json"].apply(lambda s: safe_json_load(s, []))

    # leadership_json may be stored as JSON string; parse it
    df["leadership_obj"] = df["leadership_json"].apply(lambda s: safe_json_load(s, {}))

    # career pathway
    df["career_obj"] = df["career_pathway_json"].apply(lambda s: safe_json_load(s, {}))

    # Derived counts
    df["n_skills"] = df["skills_list"].apply(lambda x: len(x) if isinstance(x, list) else 0)
    df["n_goals"] = df["goals_list"].apply(lambda x: len(x) if isinstance(x, list) else 0)
    df["n_courses_enrolled"] = df["courses_enrolled_map"].apply(lambda d: len(d) if isinstance(d, dict) else 0)
    df["n_courses_recommended"] = df["courses_recommended"].apply(lambda x: len(x) if isinstance(x, list) else 0)

    # Extract leadership category / score if present
    def leadership_category(obj):
        if not isinstance(obj, dict):
            return None
        # try common keys
        for k in ("potential_category", "potential_level", "potential"):
            val = obj.get(k)
            if isinstance(val, str) and val.strip():
                return val
        # fallback: check nested keys
        if "overall_potential_score" in obj:
            score = obj.get("overall_potential_score")
            try:
                s = float(score)
                if s >= 7.5:
                    return "High"
                if s >= 4.0:
                    return "Mid"
                return "Low"
            except Exception:
                pass
        # fallback None
        return None

    def leadership_score(obj):
        if not isinstance(obj, dict):
            return None
        # try to extract numeric overall_score / overall_potential_score
        for key in ("overall_score", "overall_potential_score"):
            if key in obj:
                try:
                    return float(obj.get(key))
                except Exception:
                    pass
        # try flattened leadership_score.overall_score
        if "leadership_score" in obj and isinstance(obj["leadership_score"], dict):
            try:
                return float(obj["leadership_score"].get("overall_score"))
            except Exception:
                pass
        return None

    df["leadership_category"] = df["leadership_obj"].apply(leadership_category)
    df["leadership_score"] = df["leadership_obj"].apply(leadership_score)

    return df

# -------------------------
# Statistics / Dashboard computations
# -------------------------
def compute_statistics(df: pd.DataFrame) -> dict:
    stats = {}

    stats["total_employees"] = len(df)
    stats["roles_count"] = df["role"].value_counts().to_dict()
    stats["department_count"] = df["department_id"].value_counts().to_dict()
    stats["level_count"] = df["level"].value_counts().to_dict()

    # Skills: flatten skill lists and count
    skill_counter = Counter()
    for skills in df["skills_list"]:
        if not isinstance(skills, list):
            continue
        skill_counter.update(skills)
    stats["top_skills"] = top_n(skill_counter, 30)

    # Goals: simple keyword counting (by exact goal string)
    goal_counter = Counter()
    for goals in df["goals_list"]:
        if not isinstance(goals, list):
            continue
        goal_counter.update(goals)
    stats["top_goals"] = top_n(goal_counter, 30)

    # Courses enrolled popularity
    enrolled_counter = Counter()
    for cmap in df["courses_enrolled_map"]:
        if isinstance(cmap, dict):
            for course_id_or_name, status in cmap.items():
                enrolled_counter[course_id_or_name] += 1
    stats["top_enrolled_courses"] = top_n(enrolled_counter, 30)

    # Courses recommended popularity (by title if provided)
    rec_course_counter = Counter()
    for recs in df["courses_recommended"]:
        if isinstance(recs, list):
            for rec in recs:
                # rec might be dict with title or string
                if isinstance(rec, dict):
                    title = rec.get("title") or rec.get("name") or rec.get("id")
                    if title:
                        rec_course_counter[title] += 1
                elif isinstance(rec, str):
                    rec_course_counter[rec] += 1
    stats["top_recommended_courses"] = top_n(rec_course_counter, 30)

    # Leadership potential distribution
    leadership_counter = Counter()
    for cat in df["leadership_category"]:
        if cat:
            leadership_counter[cat] += 1
        else:
            leadership_counter["Unknown"] += 1
    stats["leadership_distribution"] = dict(leadership_counter)

    # Who are high potential (if category or score)
    high_potential = []
    for _, row in df.iterrows():
        cat = row.get("leadership_category")
        score = row.get("leadership_score")
        if (isinstance(cat, str) and cat.lower().startswith("h")) or (isinstance(score, (int, float)) and score >= 7.5):
            high_potential.append({
                "id": row["id"],
                "name": row["name"],
                "role": row["role"],
                "department": row["department_id"],
                "level": row["level"],
                "years_with_company": row.get("years_with_company"),
                "leadership_score": score,
                "leadership_category": cat
            })
    stats["high_potential_employees"] = high_potential

    # Seniority: top N by years_with_company
    top_senior = df.sort_values("years_with_company", ascending=False).head(10)[
        ["id", "name", "role", "department_id", "level", "years_with_company"]
    ].to_dict(orient="records")
    stats["most_senior"] = top_senior

    # Role-level analytics: avg skills per role, avg leadership score per role, counts
    role_groups = df.groupby("role").agg(
        count=("id", "count"),
        avg_skills=("n_skills", "mean"),
        avg_leadership_score=("leadership_score", lambda s: float(s.dropna().mean()) if not s.dropna().empty else None),
        avg_years=("years_with_company", "mean")
    ).reset_index()
    stats["role_analytics"] = role_groups.to_dict(orient="records")

    # Roles lacking: roles with lowest avg_skills (and count threshold)
    role_groups_filtered = role_groups[role_groups["count"] >= 1]  # threshold can be adjusted
    lacking_roles = role_groups_filtered.sort_values("avg_skills").head(10)[["role", "count", "avg_skills"]].to_dict(orient="records")
    stats["roles_lacking_skills"] = lacking_roles

    return stats

# -------------------------
# Plotting helpers
# -------------------------
def plot_bar(counter_items, title, xlabel, ylabel, out_path: Path, top_n_items=10):
    labels = [str(k) for k, _ in counter_items[:top_n_items]]
    values = [v for _, v in counter_items[:top_n_items]]

    plt.figure(figsize=(10, 6))
    plt.bar(range(len(labels)), values)
    plt.xticks(range(len(labels)), labels, rotation=45, ha="right")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()

def plot_horizontal_bar_from_df(df, x_col, y_col, title, out_path: Path, top_n_items=10):
    df_sorted = df.sort_values(by=y_col, ascending=True).tail(top_n_items)
    plt.figure(figsize=(10, 6))
    plt.barh(df_sorted[x_col].astype(str), df_sorted[y_col])
    plt.xlabel(y_col)
    plt.title(title)
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()

# -------------------------
# Main generate function
# -------------------------
def generate_dashboard(db_path: Path, report_dir: Path, plots_dir: Path) -> dict:
    df_raw = load_insights_table(db_path)
    if df_raw.empty:
        print("No data found in employee_insights table.")
        return {}

    df = normalize_df(df_raw)

    # If years_with_company not present compute or coerce to numeric
    if "years_with_company" not in df.columns:
        df["years_with_company"] = df["years_with_company"].apply(lambda x: float(x) if x else None)
    df["years_with_company"] = pd.to_numeric(df["years_with_company"], errors="coerce")

    stats = compute_statistics(df)

    # Save reports
    df[["id", "name", "department_id", "role", "level", "years_with_company", "n_skills", "n_goals", "n_courses_enrolled"]].to_csv(
        report_dir / "employee_summary_table.csv", index=False
    )
    pd.DataFrame(stats["high_potential_employees"]).to_csv(report_dir / "high_potential_employees.csv", index=False)
    pd.DataFrame(stats["role_analytics"]).to_csv(report_dir / "role_analytics.csv", index=False)

    # Save overall JSON summary
    summary_path = report_dir / "summary.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)

    # Plots
    plot_bar(stats["top_skills"], "Top Skills (requested / present)", "Skill", "Count", plots_dir / "top_skills.png", top_n_items=15)
    plot_bar(stats["top_recommended_courses"], "Top Recommended Courses", "Course", "Count", plots_dir / "top_recommended_courses.png", top_n_items=15)
    plot_bar(stats["top_enrolled_courses"], "Top Enrolled Courses", "Course", "Count", plots_dir / "top_enrolled_courses.png", top_n_items=15)
    leadership_items = list(stats["leadership_distribution"].items())
    plot_bar(leadership_items, "Leadership Potential Distribution", "Category", "Count", plots_dir / "leadership_distribution.png", top_n_items=len(leadership_items))
    seniors_df = pd.DataFrame(stats["most_senior"])
    if not seniors_df.empty:
        plot_horizontal_bar_from_df(seniors_df, "name", "years_with_company", "Most Senior Employees (years)", plots_dir / "most_senior.png", top_n_items=10)

    print(f"✅ Reports saved to: {report_dir}")
    print(f"✅ Plots saved to: {plots_dir}")

    # Return the stats dict so it can be used directly
    return stats


# -------------------------
# Entrypoint
# -------------------------
if __name__ == "__main__":
    print("Loading data from DB:", DB_PATH)
    summary = generate_dashboard(DB_PATH, REPORT_DIR, PLOTS_DIR)
    print("Done. Returning summary:\n")
    print(json.dumps(summary, indent=2))

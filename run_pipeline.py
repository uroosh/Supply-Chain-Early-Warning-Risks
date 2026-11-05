"""Rebuild the scored table from data/raw and check it against the published CSV.

Usage:  python scripts/run_pipeline.py
"""
import pandas as pd

from scrisk import run, validation_report
from scrisk.validation import check_tier_counts, compare_to_reference

scored = run("data")
ref = pd.read_csv("data/processed/scored_items.csv")
cmp = compare_to_reference(scored, ref)
print(cmp[cmp.mismatches > 0].to_string(index=False) or "no mismatches")
print("Deterministic columns match:", int(cmp[~cmp.column.isin(["sim_disruption_rate", "top10_stability"])].mismatches.sum()) == 0)
print("Published CSV :", check_tier_counts(ref))
print("Rebuilt CSV   :", check_tier_counts(scored))
rep = validation_report(ref)
print("\nValidation on published CSV")
print("Spearman(score, sim rate):", rep["spearman_score_vs_sim_rate"])
print(rep["tier_summary"])
print("Early warning:", rep["early_warning"])
print("Review flag:  ", rep["review_flag"])

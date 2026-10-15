#!/usr/bin/env python3
"""Recalculate the paper's descriptive tables from the released coded records.

This script uses only the Python standard library and makes no network requests.
Run from the repository root with: python reproduce_results.py
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from statistics import median


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"


def read_csv(name: str) -> list[dict[str, str]]:
    with (DATA / name).open("r", encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def pct(n: int, d: int) -> float | None:
    return round(100 * n / d, 1) if d else None


def source_visibility(rows: list[dict[str, str]]) -> dict[str, dict[str, dict[str, int | float]]]:
    by_surface: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        by_surface[row["visible_surface"]].append(row)
    result = {}
    for surface, group in sorted(by_surface.items()):
        denominator = len(group)
        strict = sum(r["local_relevance_strict"] == "yes" for r in group)
        inclusive = sum(r["local_relevance_inclusive"] == "yes" for r in group)
        result[surface] = {
            "records": denominator,
            "strict_yes": strict,
            "strict_pct": pct(strict, denominator),
            "inclusive_yes": inclusive,
            "inclusive_pct": pct(inclusive, denominator),
        }
    return result


def system_language_profiles(rows: list[dict[str, str]]) -> dict[str, dict[str, int | float]]:
    groups: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        groups[(row["system"], row["language"])].append(row)
    result = {}
    for (system, language), group in sorted(groups.items()):
        key = f"{system} / {language}"
        d = len(group)
        s = sum(r["local_relevance_strict"] == "yes" for r in group)
        i = sum(r["local_relevance_inclusive"] == "yes" for r in group)
        result[key] = {
            "records": d,
            "strict_yes": s,
            "strict_pct": pct(s, d),
            "inclusive_yes": i,
            "inclusive_pct": pct(i, d),
        }
    return result


def paired_language_contrasts(rows: list[dict[str, str]]) -> dict[str, dict[str, int | float]]:
    groups: dict[tuple[str, str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        groups[(row["pair_id"], row["system"], row["language"])].append(row)

    result = {}
    for system in sorted({r["system"] for r in rows}):
        for rule, field in (("strict", "local_relevance_strict"), ("inclusive", "local_relevance_inclusive")):
            differences = []
            for pair_id in sorted({r["pair_id"] for r in rows}):
                shares = {}
                for language in ("English", "Filipino"):
                    cell = groups.get((pair_id, system, language), [])
                    if not cell:
                        continue
                    # The released source table has one row per normalized URL per cell.
                    shares[language] = 100 * sum(r[field] == "yes" for r in cell) / len(cell)
                if set(shares) == {"English", "Filipino"}:
                    differences.append(shares["Filipino"] - shares["English"])

            result[f"{system} / {rule}"] = {
                "pairs": len(differences),
                "filipino_higher": sum(d > 1e-10 for d in differences),
                "english_higher": sum(d < -1e-10 for d in differences),
                "same": sum(abs(d) <= 1e-10 for d in differences),
                "median_difference_percentage_points": round(median(differences), 1) if differences else None,
                "range_percentage_points": [round(min(differences), 1), round(max(differences), 1)] if differences else None,
            }
    return result


def citation_overlap(rows: list[dict[str, str]]) -> dict[str, dict[str, int | float | list[float]]]:
    result = {}
    for language in ("English", "Filipino"):
        group = [r for r in rows if r["language"] == language]
        exact = [r for r in group if r["conventional_capture_status"] == "complete_exact_urls"]
        partial = [r for r in group if r["conventional_capture_status"] != "complete_exact_urls"]
        citation_denominator = sum(int(r["chatgpt_visible_citations"] or 0) for r in exact)
        exact_overlap = sum(int(r["overlap_count"] or 0) for r in exact)
        rates = [float(r["visible_overlap_pct"]) for r in exact if r["visible_overlap_pct"] != ""]
        result[language] = {
            "observations": len(group),
            "exact_captures": len(exact),
            "partial_captures": len(partial),
            "exact_citation_urls": citation_denominator,
            "exact_overlap_urls": exact_overlap,
            "exact_pooled_overlap_pct": pct(exact_overlap, citation_denominator),
            "exact_mean_query_overlap_pct": round(sum(rates) / len(rates), 1) if rates else None,
            "exact_query_overlap_range_pct": [round(min(rates), 1), round(max(rates), 1)] if rates else None,
            "partial_visible_matches": sum(int(r["overlap_count"] or 0) for r in partial),
            "partial_unobserved_citation_urls": sum(int(r["cited_not_observed_in_conventional"] or 0) for r in partial),
        }
    return result


def cohen_kappa(first: list[str], second: list[str]) -> float | None:
    if not first or len(first) != len(second):
        raise ValueError("Coder value lists must be nonempty and have equal length")
    n = len(first)
    observed = sum(a == b for a, b in zip(first, second)) / n
    cats = set(first) | set(second)
    first_counts = Counter(first)
    second_counts = Counter(second)
    expected = sum(first_counts[c] / n * second_counts[c] / n for c in cats)
    if math.isclose(expected, 1.0):
        # With no category variation, chance agreement is 1 and kappa is undefined.
        return None
    return (observed - expected) / (1 - expected)


def reliability(filename: str) -> dict[str, dict[str, int | float | None]]:
    rows = read_csv(filename)
    if not rows:
        raise ValueError(f"No coder rows in {filename}")
    first_fields = [k for k in rows[0] if k.startswith("coder_1_")]
    result = {}
    for first_key in first_fields:
        second_key = "coder_2_" + first_key.removeprefix("coder_1_")
        first = [r[first_key] for r in rows]
        second = [r[second_key] for r in rows]
        n = len(rows)
        kappa = cohen_kappa(first, second)
        result[first_key.removeprefix("coder_1_")] = {
            "n": n,
            "exact_agreement_pct": round(100 * sum(a == b for a, b in zip(first, second)) / n, 2),
            "cohens_kappa": round(kappa, 4) if kappa is not None else None,
        }
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Write JSON results to this path instead of stdout")
    args = parser.parse_args()

    sources = read_csv("full-24-pair-source-table-adjudicated.csv")
    coverage = read_csv("full-24-pair-cell-coverage.csv")
    carry = read_csv("full-24-pair-citation-carry-through-adjudicated.csv")
    result = {
        "audit_counts": {
            "query_language_system_combinations": len(coverage),
            "unique_normalized_source_records": len(sources),
            "citation_overlap_observations": len(carry),
        },
        "source_visibility_by_surface": source_visibility(sources),
        "source_visibility_by_system_and_language": system_language_profiles(sources),
        "matched_language_contrasts": paired_language_contrasts(sources),
        "chatgpt_google_conventional_overlap": citation_overlap(carry),
        "coder_agreement_P01_P08": reliability("pilot-second-coder-values.csv"),
        "coder_agreement_P09_P24": reliability("p09-p24-second-coder-values.csv"),
    }
    rendered = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Recalculate the paper's descriptive tables from the released coded records.

This script uses only the Python standard library and makes no network requests.
Version 1.2.0 uses consistent URL grouping and observed matches in partial captures.
Frozen input CSV files are preserved from version 1.1.0; see PROVENANCE.md.
Run from any directory with: python /path/to/reproduce_results.py
"""

from __future__ import annotations

import argparse
import csv
import json
import hashlib
import math
from collections import Counter, defaultdict
from pathlib import Path
from statistics import median


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"


def read_csv(name: str) -> list[dict[str, str]]:
    with (DATA / name).open("r", encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def collapse_identical_surface_records(rows):
    """Use one URL per query-language-system cell; preserve both surface memberships.

    This aggregation does not change code values. Incompatible codes fail closed
    and require an author decision rather than automatic recoding.
    """
    groups = defaultdict(list)
    code_fields = ("publisher_sector", "geographic_reach", "source_language",
                   "local_relevance_strict", "local_relevance_inclusive", "topical_relation",
                   "publisher_location", "conventional_top10_presence", "access_status")
    for row in rows:
        groups[(row["cell_id"], row["normalized_url"])].append(row)
    collapsed = []
    for key, group in groups.items():
        for field in code_fields:
            if len({r[field] for r in group}) != 1:
                raise ValueError(f"Conflicting {field} codes at {key}; human decision required")
        merged = dict(group[0])
        memberships = {role for r in group for role in r["source_role"].split(";")}
        merged["visible_surface"] = ";".join(sorted(memberships))
        merged["source_role"] = merged["visible_surface"]
        merged["input_source_ids"] = ";".join(r["source_id"] for r in group)
        collapsed.append(merged)
    return collapsed


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
                    # The grouped analysis has one row per normalized URL per cell.
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


def citation_overlap(carry_rows, source_rows):
    """Verify matches from preserved URL sets; never inherit page-complete flags.

    None of the available capture records documents ten identifiable positions.
    The URL sets contain 0-9 conventional URLs per cell and no ten-position rank
    mapping. Original input tags and classifications remain unchanged on disk.
    """
    result = {}
    for language in ("English", "Filipino"):
        per_query = []
        for row in [r for r in carry_rows if r["language"] == language]:
            pair = row["pair_id"]
            chat = {r["normalized_url"] for r in source_rows if r["pair_id"] == pair and r["language"] == language and r["system"] == "ChatGPT_Search"}
            conv = {r["normalized_url"] for r in source_rows if r["pair_id"] == pair and r["language"] == language and "google_conventional" in r["source_role"]}
            if len(conv) >= 10:
                raise ValueError("New capture evidence needs review; do not reuse the all-partial assumption")
            matches = len(chat & conv)
            if matches != int(row["overlap_count"]):
                raise ValueError(f"Preserved URL sets disagree with overlap count for {pair}/{language}")
            per_query.append({"pair_id": pair, "original_capture_status": row["conventional_capture_status"],
                              "analysis_capture_status": "partial_no_ten_position_record",
                              "identifiable_conventional_urls": len(conv), "chatgpt_citation_urls": len(chat),
                              "observed_matches": matches, "citation_urls_not_observed": len(chat)-matches})
        citations = sum(r["chatgpt_citation_urls"] for r in per_query)
        matches = sum(r["observed_matches"] for r in per_query)
        result[language] = {"observations": len(per_query), "verified_exact_captures": 0,
                            "partial_captures": len(per_query), "citation_urls": citations,
                            "observed_matches": matches, "citation_urls_not_observed": citations-matches,
                            "observed_match_pct": pct(matches,citations), "per_query": per_query}
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


def batch_totals(filename: str) -> dict:
    rows = read_csv(filename)
    fields = [k.removeprefix("coder_1_") for k in rows[0] if k.startswith("coder_1_")]
    disagreements = [sum(r["coder_1_"+f] != r["coder_2_"+f] for f in fields) for r in rows]
    pairs = len(rows) * len(fields)
    return {
        "coding_records": len(rows), "fields_per_record": len(fields),
        "field_pairs": pairs, "matching_field_pairs": pairs-sum(disagreements),
        "field_disagreements": sum(disagreements),
        "overall_exact_agreement_pct": round(100*(pairs-sum(disagreements))/pairs, 2),
        "records_with_all_fields_agreeing": sum(n == 0 for n in disagreements),
        "records_with_any_disagreement": sum(n > 0 for n in disagreements),
    }


def collection_coverage(coverage, overlap):
    result = {}
    for system in ("ChatGPT_Search", "Google_Search"):
        for language in ("English", "Filipino"):
            rows = [r for r in coverage if r["system"] == system and r["language"] == language]
            allowed = {"complete", "complete_visible", "complete_conventional_only_ai_missing"}
            if any(r["completion_status"] not in allowed for r in rows):
                raise ValueError("Unreviewed completion status in frozen coverage records")
            google = system == "Google_Search"
            result[f"{system} / {language}"] = {
                "cells": len(rows), "answer_or_page_observed": len(rows),
                "verified_exact_conventional_captures": overlap[language]["verified_exact_captures"] if google else None,
                "partial_conventional_captures": overlap[language]["partial_captures"] if google else None,
                "ai_overview_visible": sum(r["ai_overview_status"].startswith("verified_visible") for r in rows) if google else None,
            }
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--output", type=Path, help="Write JSON results to this path instead of stdout")
    mode.add_argument("--check", action="store_true", help="Compare recalculation with results/reproduced-results.json without changing files")
    args = parser.parse_args()

    hashes = json.loads((ROOT / "input-sha256.json").read_text(encoding="utf-8"))
    for name, expected in hashes.items():
        actual = hashlib.sha256((DATA / name).read_bytes()).hexdigest()
        if actual != expected:
            raise ValueError(f"Input hash mismatch for {name}; review the changed evidence")

    released_sources = read_csv("full-24-pair-source-table-adjudicated.csv")
    sources = collapse_identical_surface_records(released_sources)
    coverage = read_csv("full-24-pair-cell-coverage.csv")
    carry = read_csv("full-24-pair-citation-carry-through-adjudicated.csv")
    overlap = citation_overlap(carry, sources)
    result = {
        "audit_counts": {
            "frozen_coding_records": len(released_sources),
            "duplicate_cross_surface_records_grouped": len(released_sources)-len(sources),
            "query_language_system_combinations": len(coverage),
            "unique_normalized_source_records": len(sources),
            "analysis_unit": "unique normalized URL per query-language-system cell",
            "citation_overlap_observations": len(carry),
        },
        "source_visibility_by_surface": source_visibility(sources),
        "source_visibility_by_system_and_language": system_language_profiles(sources),
        "matched_language_contrasts": paired_language_contrasts(sources),
        "collection_coverage": collection_coverage(coverage, overlap),
        "chatgpt_google_conventional_overlap": overlap,
        "coder_agreement_P01_P08": reliability("pilot-second-coder-values.csv"),
        "coder_agreement_P09_P24": reliability("p09-p24-second-coder-values.csv"),
        "coding_batch_totals_P01_P08": batch_totals("pilot-second-coder-values.csv"),
        "coding_batch_totals_P09_P24": batch_totals("p09-p24-second-coder-values.csv"),
    }
    rendered = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.check:
        expected = json.loads((ROOT / "results/reproduced-results.json").read_text(encoding="utf-8"))
        if expected != result:
            changed = sorted(k for k in set(expected) | set(result) if expected.get(k) != result.get(k))
            raise SystemExit("Reproduction differs in: " + ", ".join(changed))
        print("Reproduction matches results/reproduced-results.json; input checksums verified.")
    elif args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()

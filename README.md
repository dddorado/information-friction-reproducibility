# Local Source Visibility in Generative Search — reproducibility materials

Version **1.2.0**, 16 October 2026. Materials for *Local Source Visibility in Generative Search: A Paired Audit of English and Filipino Queries in the Philippines* by Dan Anthony Dorado.

The study compares 24 matched English–Filipino information needs, four Philippine locations, ChatGPT Search and Google Search. This repository supports recalculation from frozen coded records. It does not reconstruct original interface behavior or permit independent recoding of every source.

## Reproduce

Use **Python 3.10 or later**. Only the standard library is used; no package installation, network connection or API key is needed. From the repository folder:

```text
python reproduce_results.py --check
```

This verifies nine input checksums, recalculates results and compares them with `results/reproduced-results.json` without changing files. A mismatch exits unsuccessfully. Input and expected-output paths are relative to the script, so invocation by absolute path from another folder also works.

To print results or save a separate copy:

```text
python reproduce_results.py
python reproduce_results.py --output recalculated-results.json
```

Do not overwrite expected results to hide a mismatch. Investigate changed inputs or procedures. `.gitattributes` preserves LF line endings so byte-level hashes agree across operating systems.

## Map to the paper

| Result | JSON section |
|---|---|
| Table 1: coverage and visible panels | `collection_coverage` |
| Table 2: local relevance by exclusive category | `source_visibility_by_surface` |
| Pooled language/system profiles | `source_visibility_by_system_and_language` |
| Table 3: matched language contrasts | `matched_language_contrasts` |
| Table 4: observed citation matches and per-query capture counts | `chatgpt_google_conventional_overlap` |
| Table 5: agreement/kappa | `coder_agreement_P01_P08`, `coder_agreement_P09_P24` |
| Initial agreement/disagreement totals | `coding_batch_totals_P01_P08`, `coding_batch_totals_P09_P24` |

Expected checks: **561 coding records → 533 distinct cell–URL records** (182 ChatGPT, 351 Google); 28 duplicate cross-surface representations grouped; 49 shared Google URLs within cells. All 48 conventional captures are partial. The archive establishes 13/90 English and 5/92 Filipino citation matches; **164 citations remain unobserved**, not proven absent. Four matched comparisons have median difference zero. Initial P01–P08 agreement is 69.10% (1,250/1,809 field pairs), with 559 disagreements.

## Complete inventory

Every retained file supports calculation, interpretation or provenance. Submission drafts, duplicate pilot subsets, stale summary exports, empty correction tables and working caches are excluded.

| File | Purpose |
|---|---|
| `reproduce_results.py` | Calculates reported summaries and checks inputs/expected results |
| `input-sha256.json` | SHA-256 of the nine frozen CSVs |
| `results/reproduced-results.json` | Single expected numerical output |
| `data/full-24-pair-source-table-adjudicated.csv` | 561 source/coding records, final classifications and URLs |
| `data/full-24-pair-cell-coverage.csv` | 96 cells and interface completion/panel metadata |
| `data/full-24-pair-citation-carry-through-adjudicated.csv` | 48 historical overlap/capture records, cross-checked against URL sets |
| `data/pilot-second-coder-values.csv` | Original paired/adjudicated values for 201 P01–P08 records |
| `data/p09-p24-second-coder-values.csv` | Original paired/adjudicated values for 360 P09–P24 records |
| `data/queries.csv` | 24 bilingual pairs, location/topic and equivalence status |
| `data/P01-P08-adjudication-decisions.csv` | 559 human-confirmed field decisions and rationales |
| `data/p09-p24-adjudication.csv` | Historical disagreement/exception decisions and rationales |
| `data/p09-p24-logic-corrections.csv` | 12 later consistency corrections |
| `codebook.md` | Coding rules, field guide and current analysis-unit interpretation |
| `P01-P08-codebook-addendum.md` | Preserved dated frozen-evidence clarification |
| `PROVENANCE.md` | Collection, human/AI roles, correction sequence and limits |
| `CITATION.cff` | Dataset citation and version |
| `.gitattributes` | Stable line endings for reproducible hashes |
| `.gitignore` | Excludes caches and ad hoc recalculation output |
| `README.md` | Run instructions and this inventory |

## Version and limits

Version 1.2.0 replaces mixed Google URL grouping and the superseded exact-overlap analysis. The nine retained CSVs are byte-identical to their Git objects in preceding commit `e44e609e053a4d3c0e7c92c53e57c7afdbeece31`; no coding judgment changes. Historical completeness/absence and pipeline-status labels remain in frozen inputs but are superseded for current analysis. See the codebook and provenance record. Prior release files remain in Git history.

No entropy, category-selection model, causal test, exclusion sensitivity model or repeated-run model is implemented. These selected cases and one retained observation per cell cannot establish causal language effects, national prevalence, source quality or internal retrieval.

## Access, rights and citation

Full platform answers, screenshots and raw capture logs are withheld because redistribution rights were not established. Permission to analyze exports is confirmed; that does not establish redistribution rights. Evidence paths identify the private study archive, not missing repository dependencies. Linked sites may change.

No separate data/software reuse license has been assigned; public access does not transfer third-party rights. Cite the paper and this repository version using `CITATION.cff`, the version tag or exact commit. This repository is not an institutional ethics determination or journal approval.

# Reproducibility materials for *Measuring Source Visibility in Generative Search*

This repository contains the coded data and analysis materials used for the paper's descriptive results. The study compares 24 matched English–Filipino local-information query pairs across ChatGPT Search and Google Search in four Philippine cities. The main collection was made on 8 October 2026.

## What this release supports

The released files support recalculating the source-visibility summaries, matched-pair language contrasts, ChatGPT-to-Google conventional-result overlap, and coder-agreement statistics reported in the paper. The source table has one row per unique normalized URL within a query–language–system combination. Paired coder values are supplied for the 201-record P01–P08 batch and the 360-record P09–P24 batch.

This is an analysis release based on coded records. It does not allow a reader to repeat the original searches or independently recode every page from the raw captures. Full platform answer text, screenshots, and raw capture logs are not included because redistribution rights for that material were not established. The source URLs and coded metadata are retained so readers can inspect the records, subject to the rights and availability of the linked sites.

## Reproduce the reported summaries

Requirements: Python 3.10 or later. The script uses only the Python standard library and makes no network requests.

From this repository's root directory, run:

```sh
python reproduce_results.py
```

To save the output as JSON:

```sh
python reproduce_results.py --output results/reproduced-results.json
```

The output includes:

- audit counts and source visibility by surface and by system/query language;
- strict and inclusive matched English–Filipino contrasts for each system;
- exact and partial ChatGPT citation overlap with Google conventional results; and
- exact agreement and Cohen's kappa for each coded field in both coding batches.

The script reads only the adjudicated source table, cell coverage table, citation-overlap table, and paired coder-value files in `data/`.

## File guide

| File | Purpose |
|---|---|
| `codebook.md` | Units, coding fields, definitions, and decision rules |
| `data/queries.csv` | The 24 matched query pairs |
| `data/full-24-pair-source-table-adjudicated.csv` | Final source-level records and adjudicated codes |
| `data/full-24-pair-cell-coverage.csv` | Query–language–system coverage and capture completeness |
| `data/full-24-pair-cell-results-adjudicated.csv` | Adjudicated cell-level result counts |
| `data/full-24-pair-citation-carry-through-adjudicated.csv` | ChatGPT citation overlap with Google conventional results |
| `data/full-24-pair-source-role-summary-adjudicated.csv` | Source-role totals used in the results |
| `data/pilot-second-coder-values.csv` | Paired coder values for P01–P08 (201 records) |
| `data/p09-p24-second-coder-values.csv` | Paired coder values for P09–P24 (360 records) |
| `data/p09-p24-adjudication.csv` | Field-level adjudication decisions and rationales for P09–P24 |
| `data/p09-p24-audit-corrections.csv` | Post-adjudication evidence-audit corrections |
| `data/p09-p24-logic-corrections.csv` | Strict/inclusive rule-consistency corrections |
| `reproduce_results.py` | Standard-library script for recalculating the reported summaries |

The `raw_capture_file` values in the coverage table refer to the study archive. The referenced raw capture files are not part of this public release.

## Rights and citation

No separate open-data or software license is assigned to this release. Public access does not transfer rights in linked pages or third-party platform content. Please cite the paper and this repository when using the released coded data. See `CITATION.cff` for the repository citation metadata.

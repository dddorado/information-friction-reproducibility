# Source codebook and released field guide

Status: author-attested as appropriate for the coding. All 561 frozen coding records have paired coder values and adjudicated outputs. Consistent within-cell URL grouping yields 533 source-analysis records. Reliability uses original P01–P08 (201-row) and P09–P24 (360-row) coding batches. These rules do not establish construct validity.

## Unit and record structure

- **Query--system--run record:** one submitted query under one interface and one run.
- **Source record:** one unique visible citation or source URL nested within a query--system--run record after URL normalization. The original displayed URL is retained separately.
- **No-citation/incomplete record:** a query--system--run with no visible citations, an incomplete answer panel, or an inaccessible result. These records remain in the coverage table and are not silently treated as zero local-source visibility.

## Fields and values

| Field | Allowed values or rule | Coding note |
|---|---|---|
| `publisher_sector` | government; academic; library/archive/museum; news; NGO/community; business; platform; other/unclear | Code the organization publishing or maintaining the cited page, not the topic discussed. Preserve the raw publisher label. |
| `geographic_reach` | city/community; regional; national; international; unclear | Code the apparent institutional or service remit. Do not infer reach from a country-code domain alone. |
| `source_language` | Filipino; English; another Philippine language; multilingual; other/unclear | Code the language of the cited document or page, separately from query language. For P01–P08, a language requires an explicit edition identifier or preserved page/document language; otherwise code `other/unclear`. The P01–P08 rule is detailed in `P01-P08-codebook-addendum.md`. |
| `publisher_location` | local to named place; elsewhere in Philippines; outside Philippines; unclear | Record location separately from geographic reach. |
| `topical_relation` | direct; indirect; absent; unclear | Direct means the page provides evidence about the named place, institution, event, or issue. |
| `local_relevance_strict` | yes/no/unclear | Yes only when direct topical relation is present and the source has local or Philippine grounding. |
| `local_relevance_inclusive` | yes/no/unclear | Yes when the source provides directly documented evidence about the named Philippine place or institution, even if the publisher is external. |
| `conventional_top10_presence` | present/absent/not observed | `Present` requires an exact normalized-URL match. `Absent` requires ten identifiable conventional positions and no match. If fewer than ten identifiable results were preserved, or capture was missing/incomplete, an unmatched URL is `not observed`. |
| `citation_status` | cited-and-top10; cited-outside-top10; cited-not-observed; top10-not-cited; neither observed; not_yet_coded | Derive only after both visible source sets are available, URLs are normalized, and capture completeness is known. `cited-not-observed` is used when the citation is unmatched in a partial capture. `not_yet_coded` marks a pending value in working files. |
| `access_status` | accessible; redirected; blocked; paywalled; unclear | Preserve the status; do not discard inaccessible records before reporting missingness. |

## Decision rules

1. Do not infer source quality, authority, user trust, or internal retrieval from any code above.
2. Do not treat Filipino wording, a Philippine domain, or a local publisher as sufficient by itself for local relevance.
3. If publisher location, geographic reach, or topical relation cannot be established from the page or reliable metadata, code `unclear` and preserve the reason.
4. Code the same normalized source consistently within a run; retain duplicate displayed URLs in the raw capture.
5. Both coders independently coded the records in each batch before agreement was calculated. Disagreements require a separate adjudication record with original codes, rationale, and final decision; adjudication does not alter the initial reliability values.
6. The dated P01–P08 evidence addendum is a batch-specific clarification applied to the locked pilot pass. It does not retroactively alter P09–P24 coder values or their reported agreement. The addendum and its adjudication log are included in this release.

## Current coding status

The completed 24-pair dataset has metadata, mechanically normalized and adjudicated source tables, cell-coverage audits, paired coder fields for all 561 records, adjudication records, and adjudicated summaries in this release. The original P01–P08 reliability pass remains 69.10% exact agreement before adjudication; all 559 field disagreements were resolved to Coder 2's value in the post-comparison project-lead adjudication. The adjudicated values must not be described as coder consensus. Cohen's kappa is undefined where both coders used one category for every record. Because the completed collection contains one primary run per cell and is not a probability sample, language comparisons remain bounded observational contrasts rather than population estimates.

## Version 1.2.0 interpretation

Group Google records by `cell_id` and `normalized_url` before calculating shares, preserving both surface memberships. All nine classification fields must agree within a duplicate group; conflicts require human decisions. Categories are mutually exclusive: ChatGPT citation, Google AI Overview only, Google conventional only, Google shared. Google cell denominators use its union of surfaces. A URL in a different cell remains a separate observation.

All conventional captures are partial because ten identifiable positions are undocumented. Frozen `absent` and `complete_exact_urls` values are historical labels, not current absence/completeness evidence. Agreement for `conventional_top10_presence` describes original columns rather than capture correctness. Current overlap uses URL intersections. No classification or initial coder value changes.

Strict/inclusive shares include unclear records in denominators; only yes counts positively. Matched contrasts give each need equal weight; pooled shares weight by URL count. Undefined shares are not replaced by zero. Undefined kappa is JSON `null`.

## Additional field guide

| Fields | Meaning |
|---|---|
| `pair_id`, `cell_id`, `source_id` | Stable need, query–language–system and frozen coding-record identifiers |
| `language`, `system`, `query` / `query_text` | Submitted query language, interface and wording |
| `normalized_url`, `displayed_url` | URL matching key and preserved visible spelling |
| `source_role`, `visible_surface` | ChatGPT citation, Google AI Overview or conventional; semicolon-separated memberships when shared |
| `coder_1_*`, `coder_2_*` | Original pre-adjudication codes used for agreement |
| `adjudicated_*` | Worksheet final codes; later logic corrections may apply; consolidated source table supplies final source analysis |
| `field`, coder values, `adjudicated_value`, rationale/evidence columns | Field-level decision trace; `record_type` distinguishes disagreements and exceptions |
| `original_adjudicated_value`, `corrected_value`, `correction_reason` | Later consistency-correction history |
| `raw_visible_source_mentions`, `within_cell_duplicate_mentions` | Historical mentions before normalization, not independent source counts |
| `unique_normalized_sources`, surface counts | Historical cell counts; current denominators are independently grouped from source URLs |
| `completion_status`, `ai_overview_status` | Observed page/answer response and AI-panel availability; complete page does not establish complete ranked capture |
| `visible_url_capture_status`, `conventional_capture_status` | Historical labels superseded by all-partial interpretation |
| `coding_status`, `coder_status`, `adjudication_status`, `agreement_status` | Historical workflow labels; coverage can still say pending despite later human-confirmed coding |
| `chatgpt_visible_citations`, `overlap_count`, overlap percentage/count fields | Historical summaries; current values are recalculated and match counts cross-checked |
| `raw_capture_file`, `evidence_basis`, `evidence_consulted` | Private-archive references, not public runtime dependencies |
| `collection_exception`, `unresolved_visible_source_mentions` | Missing panel/URL conditions retained without imputation |
| `adjudicator`, `adjudication_date` | Preserved attribution/date; AI-assisted-review wording retained alongside subsequent human-validation attestation |
| Query `location`, `domain`, `equivalence_status` | Case setting, topic and author-attested bilingual-equivalence workflow |

See `PROVENANCE.md` for collection conditions, attestations and correction sequence. The dated P01–P08 addendum is preserved as a historical record.

P01–P08 worksheets/decision logs use batch IDs such as `S005`, while the consolidated source table uses IDs such as `FULL-S005`. Join these files using the preserved `(cell_id, normalized_url)` key; do not assume identifiers from different files are interchangeable. P09–P24 correction logs use consolidated source IDs.

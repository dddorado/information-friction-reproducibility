# Draft Source Codebook

Status: author-attested as appropriate for the coding. All 561 source-surface records have paired coder values and adjudicated outputs. Reliability is reported separately for the P01–P08 (201-row) and P09–P24 (360-row) coding batches. This codebook defines the rules but is not, by itself, evidence of construct validity.

## Unit and record structure

- **Query--system--run record:** one submitted query under one interface and one run.
- **Source record:** one unique visible citation or source URL nested within a query--system--run record after URL normalization. The original displayed URL is retained separately.
- **No-citation/incomplete record:** a query--system--run with no visible citations, an incomplete answer panel, or an inaccessible result. These records remain in the coverage table and are not silently treated as zero local-source visibility.

## Fields and values

| Field | Allowed values or rule | Coding note |
|---|---|---|
| `publisher_sector` | government; academic; library/archive/museum; news; NGO/community; business; platform; other/unclear | Code the organization publishing or maintaining the cited page, not the topic discussed. Preserve the raw publisher label. |
| `geographic_reach` | city/community; regional; national; international; unclear | Code the apparent institutional or service remit. Do not infer reach from a country-code domain alone. |
| `source_language` | Filipino; English; another Philippine language; multilingual; other/unclear | Code the language of the cited document or page, separately from query language. |
| `publisher_location` | local to named place; elsewhere in Philippines; outside Philippines; unclear | Record location separately from geographic reach. |
| `topical_relation` | direct; indirect; absent; unclear | Direct means the page provides evidence about the named place, institution, event, or issue. |
| `local_relevance_strict` | yes/no/unclear | Yes only when direct topical relation is present and the source has local or Philippine grounding. |
| `local_relevance_inclusive` | yes/no/unclear | Yes when the source provides directly documented evidence about the named Philippine place or institution, even if the publisher is external. |
| `conventional_top10_presence` | present/absent/not observed | “Absent” means not found in the captured top ten; “not observed” is reserved for a missing or incomplete conventional capture. |
| `citation_status` | cited-and-top10; cited-outside-top10; top10-not-cited; neither observed | Derive only after both visible source sets are available and URLs are normalized. |
| `access_status` | accessible; redirected; blocked; paywalled; unclear | Preserve the status; do not discard inaccessible records before reporting missingness. |

## Decision rules

1. Do not infer source quality, authority, user trust, or internal retrieval from any code above.
2. Do not treat Filipino wording, a Philippine domain, or a local publisher as sufficient by itself for local relevance.
3. If publisher location, geographic reach, or topical relation cannot be established from the page or reliable metadata, code `unclear` and preserve the reason.
4. Code the same normalized source consistently within a run; retain duplicate displayed URLs in the raw capture.
5. A second coder must independently code a stratified subset before agreement is reported. Disagreements require an adjudication record with the original codes, rationale, and final decision.

## Current coding status

The completed 24-pair dataset has raw captures, metadata, mechanically normalized source tables, cell-coverage audits, paired coder fields for all 561 records, adjudication records, and adjudicated summaries in `data/processed/` and `notes/`. Descriptive summaries should use the adjudicated values while reporting the batch- and field-specific agreement results. Because the completed collection contains one primary run per cell and is not a probability sample, language comparisons remain bounded observational contrasts rather than population estimates.

---
doc_id: WSC-DDR-002
title: WasteWise Scan shared scan record format
project: WasteWise Scan
doc_type: Design decision record
version: "0.2"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First proposal of a scan record shared with WasteWise-ml, for joint review
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002); option 1 decided for WasteWise Scan (WSC-DDR-003 D12); WasteWise-ml adoption listed as a cross-repo action
---

# 0002: Shared scan record format

- **Date:** 2026-09-25
- **Status:** accepted for WasteWise Scan (decided by Amish, 2026-09-25: go with recommendation). Adoption by WasteWise-ml is a cross-repo action; field questions 2 and 3 below remain open.

## Context

Requirement R13 asks that low-confidence scans hand off to WasteWise-ml and that scan records use a shared, documented format. WasteWise-ml labels items with the taxonomy in its `ml/data/taxonomy.yaml` (version 0.2, 2026-09-25): a material class, a grade (for plastics, the resin code, for example "PET (1)" or "other or unknown (7)"), and two non-class outputs, "unsure" and "hazard". WasteWise Scan produces a resin, a confidence, a local price grade and an eight-band spectrum. ReflowEconomy will later want the resin of what it buys.

This note is written in the WasteWise Scan repo only. The WasteWise-ml repo was read and not changed. Amish accepted option 1 on 2026-09-25; the WasteWise-ml side has still to adopt the same fields in its own repo.

## Options considered

1. **One shared record for both tools (recommended).** Both write the same fields; each leaves the fields it cannot fill empty. Combining a photo and a scan of the same item is a join on `pair_id`.
2. **Separate records with a mapping table.** Each tool keeps its own format and a converter joins them. Less coordination now, more drift later.
3. **Adopt an external schema.** No open schema for field resin scans was found in this session; this can be revisited.

## Proposed record

Recommendation: option 1, with the fields in Table 1. Exports are CSV (one row per record, spectrum as eight columns) and JSON Lines (one object per line). Labels reuse the WasteWise-ml taxonomy strings exactly, so no mapping is needed.

*Table 1. Shared scan record, version 0.1.*

| Field | Type | Filled by | Meaning |
| --- | --- | --- | --- |
| `record_version` | text | both | "0.1" |
| `source` | text | both | "wws" (WasteWise Scan) or "wml" (WasteWise-ml) |
| `device_id` | text | both | Short random ID set at first start; no personal data |
| `record_id` | text | both | `device_id` plus a sequence number, unique per device |
| `time_utc` | text | both | ISO 8601, UTC, to the second |
| `site_id` | text | both, optional | The price table in use (cooperative or buyer site); set by the partner |
| `pair_id` | text | both, optional | Same value on a photo and a scan of the same item, entered or scanned by the user; empty if unpaired |
| `material_class` | text | both | Taxonomy class; WasteWise Scan writes "plastic" or leaves it empty for "unknown" |
| `grade` | text | both | Taxonomy grade, for example "PET (1)", "PP (5)", "other or unknown (7)" |
| `output` | text | both | "answer", "unsure" or "hazard"; WasteWise Scan never writes "hazard" |
| `confidence` | number | both | 0 to 1 |
| `price_grade` | text | both, optional | Local grade from the site price table, for example "A" |
| `model_version` | text | both | Classifier or model version |
| `wws_bands_nm` | list of 8 numbers | WasteWise Scan | 850, 940, 1050, 1200, 1300, 1450, 1550, 1650 |
| `wws_reflectance` | list of 8 numbers | WasteWise Scan | Dark-subtracted signal divided by the last white reference |
| `wws_dark_v` | number | WasteWise Scan | Mean dark level, a sunlight indicator (see WSC-CAL-001, D) |
| `wws_cal_id`, `wws_temp_c` | number | WasteWise Scan | White reference used, and board temperature |
| `wml_image_ref` | text | WasteWise-ml | File name of the consented photo, if kept |

On the scanner, each record is stored in a fixed 64-byte binary form (time, sequence, result code, confidence, price grade, flags, pair ID, eight 32-bit reflectance values, dark level, calibration ID, temperature, classifier version and a CRC-16). WSC-CAL-001 section G sizes the log from this. The CSV and JSON Lines exports are generated from it.

## Decision

Decided by Amish, 2026-09-25: go with recommendation. WasteWise Scan uses option 1, one shared record with the fields in Table 1 and a `pair_id` join (recorded in WSC-DDR-003 D12). Questions still open, with no recommendation made:

1. Whether WasteWise-ml accepts the shared field names and the `pair_id` join (cross-repo action; the WasteWise-ml side decides in its own repo).
2. How `pair_id` is created in the field: typed digits, a sticker, or the phone scanning a code on the scanner screen. Proposed, awaiting Amish.
3. Whether spectra from consented scans join the WasteWise-ml field dataset, and under which license and ownership terms (WasteWise-ml R14). Proposed, awaiting Amish.

## Consequences

- WasteWise-ml is asked to add the same fields on its side, in its own repo and session (cross-repo action in `docs/REVIEW.md`).
- R13 stays "at risk" in WSC-CAL-001 until WasteWise-ml adopts the format.

---
doc_id: WSC-REQ-001
title: WasteWise Scan requirements
project: WasteWise Scan
doc_type: Requirements
version: "0.2"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-24'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: First measurable requirements for TRL 2
---

# WasteWise Scan requirements

These are first-pass requirements for the concept. Targets are proposals for review, to be checked by calculation at TRL 3 and revised after co-design with users. Status is the concept estimate from WSC-PRC-001; **R1 and R12 are not met or not shown to be met**, and R3 and R10 are unverified.

Table 1. Requirements.

| ID | Requirement | Target | Concept status | Verification (TRL 3 or later) |
| --- | --- | --- | --- | --- |
| R1 | Identify common resins | PET, HDPE, PP, PS and PVC, plus "other" and "unknown"; 95 % or more correct on clean, dry, non-black items of 1 mm wall or more | **Not shown.** Plausible from prior work with discrete NIR bands; PE versus PP near the 1,700 nm band edge is the main risk | Band selection study on published reference spectra; later a labeled item set of 200 or more |
| R2 | Fast result | 1.5 s or less from button press to result | Met by estimate (about 0.6 s) | Timing budget |
| R3 | Fail safe on unreadable items | Black, dark, wet or very thin items read "unknown"; wrong resin shown for 2 % or fewer of all scans | Unverified; black items read unknown by design | Confidence threshold study; later item test |
| R4 | Work in sunlight | Same result indoors and in direct sun up to 100 klx when the shroud is pressed to the item | Met by design (shroud plus dark-frame subtraction), unverified for curved items | Stray light estimate |
| R5 | Last a shift | 8 h or more at 4 scans per minute on one charge; USB-C charging | Met by estimate (about 17 h) | Power budget |
| R6 | One-handed and light | 250 g or less; body no larger than 170 x 65 x 40 mm (6.7 x 2.6 x 1.6 in) plus shroud | Met by estimate (about 170 g; 160 x 62 x 34 mm) | Massing model, then weighing |
| R7 | Readable by anyone | Result as resin code, name, color and icon, legible at arm's length in direct sun; local language; no reading needed to use | Met by design with a 1.9 in IPS display; sunlight legibility unverified | Design review with users |
| R8 | Local price grade | Shows a price grade from a table the user or cooperative edits on the device; works offline | Met by design | Design review |
| R9 | Log scans | 10,000 or more scans stored on the device with time, result, confidence and spectrum; export as CSV over USB; no cloud needed | Met by estimate (about 64 B per scan, under 1 MB) | Storage calculation |
| R10 | Rugged | Survives 1.2 m (4 ft) drop onto concrete; IP54 target; 0 to 45 °C | Unverified | Design review, later drop and spray tests |
| R11 | Stay calibrated | White reference check in 10 s or less using the calibration cap; warns when a check is overdue or drift exceeds 5 % | Met by design | Design review |
| R12 | Low cost | Parts cost $150 or less per unit; no custom PCB for the first build | **Not met** (about $163, 9 % over) | Priced BOM |
| R13 | Work with WasteWise-ml | Low-confidence scans hand off to WasteWise-ml; scan records use a shared, documented format | Met by design, format not yet defined | Interface note with WasteWise-ml |
| R14 | Eye-safe illumination | LED emission in the IEC 62471 exempt group; LEDs pulse only during a scan | Met by estimate (a few mW per LED, under 1 s) | Emission estimate from datasheets |

## Assumptions

- "Clean and dry" means rinsed or wiped items without labels over the scan spot. Real waste is dirtier; the classifier must reject rather than guess.
- About 10 to 15 % of items in a mixed post-consumer stream are black or very dark (estimate; varies strongly by region and should be measured with users).
- Four scans per minute is a busy spot-check pace, not every item: most items are sorted by eye and the scanner settles doubtful ones.
- Resin prices vary by city and season; the device stores grades (for example A, B, C, reject) and a local price list, not global prices.

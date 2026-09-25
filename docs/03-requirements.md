---
doc_id: WSC-REQ-001
title: WasteWise Scan requirements
project: WasteWise Scan
doc_type: Requirements
version: "0.3"
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
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3 status from WSC-CAL-001; R12 redefined per WSC-DDR-001 D2; R13 points to the draft record in WSC-DDR-002
---

# WasteWise Scan requirements

These are the requirements for the TRL 3 design. Status is from the calculation note WSC-CAL-001 (tags in brackets). **R4 and R7 are not met** on paper, R1 and R13 are at risk, and R3 and R10 cannot be verified at TRL 3. Targets stay proposals for co-design with users; the only target changed at this revision is R12, redefined by Amish's decision of 2026-09-25 (WSC-DDR-001, D2).

Table 1. Requirements.

| ID | Requirement | Target | Status at TRL 3 (WSC-CAL-001) | Verification (TRL 3 or later) |
| --- | --- | --- | --- | --- |
| R1 | Identify common resins | PET, HDPE, PP, PS and PVC, plus "other" and "unknown"; 95 % or more correct on clean, dry, non-black items of 1 mm wall or more | **At risk.** The 1,650 nm band reaches only the short edge of the 1,650 to 1,750 nm region on standard InGaAs (centroid about 1,628 nm) [B2]; signal-to-noise ratio of 450 or more in shade [C4] | Band study on published reference spectra; later a labeled item set of 200 or more |
| R2 | Fast result | 1.5 s or less from button press to result | Met: about 0.33 s [E2] | Timing budget |
| R3 | Fail safe on unreadable items | Black, dark, wet or very thin items read "unknown"; wrong resin shown for 2 % or fewer of all scans | Not verifiable at TRL 3. Black items fall well below the 0.08 reflectance threshold [C6]; the wrong-result rate needs item data | Confidence threshold study; later item test |
| R4 | Work in sunlight | Same result indoors and in direct sun up to 100 klx when the shroud is pressed to the item | **Not met** for clear and translucent items: light through the item is about 900 times the weakest signal and hand movement leaves an error several times the signal [D3]. Met by estimate for opaque items [D5] | Stray light estimate |
| R5 | Last a shift | 8 h or more at 4 scans per minute on one charge; USB-C charging | Met: about 22 h [F2] | Power budget |
| R6 | One-handed and light | 250 g or less; body no larger than 170 x 65 x 40 mm (6.7 x 2.6 x 1.6 in) plus shroud | Met: about 202 g, 222 g with cap; 160 x 62 x 34 mm [A1, A3] | Parametric model, then weighing |
| R7 | Readable by anyone | Result as resin code, name, color and icon, legible at arm's length in direct sun; local language; no reading needed to use | **Not met** in direct sun: about 1.6:1 contrast against about 3:1 needed; about 5.2:1 when shaded [I1, I2] | Contrast estimate; design review with users |
| R8 | Local price grade | Shows a price grade from a table the user or cooperative edits on the device; works offline | Met by design | Design review |
| R9 | Log scans | 10,000 or more scans stored on the device with time, result, confidence and spectrum; export as CSV over USB; no cloud needed | Met: about 131,000 scans in an 8 MB partition [G1] | Storage calculation |
| R10 | Rugged | Survives 1.2 m (4 ft) drop onto concrete; IP54 target; 0 to 45 °C | Not verifiable at TRL 3. Corner drop about 1,200 g; the cradle must hold the cell against about 550 N [J1, J2] | Design review, later drop and spray tests |
| R11 | Stay calibrated | White reference check in 10 s or less using the calibration cap; warns when a check is overdue or drift exceeds 5 % | Met by design; 5 % drift after about 12.5 °C of temperature change [J3] | Design review |
| R12 | Low cost | $150 or less per unit is the volume target; the first prototype is accepted at about $163 in parts; no custom PCB for the first build | Met for the prototype: $163.00 [K1]. The volume target cannot be shown without volume quotes | Priced BOM |
| R13 | Work with WasteWise-ml | Low-confidence scans hand off to WasteWise-ml; scan records use a shared, documented format | **At risk.** Hand-off designed; record format drafted in WSC-DDR-002, not yet agreed with WasteWise-ml | Interface note with WasteWise-ml |
| R14 | Eye-safe illumination | LED emission in the IEC 62471 exempt group; LEDs pulse only during a scan | Met by estimate: 3.9 W/m² at 200 mm against 100 W/m²; retinal 3.8 % of the limit [H2, H3] | Emission estimate, then datasheet values |

## Assumptions

- "Clean and dry" means rinsed or wiped items without labels over the scan spot. Real waste is dirtier; the classifier must reject rather than guess.
- About 10 to 15 % of items in a mixed post-consumer stream are black or very dark (estimate; varies strongly by region and should be measured with users).
- The first prototype's accepted cost of about $163 covers one scanner with its cap; the $150 volume target assumes quantity prices for LEDs and the photodiode (WSC-DDR-001, D2).
- Four scans per minute is a busy spot-check pace, not every item: most items are sorted by eye and the scanner settles doubtful ones.
- Resin prices vary by city and season; the device stores grades (for example A, B, C, reject) and a local price list, not global prices.

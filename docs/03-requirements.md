---
doc_id: WSC-PRS-001
title: WasteWise Scan product requirements and specifications
project: WasteWise Scan
doc_type: Product requirements and specifications
version: "0.8"
status: Draft
date: '2026-10-24'
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
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002); R4, R6, R11 and R12 restated per WSC-DDR-003; status from WSC-CAL-001 v0.2
- version: "0.5"
  date: '2026-10-02'
  author: Amish Chadha
  change: Status from WSC-CAL-001 v0.3 for the constructable design (WSC-DDR-004); R6 not met; R12 reported against the value-engineering target
- version: "0.6"
  date: '2026-10-02'
  author: Amish Chadha
  change: R6 and R13 status notes record Amish's decisions of 2026-10-02 (WSC-DEC-001); no status changed
- version: "0.7"
  date: '2026-10-02'
  author: Amish Chadha
  change: R6 restated for 2.0 mm shell walls (238 g, 258 g with cap); R1 note carries the paper band study; no status changed
- version: "0.8"
  date: '2026-10-24'
  author: Amish Chadha
  change: "Kit 1.8 upgrade: WSC-REQ-001 becomes the product requirements and specifications WSC-PRS-001; R1 to R14 migrated to PR-001 to PR-014 with the same targets, verification and status, each traced to a user requirement in WSC-URS-001, with tolerance and units; PR-015 (cell safety), PR-016 (buildable) and PR-017 (optical crosstalk, fix F1) added; statuses after fixes F1 to F3 of WSC-DEC-001 (0.64 s, 21.9 h, 239 g and 259 g with cap)"
---

# WasteWise Scan product requirements and specifications

What the scanner must do, each requirement traced to a user need in WSC-URS-001 (links in the generated traceability matrix WSC-RTM-001). This document replaces the requirements WSC-REQ-001 (kit 1.8, STANDARDS section 22): each old requirement R1 to R14 is now PR-001 to PR-014 with the same target, verification and status, and the old number in "Was". Status is from the calculation note WSC-CAL-001 (tags in brackets) for option A, the current design. **On paper, 8 of the 17 are met on paper or by design, PR-006 (mass) is not met (259 g with the cap against 250 g), PR-001, PR-007 and PR-013 are at risk, PR-003, PR-010, PR-015 and PR-017 are to verify at TRL 4, and PR-012 is over the value-engineering target.** Three fixes made in this revision under Amish's standing instruction of 2026-10-23 (WSC-DEC-001 F1 to F3) changed PR-002, PR-004, PR-005, PR-006, PR-010, PR-015 and PR-017. Targets remain proposals for review with the co-design partner (first candidate SWaCH, Pune; WSC-DEC-001).

Table 1. Product requirements and specifications.

| ID | Traces to | Category | Title | Requirement | Target | Tolerance | Units | Verification | Status | Was |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PR-001 | UR-001 | Performance | Identify common resins | The scanner shall name PET, HDPE, PP, PS and PVC, plus "other" and "unknown", on clean, dry, non-black items of 1 mm wall or more | 95 | min | % correct | Analysis, paper band study WSC-CAL-001 B4 to B7 (TRL 3); labelled item set of 200 or more (TRL 4) | At risk: 89.5 % with eight bands at 1.5 % band scatter, 96.7 % at 1.0 %; PE against PP 93 %; 1,650 nm band centroid 1,628 nm [B2, B4 to B7] | R1 |
| PR-002 | UR-002 | Performance | Fast result | Button press to result shall take no longer than the target | 1.5 | max | s | Analysis, timing budget WSC-CAL-001 E (TRL 3); timed at TRL 4 | Met on paper: 0.64 s with the four-cycle sequence of fix F2 [E2] | R2 |
| PR-003 | UR-003 | Software | Fail safe on unreadable items | Black, dark, wet or very thin items shall read "unknown"; a wrong resin shall be shown for no more than the target share of all scans | 2 | max | % of scans | Analysis of the black threshold WSC-CAL-001 C6 (TRL 3); confidence threshold study on items (TRL 4) | To verify at TRL 4: black items fall well below the 0.08 reflectance threshold [C6]; the wrong-result rate needs item data | R3 |
| PR-004 | UR-004 | Performance | Work in sunlight | With the shroud pressed to the item, the result in direct sun up to 100 klx shall match the indoor result; clear and translucent items are backed with the calibration cap, and the scanner shall refuse a result ("shade or back with cap") when its dark level shows light through an unbacked item | 0.5 | max | % of signal, ambient error | Analysis, stray light WSC-CAL-001 D (TRL 3); indoor and sun test (TRL 4) | Met on paper (estimate): 0.08 % on opaque items, 0.21 % on backed clear items with fix F2; unbacked clear items refused [D5 to D7]; rests on the assumed cap leak and ambient change (STEM S5) | R4 |
| PR-005 | UR-005 | Electrical | Last a shift | The scanner shall run a shift at 4 scans per minute on one charge and charge from USB-C | 8 | min | h | Analysis, power budget WSC-CAL-001 F (TRL 3); measured at TRL 4 | Met on paper: 21.9 h [F2] | R5 |
| PR-006 | UR-006 | Physical architecture | One-handed and light | Mass including the sun hood and the carried calibration cap shall not exceed the target; body no larger than 170 x 65 x 40 mm (6.7 x 2.6 x 1.6 in) plus shroud and hood | 250 | max | g | Analysis from the model volumes WSC-CAL-001 A (TRL 3); weighing at TRL 4 (WSC-DEC-001) | Not met: 239 g, 259 g with the cap (9 g over); body 160 x 62 x 34 mm [A1, A3] | R6 |
| PR-007 | UR-007 | Usability | Readable by anyone | The result shall show as resin code, name, colour and icon, legible at arm's length in direct sun, in the local language, with no reading needed to use | 3 | min | contrast ratio | Analysis, contrast WSC-CAL-001 I (TRL 3); design review with users | At risk: about 5.2:1 where the sun hood shades the screen; about 1.6:1 with the sun near the screen normal or over the open side [I3, I4] | R7 |
| PR-008 | UR-008 | Software | Local price grade | The scanner shall show a price grade from a table the user or cooperative edits on the device, offline | 1 | min | editable local table | Inspection of the design (TRL 3); design review with the cooperative | Met by design | R8 |
| PR-009 | UR-009, UR-017 | Software | Log scans | The scanner shall store scans on the device with time, result, confidence and spectrum and export them as CSV over USB, with no cloud needed | 10000 | min | scans | Analysis, storage WSC-CAL-001 G (TRL 3) | Met on paper: about 131,000 scans in an 8 MB partition [G1] | R9 |
| PR-010 | UR-010 | Physical architecture | Rugged | The scanner shall survive a drop onto concrete from the target height, meet IP54 and work from 0 to 45 C | 1.2 | min | m drop | Analysis of drop loads WSC-CAL-001 J (TRL 3); drop and spray tests (TRL 4) | To verify at TRL 4: corner drop about 1,200 g mean on an assumed 1 mm crush; the 11 x 10 mm cell strap (fix F3) carries the 869 N peak with a margin of 1.45 [J1, J2, J4] | R10 |
| PR-011 | UR-011 | Usability | Stay calibrated | A white reference check and an open-air crosstalk reading with the calibration cap shall take no longer than the target, with a warning when a check is overdue or drift exceeds 5 % | 10 | max | s | Inspection of the design and WSC-CAL-001 J3 (TRL 3) | Met by design: 5 % drift after about 12.5 C of change [J3] | R11 |
| PR-012 | UR-012 | Physical architecture | Low cost | Parts cost per unit against the value-engineering target, with no custom PCB for the first build | 150 | target | USD | Priced BOM, WSC-CAL-001 K (TRL 3) | Over target: USD 167.50, USD 17.50 over the USD 150 value-engineering target [K2] | R12 |
| PR-013 | UR-013, UR-017 | Software | Work with WasteWise-ml | Low-confidence scans shall hand off to WasteWise-ml; scan records shall use the shared, documented format of WSC-DDR-002 | 1 | min | shared record | Inspection, interface note with WasteWise-ml | At risk: record decided on this side (WSC-DDR-002 v0.4), not yet adopted by WasteWise-ml | R13 |
| PR-014 | UR-014 | Safety | Eye-safe illumination | LED emission shall stay in the IEC 62471 exempt group, the LEDs pulsing only during a scan, with a hardware limit on on-time | 100 | max | W/m2 at 200 mm | Analysis WSC-CAL-001 H (TRL 3); datasheet values and measurement (TRL 4) | Met on paper (estimate): 3.9 W/m2 at 200 mm; retinal 3.8 % of the limit [H2, H3] | R14 |
| PR-015 | UR-015 | Safety | Safe cell | The scanner shall use one protected 18650 cell from a named maker in a cradle and strap that hold it against the peak corner-drop load, charged only by the board charger and not above 45 C | 870 | min | N cell retention (peak) | Analysis WSC-CAL-001 J2, J4 (TRL 3); STEM S10, S17, S18; drop test at TRL 4 | To verify at TRL 4: the 11 x 10 mm strap (fix F3) carries 869 N at a bending margin of 1.45, on an assumed crush [J4] | |
| PR-016 | UR-016 | Physical architecture | Buildable by a local maker | The first prototype shall be built from bought modules, FDM-printed PETG and TPU parts, perfboard and screws, with through-hole soldering, hand tools and a drill | 0 | max | custom PCBs | Inspection of the build plan WSC-BLD-001 and the BOM (TRL 3) | Met by design (WSC-BLD-001; the 8.4 mm hole in the LED window of fix F1 needs a drill and an 8 mm diamond core drill) | |
| PR-017 | UR-001, UR-011 | Performance | Optical crosstalk | LED light reaching the detector without leaving through the item shall stay under the target share of the signal after the open-air reading, with a 10 % change of the window state between readings | 0.5 | max | % of signal | Analysis WSC-CAL-001 C5, C7, C8 and STEM S12 (TRL 3); wall-opacity coupon, open-air and dirty-window readings (TRL 4) | To verify at TRL 4: 0.003 % with the baffle through the glass on assumed leak values (fix F1; 10 % before the fix); the tube wall needs an opacity of 2 x 10⁻² or better [C8] | |

Categories: physical architecture, performance, materials, usability, packaging and transport, safety, electrical, software. Status: met on paper, met by design, at risk, not met, over target, withdrawn, to verify at TRL 4.

## Assumptions

- "Clean and dry" means rinsed or wiped items without labels over the scan spot. Real waste is dirtier; the classifier must reject rather than guess.
- About 10 to 15 % of items in a mixed post-consumer stream are black or very dark (estimate; varies strongly by region and should be measured with users).
- The first prototype's accepted cost of about USD 164 covers one scanner with its cap and sun hood; the USD 150 value-engineering target assumes quantity prices for LEDs and the photodiode (WSC-DDR-001, D2), and is the price a cooperative pays for a shared scanner (WSC-DEC-001).
- Four scans per minute is a busy spot-check pace, not every item: most items are sorted by eye and the scanner settles doubtful ones.
- Resin prices vary by city and season; the device stores grades (for example A, B, C, reject) and a local price list, not global prices.
- PR-006 counts the calibration cap because it is carried for backing clear items (decided by Amish, 2026-10-02).

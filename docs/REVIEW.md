# Review note: WasteWise Scan

## Session 2026-09-25: /populate to a strong TRL 2 (overnight batch)

### What was done

- `docs/01-problem.md` (WSC-PRB-001 v0.2): problem, prior work (Plastic Scanner, AS7265x, commercial NIR sorters and handhelds, black plastics), users and context, constraints, out of scope, open questions; co-design checklist kept.
- `docs/03-requirements.md` (WSC-REQ-001 v0.2): 14 measurable requirements (R1 to R14) with targets, concept status and planned verification; assumptions.
- `docs/02-concept.md` (WSC-PRC-001 v0.2): key sensor finding, how it works, numbered components, first-order numbers, design choices, safety, open questions.
- `cad/src/concept_media.py`: massing model of the handheld (shells, display board, LED ring, photodiode, amplifier board, window, shroud, 18650 cell, charger, button, calibration cap and PTFE disc), with a hand and an HDPE crate panel as context parts for scale.
- `media/`: `hero.png`, `concept-blueprint.png`, `.pdf` and `.svg`, `cutaway.png` (optical axis), `exploded.png` (callouts 1 to 13 matching the BOM), `flow.png` (item flow per 100 items, all values estimates), `model.glb` and `viewer.html`.
- `bom/bom.csv`: 15 lines with indicative prices, items 1 to 13 numbered to match the exploded view; `bom/bom-notes.md` with cost groups.
- `README.md`: hero image and links line before "## Problem"; Concept, Key components and Safety updated to the proposed concept.
- `docs/pdf/`: branded PDFs of the three controlled documents.

### Key results (estimates, to be checked at TRL 3)

| Quantity | Estimate | Requirement |
| --- | --- | --- |
| Scan time | about 0.6 s | R2 met |
| Battery life, one 3,000 mAh 18650 | about 17 h at about 0.5 W | R5 met |
| Mass | about 170 g (195 g with cap) | R6 met |
| Size | 160 x 62 x 34 mm plus 18 mm shroud | R6 met |
| Log capacity | 10,000 scans under 1 MB | R9 met |
| Items identified per 100 mixed items | about 78 (12 black, 10 low confidence) | R3 intent |
| Parts cost | about $163 | **R12 not met, 9 % over** |

Requirements not met or not shown:

- **R12 (cost) not met:** about $163 against $150. SWIR LEDs (about $62) and the InGaAs photodiode (about $30) are most of the cost.
- **R1 (resin accuracy) not shown:** plausible from Plastic Scanner prior work, but PE versus PP relies on features near 1,700 nm, at the edge of standard InGaAs.
- **R3, R4 on curved items, R7 sunlight legibility, R10 ruggedness: unverified.**

### Proposed, awaiting Amish

1. **Sensor approach (affects the scaffold's component list, not the pitch).** A: discrete NIR and SWIR LEDs with an InGaAs photodiode (covers the polymer bands). B: AS7265x only, as scaffolded (about 410 to 940 nm, misses the main bands, unlikely to meet R1). C: A plus AS7265x for color (about $70 more). Recommendation: A. The pitch still reads true ("low-cost multispectral sensor", "about a second"), so `project.yaml` pitch and problem are unchanged.
2. **Budget.** (a) Raise `budget_usd` to $175; (b) cut to six bands (drop 1,050 and 1,300 nm, saving about $18, to about $145) at some accuracy risk; (c) keep $150 as a volume target and accept about $163 for the prototype. Recommendation: (c) for now, then (b) if the band study at TRL 3 shows six bands suffice. `budget_usd` is unchanged.
3. Controller: LilyGO T-Display-S3-class board (no custom PCB) rather than a bare ESP32-S3 with a separate display.
4. Band set: 850, 940, 1,050, 1,200, 1,300, 1,450, 1,550 and 1,650 nm, to be confirmed on reference spectra.
5. Classifier: linear discriminant analysis or a small decision tree on the device first; share labeled data with Plastic Scanner and WasteWise-ml where licenses allow.
6. White PTFE reference in the storage cap as the calibration method.
7. One protected 18650 cell rather than a flat LiPo pouch.
8. First partner and region for co-design and the first price table.

### Safety concerns

- Misuse on hazardous, medical or chemical waste: the documents say the scanner must never be used to judge safety; keep this in any user-facing material and on the device's start screen.
- 18650 lithium-ion cell (about 11 Wh) used outdoors in heat: protected cell, no charging above 45 °C or in direct sun.
- Invisible SWIR LEDs: low power and short pulses, estimated IEC 62471 exempt group; confirm from datasheets.
- Wrong results can cost users money or contaminate bales: the design prefers "unknown" to a guess.

### Problems and notes

- **Sources were not checked live.** Web search and page fetches were unavailable in this session (search budget exhausted; fetches needed approval), so the inline citations in WSC-PRB-001 and WSC-PRC-001 were written from known references (Lau et al. 2020; Neo et al. 2023; Plastic Scanner; SparkFun AS7265x board; trinamiX; WRAP; WIEGO; ASTM D7611). Check each link and figure before release, especially the 58 % statistic, the trinamiX wavelength range and the ASTM URL.
- SWIR LED prices are the least certain number in the BOM.
- The legacy `cad/src/model.py` placeholder is untouched (TRL 3 work).
- The sibling repos WasteWise-ml and ReflowEconomy were read for context and not modified. The shared scan record format (R13) needs a joint note with WasteWise-ml.
- SwapCell is not used; a handheld does not need a 48 V pack.

### Recommended next step

Review this note and the media, then decide items 1 and 2. If approved, run `/advance-trl3` to select the band set on published reference spectra, estimate signal-to-noise and stray light, confirm the power and eye-safety numbers by calculation, and produce the parametric model and drawing sheet.

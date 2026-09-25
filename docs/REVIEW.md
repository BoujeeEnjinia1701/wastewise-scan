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

## Session 2026-09-25: TRL 3

Amish approved all TRL 2 recommendations on 2026-09-25 ("proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them."). This session advanced WasteWise Scan to TRL 3 and stopped there.

### What was done

- `docs/decisions/0001-trl2-review-decisions.md` (WSC-DDR-001 v0.1): D1 to D7 recorded as "Decided by Amish, 2026-09-25: go with recommendation"; O1 to O4 left open.
- `docs/decisions/0002-scan-record-format.md` (WSC-DDR-002 v0.1): proposed shared scan record for joint review with WasteWise-ml (field list, CSV and JSON Lines export, 64-byte on-device record). Written in this repo only; WasteWise-ml was read, not modified.
- `docs/01-problem.md`, `docs/02-concept.md`, `docs/03-requirements.md` revised to v0.3: cost constraint and R12 redefined per D2, design choices no longer "proposed", numbers replaced by WSC-CAL-001 values, citations corrected.
- `docs/04-calcs/01-sizing.md` (WSC-CAL-001 v0.1) and `docs/04-calcs/sizing.py`: mass, band coverage, signal and noise, window crosstalk, sunlight, timing, power, logging, eye safety, display contrast, drop and drift, cost; a status for every requirement. The script imports the model and reads the BOM and budget.
- `cad/src/model.py`: parametric build123d model (shells, shroud, window, LED holder with eight tilted LEDs, photodiode and baffle, amplifier board, display board, cell and cradle, button, calibration cap) exporting `cad/step/wastewise-scan-{assembly,top-shell,bottom-shell,shroud,led-holder,cal-cap}.step` and matching STL files for the printed parts.
- `cad/src/sheets.py` and `cad/drawings/WSC-DWG-001.{svg,pdf,png}`: general arrangement at Rev P1 (top and front views at 1:1, section A-A on the optical axis at 2:1, isometric, interface notes), marked "CONCEPT, NOT FOR FABRICATION" and "PRELIMINARY, NOT FOR FABRICATION". The concept sheet stays WSC-DWG-010, so DWG-001 was free.
- `bom/bom.csv`: 15 lines, all priced with a supplier or supplier type; item 5 now specifies the 47 kΩ gain. `bom/bom-notes.md` updated. Total $163.00 against `budget_usd` $150 (volume target).
- `cad/src/concept_media.py` now builds from `model.py`; all media re-rendered and checked (hero, blueprint, cutaway, exploded, flow, GLB and viewer). No `_views` folders remain.
- `project.yaml`: `trl: 3`, `trl_target: 3`, `trl_evidence` lists the docs, DDRs, CAL note and script, model, STEP and STL, drawing and BOM. Pitch and problem unchanged (REVIEW item 1 recommended no change). `README.md` matches.

### Requirements at TRL 3 (WSC-CAL-001, Table 2)

Two not met, two at risk, two not verifiable at TRL 3, eight met.

| Status | Requirements |
| --- | --- |
| Not met | **R4** (sunlight through clear or translucent items reaches the detector at about 900 times the weakest band signal; a 1 % change in ambient per 10 ms from hand movement leaves about 7.5 mV of error against 1.14 mV of signal; opaque items are fine at 0.13 %); **R7** (about 1.6:1 display contrast in 100 klx sun against about 3:1 needed; 5.2:1 shaded) |
| At risk | R1 (1,650 nm band clipped by the InGaAs cutoff: centroid about 1,628 nm, 31 % of its signal at 1,650 nm or above; PE versus PP unproven); R13 (record format drafted, not agreed) |
| Not verifiable at TRL 3 | R3 (wrong-result rate needs item data; black items fall well below the threshold); R10 (drop, IP54, temperature; corner drop about 1,200 g, cell cradle needs about 550 N) |
| Met | R2 (0.33 s), R5 (22.1 h), R6 (202 g, 222 g with cap), R8, R9 (about 131,000 scans), R11, R12 ($163.00 prototype), R14 (3.9 W/m² at 200 mm) |

Key numbers: signal-to-noise ratio 450 or more in shade on every band; 0.39 W average draw; 42 mJ of LED energy per scan; window crosstalk of the same order as the signal.

Changes forced by the calculations: transimpedance gain from 1 MΩ to 47 kΩ (sunlight through clear items would saturate 1 MΩ at about 23 V); each band reading between two dark readings; a short baffle tube around the photodiode. Mass rose from about 170 g to 202 g (shells from model volumes); scan time fell from about 0.6 s to 0.33 s; battery life rose from about 17 h to 22 h.

### Decisions recorded

D1 to D7 in WSC-DDR-001: discrete LEDs with an InGaAs photodiode (sensor option A); budget option (c), `budget_usd` kept at $150 as the volume target with about $163 accepted for the prototype and R12 redefined (six bands only if a band study shows they suffice; not yet shown, so eight bands stay); T-Display-S3 class controller; eight-band set; LDA or small decision tree classifier with shared data; PTFE white reference in the cap; one protected 18650 cell. The SwapCell interface v0.3 items and shared-pack pricing do not apply: WasteWise Scan uses no SwapCell pack.

### Proposed, awaiting Amish

1. **First partner and region (O1).** No recommendation; partners are picked per area later.
2. **Who the $150 volume target is for (O2).** No recommendation.
3. **Extended InGaAs band for PE versus PP (O3).** No recommendation yet; the next step is a band study on published reference spectra.
4. **Shared scan record (O4, WSC-DDR-002).** Recommendation: one shared record with a `pair_id` join; needs a joint review with the WasteWise-ml side.
5. **Clear items in sun (R4, new).** Options: (a) modulate the LEDs at about 2 kHz and demodulate synchronously, which rejects ambient changes but needs a faster ADC or an analog demodulator (a few dollars more); (b) instruct users to back clear items with the calibration cap or scan them in shade; (c) restate R4 to cover opaque items only. Recommendation: (b) for the first prototype and (a) studied on paper before any build; (c) only if (a) fails. This changes the R4 target or the user workflow, so it is Amish's.
6. **Display in direct sun (R7, new).** Options: (a) a printed visor over the display (about 5.2:1 when shaded, negligible cost); (b) a sunlight-readable reflective display such as a memory LCD (about $20 to $40 more, over budget); (c) restate R7 to "legible when shaded by the hand or visor". Recommendation: (a), keeping large color and icon cues.
7. **Window crosstalk (new).** Options: (a) an open-air reading in the calibration routine to subtract the crosstalk offset (firmware only); (b) extend the baffle through the glass with separate LED and detector windows (mechanical change); (c) an anti-reflection coated window (cost). Recommendation: (a) now, and (b) if the offset proves unstable with window dirt.

### Safety concerns

- Misuse on hazardous, medical or chemical waste: the scanner identifies resin only; keep this on the start screen and in all user material.
- 18650 lithium-ion cell (about 11 Wh) outdoors in heat, and about 550 N on the cell in a corner drop: protected cell, a firm cradle, no charging above 45 °C or in direct sun.
- Invisible SWIR LEDs: exempt by a wide margin in normal use (3.9 W/m² at 200 mm), but a stuck LED at the shroud rim could exceed 100 W/m² over long exposures; a hardware on-time limit is required.
- Wrong results can cost users money or contaminate bales, especially on clear items in sun (R4): the design prefers "unknown" to a guess.

### Other notes

- **Citations checked** with web search and fetch in this session: Lau et al. 2020 58 % figure confirmed through the ISWA report that cites it (the primary text was not readable); Neo et al. is 2022, not 2023 (corrected); the WIEGO page does not say waste pickers are "among the lowest-paid", so the sentence was reworded to what the page says; the ASTM link now points to the store page and the title was confirmed; the WRAP link returned 404 and was replaced by a WRAP page confirming that carbon black prevents NIR sorting; the trinamiX 1,450 to 2,450 nm range was confirmed from a fact sheet (its price level is still an estimate); Plastic Scanner's LED range, InGaAs detector and TU Delft origin were confirmed. The polymer band positions (1,150 to 1,250 and 1,650 to 1,750 nm) were not confirmed from Neo et al., which is paywalled; they remain to be checked against a reference spectrum source.
- LED powers, detector responsivity, display brightness and item reflectances are assumptions; they drive R1, R4 and R7.
- No existing TRL 4 material was found: `build-log/` holds only its README, and `electronics/` and `firmware/` are empty. Nothing was added to them.

### Recommended next step

Decide items 5 to 7 above, and name a partner and region when ready. Then a paper-only follow-up within TRL 3: a band study on published reference spectra (R1, O3, and whether six bands suffice) and the joint review of WSC-DDR-002 with WasteWise-ml. **TRL 4 is on hold by Amish's instruction**, and no TRL 4 work was started. For reference only, TRL 4 would need: measured LED spectra and powers and the photodiode's responsivity curve; a lab test article of the optical head scanning labeled resin chips, indoors and in sun; a display legibility check outdoors; a drop and spray check of printed shells; a test report (TST, `environment: lab`) and build log entries.

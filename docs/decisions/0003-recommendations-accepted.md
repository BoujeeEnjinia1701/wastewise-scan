---
doc_id: WSC-DDR-003
title: WasteWise Scan recommendations accepted
project: WasteWise Scan
doc_type: Design decision record
version: "0.2"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002); record every newly decided item, what changed, and what remains open
- version: "0.2"
  date: '2026-10-02'
  author: Amish Chadha
  change: Open items recorded as decided by Amish on 2026-10-02 (WSC-DEC-001)
---

# 0003: Recommendations accepted

- **Date:** 2026-09-25
- **Status:** accepted for items D8 to D12; items O1 to O3 and the two field questions of WSC-DDR-002 decided by Amish on 2026-10-02 (WSC-DEC-001)

This is the portfolio's "recommendations accepted" record (DDR-002 in most repos). In WasteWise Scan the number 0002 was already used by the shared scan record, WSC-DDR-002, so this record is WSC-DDR-003.

## Context

On 2026-09-25 Amish wrote: "i accept all your recommendations, go with them across all repos." Every item in `docs/REVIEW.md` and `docs/decisions/` that was marked "Proposed, awaiting Amish" and carried a recommendation is therefore decided in favor of that recommendation. Where a recommendation named several options in order, the recommended option is the decision. Items with no recommendation stay open. TRL 4 remains on hold by Amish's instruction, so decisions that need a build or a measurement are recorded as decided but on hold.

D1 to D7 were decided earlier the same day and are recorded in WSC-DDR-001.

## Options considered

The options for each item are those listed in `docs/REVIEW.md` (session 2026-09-25, TRL 3, "Proposed, awaiting Amish", items 4 to 7) and in WSC-DDR-002.

## Decision

*Table 1. Newly decided items. Each is "Decided by Amish, 2026-09-25: go with recommendation."*

| # | Item | Decision | What changed in the repo |
| --- | --- | --- | --- |
| D8 | Clear items in sun (R4), REVIEW item 5 | Option (b) for the first prototype: users back clear and translucent items with the calibration cap or scan them in shade. Option (a), LED modulation with synchronous demodulation, studied on paper first; option (c), restating R4 to opaque items, only if (a) fails | Firmware rule added: show "shade or back with cap" when the mean dark level exceeds 0.71 times the weakest band reading (WSC-CAL-001 D7). Paper check of (a) done: at 2 kHz an unbacked clear item in sun still carries about 23 % error, so (a) does not replace the backing step and (c) is not needed (D8). R4 restated to include the backing step and the prompt; status **not met to met by estimate** (0.36 % error on backed clear items, 0.13 % on opaque items) |
| D9 | Cap as a backing (part of D8) | The calibration cap is printed in black PETG so it blocks light from behind a clear item | BOM item 12 respecified (cost unchanged); WSC-PRC-001 components and safety updated; the classifier needs training data in the backed mode |
| D10 | Display in direct sun (R7), REVIEW item 6 | Option (a): a printed sun hood over the display, keeping large color and icon cues | Clip-on hood added to `cad/src/model.py` (walls 20 mm on both sides and the head end, open toward the user; 5.8 cm³, about 7 g); new BOM item 14 at $1.00 (items 14 and 15 renumbered 15 and 16); STEP and STL exported; drawing WSC-DWG-001 to Rev P2; concept media regenerated. R7 **not met to at risk**: 5.2:1 where the hood shades the screen, 1.6:1 with the sun near the screen normal or over the open side (WSC-CAL-001 I3, I4). Mass 202 g to 209 g; parts cost $163.00 to $164.00. R6 and R12 text updated to include the hood |
| D11 | Window crosstalk, REVIEW item 7 | Option (a) now: an open-air reading in the calibration routine subtracts the crosstalk offset (firmware only). Option (b), a baffle extended through the glass with separate windows, if the offset proves unstable with window dirt | Calibration routine and R11 text updated. WSC-CAL-001 C7 shows the offset must stay within 0.5 % of itself between readings, so option (b) is probably needed; proving that needs measurement, which is TRL 4 and **on hold** |
| D12 | Shared scan record (O4, REVIEW item 4, WSC-DDR-002) | Option 1: one shared record for WasteWise Scan and WasteWise-ml with a `pair_id` join | WSC-DDR-002 to v0.2 and WSC-DDR-001 to v0.2. Adoption by WasteWise-ml is a **cross-repo action**; R13 stays at risk until then |

No budget change: `budget_usd` stays $150 as the volume target (WSC-DDR-001 D2). The prototype figure moves from about $163 to about $164 because of the hood.

*Table 2. Items left open on 2026-09-25 (no recommendation was made then), decided by Amish on 2026-10-02.*

| # | Item | Status |
| --- | --- | --- |
| O1 | First partner and region for co-design and the first price table | Decided 2026-10-02: SWaCH in Pune as the first candidate to approach, Pune scrap prices as the first price table |
| O2 | Who the $150 volume target is for: cooperatives or individual pickers | Decided 2026-10-02: cooperatives |
| O3 | Extended InGaAs band (1,700 to 1,750 nm) to separate PE from PP | Decided 2026-10-02: eight bands; the band study comes first and decides any ninth band |
| WSC-DDR-002 Q2 | How `pair_id` is created in the field | Decided 2026-10-02: QR code on the scanner screen, digits as a fallback |
| WSC-DDR-002 Q3 | Whether consented spectra join the WasteWise-ml dataset, and on what terms | Decided 2026-10-02: yes, opt-in, co-owned by the pickers' organization, CC BY 4.0 with its agreement |

## Consequences

- WSC-PRC-001 v0.4, WSC-REQ-001 v0.4, WSC-CAL-001 v0.2, WSC-DDR-001 v0.2, WSC-DDR-002 v0.2 and drawing WSC-DWG-001 Rev P2 carry these decisions.
- Requirement status on paper: none not met; R1, R7 and R13 at risk; R3 and R10 not verifiable at TRL 3; nine met.
- On hold for TRL 4: measuring cap opacity and crosstalk stability, the indoor and sun test of the backing step, an outdoor legibility check of the hood, and any firmware beyond a sketch.
- Cross-repo: WasteWise-ml to adopt the shared record fields (D12). No other repo was edited.
- `project.yaml` keeps `trl: 3` and `trl_target: 3`.

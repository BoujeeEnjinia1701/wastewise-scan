---
doc_id: WSC-DDR-001
title: WasteWise Scan TRL 2 review decisions
project: WasteWise Scan
doc_type: Design decision record
version: "0.4"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record Amish's decisions on the TRL 2 review items and the items that remain open
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002); O4 decided, see WSC-DDR-003 D12
- version: "0.3"
  date: '2026-10-02'
  author: Amish Chadha
  change: O1 to O3 recorded as decided by Amish on 2026-10-02
- version: "0.4"
  date: '2026-10-02'
  author: Amish Chadha
  change: O3 band study run on paper (WSC-CAL-001 v0.4); result recorded
---

# 0001: TRL 2 review decisions

- **Date:** 2026-09-25
- **Status:** accepted for items D1 to D7 and, since v0.2, O4 (WSC-DDR-003 D12); items O1 to O3 decided by Amish on 2026-10-02 (WSC-DEC-001)

## Context

The TRL 2 review note (`docs/REVIEW.md`, session 2026-09-25, /populate) listed eight items as "Proposed, awaiting Amish". The design precis WSC-PRC-001 v0.2 and the problem statement WSC-PRB-001 v0.2 listed further open questions. On 2026-09-25 Amish reviewed the review points for every portfolio repo and wrote: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." Every item that carried a recommendation is therefore decided in favor of that recommendation. Items without a recommendation stay open.

The same instruction approved three portfolio-wide decisions: SwapCell interface v0.3 adds a wake method for hosts without CAN, a charge-while-discharging mode and a latch vibration rating for vehicles; shared SwapCell packs are priced once and excluded from each dependent kit budget; and community designs pick co-design partners per area later. WasteWise Scan runs from one 18650 cell (D7) and uses no SwapCell pack, so the first two do not change this design. The third keeps O1 open.

## Options considered

The options for each item are those listed in `docs/REVIEW.md` (session 2026-09-25, /populate), in WSC-PRC-001 v0.2 (Key design choices and Open questions) and in WSC-PRB-001 v0.2 (Open questions).

## Decision

*Table 1. Decided items.*

| # | Item | Decision |
| --- | --- | --- |
| D1 | Sensor approach | Option A: discrete NIR and SWIR LEDs with one InGaAs photodiode, following the open Plastic Scanner project. Option B (AS7265x only) and option C (A plus AS7265x) are not pursued. The pitch still reads true, so `project.yaml` pitch and problem are unchanged. Decided by Amish, 2026-09-25: go with recommendation. |
| D2 | Budget | Option (c): keep `budget_usd` at $150 as the volume target and accept about $163 in parts for the first prototype; move to option (b), six bands, only if a band study on reference spectra shows six bands suffice. `budget_usd` stays $150 and requirement R12 is redefined accordingly (WSC-REQ-001 v0.3). WSC-CAL-001 could not run that band study without reference spectra, so the design keeps eight bands. Decided by Amish, 2026-09-25: go with recommendation. |
| D3 | Controller | A LilyGO T-Display-S3 class board (ESP32-S3, 1.9 in display, on-board charger); no custom PCB. Decided by Amish, 2026-09-25: go with recommendation. |
| D4 | Band set | Eight bands at 850, 940, 1,050, 1,200, 1,300, 1,450, 1,550 and 1,650 nm, subject to confirmation on published reference spectra. Decided by Amish, 2026-09-25: go with recommendation. |
| D5 | Classifier | Linear discriminant analysis or a small decision tree on the device first; share labeled data with Plastic Scanner and WasteWise-ml where licenses allow. Decided by Amish, 2026-09-25: go with recommendation. |
| D6 | Calibration | A white PTFE reference disc in the storage cap. Decided by Amish, 2026-09-25: go with recommendation. |
| D7 | Battery | One protected 18650 Li-ion cell rather than a flat LiPo pouch. Decided by Amish, 2026-09-25: go with recommendation. |

*Table 2. Items left open at v0.1. O4 had a recommendation and was decided on 2026-09-25; O1 to O3 were decided by Amish on 2026-10-02 (WSC-DEC-001).*

| # | Item | Status |
| --- | --- | --- |
| O1 | First partner and region for co-design and the first price table (REVIEW item 8; PRB open questions 1 and 2) | Decided by Amish, 2026-10-02: a member-owned waste picker cooperative that already sells sorted plastics to scrap buyers; the first candidate to approach is SWaCH in Pune, India, the partner chosen for WasteWise-ml, with Pune scrap prices as the first price table. |
| O2 | Whether the $150 target is the price a cooperative would pay or should be lower for individual pickers (PRB open question 3) | Decided by Amish, 2026-10-02: the USD 150 value-engineering target is the price a cooperative pays for a shared scanner, not an individual picker. |
| O3 | Whether to add a 1,700 to 1,750 nm band on an extended InGaAs detector to separate PE from PP (PRC open question 2) | Decided by Amish, 2026-10-02: eight bands for the prototype; the paper band study on published reference spectra comes first, and the extended InGaAs band is added only if that study shows PE and PP cannot be told apart to R1 with eight. WSC-CAL-001 section B shows the 1,650 nm band reaches only the short edge of that region. Paper band study done 2026-10-02 (WSC-CAL-001 v0.4, B4 to B7): 89.5 % correct with eight bands and 93 % for PE against PP at the assumed item scatter, above 98 % at 1.0 % scatter. It neither shows nor rules out the problem, so the extended band is not added and is proposed to Amish (WSC-DEC-001). |
| O4 | Scan record format shared with WasteWise-ml and ReflowEconomy (PRC open question 5) | Decided by Amish, 2026-09-25: go with recommendation. One shared record with a `pair_id` join (WSC-DDR-002 option 1); recorded in WSC-DDR-003 D12. Adoption by WasteWise-ml is a cross-repo action. |

## Consequences

- WSC-PRB-001, WSC-PRC-001 and WSC-REQ-001 move to v0.3 with these choices no longer marked "proposed".
- R12 now reads as a $150 volume target with the first prototype accepted at about $163.
- WSC-CAL-001, the parametric model, drawing WSC-DWG-001 and the BOM use the eight-band, single-photodiode, T-Display-S3, 18650 design.
- New items raised by WSC-CAL-001 (sunlight through clear items, display legibility, window crosstalk) were decided on 2026-09-25 and are recorded in WSC-DDR-003, not here.

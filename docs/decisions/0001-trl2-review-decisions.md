---
doc_id: WSC-DDR-001
title: WasteWise Scan TRL 2 review decisions
project: WasteWise Scan
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record Amish's decisions on the TRL 2 review items and the items that remain open
---

# 0001: TRL 2 review decisions

- **Date:** 2026-09-25
- **Status:** accepted for items D1 to D7; items O1 to O4 remain proposed

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

*Table 2. Items that remain open (no recommendation was made).*

| # | Item | Status |
| --- | --- | --- |
| O1 | First partner and region for co-design and the first price table (REVIEW item 8; PRB open questions 1 and 2) | Proposed, awaiting Amish. Per the portfolio decision, partners are picked per area later. |
| O2 | Whether the $150 target is the price a cooperative would pay or should be lower for individual pickers (PRB open question 3) | Proposed, awaiting Amish. D2 fixes $150 as the volume target but not who pays it. |
| O3 | Whether to add a 1,700 to 1,750 nm band on an extended InGaAs detector to separate PE from PP (PRC open question 2) | Proposed, awaiting Amish. WSC-CAL-001 section B shows the 1,650 nm band reaches only the short edge of that region. |
| O4 | Scan record format shared with WasteWise-ml and ReflowEconomy (PRC open question 5) | Proposed, awaiting Amish. A draft is in WSC-DDR-002. |

## Consequences

- WSC-PRB-001, WSC-PRC-001 and WSC-REQ-001 move to v0.3 with these choices no longer marked "proposed".
- R12 now reads as a $150 volume target with the first prototype accepted at about $163.
- WSC-CAL-001, the parametric model, drawing WSC-DWG-001 and the BOM use the eight-band, single-photodiode, T-Display-S3, 18650 design.
- New items raised by WSC-CAL-001 (sunlight through clear items, display legibility, window crosstalk) are listed in `docs/REVIEW.md` as proposed, awaiting Amish. They are not decided here.

---
doc_id: WSC-RSK-001
title: WasteWise Scan risk register and hazard analysis
project: WasteWise Scan
doc_type: Risk register and hazard analysis
version: "0.1"
status: Draft
date: '2026-10-24'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-24'
    author: Amish Chadha
    change: First risk register, preliminary hazard analysis and first-pass design FMEA (kit 1.8 upgrade, stage P3) for option A
---

# WasteWise Scan risk register and hazard analysis

The top project risks are that eight bands cannot tell PE from PP to the 95 % target, and that the SWIR LEDs and InGaAs photodiode cost far more than the BOM's indicative prices. The top hazards are the lithium-ion cell (heat, drop, charging in sun), invisible LED light if a driver sticks on, and misuse of a resin result to judge whether waste is safe to handle. The highest design FMEA items are a wrong but confident resin call and a leaking baffle tube. Method: STANDARDS section 23. Likelihood, impact, severity and occurrence are scored 1 (low) to 5 (high); detection 1 (certain to be caught) to 5 (not caught).

> **Safety:** The scanner holds a lithium-ion cell of about 11 Wh and drives invisible infrared LEDs. It identifies resin only and must never be used to judge whether waste is safe to handle. See WSC-PRC-001, Safety, and the safety stops in WSC-BLD-001.

## Project risk register

Table 1. Project risks.

| # | Risk | Cause | Effect | Likelihood | Impact | Owner (role) | Response |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P1 | PE and PP cannot be told apart to 95 % | 1,650 nm band clipped by the detector cutoff; real item scatter above 1 % | PR-001 not met; users lose trust | 3 | 4 | Design lead | Labelled item set first at TRL 4; ninth band with extended InGaAs ready as an option (WSC-DEC-001 open 1); option B as the fallback principle (WSC-OPT-001) |
| P2 | Critical optics cost more than the BOM shows | SWIR LED prices indicative; a named 1 mm InGaAs photodiode lists at EUR 104 against USD 30 | Cost far over the USD 150 target | 3 | 3 | Procurement | Quotes from two suppliers; LED set from one maker; six-band saving if items allow (WSC-DEC-001, Value engineering) |
| P3 | No co-design partner engaged | Outreach to SWaCH not yet made | Requirements unconfirmed; no item set or price table | 3 | 4 | Project lead (Amish) | Approach SWaCH jointly with WasteWise-ml (decided 2026-10-02) |
| P4 | WasteWise-ml does not adopt the shared record | Separate project timelines | PR-013 stays at risk | 2 | 2 | Project lead | Joint interface note (WSC-DDR-002) |
| P5 | Radio or cell approvals block a pilot in India | WPC ETA for the board's module; BIS registration of cells | Delay to any field use | 2 | 3 | Procurement (partner) | Buy approved modules and registered cells (WSC-REG-001 R3, R5) |
| P6 | Display unreadable in direct sun | Hood cannot shade every sun angle | PR-007 at risk | 3 | 2 | Design lead | Colour and icon cues; user guidance on holding angle; design review with users |
| P7 | Mass over 250 g | Parts added for construction | PR-006 not met by 9 g | 4 | 1 | Design lead | Weigh at TRL 4; trim frame and head block if it matters to users |

## Preliminary hazard analysis

Table 2. Hazards.

| # | Hazard | Cause | Harm | Severity | Likelihood | Control | Residual |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H1 | Lithium-ion cell fire or venting | Charging in sun or above 45 C; crushed or dented cell; cell loose in a drop | Burns, smoke | 5 | 2 | Protected cell from a named maker (BIS registered); board charger only; no charging above 45 C or in sun; cradle and strap hold the cell against 869 N peak (PR-015, WSC-CAL-001 J4, fix F3); safety stops S1 and S4 in WSC-BLD-001 | Low, if the charging rule is followed |
| H2 | Invisible infrared light to the eye | LED driver stuck on; looking into the window | Corneal or retinal heating over long exposure | 3 | 1 | Exempt group in normal use (3.9 W/m2 at 200 mm); hardware on-time limit that firmware cannot override; label "do not look into the window" | Very low |
| H3 | Resin result used to judge hazardous waste | User trusts the scanner beyond its purpose | Cuts, needle-stick, chemical exposure | 4 | 2 | Start-screen warning; "unknown" rather than a guess; out-of-scope statement in all user material | Low |
| H4 | Hand near sharp items when backing clear items with the cap | Backing step in sun | Cuts | 3 | 2 | Scan sharp or broken items in shade instead; gloves | Low |
| H5 | Burns from the soldering iron when setting inserts (build) | 230 C iron | Burns | 2 | 2 | Stand, clamped work, build plan safety notes | Low |
| H6 | Glass fragments when core-drilling the window (build, fix F1) | Diamond core drill on borosilicate | Cuts, eye injury | 3 | 2 | Wet drilling at low speed, disc clamped on scrap wood, safety glasses, deburr the edge | Low |
| H7 | Wrong sorting decisions | Confident wrong result | Loss of income, contaminated bales | 2 | 3 | Confidence threshold set for few false results (PR-003); white reference check; "unknown" for black items | Medium until item data exists |

## Design FMEA (first pass, P3)

Table 3. Failure modes. RPN = severity x occurrence x detection.

| # | Item | Function | Failure mode | Effect | Cause | S | O | D | RPN | Action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F1 | Classifier and band set | Name the resin | Confident wrong call between PE and PP | Wrong pile, lost value | Clipped 1,650 nm band; item scatter | 5 | 3 | 4 | 60 | Labelled item set; confidence threshold tuned for few false results; ninth band option |
| F2 | Baffle tube (fix F1) | Keep LED light from reaching the detector inside the glass | Tube passes near-infrared light | Offset changes with dirt; wrong ratios | Dye-coloured black filament | 4 | 2 | 3 | 24 | Carbon-black filament; 1 mm sample check (WSC-BLD-001 3.3); open-air reading still taken |
| F3 | Detector window glue joint | Hold the 5.8 mm window flush in the tube | Window loose or glue on the optical face | Light leak or signal loss | Poor bead; drop | 3 | 2 | 2 | 12 | Edge bead only; check under magnification; white reference shows signal loss |
| F4 | LED driver | Pulse each LED for about 14 ms | Stuck on | Eye exposure; battery drain | Firmware fault or failed switch | 4 | 2 | 3 | 24 | Hardware on-time limit; current monitor |
| F5 | Cell strap and inserts | Hold the cell in a 1.2 m drop | Strap cracks along layers or insert pulls out | Cell loose; contacts open | Printed PETG strength; margin 1.45 at the peak (fix F3) on an assumed crush | 4 | 2 | 3 | 24 | Print with layers along the bar; drop test at TRL 4; thicker strap if it fails |
| F6 | Shell gasket and button seal | Keep dust and rain out (IP54) | Water ingress | Corrosion, short | Gasket over- or under-squeezed | 3 | 3 | 3 | 27 | Bosses set the squeeze at 0.6 mm; spray test at TRL 4 |
| F7 | Calibration cap and PTFE disc | White reference at the item distance | Disc dirty or worn | Drift in every result | Handling, dust | 3 | 3 | 2 | 18 | Clean and replace the disc; drift warning at 5 % |
| F8 | Shroud (TPU) | Block direct light and set the distance | Rim worn or torn | Sunlight leak; wrong distance | Abrasion on rough items | 3 | 3 | 2 | 18 | Replaceable wear part; dark-level prompt catches leaks |
| F9 | Display and sun hood | Show the result | Unreadable in sun | Misread result | Sun near the screen normal | 3 | 3 | 2 | 18 | Colour and icon cues; hold angle guidance |
| F10 | Slide switch in the battery lead | Turn the scanner on and allow charging | Cannot charge with the switch off | Flat cell at shift start | Wiring choice | 2 | 3 | 2 | 12 | Confirm the board's charging path (WSC-DEC-001 confirm item 3) |

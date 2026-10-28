---
doc_id: WSC-FEA-001
title: WasteWise Scan feasibility assessment
project: WasteWise Scan
doc_type: Feasibility assessment
version: "0.1"
status: Draft
date: '2026-10-24'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-24'
    author: Amish Chadha
    change: First feasibility assessment (kit 1.8 upgrade) of option A, the current design
---

# WasteWise Scan feasibility assessment

Option A is feasible on paper to build and run as a proof-of-concept prototype: the optics, power, timing, sunlight handling and eye safety close by calculation on stated assumptions (fixes F1 to F3 made in this session), and every part can be bought or printed and assembled with hand tools (WSC-BLD-001). The open question is performance, not buildability: whether eight bands tell PE from PP to 95 % (PR-001, rated Medium), which only a labelled item set at TRL 4 can show. Mass (9 g over), direct-sun legibility and the price of the SWIR parts are the other weak points. Method: STANDARDS section 23.

Table 1. Feasibility by aspect.

| Aspect | Assessment | Rating | Risks and notes | Evidence |
| --- | --- | --- | --- | --- |
| Design: optical principle | Discrete-band NIR reflectance with one InGaAs photodiode identifies resins in prior work; signal-to-noise ratio of 640 or more in shade with the four-cycle scan of fix F2; the window crosstalk glass path closed by fix F1 (wall leak to measure) | High | Item scatter decides accuracy; backed mode needs its own training data | WSC-STM-001 S1 to S7, S12; WSC-CAL-001 B, C, D |
| Design: classification accuracy | Paper band study 89.5 % for five resins, 93 % for PE against PP at 1.5 % item scatter; 96.7 % at 1.0 % | Medium | Approximate reference spectra, not measured items; an extended InGaAs band may be needed (WSC-DEC-001 open decision 1) | WSC-CAL-001 B4 to B7; STEM S23 |
| Design: mass and handling | 239 g, 259 g with the cap, against 250 g | Medium | 9 g over; thinner display frame or head block, or counting without the cap, are the remaining levers | WSC-CAL-001 A3; PR-006 |
| Design: display in sun | 5.2:1 where the hood shades the screen, 1.6:1 otherwise | Medium | Depends on how the user holds it; colour and icon cues stay primary | WSC-CAL-001 I; PR-007 |
| Materials | PETG and TPU prints, borosilicate windows, PTFE reference disc; carbon-black PETG for the head block (fix F1) | High | Printed PETG strength along layers (strap margin 1.45 at the peak drop load after fix F3); filament opacity in NIR to confirm | WSC-CAL-001 J4, C8; WSC-DEC-001 confirm items 10, 11 |
| Manufacturing and assembly | FDM printing, heat-set inserts, through-hole soldering on perfboard, one 8.4 mm cored hole in glass; 21 components in 13 steps | High | Core-drilling glass needs care and safety glasses; SWIR LED pockets need reaming | WSC-BLD-001; DWG-101 to DWG-109 |
| Power and controls | One protected 18650 cell, 21.9 h at 4 scans per minute; ESP32-S3 board with its charger; ADS1220-class converter | High | Charging through the slide switch to confirm on the board; hardware LED on-time limit to design | WSC-CAL-001 F; WSC-DEC-001 confirm item 3 |
| Supply of parts | Display board, cell, switch and screws are common; SWIR LEDs and InGaAs photodiodes come from specialist distributors | Medium | SWIR LEDs about USD 8 to 15 each (indicative); a named 1 mm InGaAs photodiode lists at EUR 104 against USD 30 in the BOM | BOM lines 3, 4; WSC-MKT-001 |
| Software | Classifier (LDA or small tree) on the ESP32-S3; local price table; 64-byte records and CSV export | High | Firmware is TRL 4 work beyond a labelled sketch | WSC-DDR-001 D5; WSC-DDR-002 |
| Regulatory | Eye safety exempt by estimate; cell and radio approvals to assess in India | Medium | WPC ETA of the board's module; BIS registration of the cell | WSC-REG-001 R1 to R6 |

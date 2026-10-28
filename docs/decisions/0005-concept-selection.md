---
doc_id: WSC-DDR-005
title: WasteWise Scan concept selection
project: WasteWise Scan
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-10-24'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-24'
  author: Amish Chadha
  change: Concept selection between option A (eight-band LED scanner, the current design) and option B (tunable-filter spectrometer); scores within 10 %, both sent to Amish without a pick
---

# 0005: Concept selection

- **Date:** 2026-10-24
- **Status:** proposed. Proposed, awaiting Amish. No option is recommended because the two scores are within 10 % (STANDARDS section 21).

## Context

Kit 1.8 asks every repo for at least two concept options with different working principles, scored against the user requirements (WSC-URS-001). WasteWise Scan was designed before kit 1.8, so its current design is option A and stays the repo's design until Amish decides. The options, numbers and scoring are in WSC-OPT-001; the STEM rows of each option are in WSC-STM-001.

## Options considered

| Option | Working principle | Weighted score (of 235) | Strengths | Weaknesses |
| --- | --- | --- | --- | --- |
| A: eight-band LED scanner | Eight LEDs from 850 to 1,650 nm flash in turn; one InGaAs photodiode reads each reflection; band ratios are classified | 186 | USD 167.50; 0.64 s; 21.9 h; solid-state and drop tolerant; modelled, drawn and planned to build | Reaches the 1,650 to 1,765 nm polymer bands only at their short edge (PE against PP 93 % on paper); invisible LEDs need a hardware on-time limit |
| B: tunable-filter spectrometer | Two tungsten lamps light the item; a MEMS Fabry-Perot filter on an InGaAs detector sweeps 1,550 to 1,850 nm | 173 | Continuous spectrum across the PE and PP bands; visible, low-hazard light | At least USD 375 (sensor about USD 300); about 0.74 s; lamp heat and filament life; filter calibration; loses the 1,200 nm band |

A is ahead by 13 points, 7.0 %, inside the 10 % band.

## Decision

Proposed, awaiting Amish, with no pick. If A is chosen, the repo is unchanged and the runner-up's best idea (a ninth band near 1,720 nm with an extended InGaAs photodiode) stays open as WSC-DEC-001 open decision 1. If B is chosen, the optical head, its board, the BOM, the build plan and the CAL are redone at the next session, with A's 1,200 nm band kept as one LED beside the lamps.

## Consequences

- `concept_options: [A, B]` in `project.yaml`; `concept_chosen` stays unset until Amish decides.
- The drawing, priced BOM and build plan describe option A, the current design.
- Both options are modelled at D3 in `cad/src/model.py` and checked by `python .kit/cad_check.py --export` (`cad/fidelity.json`).

---
doc_id: WSC-DEC-001
title: WasteWise Scan design decisions register
project: WasteWise Scan
doc_type: Design decisions register
version: "0.1"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-02'
  author: Amish Chadha
  change: Register opened with the build plan; budget treated as a value-engineering target
---

# WasteWise Scan design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

| # | Decision needed | Options | Recommendation | Affects in the build | Source |
| --- | --- | --- | --- | --- | --- |
| 1 | Accept the design-for-construction changes P1 to P12 (shell screws and gasket, window clamp, shroud flange, optical head block, photodiode seat, cradle and strap, USB-C seat, display frame, button hole, slide switch, hood clips, calibration cap) | Accept; accept with changes; reject | Accept | The whole build plan | WSC-DDR-004, A2 |
| 2 | Mass (R6) is now not met: 274 g with the cap, 254 g without, against 250 g | (a) shell walls 2.0 mm instead of 2.5 mm, saving about 20 g, with the drop case checked at TRL 4; (b) count R6 without the cap; (c) accept about 275 g and restate R6 | (a), then weigh the first prototype before (b) or (c) | Shell print settings and the making sketches of both shells | WSC-DDR-004, A1; WSC-CAL-001 [A3] |
| 3 | First partner and region for co-design and the first price table | Partners are picked per area later | None yet | Not part of the TRL 3 build; sets the price table in the firmware | WSC-DDR-001, O1 |
| 4 | Who the USD 150 value-engineering target is for: cooperatives or individual pickers | Cooperatives; individual pickers | None yet | Not part of the build | WSC-DDR-001, O2 |
| 5 | An extended InGaAs band (1,700 to 1,750 nm) to separate PE from PP | Add a ninth band on an extended InGaAs detector; keep eight bands | None yet; a paper band study on published reference spectra comes first | The LED set, the photodiode and the head block pockets | WSC-DDR-001, O3 |
| 6 | How the pair ID that joins a scan to a WasteWise-ml photo is created in the field | Typed digits; a sticker; the phone scanning a code on the scanner screen | None yet | Firmware only | WSC-DDR-002, question 2 |
| 7 | Whether consented spectra join the WasteWise-ml dataset, and on what license and ownership terms | To be set with the WasteWise-ml side | None yet | Not part of the build | WSC-DDR-002, question 3 |

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The protected cell's length (the cradle allows 69 mm) and the contact pair's thickness and spring travel | The cradle end walls are 75 mm apart for a 69 mm cell, a 1 mm flat contact and a spring compressed to 4 mm plus its 1 mm plate | WSC-DDR-004, P6 |
| 2 | The display board's real outline (about 62 x 26 x 9.5 mm is assumed), its connector positions and its battery input | The display frame and the 0.25 mm gap to the ceiling are set from the assumed outline; the slide switch is wired in the battery lead | WSC-DDR-004, P8 |
| 3 | Whether the board charges the cell with the switch in the battery lead, and from its 5 V pin | Charging needs the switch on; if the board cannot charge through its 5 V pin, the USB-C board wiring changes | Build plan, wiring |
| 4 | The button's bezel (19 mm or less), its depth under the panel (14 mm or less) and its nut (20 mm or less across) | They set the button hole and its clearance to the display frame and the amplifier board | WSC-DDR-004, P9 |
| 5 | The slide switch's mounting hole pitch (15 mm) and body size (10 x 6 x 6 mm) | The wall slot and holes are printed into the bottom shell | WSC-DDR-004, P10 |
| 6 | Each LED's package: TO-46 (5.4 mm) or 5 mm lens LED (5.8 mm rim) | The head block pockets are 5.6 mm, for TO-46 cans | WSC-DDR-004, P4 |
| 7 | The foam gasket squeezes to about 0.6 mm with the bosses touching | The bosses stop the squeeze at 0.6 mm; a harder foam will not seal | WSC-DDR-004, P1 |
| 8 | The photodiode's responsivity curve near 1,700 nm | It decides how much of the 1,650 nm band is seen (R1) | BOM line 4; WSC-CAL-001 B |

## Value engineering

Value-engineering target: USD 150 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 167.50 (USD 17.50 over the target). Main cost drivers and savings worth trying:

- The largest lines are the eight LEDs with their drivers (USD 62; the six short-wave infrared LEDs cost about USD 8 to 15 each), the InGaAs photodiode (USD 30) and the display board (USD 20). Optics are 55 % of the cost.
- Making the design constructable added USD 3.50 net: the display frame, cell strap and gasket (lines 17 to 19) and more fixings; the bought cell holder became contacts in a printed cradle, which saved USD 1.
- Savings worth trying: the six-band option (dropping 1,050 and 1,300 nm saves about USD 18) if the band study shows six bands suffice (WSC-DDR-001 D2); buying the LEDs as a set from one maker; a second source for the photodiode; at volume, a bare ESP32-S3 module and display in place of the display board.

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | D1 to D7: discrete LEDs with an InGaAs photodiode; USD 150 kept as the volume target with about USD 163 accepted for the prototype; T-Display-S3 class board; the eight-band set; a small on-device classifier with shared data; PTFE white reference in the cap; one protected 18650 cell | Amish: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." | WSC-DDR-001 |
| 2026-09-25 | D8 to D12: back clear items in sun with the black cap and refuse a result on through-light; black calibration cap; clip-on sun hood; open-air crosstalk reading in calibration; one shared scan record with a pair ID join | Amish: "i accept all your recommendations, go with them across all repos." | WSC-DDR-003, WSC-DDR-002 |
| 2026-09-26 | WasteWise Scan chosen as the pilot for product-grade renders; every drawing names the project and its repository | Amish | `docs/REVIEW.md`, session 2026-09-26 |
| 2026-09-30 | Make the design physically buildable while drawing the build plan; outstanding decisions go in this register, not the build plan | Amish: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." | WSC-DDR-004 (changes open for review, item 1 above) |
| 2026-10-01 | `budget_usd` is a value-engineering target, not a limit | Amish: "the budgets are a hypothethical control target to ensure we are thinking along a value engineering lens." | This register, Value engineering |

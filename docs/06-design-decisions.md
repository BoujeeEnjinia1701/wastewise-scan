---
doc_id: WSC-DEC-001
title: WasteWise Scan design decisions register
project: WasteWise Scan
doc_type: Design decisions register
version: "0.4"
status: Draft
date: '2026-10-24'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-02'
  author: Amish Chadha
  change: Register opened with the build plan; budget treated as a value-engineering target
- version: "0.2"
  date: '2026-10-02'
  author: Amish Chadha
  change: Amish approved the recommendations for open items 1 to 7 on 2026-10-02 (WSC-DDR-004 accepted, R6 by thinner walls, SWaCH as first candidate partner, cooperative price, eight bands, QR pair ID, consented spectra terms); moved to decisions made
- version: "0.3"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Decisions carried out: 2.0 mm walls in the model (R6 238 g, 258 g with the cap); paper band study result raised as an open decision on the extended InGaAs band"
- version: "0.4"
  date: '2026-10-24'
  author: Amish Chadha
  change: "Kit 1.9.1 upgrade: concept selection between options A and B added as open decision 2 (within 10 %, no pick) and the per-band drift warning as open decision 3; fixes F1 to F4 recorded as decided under Amish's standing instruction of 2026-10-23; items to confirm when parts are bought; value engineering notes cited prices"
---

# WasteWise Scan design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

| # | Decision | Options | Recommendation | Source |
| --- | --- | --- | --- | --- |
| 2 | Concept selection: option A, the eight-band LED scanner (current design, 186 of 235), or option B, the tunable-filter spectrometer (173 of 235). The scores are within 10 %, so no option is recommended (STANDARDS section 21). | (A) keep the current design; R1's PE and PP risk settled by the labelled item set at TRL 4. (B) redo the optical head with two tungsten lamps and a MEMS Fabry-Perot sensor sweeping 1,550 to 1,850 nm (at least USD 375 in parts, about 0.74 s per scan). | None (within 10 %). The repo keeps option A until Amish decides. | WSC-DDR-005; WSC-OPT-001 |
| 3 | Drift warning (PR-011): keep the 5 % warning on overall LED drift, or warn when any band drifts 1.5 % from the others. The independent review of WSC-STM-001 found 5 % loose against the 1.5 % band-to-band item scatter the band study assumes; a common drift cancels in the band ratios, a band-to-band drift does not. | (a) keep 5 % overall (recalibrate after about 12.5 C of change); (b) 1.5 % per band from the board temperature with per-band coefficients (recalibrate about three times as often, after about 4 C of change on the assumed coefficient). | (b), with the coefficients measured at TRL 4; it changes the user's calibration routine, so it is Amish's | WSC-STM-001 S19; WSC-CAL-001 J3 |
| 1 | Whether to add the extended InGaAs band now. The paper band study (WSC-CAL-001 v0.4, B4 to B7) gave 89.5 % correct with eight bands and 93 % for PE against PP at the assumed item scatter, above 98 % at 1.0 % scatter, so it neither shows nor rules out the problem that would trigger it. | (a) keep eight bands and settle it with the first labeled item set at TRL 4; (b) add a 1,700 to 1,750 nm band and an extended InGaAs photodiode now (extra cost not yet quoted; extended InGaAs photodiodes cost more than the USD 30 standard part). | (a): the result turns on item scatter, which only measured items can fix. | WSC-DDR-001, O3 |

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
| 9 | The photodiode's price: a named 1 mm InGaAs PIN in TO-18 (Hamamatsu G12180-010A) lists at EUR 104.09 each excluding VAT (RS Components Ireland, checked 2026-10-25), against the USD 30 indicative price in BOM line 4 for a generic part | The BOM total and PR-012 move by up to about USD 90 if no cheaper part with a suitable curve is found | BOM line 4; WSC-MKT-001 |
| 10 | The black PETG filament for the head block is coloured with carbon black and a 1 mm wall stops the LED light (fix F1 assumes 10⁻³ or less) | Some black filaments use dyes that pass near-infrared light; the baffle tube would then leak | Fix F1; WSC-CAL-001 C8 |
| 11 | A 5.8 mm by 2 mm borosilicate disc for the detector window, and a supplier or workshop for the 8.4 mm cored hole in the 25 mm window | Fix F1 needs both; their prices are to assess | Fix F1; BOM line 6 |

## Value engineering

Value-engineering target: USD 150 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 167.50 (USD 17.50 over the target). Main cost drivers and savings worth trying:

- The largest lines are the eight LEDs with their drivers (USD 62; the six short-wave infrared LEDs cost about USD 8 to 15 each), the InGaAs photodiode (USD 30) and the display board (USD 20). Optics are 55 % of the cost.
- Making the design constructable added USD 3.50 net: the display frame, cell strap and gasket (lines 17 to 19) and more fixings; the bought cell holder became contacts in a printed cradle, which saved USD 1.
- Cited prices checked on 2026-10-24 (WSC-MKT-001): a T-Display-S3 board lists from USD 9.04 at LilyGO's store against USD 20 in BOM line 2, a possible saving; a named Hamamatsu 1 mm InGaAs photodiode lists at EUR 104.09 against USD 30 in line 4, a possible overrun (to confirm item 9). The BOM keeps its indicative prices until parts are quoted.
- Fix F1 (2026-10-24) leaves the line prices unchanged; the small detector window and the cored hole are to assess.
- Savings worth trying: the six-band option (dropping 1,050 and 1,300 nm saves about USD 18) if measured items show six bands suffice (WSC-DDR-001 D2; the paper band study scores six bands at 88 % against 89.5 % for eight, WSC-CAL-001 v0.4 B4); buying the LEDs as a set from one maker; a second source for the photodiode; at volume, a bare ESP32-S3 module and display in place of the display board.

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | D1 to D7: discrete LEDs with an InGaAs photodiode; USD 150 kept as the volume target with about USD 163 accepted for the prototype; T-Display-S3 class board; the eight-band set; a small on-device classifier with shared data; PTFE white reference in the cap; one protected 18650 cell | Amish: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." | WSC-DDR-001 |
| 2026-09-25 | D8 to D12: back clear items in sun with the black cap and refuse a result on through-light; black calibration cap; clip-on sun hood; open-air crosstalk reading in calibration; one shared scan record with a pair ID join | Amish: "i accept all your recommendations, go with them across all repos." | WSC-DDR-003, WSC-DDR-002 |
| 2026-09-26 | WasteWise Scan chosen as the pilot for product-grade renders; every drawing names the project and its repository | Amish | `docs/REVIEW.md`, session 2026-09-26 |
| 2026-09-30 | Make the design physically buildable while drawing the build plan; outstanding decisions go in this register, not the build plan | Amish: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." | WSC-DDR-004 (changes open for review, item 1 above) |
| 2026-10-01 | `budget_usd` is a value-engineering target, not a limit | Amish: "the budgets are a hypothethical control target to ensure we are thinking along a value engineering lens." | This register, Value engineering |
| 2026-10-02 | Design for construction accepted: the changes P1 to P12 of WSC-DDR-004, as made | Amish: "APPROVED: The open decisions from the last wave (TremorTrace to ZeerBox) came in after the review and aren't on the page either." | WSC-DDR-004, A2 |
| 2026-10-02 | Mass (R6): 2.0 mm shell walls, keeping the bosses and ribs, with the drop case checked at TRL 4; R6 stays not met until the first prototype is weighed (carried into the model 2026-10-02: 238 g, 258 g with the cap, 8 g over, since the shells saved 17 g rather than about 20 g), and the cap stays counted because it is carried for backing clear items | Amish: "APPROVED: The open decisions from the last wave (TremorTrace to ZeerBox) came in after the review and aren't on the page either." | WSC-DDR-004, A1; WSC-CAL-001 [A3] |
| 2026-10-02 | First partner and region: a member-owned waste picker cooperative that already sells sorted plastics to scrap buyers; the first candidate to approach is SWaCH in Pune, India, the partner chosen for WasteWise-ml, with Pune scrap prices as the first price table | Amish: "APPROVED: The open decisions from the last wave (TremorTrace to ZeerBox) came in after the review and aren't on the page either." | WSC-DDR-001, O1 |
| 2026-10-02 | Value-engineering target: the USD 150 value-engineering target is the price a cooperative pays for a shared scanner, not an individual picker | Amish: "APPROVED: The open decisions from the last wave (TremorTrace to ZeerBox) came in after the review and aren't on the page either." | WSC-DDR-001, O2 |
| 2026-10-02 | Extended InGaAs band: eight bands for the prototype; the paper band study on published reference spectra comes first, and the extended InGaAs band is added only if that study shows PE and PP cannot be told apart to R1 with eight | Amish: "APPROVED: The open decisions from the last wave (TremorTrace to ZeerBox) came in after the review and aren't on the page either." | WSC-DDR-001, O3 |
| 2026-10-02 | Pair ID in the field: the scanner creates the pair ID and shows it as a QR code on its screen for the phone to scan, with the same short code in digits as a typed fallback | Amish: "APPROVED: The open decisions from the last wave (TremorTrace to ZeerBox) came in after the review and aren't on the page either." | WSC-DDR-002, question 2 |
| 2026-10-02 | Consented spectra: consented spectra join the WasteWise-ml field dataset on the same terms as field photos: opt-in per scan, co-owned by the pickers' organization, and published under CC BY 4.0 only with that organization's agreement | Amish: "APPROVED: The open decisions from the last wave (TremorTrace to ZeerBox) came in after the review and aren't on the page either." | WSC-DDR-002, question 3 |
| 2026-10-24 | F1, window crosstalk (STEM check S12, which failed at 10 % of the signal against 0.5 %): the head block's baffle tube, 8 mm across in carbon-black PETG, passes through an 8.4 mm cored hole in the 25 mm LED window to its item-side face and holds a separate 5.8 mm detector window, so LED light reflected inside the glass cannot reach the photodiode; the 0.2 mm gap round the tube is sealed with a bead of black RTV; crosstalk 0.003 % of the signal on assumed leak values, to verify at TRL 4 (WSC-CAL-001 C8). This is the fallback Amish accepted on 2026-09-25 (WSC-DDR-003 D11, option (b)). Options weighed: open-air reading only (10 %, fails), anti-reflection coated window (about 1 %, still over), baffle through the glass (chosen; line prices unchanged, small window and coring to assess). With it, the model now has a 4 mm light channel from each LED face to the window, which the head block lacked (a modelling correction). Model, drawings WSC-DWG-001 Rev P6 and 103, CAL v0.5, BOM lines 3 and 6, build plan v0.3 and PR-017 changed. Amish can reverse it. | Decided under Amish's standing instruction of 2026-10-23 (fix rule, STANDARDS section 20): a failed STEM row is fixed in the design in the same session and recorded here | WSC-STM-001 S12; WSC-CAL-001 C7, C8 |
| 2026-10-24 | F2, scan sequence (STEM check S5 and S7 after the independent review: with the dark gap taken from the timing, a backed clear item carried 0.73 % against 0.5 %; S3 needed a 3-sigma criterion): the firmware repeats the dark-band-dark sequence four times with two conversions per reading (8.1 ms) and averages. Backed clear item 0.21 %, opaque 0.08 %, dark-level prompt at 1.24 times the weakest band, signal-to-noise ratio 643 against 600, scan 0.64 s (was 0.33 s, still under 1.5 s), battery 21.9 h (was 22.1 h). Options weighed: one cycle of two conversions (0.42 %, but SNR 321), a faster ADC mode (noise to assess), four cycles (chosen; no parts change). CAL v0.5 D3 to D7, C4, E, F, H changed. Amish can reverse it. | Decided under Amish's standing instruction of 2026-10-23 (fix rule, STANDARDS section 20) | WSC-STM-001 S3, S5, S7; WSC-CAL-001 D6, D7, E2 |
| 2026-10-24 | F3, cell strap (STEM check S18 after the independent review: at the peak of a half-sine pulse, 1.57 times the mean, the 10 x 8 mm strap reached 59 MPa against about 50 MPa): the strap is now 11 x 10 mm, its two M3 x 25 low-head screws sit in 6.2 mm counterbores 2 mm deep so the heads still clear the ceiling; 34 MPa at the 869 N peak, margin 1.45. Mass rises 1.3 g (scanner 239 g, 259 g with the cap). Options weighed: a wider strap only (clashes with the display frame clearance), a deeper strap without counterbores (heads hit the ceiling), deeper and wider with counterbores (chosen; filament only). Model, DWG-106, CAL J4, BOM line 18 and the build plan changed. Amish can reverse it. | Decided under Amish's standing instruction of 2026-10-23 (fix rule, STANDARDS section 20) | WSC-STM-001 S18; WSC-CAL-001 J4 |
| 2026-10-24 | F4, option B lamp heat (STEM check S36, judged a likely failure by the independent review: bulb glass well above 80 C, 0.2 mm from the PETG head block): in the option B model each lamp sits in an aluminium sleeve with a 0.2 mm air gap that spreads the heat into the block. Option B is not the current design; the fix keeps its STEM row from failing so it can be scored. | Decided under Amish's standing instruction of 2026-10-23 (fix rule, STANDARDS section 20) | WSC-STM-001 S36; WSC-OPT-001 |

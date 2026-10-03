---
doc_id: WSC-CAL-001
title: WasteWise Scan sizing calculations
project: WasteWise Scan
doc_type: Calculation
version: "0.4"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First issue for TRL 3 (mass, band coverage, signal and noise, sunlight, timing, power, logging, eye safety, display, drop and drift, cost)
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002); decisions recorded in WSC-DDR-003 applied (sun hood, backing step and dark-level prompt, open-air crosstalk reading, modulation check)
- version: "0.3"
  date: '2026-10-02'
  author: Amish Chadha
  change: Constructable design (WSC-DDR-004); masses from the new model, fixings allowance, cell strap check J4, cost against the value-engineering target K2
- version: "0.4"
  date: '2026-10-02'
  author: Amish Chadha
  change: Shell walls 2.0 mm (decision of 2026-10-02); masses and R6 recomputed; drop energy; paper band study for R1 (B4 to B7)
---

# WasteWise Scan sizing calculations

**Revision 0.4 (2026-10-02).** Amish decided on 2026-10-02 that both shells have 2.0 mm walls (WSC-DEC-001). The model now has them; the bosses, ribs and tongue are kept and all 314 constructability checks pass. The scanner weighs about 238 g, 258 g with the cap [A3], 16 g lighter than at v0.3 and still **not meeting R6 (250 g)**: 8 g over with the cap, not the 4 g the decision expected, because the shells save 17 g rather than about 20 g and the head block, display frame and strap gain about 1 g on the thinner floor and ceiling. The drop case is unchanged in kind (about 1,200 g on a shell corner, 550 N on the cell) and is checked at TRL 4 [J1, J2]. A paper band study on approximate published band positions gives 89 % correct for the five resins with eight bands, and 93 % for PE against PP, short of the 95 % target at the assumed item scatter [B4 to B7]. Nothing else changed.

**Revision 0.3 (2026-10-02).** The model was made constructable under Amish's instruction of 2026-09-30 (WSC-DDR-004): screws, bosses, a gasket, an optical head block, a cradle and strap, a display frame and clip legs on the hood were added. The optics, power, timing, sunlight and display results below are unchanged. The scanner now weighs about 254 g, 274 g with the cap [A3], so **R6 (250 g) is not met**, 24 g over; the options are in the design decisions register WSC-DEC-001. The cell strap carries the corner-drop load with a margin of 1.3 [J4]. The parts cost is USD 167.50 against the USD 150 value-engineering target, USD 17.50 over [K2]. The paragraph below describes revision 0.2.

On paper, WasteWise Scan now meets nine of its fourteen requirements, has three at risk and none not met; two cannot be verified at TRL 3. This revision applies the decisions Amish accepted on 2026-09-25 (WSC-DDR-003). Sunlight (R4) moves from not met to met: clear and translucent items are backed with the black calibration cap, which cuts the ambient error to 0.36 % of signal, and a firmware rule refuses a result, rather than guessing, when the dark level shows light through an unbacked item. Display legibility (R7) moves from not met to at risk: a clip-on sun hood gives about 5.2:1 contrast where it shades the screen, but the screen still washes out with the sun near its normal or over the open side. Resin accuracy (R1) stays at risk because the 1,650 nm band reaches only the short edge of the 1,650 to 1,750 nm polymer region, and the shared record (R13) stays at risk until WasteWise-ml adopts it. The hood adds about 7 g and $1: mass rises from 202 g to 209 g and the prototype cost from $163.00 to $164.00. The calculations at v0.1 changed two parts of the TRL 2 concept: the transimpedance gain dropped from 1 MΩ to 47 kΩ and each band reading sits between two dark readings. Every number in this note is printed by `docs/04-calcs/sizing.py`; the tag in brackets, for example [C4], is the line of that script's output that carries it.

> **Safety:** These are first-principles estimates for a paper proof of concept. They do not replace measurements of LED emission, drop behavior, cell temperature or classification accuracy. The scanner identifies resin only and must never be used to judge whether waste is safe to handle. See WSC-PRC-001, Safety.

## Scope and method

The note checks every requirement in WSC-REQ-001 v0.3 against the design in WSC-PRC-001 v0.3 and the parametric model `cad/src/model.py`. The script imports the model's `PARAMS`, `derived()` and part solids, so the shells, shroud, window and optics geometry used here are those in the STEP files and in drawing WSC-DWG-001. It also reads `bom/bom.csv` and `budget_usd` in `project.yaml`. Run it from the repo root with `python docs/04-calcs/sizing.py`.

The design case is the decided configuration (WSC-DDR-001 and WSC-DDR-003): eight LEDs from 850 to 1,650 nm, one 1 mm InGaAs photodiode, an ADS1220-class 24-bit ADC, a T-Display-S3-class board, one protected 3,000 mAh 18650 cell and an 18 mm shroud that puts the item 22 mm from the detector [C1], a black calibration cap that doubles as a backing for clear items, and a clip-on sun hood 20 mm high over the display.

## Assumptions

*Table 1. Main assumptions. All are to be confirmed from datasheets or measurement.*

| Area | Assumption | Basis |
| --- | --- | --- |
| LEDs | Radiant power at 100 mA: 15 mW at 850 and 940 nm, 4 mW at 1,050 nm, 2 mW at 1,200 and 1,300 nm, 1.5 mW at 1,450 and 1,550 nm, 1 mW at 1,650 nm. FWHM 40 to 120 nm, widening with wavelength. Beam half-angle 10 to 15°. Output falls 0.4 %/°C | Typical catalog ranges for small IR and SWIR LEDs; not from a chosen part |
| Detector | Standard InGaAs, 1 mm active diameter; responsivity 0.35 A/W at 900 nm, 0.90 at 1,300 nm, 0.95 at 1,550 nm, 0.50 at 1,680 nm, 0.05 at 1,720 nm, linear between | Typical curve shape; confirm from the chosen part |
| Optics | Uncoated borosilicate window, 0.92 transmission per pass, 4 % reflection per surface; illuminated spot 8 mm radius; item a Lambertian reflector | Standard values for uncoated glass; Lambertian is a first-order model |
| Items | Diffuse reflectance 0.9 for the PTFE reference, 0.5 for a typical opaque item, 0.10 for a clear item, 0.04 for a carbon-black item. Diffuse transmittance of a clear or translucent wall 0.30 (worst case) | Assumed; to measure on reference chips |
| Electronics | ADC at 330 samples/s, 5 µV rms per conversion, 2.048 V range; 4 conversions averaged; 2 ms LED settling; 3.3 V amplifier rail | ADS1220-class figures, conservative |
| Sunlight | 300 W/m² in the 900 to 1,700 nm band at about 100 klx; hand movement changes ambient light by 1 % per 10 ms | Share of the solar spectrum, rounded; movement figure assumed |
| Power | ESP32-S3 at 240 MHz with radio off 45 mA, display at full backlight 60 mA, analog front end 3 mA; LEDs 100 mA while on; 4 scans per minute; 80 % of 10.8 Wh usable | Typical values; to measure on the board |
| Display | 400 cd/m² white, 0.4 cd/m² black, 2 % diffuse-equivalent screen reflectance; about 3:1 contrast needed for large colored icons | Not from a datasheet; legibility threshold assumed |
| Drop | 1.2 m; 1 mm crush on a shell corner, 10 mm on the TPU shroud | First-order stopping distances |
| Construction (v0.3) | Printed parts solid at the model volume; fixings, gasket and wire 25 g (17 steel screws, 15 brass inserts); cell contacts 2 g; printed PETG bending strength 50 MPa along the layers | Catalog masses; conservative strength for printed PETG |
| Decided options | Black cap leaves 10⁻³ of the through-light when backing a clear item; ambient error limit 0.5 % of signal; window crosstalk changes by 10 % between open-air readings; modulation check at 2 kHz | Assumed; cap opacity and crosstalk stability to measure at TRL 4 |

## A. Geometry and mass (R6)

The constructable design with 2.0 mm shell walls weighs about 238 g, and 258 g with the calibration cap [A3], against 250 g. The printed shells are the largest share (42 g and 47 g from the model volumes in PETG, now including the bosses, the cradle and the tongue), followed by the cell (47 g), the fixings, gasket and wire (25 g), the display board (15 g), the sun hood with its clip legs (11 g) and the display frame and cell strap (11 g) [A2]. At v0.3, with 2.5 mm walls, the scanner was 254 g (274 g with the cap), and at v0.2 it was 209 g (229 g with the cap); the parts added for construction and a realistic allowance for 17 screws and 15 inserts (25 g in place of 10 g) account for the rise. The body is 160 x 62 x 34 mm (6.3 x 2.4 x 1.3 in); the 18 mm shroud below (rim 42 mm outside and 36 mm inside) and the 20 mm hood above make it 72 mm high overall, and the hood legs make it 68 mm wide [A1]. R6 is **not met**: 8 g over with the cap, 12 g under without it. Amish decided on 2026-10-02 to thin the shell walls to 2.0 mm (WSC-DDR-004, A1), which saved 17 g from the shells and 16 g in all, and to count the cap, which is carried for backing clear items. The remaining 8 g is left until the first prototype is weighed at TRL 4; the register WSC-DEC-001 holds the decision.

## B. Band coverage and detector response (R1)

Seven of the eight bands sit where a standard InGaAs detector responds well, but the 1,650 nm band is clipped by the detector's cutoff: its detected centroid moves down to about 1,628 nm and only about 31 % of its detected signal lies at 1,650 nm or above [B1, B2]. Responsivity falls to 0.28 A/W at 1,700 nm and 0.05 A/W at 1,720 nm [B2]. Only the 1,200 nm band falls inside the 1,150 to 1,250 nm C-H second-overtone region; the 1,650 to 1,750 nm first-overtone region is reached only at its short edge [B3]. The 850 nm band has a mean responsivity of only 0.20 A/W, which the brighter 850 nm LED offsets [B1].

This supports the TRL 2 concern that PE versus PP, which relies on features near 1,700 nm, is the weak point. R1 is **at risk**. It cannot be verified without a labeled item set, so the design keeps eight bands.

**Paper band study (decision O3 of 2026-10-02) [B4 to B7].** The study builds a reference reflectance spectrum for PET, HDPE, PP, PS and PVC from the published near-infrared band positions of each polymer (the C-H second overtone near 1,200 nm, the combination bands from 1,370 to 1,420 nm, the first overtone from 1,680 to 1,765 nm, and the aromatic bands of PET and PS). Positions come from the polymer near-infrared literature; the depths and widths are approximate, and these are not digitized spectra, so the result is an indication only. Each LED band is a Gaussian multiplied by the detector responsivity, and 4,000 simulated items per resin carry a 15 % common scale error (which cancels in the band ratios), 1.5 % independent scatter per band for texture, wall and dirt, a tilt of 10 % across the bands and the 1/450 reading noise. A linear discriminant classifier on the log band ratios then scores a fresh set. With eight bands, 89.5 % of items are classified correctly; PE is called PP 7.4 % of the time and PP is called PE 6.9 % of the time [B4, B5]. Without the 1,650 nm band the figure falls to 72 %, so that band, although clipped by the detector, carries the PE and PP difference. A six-band set (no 1,050 or 1,300 nm) scores 88 %, close to eight, which is a pointer for the savings in WSC-DEC-001. The answer is sensitive to the assumed item scatter: 96.7 % at 1.0 % scatter and 99.9 % at 0.5 % [B6]. So the study does not show eight bands meeting the 95 % target at the assumed scatter, and does not show that they cannot; only measured items can settle it [B7]. The decision of 2026-10-02 adds the extended InGaAs band only if the study shows PE and PP cannot be told apart to R1 with eight bands. That is not shown either way, so the extended band is **not added**; it is raised as a proposal for Amish in WSC-DEC-001 and the first labeled item set at TRL 4 should decide it.

## C. Optical signal, crosstalk and noise (R1, R3)

In shade, every band has a signal-to-noise ratio of about 450 or more even on a clear, weakly reflecting item, against about 200 needed to resolve 0.5 % reflectance differences [C4]. The Lambertian collection factor is 4.6 x 10⁻⁴ per unit reflectance [C1]. On the white reference, the detected power ranges from 0.35 µW at 1,650 nm to 5.2 µW at 850 and 940 nm, giving 10 to 115 mV at 47 kΩ [C2]. The TRL 2 figure of 0.1 to 1 µA stands; the strongest band gives 2.45 µA [C3].

Two findings matter more than noise:

- **Window crosstalk.** LED light reflected by the window's item-side surface can reach the detector through the glass under the baffle tube. The path is 13.8 mm, and the crosstalk is of the same order as the signal from a 0.5-reflectance item [C5]. It is a fixed offset per band that an open-air reading can remove, but dirt or scratches on the window change it. Amish accepted option (a) on 2026-09-25 (WSC-DDR-003 D11): the calibration routine takes an open-air reading and subtracts the offset. Because the offset is as large as the signal, a 10 % change from window dirt leaves about 10 % of the signal as error; to stay under 0.5 % the offset must stay within 0.5 % of itself between open-air readings [C7]. That is unlikely on a dirty window, so the decided fallback, a baffle extended through the glass with separate LED and detector windows (option (b)), is probably needed. Whether it is needed can only be shown by measurement at TRL 4.
- **Black items.** A carbon-black item returns about 8 % of a typical item's signal. A threshold at mean reflectance 0.08 separates it with a signal-to-noise ratio of about 180, so black items read "unknown" reliably [C6]. The wrong-result rate in R3 needs labeled item data, so R3 is **not verifiable at TRL 3**.

## D. Sunlight and stray light (R4)

The shroud stops sunlight falling on the spot, but not light passing through the item from behind. For a clear or translucent item in direct sun, light through the item fills the 36 mm rim with a view factor of 0.40 and puts about 28 µW, or 22.7 µA, on the detector [D1]. The TRL 2 gain of 1 MΩ would saturate at 22.7 V; 47 kΩ keeps the output at 1.07 V, inside the 2.048 V ADC range [D2], and the design now uses 47 kΩ. The shot-noise-limited signal-to-noise ratio is still about 430 [D4].

The limit is change in the ambient light, not noise. Ambient is about 936 times the 1,650 nm signal from a clear item, so a 1 % change per 10 ms from hand movement leaves about 7.5 mV after interleaved dark subtraction, against 1.14 mV of signal [D3]. On an opaque item the rim leak is small and the same error is 0.13 % of signal [D5]. Without a change, R4 would not be met for clear and translucent items in direct sun. Amish accepted option (b) on 2026-09-25 (WSC-DDR-003 D8 and D9):

- **Backing step.** The user backs a clear or translucent item with the calibration cap, which is now printed in black PETG. The PTFE disc sits behind the wall, so the scanner reads light that passes through the wall and back (effective reflectance about 0.18), and the black cap blocks sunlight from behind. With 10⁻³ of the through-light left, the drift error is 7.5 µV against 2.06 mV, or 0.36 % of signal, inside the 0.5 % limit [D6]. The classifier needs training data taken in this backed mode.
- **Dark-level prompt.** The firmware shows "shade or back with cap" instead of a result when the mean dark level exceeds 0.71 times the weakest band reading, the point at which the drift error reaches 0.5 %. An unbacked clear item in sun sits at about 936 times and is refused; a backed item (0.52) and an opaque item (0.19) get a result [D7].
- **Modulation check (option (a), paper only).** Pulsing the LEDs at 2 kHz with synchronous demodulation shortens the light-to-dark gap to 0.25 ms, but an unbacked clear item in sun would still carry an error of about 23 % of the 1,650 nm signal, and the ADC would need 8 kS/s or more or an analog demodulator [D8]. Option (a) therefore does not replace the backing step; restating R4 (option (c)) is not needed.

With these, R4 as restated in WSC-REQ-001 v0.4 is **met by estimate**: opaque items carry 0.13 % error, backed clear items 0.36 %, and unbacked clear items in sun are refused rather than misread.

## E. Scan timing (R2)

A reading takes 14.1 ms: 2 ms of settling plus four conversions of 3.03 ms. Eight bands and nine interleaved dark readings take 240 ms [E1]. With classification, display update and debounce, button to result is about 0.33 s against 1.5 s [E2]. R2 is met.

## F. Power and battery (R5)

The average draw is about 109 mA (0.39 W), dominated by the display backlight and the microcontroller; the LEDs use about 42 mJ per scan, or 0.77 mA on average [F1, F2]. The 10.8 Wh cell, 80 % usable, lasts about 22.1 h against 8 h [F2]. A USB charge takes about 7.2 h at an assumed 500 mA [F3]. R5 is met.

## G. Log storage (R9)

At 64 bytes per record (layout in WSC-DDR-002), 10,000 scans take 625 kB, and an 8 MB log partition of the 16 MB flash holds about 131,000 scans. A CSV export of 10,000 rows is about 1.4 MB [G1]. R9 is met.

## H. Eye safety (R14)

The emission stays well inside the IEC 62471 exempt group by estimate. The brightest LED (850 nm, 15 mW, ±10°) has a radiant intensity of about 157 mW/sr [H1]. At the 200 mm reference distance, corneal irradiance is 3.9 W/m², against an exempt limit of 100 W/m²; at the shroud rim it would be about 241 W/m² if an LED were held on continuously, and about 0.23 W/m² averaged over normal use [H2]. The weighted retinal thermal radiance is about 3.8 % of the exempt limit [H3]. R14 is met by estimate. Because a stuck LED at the rim would exceed the corneal limit over long exposures, the LED drivers need a hardware limit on on-time (see WSC-PRC-001, Safety). The limit values are those of IEC 62471:2006 as understood here; confirm them against the standard and the LED datasheets.

## I. Display legibility (R7)

In 100 klx sun, the screen reflects about 637 cd/m² over a 400 cd/m² image, giving about 1.6:1 contrast against about 3:1 needed [I1]. Shaded from direct sun (about 15 klx of sky light), contrast is about 5.2:1 [I2]. Amish accepted option (a) on 2026-09-25 (WSC-DDR-003 D10): a clip-on sun hood with walls 20 mm high on both sides and at the head end of the 46 x 24 mm window, open toward the user. The screen is fully shaded when the sun is at least 50° from the screen normal on a side, or 67° on the head end. At 45° the hood shades 83 % of the screen from the side and 43 % from the head end; at 30°, 48 % and 25 % [I3]. The shaded part reads at about 5.2:1; with the sun near the screen normal or over the open side, contrast stays about 1.6:1 [I4]. Large color and icon cues remain the main result. R7 moves from not met to **at risk**: legibility in direct sun now depends on how the user holds the scanner relative to the sun.

## J. Drop and temperature (R10, R11)

A 1.2 m drop delivers about 2.8 J. On a shell corner with about 1 mm of crush, deceleration is about 1,200 g; landing on the TPU shroud, about 120 g [J1]. The cell cradle must then hold the cell against about 550 N and the display board against about 180 N [J2]. In the constructable design the cell is held down by a printed PETG strap 10 mm wide and 8 mm deep over a 29 mm span: with the whole 553 N at mid-span its bending stress is about 38 MPa against about 50 MPa for printed PETG along the layers, a margin of 1.3, and each of its two M3 inserts carries about 277 N, well inside the pull-out strength of a brass insert in PETG [J4]. The margin is thin because the drop load is a first-order estimate; the strap is printed with its layers along the bar for that reason. IP54 and the 0 to 45 °C range depend on the gasket and the cell, so The 2.0 mm walls leave the cell load unchanged; the thinner shell corners and the bosses and ribs that stiffen them are checked in the drop test at TRL 4, which is the decided way to close R10 for this change. R10 is **not verifiable at TRL 3**.

LED output drifts about 0.4 %/°C, so the 5 % drift warning in R11 trips after about 12.5 °C of change since the last white reference [J3]. A morning calibration at 25 °C will need repeating by a hot midday. The cap makes this a 10 s step, so R11 is met by design.

## K. Cost (R12)

Value-engineering target: USD 150 (`budget_usd`, a hypothetical control target, not a limit; Amish, 2026-10-01). Estimated cost of the constructable design: USD 167.50 (USD 17.50 over the target) [K2]. The priced BOM has 19 lines; the LEDs and photodiode are USD 92.00, or 55 % [K1]. Making the design constructable added USD 3.50 net (display frame, cell strap, gasket and more fixings; the bought cell holder became contacts in a printed cradle). The cost drivers and the savings worth trying are in the design decisions register WSC-DEC-001.

## Results

*Table 2. Requirement status at TRL 3, weakest first [L1, L2]. One is not met (R6); R12 is reported against the value-engineering target.*

| ID | Requirement | Value | Target | Status |
| --- | --- | --- | --- | --- |
| R6 | One-handed and light | 238 g (258 g with cap); 160 x 62 x 34 mm | 250 g; 170 x 65 x 40 mm plus shroud and hood | **Not met** (was met) |
| R1 | Identify common resins | 8 bands; paper band study 89 % correct, PE versus PP 93 %; 1,650 nm band centroid 1,628 nm, 31 % of its signal at or above 1,650 nm | 95 % correct on 5 resins | At risk |
| R7 | Readable by anyone | 5.2:1 where the hood shades the screen; 1.6:1 with the sun near the screen normal or over the open side | Legible in direct sun (about 3:1) | At risk (was not met) |
| R13 | Work with WasteWise-ml | Record decided on this side (WSC-DDR-002 v0.2); not yet adopted by WasteWise-ml | Shared documented format | At risk |
| R3 | Fail safe on unreadable items | Black items fall below the 0.08 threshold; wrong-result rate needs item data | 2 % or fewer wrong | Not verifiable at TRL 3 |
| R10 | Rugged | Corner drop about 1,200 g; cell needs about 550 N retention | 1.2 m drop, IP54, 0 to 45 °C | Not verifiable at TRL 3 |
| R2 | Fast result | 0.33 s | 1.5 s or less | Met |
| R4 | Work in sunlight | Opaque 0.13 %, backed clear 0.36 % of signal; unbacked clear items in sun refused by the dark-level prompt | Same result in 100 klx sun; clear items backed with the cap | Met (estimate; was not met) |
| R5 | Last a shift | 22.1 h | 8 h or more | Met |
| R8 | Local price grade | Price table on the device, offline | Editable local grades | Met (by design) |
| R9 | Log scans | About 131,000 scans | 10,000 scans | Met |
| R11 | Stay calibrated | Cap reference and open-air reading; 5 % drift after about 12.5 °C | Check in 10 s; warn at 5 % | Met (by design) |
| R12 | Low cost | USD 167.50 prototype | USD 150 value-engineering target | USD 17.50 over the target |
| R14 | Eye-safe illumination | 3.9 W/m² at 200 mm; 3.8 % of the retinal limit | IEC 62471 exempt | Met (estimate) |

Summary: 1 not met (R6), 3 at risk (R1, R7, R13), 2 not verifiable at TRL 3 (R3, R10), 7 met; R12 USD 17.50 over the value-engineering target.

## Checks against earlier documents

- Scan time: the TRL 2 figure of about 0.6 s assumed 15 ms per conversion; with 330 samples/s and interleaved darks it is about 0.33 s. WSC-PRC-001 v0.3 now uses 0.33 s.
- Battery life: about 17 h at TRL 2 (0.5 W); about 22 h here (0.39 W). The precis now uses about 22 h.
- Mass: about 170 g at TRL 2; 202 g here from model volumes. The precis now uses 202 g.
- Photocurrent: the TRL 2 range of 0.1 to 1 µA is confirmed for most bands; the brightest reaches about 2.5 µA.
- Cost: $163.00 at v0.1; $164.00 at v0.2 with the sun hood.
- Mass: 202 g at v0.1; 209 g at v0.2 with the sun hood.
- Cost: USD 167.50 at v0.3 with the parts added for construction (WSC-DDR-004).
- Mass: 254 g at v0.3 (274 g with the cap), with the parts added for construction and a 25 g fixings allowance.
- Mass: 238 g at v0.4 (258 g with the cap), with 2.0 mm shell walls (decision of 2026-10-02).

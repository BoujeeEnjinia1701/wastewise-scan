---
doc_id: WSC-CAL-001
title: WasteWise Scan sizing calculations
project: WasteWise Scan
doc_type: Calculation
version: "0.1"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First issue for TRL 3 (mass, band coverage, signal and noise, sunlight, timing, power, logging, eye safety, display, drop and drift, cost)
---

# WasteWise Scan sizing calculations

On paper, WasteWise Scan meets eight of its fourteen requirements, has two at risk and two not met; two cannot be verified at TRL 3. The two not met are sunlight (R4), because light passing through a clear or translucent item in direct sun reaches the detector at about 900 times the weakest band signal and hand movement leaves an error several times the signal after dark subtraction; and display legibility (R7), because an IPS screen of about 400 cd/m² gives about 1.6:1 contrast in 100 klx sun, against about 3:1 needed. The two at risk are resin accuracy (R1), because the 1,650 nm band reaches only the short edge of the 1,650 to 1,750 nm polymer region on a standard InGaAs detector, and the shared record (R13), which is drafted but not agreed. The calculations changed two parts of the TRL 2 concept: the transimpedance gain drops from 1 MΩ to 47 kΩ so that sunlight through clear items does not saturate the amplifier, and each band reading now sits between two dark readings. Scan time falls from the TRL 2 estimate of about 0.6 s to about 0.33 s; mass rises from about 170 g to 202 g. Every number in this note is printed by `docs/04-calcs/sizing.py`; the tag in brackets, for example [C4], is the line of that script's output that carries it.

> **Safety:** These are first-principles estimates for a paper proof of concept. They do not replace measurements of LED emission, drop behavior, cell temperature or classification accuracy. The scanner identifies resin only and must never be used to judge whether waste is safe to handle. See WSC-PRC-001, Safety.

## Scope and method

The note checks every requirement in WSC-REQ-001 v0.3 against the design in WSC-PRC-001 v0.3 and the parametric model `cad/src/model.py`. The script imports the model's `PARAMS`, `derived()` and part solids, so the shells, shroud, window and optics geometry used here are those in the STEP files and in drawing WSC-DWG-001. It also reads `bom/bom.csv` and `budget_usd` in `project.yaml`. Run it from the repo root with `python docs/04-calcs/sizing.py`.

The design case is the decided configuration (WSC-DDR-001): eight LEDs from 850 to 1,650 nm, one 1 mm InGaAs photodiode, an ADS1220-class 24-bit ADC, a T-Display-S3-class board, one protected 3,000 mAh 18650 cell and an 18 mm shroud that puts the item 22 mm from the detector [C1].

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

## A. Geometry and mass (R6)

The scanner weighs about 202 g, and 222 g with the calibration cap [A3], against 250 g. The printed shells are the largest share (48 g and 47 g from the model volumes in PETG), followed by the cell (47 g) and the display board (15 g) [A2]. The TRL 2 estimate of about 170 g undercounted the shells. The body is 160 x 62 x 34 mm (6.3 x 2.4 x 1.3 in), 55 mm high with the button and the 18 mm shroud, whose rim is 42 mm outside and 36 mm inside [A1]. R6 is met.

## B. Band coverage and detector response (R1)

Seven of the eight bands sit where a standard InGaAs detector responds well, but the 1,650 nm band is clipped by the detector's cutoff: its detected centroid moves down to about 1,628 nm and only about 31 % of its detected signal lies at 1,650 nm or above [B1, B2]. Responsivity falls to 0.28 A/W at 1,700 nm and 0.05 A/W at 1,720 nm [B2]. Only the 1,200 nm band falls inside the 1,150 to 1,250 nm C-H second-overtone region; the 1,650 to 1,750 nm first-overtone region is reached only at its short edge [B3]. The 850 nm band has a mean responsivity of only 0.20 A/W, which the brighter 850 nm LED offsets [B1].

This supports the TRL 2 concern that PE versus PP, which relies on features near 1,700 nm, is the weak point. R1 is **at risk**. It cannot be verified without reference spectra and a labeled item set, and the band study that would allow six bands (WSC-DDR-001, D2) could not be run without reference spectra, so the design keeps eight bands. Whether to add a 1,700 to 1,750 nm band on an extended InGaAs detector remains open (WSC-DDR-001, O3).

## C. Optical signal, crosstalk and noise (R1, R3)

In shade, every band has a signal-to-noise ratio of about 450 or more even on a clear, weakly reflecting item, against about 200 needed to resolve 0.5 % reflectance differences [C4]. The Lambertian collection factor is 4.6 x 10⁻⁴ per unit reflectance [C1]. On the white reference, the detected power ranges from 0.35 µW at 1,650 nm to 5.2 µW at 850 and 940 nm, giving 10 to 115 mV at 47 kΩ [C2]. The TRL 2 figure of 0.1 to 1 µA stands; the strongest band gives 2.45 µA [C3].

Two findings matter more than noise:

- **Window crosstalk.** LED light reflected by the window's item-side surface can reach the detector through the glass under the baffle tube. The path is 13.8 mm, and the crosstalk is of the same order as the signal from a 0.5-reflectance item [C5]. It is a fixed offset per band that an open-air reading can remove, but dirt or scratches on the window change it. This is listed for Amish in `docs/REVIEW.md`.
- **Black items.** A carbon-black item returns about 8 % of a typical item's signal. A threshold at mean reflectance 0.08 separates it with a signal-to-noise ratio of about 180, so black items read "unknown" reliably [C6]. The wrong-result rate in R3 needs labeled item data, so R3 is **not verifiable at TRL 3**.

## D. Sunlight and stray light (R4)

The shroud stops sunlight falling on the spot, but not light passing through the item from behind. For a clear or translucent item in direct sun, light through the item fills the 36 mm rim with a view factor of 0.40 and puts about 28 µW, or 22.7 µA, on the detector [D1]. The TRL 2 gain of 1 MΩ would saturate at 22.7 V; 47 kΩ keeps the output at 1.07 V, inside the 2.048 V ADC range [D2], and the design now uses 47 kΩ. The shot-noise-limited signal-to-noise ratio is still about 430 [D4].

The limit is change in the ambient light, not noise. Ambient is about 936 times the 1,650 nm signal from a clear item, so a 1 % change per 10 ms from hand movement leaves about 7.5 mV after interleaved dark subtraction, against 1.14 mV of signal [D3]. On an opaque item the rim leak is small and the same error is 0.13 % of signal [D5]. R4 is therefore **not met** for clear and translucent items in direct sun and met by estimate for opaque items. Options are listed in `docs/REVIEW.md`.

## E. Scan timing (R2)

A reading takes 14.1 ms: 2 ms of settling plus four conversions of 3.03 ms. Eight bands and nine interleaved dark readings take 240 ms [E1]. With classification, display update and debounce, button to result is about 0.33 s against 1.5 s [E2]. R2 is met.

## F. Power and battery (R5)

The average draw is about 109 mA (0.39 W), dominated by the display backlight and the microcontroller; the LEDs use about 42 mJ per scan, or 0.77 mA on average [F1, F2]. The 10.8 Wh cell, 80 % usable, lasts about 22.1 h against 8 h [F2]. A USB charge takes about 7.2 h at an assumed 500 mA [F3]. R5 is met.

## G. Log storage (R9)

At 64 bytes per record (layout in WSC-DDR-002), 10,000 scans take 625 kB, and an 8 MB log partition of the 16 MB flash holds about 131,000 scans. A CSV export of 10,000 rows is about 1.4 MB [G1]. R9 is met.

## H. Eye safety (R14)

The emission stays well inside the IEC 62471 exempt group by estimate. The brightest LED (850 nm, 15 mW, ±10°) has a radiant intensity of about 157 mW/sr [H1]. At the 200 mm reference distance, corneal irradiance is 3.9 W/m², against an exempt limit of 100 W/m²; at the shroud rim it would be about 241 W/m² if an LED were held on continuously, and about 0.23 W/m² averaged over normal use [H2]. The weighted retinal thermal radiance is about 3.8 % of the exempt limit [H3]. R14 is met by estimate. Because a stuck LED at the rim would exceed the corneal limit over long exposures, the LED drivers need a hardware limit on on-time (see WSC-PRC-001, Safety). The limit values are those of IEC 62471:2006 as understood here; confirm them against the standard and the LED datasheets.

## I. Display legibility (R7)

In 100 klx sun, the screen reflects about 637 cd/m² over a 400 cd/m² image, giving about 1.6:1 contrast against about 3:1 needed [I1]. Shaded from direct sun (about 15 klx of sky light), contrast is about 5.2:1 [I2]. R7 is **not met** in direct sun. Options (a visor, a sunlight-readable reflective display, or a user instruction to shade the screen) are listed in `docs/REVIEW.md`.

## J. Drop and temperature (R10, R11)

A 1.2 m drop delivers about 2.4 J. On a shell corner with about 1 mm of crush, deceleration is about 1,200 g; landing on the TPU shroud, about 120 g [J1]. The cell cradle must then hold the cell against about 550 N and the display board against about 180 N [J2]. IP54 and the 0 to 45 °C range depend on the gasket and the cell, so R10 is **not verifiable at TRL 3**.

LED output drifts about 0.4 %/°C, so the 5 % drift warning in R11 trips after about 12.5 °C of change since the last white reference [J3]. A morning calibration at 25 °C will need repeating by a hot midday. The cap makes this a 10 s step, so R11 is met by design.

## K. Cost (R12)

The priced BOM has 15 lines and totals $163.00, 8.7 % over the $150 volume target in `budget_usd`; the LEDs and photodiode are $92.00, or 56 % [K1]. Amish accepted about $163 for the first prototype on 2026-09-25 (WSC-DDR-001, D2), so R12 as redefined in WSC-REQ-001 v0.3 is met for the prototype. The $150 volume target cannot be shown without volume quotes.

## Results

*Table 2. Requirement status at TRL 3, not met first [L1, L2].*

| ID | Requirement | Value | Target | Status |
| --- | --- | --- | --- | --- |
| R4 | Work in sunlight | Opaque items: error 0.13 % of signal. Clear items in sun: ambient 936 x signal, drift error 6.6 x signal | Same result in 100 klx sun with the shroud pressed on | **Not met** (clear and translucent items) |
| R7 | Readable by anyone | 1.6:1 contrast in direct sun; 5.2:1 shaded | Legible in direct sun (about 3:1) | **Not met** |
| R1 | Identify common resins | 8 bands; 1,650 nm band centroid 1,628 nm, 31 % of its signal at or above 1,650 nm | 95 % correct on 5 resins | At risk |
| R13 | Work with WasteWise-ml | Hand-off designed; record drafted in WSC-DDR-002, not agreed | Shared documented format | At risk |
| R3 | Fail safe on unreadable items | Black items fall below the 0.08 threshold; wrong-result rate needs item data | 2 % or fewer wrong | Not verifiable at TRL 3 |
| R10 | Rugged | Corner drop about 1,200 g; cell needs about 550 N retention | 1.2 m drop, IP54, 0 to 45 °C | Not verifiable at TRL 3 |
| R2 | Fast result | 0.33 s | 1.5 s or less | Met |
| R5 | Last a shift | 22.1 h | 8 h or more | Met |
| R6 | One-handed and light | 202 g (222 g with cap); 160 x 62 x 34 mm | 250 g; 170 x 65 x 40 mm | Met |
| R8 | Local price grade | Price table on the device, offline | Editable local grades | Met (by design) |
| R9 | Log scans | About 131,000 scans | 10,000 scans | Met |
| R11 | Stay calibrated | Cap reference; 5 % drift after about 12.5 °C | Check in 10 s; warn at 5 % | Met (by design) |
| R12 | Low cost | $163.00 prototype | About $163 prototype (accepted); $150 volume target | Met (prototype) |
| R14 | Eye-safe illumination | 3.9 W/m² at 200 mm; 3.8 % of the retinal limit | IEC 62471 exempt | Met (estimate) |

Summary: 2 not met (R4, R7), 2 at risk (R1, R13), 2 not verifiable at TRL 3 (R3, R10), 8 met.

## Checks against earlier documents

- Scan time: the TRL 2 figure of about 0.6 s assumed 15 ms per conversion; with 330 samples/s and interleaved darks it is about 0.33 s. WSC-PRC-001 v0.3 now uses 0.33 s.
- Battery life: about 17 h at TRL 2 (0.5 W); about 22 h here (0.39 W). The precis now uses about 22 h.
- Mass: about 170 g at TRL 2; 202 g here from model volumes. The precis now uses 202 g.
- Photocurrent: the TRL 2 range of 0.1 to 1 µA is confirmed for most bands; the brightest reaches about 2.5 µA.
- Cost: $163.00, unchanged.

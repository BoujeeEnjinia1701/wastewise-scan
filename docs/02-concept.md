---
doc_id: WSC-PRC-001
title: WasteWise Scan design precis
project: WasteWise Scan
doc_type: Design precis
version: "0.2"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-24'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Populate to TRL 2 (architecture, first-order numbers, safety, media)
---

# WasteWise Scan design precis

WasteWise Scan is a palm-sized scanner that the user presses against a plastic item. It flashes eight near-infrared bands one after another, reads the reflection with an InGaAs photodiode, and within about a second shows the resin, a confidence mark and the local price grade. First-order numbers suggest it can meet the speed, battery, mass and logging requirements; resin accuracy (R1) is not yet shown, and the parts cost of about $163 is about 9 % over the $150 target (R12).

![Hero render](../media/hero.png)

*Figure 1. Concept render. The grey hand and the blue crate panel are for scale only.*

## Key finding: the sensor

The scaffold named an 18-channel AS7265x-class sensor. That chip covers about 410 to 940 nm ([SparkFun Triad board](https://www.sparkfun.com/products/15050)), which misses the polymer absorption bands near 1,150 to 1,250 nm and 1,650 to 1,750 nm that NIR sorters rely on ([Neo et al. 2023](https://doi.org/10.1016/j.resconrec.2022.106217)). In the visible range it mostly sees pigment color, which an ordinary camera and WasteWise-ml already see. This precis therefore proposes the approach proven by the open [Plastic Scanner](https://github.com/Plastic-Scanner) project: discrete NIR and short-wave infrared (SWIR) LEDs from 850 to 1,650 nm and one InGaAs photodiode. It is still a low-cost multispectral sensor, so the pitch is unchanged. **Proposed, awaiting Amish** (see Open questions).

## How it works

1. **Press.** The user presses the soft black shroud against a flat or gently curved part of the item. The shroud blocks sunlight and fixes the distance between optics and item.
2. **Illuminate and read.** On a button press the firmware takes a dark reading, then pulses each of eight LEDs in turn (850, 940, 1,050, 1,200, 1,300, 1,450, 1,550 and 1,650 nm, proposed set) while a transimpedance amplifier and 24-bit ADC read the diffuse reflection at the photodiode. Each band is read four times and averaged; the dark reading is subtracted.
3. **Normalize.** Readings are divided by the last white reference taken in the calibration cap, giving a reflectance value per band that is independent of LED aging and temperature, to first order.
4. **Classify.** A small classifier on the ESP32-S3 (for example linear discriminant analysis or a small decision tree on normalized band ratios, trained on labeled items) returns a resin and a confidence. Below the confidence threshold, or when overall reflectance is too low (black items), it shows "unknown".
5. **Show and log.** The display shows resin code, name, color and icon, plus the grade from the local price table. Each scan is logged with time, bands, result and confidence for export over USB.
6. **Hand off.** Unknown or low-confidence items can be photographed with a phone and passed to WasteWise-ml; the shared scan record lets the two results be combined later.

![Item flow](../media/flow.png)

*Figure 2. Item flow per 100 mixed plastic items. All values are estimates for concept review.*

## Main components

Table 1. Main components. Numbers match the BOM and the exploded view.

| # | Component | Proposed choice | Notes |
| --- | --- | --- | --- |
| 1 | Top shell | 3D-printed PETG with display window and button hole | Sealed with a gasket to the bottom shell |
| 2 | Controller and display | ESP32-S3 board with 1.9 in IPS display and on-board Li-ion charger (LilyGO T-Display-S3 class) | No custom PCB. Proposed, awaiting Amish |
| 3 | LED ring | Eight LEDs, 850 to 1,650 nm, around the photodiode at about 45° to the window | SWIR LEDs dominate cost |
| 4 | Photodiode | InGaAs PIN photodiode, 1 mm, about 900 to 1,700 nm | Standard InGaAs, cutoff near 1,700 nm |
| 5 | Amplifier and ADC | Low-noise op-amp transimpedance stage, 24-bit ADC (ADS1220 class), LED current drivers | On perfboard for the first build |
| 6 | Window | Borosilicate glass disc, 25 mm, 2 mm | Transmits well to beyond 2 µm; keeps dust out |
| 7 | Light shroud | Black TPU cone, 18 mm deep, 42 mm across the rim | Blocks sunlight, sets distance |
| 8 | Battery | One protected 18650 Li-ion cell, 3,000 mAh | Common, cheap and replaceable |
| 9 | Cell holder and USB-C | Holder, protection and wiring to the board charger | |
| 10 | Bottom shell and grip | 3D-printed PETG, textured grip | |
| 11 | Scan button | Large sealed push button for gloved hands | |
| 12, 13 | Calibration cap | Printed cap with a white PTFE reference disc; stores over the shroud | Protects the window and gives a daily white reference |

![Exploded view](../media/exploded.png)

*Figure 3. Exploded view with BOM numbers.*

## First-order numbers

All values are estimates for concept review and will be checked at TRL 3.

Table 2. First-order numbers.

| Quantity | Estimate | Basis | Requirement |
| --- | --- | --- | --- |
| Scan time | about 0.6 s | 9 readings (8 bands plus dark) x 4 averages x about 15 ms (LED settle plus ADC conversion), plus classify and display about 50 ms | R2 (1.5 s) met |
| Photocurrent at the detector | about 0.1 to 1 µA (estimate) | 2 to 5 mW LED output, a few percent of diffuse reflection reaching a 1 mm detector, about 1 A/W InGaAs responsivity | Gives 0.1 to 1 V from a 1 MΩ transimpedance stage |
| Average power | about 0.5 W | ESP32-S3 and display backlight about 110 mA at 3.7 V; LED pulses negligible at 4 scans per minute | |
| Battery life | about 17 h | 3,000 mAh x 3.6 V = 10.8 Wh, 80 % usable | R5 (8 h) met |
| Log size | about 64 B per scan, 10,000 scans under 1 MB | 8 bands and dark as 4-byte values plus time, result, confidence | R9 met |
| Mass | about 170 g without cap, about 195 g with cap | Shells 70 g, cell 47 g, board 15 g, optics 15 g, shroud 10 g, window 3 g, fixings 10 g; cap 25 g | R6 (250 g) met |
| Size | 160 x 62 x 34 mm (6.3 x 2.4 x 1.3 in) plus 18 mm shroud | Massing model | R6 met |
| Share of items identified | about 78 of 100 (estimate) | About 12 % black or dark, about 10 % low confidence; both depend on the local waste stream | R3 intent |
| Parts cost | about $163 | Indicative prices, see bom/bom.csv | **R12 ($150) not met** |

## Key design choices

- **Discrete LEDs and one InGaAs photodiode rather than a spectrometer or a visible-range chip.** A SWIR spectrometer module costs far more than the budget; a visible-range chip misses the polymer bands. Eight well-chosen bands are enough to separate the five target resins in prior work, but the band set needs a study on reference spectra at TRL 3. Proposed, awaiting Amish.
- **Contact measurement through a shroud.** Pressing on the item removes most sunlight and fixes geometry, which matters more than extra bands for a low-cost device.
- **Say "unknown" rather than guess.** A wrong call can contaminate a bale; the confidence threshold is set for few false results, accepting more unknowns (R3).
- **White reference in the protective cap.** The user calibrates by pressing the scanner into its own cap, so calibration happens naturally at the start of each shift.
- **Local price table on the device.** Grades are what matter to users, and prices are local and change often. The cooperative edits them; no cloud service is needed.
- **One common 18650 cell.** Available and replaceable in most markets; the board's charger keeps the build simple.

![Cutaway](../media/cutaway.png)

*Figure 4. Cutaway through the optical axis: LED ring, photodiode, amplifier board and window above the shroud, with the cell and controller behind.*

## Safety

> **Safety:** The scanner identifies plastic resin only. It must never be used to judge whether an item is safe to handle, or to classify hazardous, medical, chemical or pesticide containers. Waste handling carries cut, needle-stick and chemical risks: wear gloves and follow local guidance.

> **Safety:** The 18650 lithium-ion cell stores about 11 Wh. Use a protected cell from a known supplier, charge with the board's charger only, do not charge in direct sun or above 45 °C, and stop using a cell that is dented, swollen or wet. Do not leave the device on hot surfaces or in closed vehicles.

> **Safety:** The SWIR LEDs are invisible to the eye, so a user cannot tell when they are on. They are low power (a few mW each), pulse for under a second and fire only on a button press, which keeps emission in the IEC 62471 exempt group by estimate. Do not look into the window during a scan. This must be confirmed from LED datasheets at TRL 3.

- Black and dark items read "unknown". Users must not treat "unknown" as any particular resin.
- The result is advice for sorting, not a certificate of material grade for sale.

## Open questions for TRL 3

1. **Sensor approach.** Option A: discrete NIR and SWIR LEDs with an InGaAs photodiode (recommended; covers the polymer bands; about $92 of optics). Option B: AS7265x only (cheaper and simpler, about $70 board, but unlikely to meet R1 beyond color). Option C: A plus an AS7265x for color (best data for WasteWise-ml, about $70 more, well over budget). Proposed: A, awaiting Amish.
2. **Band set.** Confirm the eight wavelengths against published reference spectra; decide whether a 1,700 to 1,750 nm band (extended InGaAs, higher cost) is needed to separate PE from PP.
3. **Classifier.** Linear discriminant analysis or a small decision tree first, trained on an open labeled dataset shared with Plastic Scanner where licenses allow. Proposed, awaiting Amish.
4. **Budget.** About $163 against $150. See docs/REVIEW.md for options.
5. **Scan record format** shared with WasteWise-ml and the material passport in ReflowEconomy.
6. **First users and region** for co-design and for the first price table.

Concept media: [blueprint sheet](../media/concept-blueprint.pdf), [interactive 3D model](../media/viewer.html).

# WasteWise Scan

![TRL 2](https://img.shields.io/badge/TRL-2%20of%209-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827)

**Area:** Circular Materials · **TRL:** 2 of 9 (concept formulated) · **Prototype budget:** about $150 USD · **Difficulty:** 3 of 5

Handheld near-infrared scanner that identifies common plastic resins (PET, HDPE, PP, PS, PVC) in about a second using a low-cost multispectral sensor, shows the result and a local price grade, and logs scans. It pairs with WasteWise-ml for items the spectrum cannot resolve.

![WasteWise Scan concept](media/hero.png)

[Interactive 3D model](media/viewer.html) · [Concept blueprint (PDF)](media/concept-blueprint.pdf) · [Review note](docs/REVIEW.md)

## Problem

Cameras cannot reliably tell PET from PP or HDPE, yet resin type sets the price a waste picker or small recycler receives. Commercial near-infrared sorters cost far too much for informal and small-scale operators.

## Concept

Press the soft shroud against an item and press the button. The scanner pulses eight near-infrared bands from 850 to 1,650 nm, reads the reflection with an InGaAs photodiode, and in about 0.6 s (estimate) shows the resin, a confidence mark and the local price grade. Black, dark and low-confidence items read "unknown" and can be passed to WasteWise-ml. A white reference inside the protective cap keeps it calibrated.

The scaffold named an AS7265x-class sensor, but that chip stops at 940 nm, short of the main polymer bands. The precis proposes discrete LEDs and an InGaAs photodiode instead, following the open Plastic Scanner project; this choice is awaiting Amish.

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- Ring of eight NIR and SWIR LEDs, 850 to 1,650 nm
- InGaAs photodiode with transimpedance amplifier and 24-bit ADC
- ESP32-S3 board with 1.9 in display
- One 18650 Li-ion cell with USB-C charging
- Printed rugged housing with black TPU light shroud
- Calibration cap with white PTFE reference

Indicative parts cost is about $163, about 9 % over the $150 target (proposed budget options in [docs/REVIEW.md](docs/REVIEW.md)). The working bill of materials is in [bom/bom.csv](bom/bom.csv).

## Safety

> **Safety:** The scanner identifies plastic resin only. Never use it to judge whether hazardous, medical or chemical waste is safe to handle. Black and dark plastics absorb NIR and read as unknown. The 18650 lithium-ion cell must be a protected cell, charged only with the built-in charger and kept out of heat. The SWIR LEDs are invisible; do not look into the window during a scan.

## Repository layout

| Folder | Contents |
| --- | --- |
| `docs/` | Problem, concept, requirements, calculations and design decisions |
| `cad/src/` | build123d Python source, the source of truth for all geometry |
| `cad/step/`, `cad/stl/` | Exported models for FreeCAD, other CAD tools and printing |
| `cad/drawings/` | 2D sketches and dimensioned drawings |
| `bom/` | Bill of materials |
| `electronics/` | KiCad schematics and PCB layouts |
| `firmware/` | Microcontroller code |
| `media/` | Renders, perspectives and photos |
| `build-log/` | Dated prototyping notes |

## Documentation

Controlled documents follow the portfolio [documentation standard](.kit/STANDARDS.md). Each carries a document ID (WSC-PRC-001 for the precis), a version and a revision history. Branded PDFs are built with `python .kit/render.py` and attached to GitHub Releases when a document is tagged, for example `WSC-PRC-001/v1.0`.

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

Part of the open hardware portfolio at [amishchadha.com](https://amishchadha.com).

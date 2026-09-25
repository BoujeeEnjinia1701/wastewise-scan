# WasteWise Scan

![TRL 2](https://img.shields.io/badge/TRL-2%20of%209-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827)

**Area:** Circular Materials · **TRL:** 2 of 9 (concept formulated) · **Prototype budget:** about $150 USD · **Difficulty:** 3 of 5

Handheld near-infrared scanner that identifies common plastic resins (PET, HDPE, PP, PS, PVC) in about a second using a low-cost multispectral sensor, shows the result and a local price grade, and logs scans. It pairs with WasteWise-ml for items the spectrum cannot resolve.

## Problem

Cameras cannot reliably tell PET from PP or HDPE, yet resin type sets the price a waste picker or small recycler receives. Commercial near-infrared sorters cost far too much for informal and small-scale operators.

## Concept

Handheld near-infrared scanner that identifies common plastic resins (PET, HDPE, PP, PS, PVC) in about a second using a low-cost multispectral sensor, shows the result and a local price grade, and logs scans. It pairs with WasteWise-ml for items the spectrum cannot resolve.

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- Multispectral NIR sensor (e.g. AS7265x class, 18 bands)
- Broadband halogen or NIR LED illumination
- ESP32-S3 with display
- Li-ion cell and USB-C charging
- Printed rugged housing with light shroud
- Reference calibration tiles

The working bill of materials is in [bom/bom.csv](bom/bom.csv).

## Safety

> Black and dark plastics absorb NIR and will read as unknown. The scanner must never be used to classify hazardous or medical waste. 

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

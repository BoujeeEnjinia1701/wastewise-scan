---
doc_id: WSC-MKT-001
title: WasteWise Scan market and viability
project: WasteWise Scan
doc_type: Market and viability
version: "0.1"
status: Draft
date: '2026-10-24'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-24'
    author: Amish Chadha
    change: First market and viability note (kit 1.8 upgrade)
---

# WasteWise Scan market and viability

WasteWise Scan is for waste picker cooperatives that sort plastics by hand and are paid by resin grade, and who today choose between guessing and a handheld plastics identifier listed at EUR 4,930. At an estimated USD 167.50 in parts for the prototype, against a USD 150 value-engineering target for a cooperative's shared scanner, it competes on cost and on being open, so a cooperative, a makerspace or a university can build, repair and adapt it. Prices and benchmarks are cited with the date they were checked. Method: STANDARDS section 23.

Table 1. Market segments.

| Segment | Target users and region | Competitive benchmark (cited price) | Estimated cost per unit (USD) | Value proposition |
| --- | --- | --- | --- | --- |
| Waste picker cooperatives and aggregators | Member-owned cooperatives selling sorted plastics to scrap buyers; first candidate SWaCH, Pune, India | Matoha PlasTell Handheld NIR plastics identifier, EUR 4,930 (filament2print, checked 2026-10-25 for WML-MKT-001) | 167.50 (priced BOM, prototype) | Resin, confidence and the cooperative's own price grade in about a second, offline, at a small fraction of the benchmark |
| Small recyclers and buyers | Receiving bays checking bales for PVC in PET | Same benchmark; industrial NIR sorters cost far more (price not published; WSC-PRB-001, an estimate) | 167.50 | Spot checks before paying; "unknown" rather than a guess |
| Trainers, NGOs and researchers | Workshops, studies, WasteWise-ml data collection | Open Plastic Scanner (discrete-band principle; no price published on its James Dyson Award page, checked 2026-10-25) | 167.50 | Open design, documented calibration, exportable consented records |
| Individual waste pickers | Pickers who cannot buy a shared device | WasteWise-ml on a phone they own (free app) | Not targeted; the USD 150 target is for a cooperative's shared scanner (decided 2026-10-02) | Through the cooperative's shared scanner and the sibling app |

Table 2. Cited prices of the cost-driving parts (checked 2026-10-25).

| Part | BOM line and price | Cited price | Note |
| --- | --- | --- | --- |
| ESP32-S3 display board (T-Display-S3) | Line 2, USD 20.00 | From USD 9.04 at LilyGO's own store (variant-dependent) | Possible saving; shipping and duties not included |
| 1 mm InGaAs PIN photodiode | Line 4, USD 30.00 (generic, indicative) | Hamamatsu G12180-010A, EUR 104.09 each excluding VAT (RS Components Ireland; back-ordered) | A named branded part costs about three times the BOM figure; a cheaper part with a suitable curve near 1,700 nm is to assess (WSC-DEC-001 confirm item 9) |
| Eight NIR and SWIR LEDs with drivers | Line 3, USD 62.00 (indicative) | No single-unit price was found in this session | To assess with Marktech or Roithner quotes |
| MEMS-FPI sensor (option B only) | Not in the BOM | INR 26,640 per piece excluding taxes (IndiaMART, Hamamatsu C13272-02 listing) | About USD 300 at an assumed INR 88 per USD |

Value-engineering target: USD 150 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 167.50 (USD 17.50 over the target). If the photodiode is the named Hamamatsu part, the estimate rises by about USD 90; the cited display board price would take about USD 11 off.

The benefit to a cooperative is the price difference between a correctly sorted grade and mixed or rejected material, times the mass settled by the scanner. No Pune price list has been collected yet, so no figure is claimed; the first co-design sessions record the buyers' grade prices and how many doubtful items a sorter meets in a shift.

## Open route

- **Who builds it.** A makerspace, a university lab or a trained cooperative member, from the build plan WSC-BLD-001: FDM printing, heat-set inserts, through-hole soldering and one cored hole in glass. The specialist optics are bought.
- **How it spreads.** Through waste picker networks (WIEGO and the International Alliance of Waste Pickers), the Helpful Engineering volunteer network, universities and the Plastic Scanner community, alongside WasteWise-ml.
- **What keeps it open.** Hardware under CERN-OHL-S-2.0, software under MIT (REUSE.toml); calibration and classifier method published; consented spectra co-owned by the pickers' organization (decided 2026-10-02). No paid service is needed at the point of use.
- **Non-commercial by intent.** The project sells nothing; any income from better-sorted material stays with the pickers.

## Sources

- filament2print. "Identificador de Plásticos Matoha PlasTell" (PlasTell Handheld EUR 4,930.00). https://filament2print.com/es/fabricacion-filamentos/4664-identificador-plasticos-matoha-plastell.html. Checked 2026-10-25 (for WasteWise-ml WML-MKT-001, the focus-area benchmark).
- LilyGO. T-Display series collection (T-Display S3 from USD 9.04). https://lilygo.cc/collections/t-display-series. Checked 2026-10-25.
- RS Components Ireland. Hamamatsu G12180-010A InGaAs photodiode, TO-18, EUR 104.085 each excluding VAT, tube of 2. https://ie.rs-online.com/web/p/photodiodes/2616238. Checked 2026-10-25.
- IndiaMART. Hamamatsu C13272-02 MEMS-FPI spectrum sensor, INR 26,640 per piece excluding taxes. https://m.indiamart.com/proddetail/mems-fpi-spectrum-sensor-23949601312.html. Checked 2026-10-25.
- James Dyson Award. Plastic Scanner project page (low-cost discrete infrared spectroscopy; no price given). https://www.jamesdysonaward.org/ja-JP/2021/project/plastic-scanner. Checked 2026-10-25.
- BOM `bom/bom.csv` and WSC-CAL-001 K for every cost of this design.

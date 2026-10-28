---
doc_id: WSC-PLN-001
title: WasteWise Scan project plan
project: WasteWise Scan
doc_type: Project plan
version: "0.1"
status: Draft
date: '2026-10-24'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-24'
    author: Amish Chadha
    change: First project plan with resources, stage gates and references (kit 1.8 upgrade)
---

# WasteWise Scan project plan

WasteWise Scan is at stage P3 (design outputs, TRL 3): option A is modelled at D3, drawn, priced and planned to build, and option B is modelled at D3 for comparison. The next gate, P4 (verification, TRL 4), is on hold under the portfolio cap. The decisions requested from Amish are the concept selection between A and B (within 10 %, no pick) and the extended InGaAs band (WSC-DEC-001 open decisions 1 and 2). Method: STANDARDS sections 19 and 23.

## Workstreams

Table 1. Workstreams.

| Workstream | Owner (role) | Deliverable | Status |
| --- | --- | --- | --- |
| Optics and calculations | Design lead | WSC-CAL-001, WSC-STM-001 | Done at TRL 3; fix F1 in |
| Mechanical design and CAD | Design lead | `cad/src/model.py` (D3, both options), WSC-DWG-001, DWG-101 to 109 | Done at TRL 3 |
| Build plan | Design lead | WSC-BLD-001 | Done (plan, not built) |
| Requirements and traceability | Design lead | WSC-URS-001, WSC-PRS-001, WSC-RTM-001 | Done; targets to confirm in co-design |
| Co-design and partner | Project lead (Amish) | Sessions with a waste picker cooperative (first candidate SWaCH, Pune), price grades, labelled items | Not started (outreach is Amish's) |
| Shared record with WasteWise-ml | Project lead | WSC-DDR-002 adopted on both sides | At risk until WasteWise-ml adopts it |
| Regulatory | Procurement with a qualified reviewer | WSC-REG-001 items to assess (cell, radio, eye safety) | Register written; items to assess |
| Verification (P4) | Test lead | Test plans and lab reports (TST) | On hold (TRL cap 3) |

## Resources needed

Table 2. Resources. Costs are estimates for planning, not quotes.

| Resource | Deliverable | Effort | Estimated cost (USD) |
| --- | --- | --- | --- |
| Parts for one prototype | Scanner, cap, spares of the printed parts | Purchase | 167.50 (BOM); up to about 260 with a branded photodiode (WSC-MKT-001) |
| Labelled item set | 200 or more clean items of known resin, collected with the partner | 2 to 3 days with the partner | To assess |
| Maker time | Build to WSC-BLD-001 | About 3 days | To assess |
| Co-design facilitation | Two sessions with the cooperative | 2 days | To assess |
| Regulatory review | Cell, radio and eye-safety items of WSC-REG-001 | Half a day | To assess |

## Stage gates

Table 3. Stages (P4 to P6 on hold while the stage cap is P3).

| Stage | Gate criteria | Status |
| --- | --- | --- |
| P0 Proposal | PRB, STM, OPT, REG, FEA, PLN | Met (2026-10-24) |
| P1 Definition | URS, PRS draft, RSK with hazard analysis, MKT | Met (2026-10-24) |
| P2 Design inputs | PRS with targets and verification, CAL, RTM, concept selection DDR, STEM closed, feasibility | Met except the STEM check stays open (S22, S23 need users and items) and the concept selection awaits Amish |
| P3 Design outputs | Model, STEP, drawings, priced BOM, build plan, DEC, design FMEA, traceability | Met (2026-10-24) |
| P4 Verification | Lab tests of optics, accuracy on labelled items, drop and spray, timing and battery | On hold (TRL cap 3) |
| P5 Validation | Field trial with the cooperative; human factors | On hold |
| P6 Commercialization | Only with a named deployment partner | On hold |

## Next steps and decision requested

1. Amish decides the concept selection (WSC-DEC-001 open decision 2): A, the current design, or B; no pick because the scores are within 10 %.
2. Amish decides open decision 1 (extended InGaAs band now, or after the first labelled item set).
3. Approach SWaCH in Pune jointly with WasteWise-ml (decided 2026-10-02; outreach is Amish's).
4. When TRL 4 is opened: build to WSC-BLD-001, measure LED spectra, the photodiode curve, window crosstalk with fix F1, cap opacity and tube opacity, then scan the labelled item set.

## References

- ASTM International. *ASTM D7611/D7611M-21, Standard Practice for Coding Plastic Manufactured Articles for Resin Identification*. https://store.astm.org/d7611_d7611m-21.html.
- BAuA. 2013. *Photobiological Safety of Light Emitting Diodes (LEDs)*. Report F 2115. https://baua.de/EN/Service/Publications/Report/F2115. Accessed October 25, 2026.
- Bureau of Indian Standards. IS 16046 (Part 2):2018 test report format. https://www.bis.gov.in/wp-content/uploads/2026/03/UTRF_16046_2_2018.pdf. Accessed October 25, 2026.
- filament2print. "Identificador de Plásticos Matoha PlasTell." https://filament2print.com/es/fabricacion-filamentos/4664-identificador-plasticos-matoha-plastell.html. Accessed October 25, 2026.
- Granite River Labs. "A Guide to WPC and ETA Certification." https://www.graniteriverlabs.com/en-us/market-access-services/country/india/wpc-mark. Accessed October 25, 2026.
- Hackaday. 2021. "An Open Source Detector for Identifying Plastics." December 13, 2021. https://hackaday.com/2021/12/13/an-open-source-detector-for-identifying-plastics/.
- IndiaMART. "HAMAMATSU C13272-02 MEMS-FPI Spectrum Sensor." https://m.indiamart.com/proddetail/mems-fpi-spectrum-sensor-23949601312.html. Accessed October 25, 2026.
- International Electrotechnical Commission. 2006. *IEC 62471, Photobiological Safety of Lamps and Lamp Systems*.
- ISWA. 2022. *A Seat at the Table*. https://www.iswa.org/wp-content/uploads/2022/09/A-Seat-at-the-Table.pdf.
- James Dyson Award. "Plastic Scanner." 2021. https://www.jamesdysonaward.org/ja-JP/2021/project/plastic-scanner. Accessed October 25, 2026.
- Lau, Winnie W. Y., et al. 2020. "Evaluating Scenarios toward Zero Plastic Pollution." *Science* 369 (6510): 1455 to 1461. https://doi.org/10.1126/science.aba9475.
- LilyGO. "T-Display Series." https://lilygo.cc/collections/t-display-series. Accessed October 25, 2026.
- Neo, Eric Rong Kai, et al. 2022. "A Review on Chemometric Techniques with Infrared, Raman and Laser-Induced Breakdown Spectroscopy for Sorting Plastic Waste in the Recycling Industry." *Resources, Conservation and Recycling* 180: 106217. https://doi.org/10.1016/j.resconrec.2022.106217.
- NIOSH. 2004. *Easy Ergonomics: A Guide to Selecting Non-Powered Hand Tools*. DHHS (NIOSH) Publication No. 2004-164. https://cdc.gov/niosh/docs/2004-164/pdfs/2004-164.pdf. Accessed October 25, 2026.
- Photonics Online. "Ultra-Small MEMS-FPI Spectrum Sensor C13272 Datasheet." 2016. https://www.photonicsonline.com/doc/ultra-small-mems-fpi-spectrum-sensor-c-datasheet-0001. Accessed October 25, 2026.
- Photonics.com. "MEMS-FPI Sensors Detect NIR Spectra." https://www.photonics.com/Product.aspx?PRID=61532. Accessed October 25, 2026.
- Plastic Scanner. https://plasticscanner.com/ and https://github.com/Plastic-Scanner.
- pv magazine India. 2022. "Government Notifies Battery Waste Management Rules, 2022." August 25, 2022. https://www.pv-magazine-india.com/?p=10815. Accessed October 25, 2026.
- RS Components Ireland. "Hamamatsu G12180-010A IR InGaAs Photodiode." https://ie.rs-online.com/web/p/photodiodes/2616238. Accessed October 25, 2026.
- SparkFun. "SparkFun Triad Spectroscopy Sensor, AS7265x." https://www.sparkfun.com/products/15050.
- trinamiX. Mobile NIR spectroscopy. https://trinamixsensing.com/products/mobile-nir-spectroscopy/.
- WIEGO. "Waste Pickers." https://www.wiego.org/informal-economy/occupational-groups/waste-pickers.
- WRAP. "Recyclability of Black Plastic Packaging." https://www.wrap.ngo/resources/report/recyclability-black-plastic-packaging.
- WasteWise-ml regulatory register WML-REG-001 and market note WML-MKT-001 (Circular Materials focus-area research).

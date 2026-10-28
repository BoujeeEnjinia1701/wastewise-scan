---
doc_id: WSC-PRB-001
title: WasteWise Scan problem statement
project: WasteWise Scan
doc_type: Problem statement
version: "0.5"
status: Draft
date: '2026-10-24'
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
  change: Populate to TRL 2 (problem, users, context, constraints, prior work)
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: Citations checked and corrected (Neo et al. year, WIEGO wording, ASTM and WRAP links, trinamiX source); cost constraint per WSC-DDR-001 D2; open questions updated
- version: "0.4"
  date: '2026-10-02'
  author: Amish Chadha
  change: Partner, region and price-target questions answered by Amish's decisions of 2026-10-02 (WSC-DEC-001)
- version: "0.5"
  date: '2026-10-24'
  author: Amish Chadha
  change: "Kit 1.8 upgrade: users-and-needs table (Table 1) and stakeholders table (Table 2) added for the user requirements WSC-URS-001"
---

# WasteWise Scan problem statement

Resin type sets the price of a plastic item, but the people who sort most of the world's recycled plastic have no affordable way to measure it. They rely on the molded resin code, touch, sound and burn tests, and a wrong call either loses value or contaminates a whole bale.

## The problem

Mixed plastic is worth little; plastic sorted by resin (PET, HDPE, PP, PS, PVC) is worth several times more to a recycler, and a small share of the wrong resin can spoil a batch. PVC in a PET stream is the classic example, because it degrades at PET processing temperatures and discolors the melt. The informal sector carries most of this sorting work: one widely cited model estimates that the informal sector collects about 58 % of the plastic waste collected for recycling worldwide ([Lau et al. 2020, *Science*](https://doi.org/10.1126/science.aba9475), as cited in [ISWA, *A Seat at the Table*, 2022](https://www.iswa.org/wp-content/uploads/2022/09/A-Seat-at-the-Table.pdf)). Waste pickers' earnings vary widely between cities, and in many places they subsist on meager returns ([WIEGO, waste pickers](https://www.wiego.org/informal-economy/occupational-groups/waste-pickers)).

Sorting by eye is unreliable. The resin identification code molded into an item ([ASTM D7611/D7611M-21, *Standard Practice for Coding Plastic Manufactured Articles for Resin Identification*](https://store.astm.org/d7611_d7611m-21.html)) is often missing, worn or wrong, and many items look alike: a clear PP tray and a clear PET tray, or a white HDPE bottle and a white PP bottle. An ordinary camera sees color and shape, not chemistry, which is why the image model in the sibling project WasteWise-ml will struggle with exactly these pairs.

Industry solves this with near-infrared (NIR) spectroscopy. Polymers absorb short-wave infrared light at wavelengths set by their chemical bonds, mainly overtones of the C-H stretch near 1,150 to 1,250 nm and 1,650 to 1,750 nm, and those signatures differ between resins ([Neo et al. 2022, review, *Resources, Conservation and Recycling* 180](https://doi.org/10.1016/j.resconrec.2022.106217)). Materials recovery facilities use NIR optical sorters costing hundreds of thousands of dollars, and handheld NIR spectrometers for plastics (for example the [trinamiX mobile NIR system](https://trinamixsensing.com/products/mobile-nir-spectroscopy/), which works at 1,450 to 2,450 nm according to its [fact sheet](https://www.lc-oe.com/pdf/3900/factsheet_trinamix_nir_spectrometer%20vv21_10.pdf)) cost thousands of dollars plus subscriptions (price level is an estimate). None of this is within reach of a waste picker, a cooperative or a small aggregator.

## Prior work

- **Plastic Scanner** ([plasticscanner.com](https://plasticscanner.com/), [GitHub](https://github.com/Plastic-Scanner)), an open-source handheld that began as Jerry de Vos's graduation project at TU Delft ([Raspberry Pi news](https://www.raspberrypi.com/news/award-winning-plastic-scanner/)), shines discrete NIR LEDs from 850 to 1,650 nm on the item one at a time and reads the reflection with a single InGaAs photodiode ([Hackaday, 2021](https://hackaday.com/2021/12/13/an-open-source-detector-for-identifying-plastics/)). It is the closest prior work and shows that a discrete-band approach can separate common resins. WasteWise Scan builds on the same principle and adds a sunlight-readable display, local price grades, logging and a hand-off to WasteWise-ml.
- **Low-cost multispectral chips** such as the ams OSRAM AS7265x (18 channels from about 410 to 940 nm; [SparkFun Triad board](https://www.sparkfun.com/products/15050)) are cheap and easy to use, but stop short of the main polymer absorption bands. Above 940 nm only weak third-overtone features are available, so resin identification with such a chip alone is at risk (see WSC-PRC-001).
- **Black plastics** are a known limit of NIR sorting: most black packaging is colored with carbon black pigments, which do not allow it to be sorted by NIR ([WRAP, recyclability of black plastic packaging](https://www.wrap.ngo/resources/report/recyclability-black-plastic-packaging)).

## Users and context

| User | Need | Context |
| --- | --- | --- |
| Waste picker | Know which pile an item belongs in, and what it is worth, without reading or guessing | Streets, dumpsites and transfer points; sun, dust, rain; no power at work; low-cost phone at most |
| Cooperative or aggregator sorter | Check disputed items quickly; keep bales clean; train new members | Sorting shed or yard, hundreds to thousands of items per shift |
| Small recycler or buyer | Spot-check incoming bales before paying; reject PVC in PET | Receiving bay |
| Trainer, NGO or researcher | A shared, open reference for resin identification and a log of what is collected | Workshops, studies, WasteWise-ml data collection |

### Users and needs

Table 1. Users and needs (the source of the user requirements in WSC-URS-001).

| User type | Goals and needs | Typical use scenario | Pain points and challenges |
| --- | --- | --- | --- |
| Waste picker | Put each item in the right pile and know what it is worth; keep earning while checking | Streets, dumpsites and transfer points; checks a doubtful clear tray or white bottle in about a second, one-handed, gloves on | Sun, dust and rain; no power at work; limited literacy for some; a wrong call costs money; black items cannot be read by any NIR device |
| Cooperative or aggregator sorter | Keep bales clean, settle disputes quickly, train new members | Sorting shed or yard, hundreds to thousands of items per shift; a shared scanner at the bench | Look-alike pairs (PP and PET trays, HDPE and PP bottles); PVC in PET; shared device must survive daily handling |
| Small recycler or buyer | Spot-check incoming bales before paying; reject PVC in PET | Receiving bay, a few scans per bale | Needs a result it can trust or an honest "unknown"; no time for training |
| Trainer, NGO or researcher | An open reference for resin identification and a log of what is collected | Workshops and studies; WasteWise-ml data collection | Records must be exportable and consented; open design to adapt |

### Stakeholders

Table 2. Stakeholders.

| Stakeholder group | Role or interest | Engagement needed |
| --- | --- | --- |
| Member-owned waste picker cooperative (first candidate SWaCH, Pune; decided 2026-10-02) | Co-design partner, owner of the shared scanner, sets the price grades | Co-design sessions, price table, labelled item set, consent terms for spectra |
| Scrap buyers and recyclers in Pune | Set the grades and prices the cooperative is paid | Price lists by grade; which resins they reject |
| WasteWise-ml project | Sibling phone app for items the spectrum cannot resolve | Adopt the shared scan record and QR pair ID (WSC-DDR-002) |
| Municipality (Pune Municipal Corporation) and waste picker networks | Waste management rules; recognition and integration of pickers | Awareness; any rules on devices used at collection points |
| Makers and makerspaces (Helpful Engineering network, local workshops) | Build and repair the scanner from the build plan | Build plan review; local parts sourcing |
| Open-hardware prior work (Plastic Scanner) | Shared approach and possible shared data | Data-sharing where licences allow (WSC-DDR-001 D5) |
| Parts suppliers (SWIR LEDs, InGaAs photodiodes, cells) | Availability and price of the critical parts | Quotes for single units and small batches |

## Constraints

- Garage-buildable prototype from off-the-shelf modules and 3D-printed parts. $150 USD in parts is the volume target; the first prototype is accepted at about $163 (Amish, 2026-09-25, WSC-DDR-001 D2).
- One hand, one button, result in about a second, readable in direct sunlight.
- Works offline for a full shift with no mains power at the work site; charges from USB.
- Usable by people with limited literacy: color, icon and resin code on screen, local language.
- Rugged enough for dusty, wet and rough handling.
- Price grades are set locally by the user or cooperative, not by a remote service.

## Out of scope

- Black and very dark plastics (reported as unknown, not identified).
- Hazardous, medical or chemical-container waste. The scanner must never be used to decide whether such waste is safe to handle.
- Conveyor or automatic sorting (a possible later project).
- Identifying additives, food-contact grade or contamination.

## Open questions

- Which users to work with first, and through which partner (a waste picker organization, a cooperative, or a university lab)? Decided by Amish, 2026-10-02 (WSC-DEC-001): a member-owned waste picker cooperative; the first candidate to approach is SWaCH in Pune, India.
- Which region's resin mix and price structure should set the first classifier and price table? Decided by Amish, 2026-10-02: Pune, India (WSC-DEC-001).
- Is the $150 volume target the price a cooperative would pay, or should the target be lower for individual pickers? Decided by Amish, 2026-10-02: it is the price a cooperative pays for a shared scanner (WSC-DEC-001).

## User research and co-design

This design is for communities the author is not part of, so requirements come from the people who will use it.

- [ ] Identify a local partner organization (Helpful Engineering network, NGO or university)
- [ ] Run co-design sessions with intended users; record who, where and what was learned
- [ ] Validate load, distance, terrain and cost assumptions in the field
- [ ] Revise requirements (REQ) from findings before freezing the design

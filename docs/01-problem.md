---
doc_id: WSC-PRB-001
title: WasteWise Scan problem statement
project: WasteWise Scan
doc_type: Problem statement
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
  change: Populate to TRL 2 (problem, users, context, constraints, prior work)
---

# WasteWise Scan problem statement

Resin type sets the price of a plastic item, but the people who sort most of the world's recycled plastic have no affordable way to measure it. They rely on the molded resin code, touch, sound and burn tests, and a wrong call either loses value or contaminates a whole bale.

## The problem

Mixed plastic is worth little; plastic sorted by resin (PET, HDPE, PP, PS, PVC) is worth several times more to a recycler, and a small share of the wrong resin can spoil a batch. PVC in a PET stream is the classic example, because it degrades at PET processing temperatures and discolors the melt. The informal sector carries most of this sorting work: one widely cited model estimates that informal collectors gathered about 58 % of the post-consumer plastic collected for recycling worldwide in 2016 ([Lau et al. 2020, *Science*](https://doi.org/10.1126/science.aba9475)). Waste pickers are among the lowest-paid workers in the economies where they work ([WIEGO, waste pickers](https://www.wiego.org/informal-economy/occupational-groups/waste-pickers)).

Sorting by eye is unreliable. The resin identification code molded into an item ([ASTM D7611](https://www.astm.org/d7611_d7611m-21.html)) is often missing, worn or wrong, and many items look alike: a clear PP tray and a clear PET tray, or a white HDPE bottle and a white PP bottle. An ordinary camera sees color and shape, not chemistry, which is why the image model in the sibling project WasteWise-ml will struggle with exactly these pairs.

Industry solves this with near-infrared (NIR) spectroscopy. Polymers absorb short-wave infrared light at wavelengths set by their chemical bonds, mainly overtones of the C-H stretch near 1,150 to 1,250 nm and 1,650 to 1,750 nm, and those signatures differ between resins ([Neo et al. 2023, review, *Resources, Conservation and Recycling*](https://doi.org/10.1016/j.resconrec.2022.106217)). Materials recovery facilities use NIR optical sorters costing hundreds of thousands of dollars, and handheld NIR spectrometers for plastics (for example the [trinamiX mobile NIR system](https://trinamixsensing.com/), which works at about 1,450 to 2,450 nm) cost thousands of dollars plus subscriptions (price level is an estimate). None of this is within reach of a waste picker, a cooperative or a small aggregator.

## Prior work

- **Plastic Scanner** ([plasticscanner.com](https://plasticscanner.com/), [GitHub](https://github.com/Plastic-Scanner)), an open-source handheld started by Jerry de Vos at TU Delft, shines a set of discrete NIR LEDs on the item one at a time and reads the reflection with a single InGaAs photodiode. It is the closest prior work and shows that a discrete-band approach can separate common resins. WasteWise Scan builds on the same principle and adds a sunlight-readable display, local price grades, logging and a hand-off to WasteWise-ml.
- **Low-cost multispectral chips** such as the ams OSRAM AS7265x (18 channels from about 410 to 940 nm; [SparkFun Triad board](https://www.sparkfun.com/products/15050)) are cheap and easy to use, but stop short of the main polymer absorption bands. Above 940 nm only weak third-overtone features are available, so resin identification with such a chip alone is at risk (see WSC-PRC-001).
- **Black plastics** are a known limit of NIR sorting: carbon black pigment absorbs across the NIR, so black items return no usable spectrum ([WRAP, NIR-detectable black plastic packaging](https://wrap.org.uk/resources/report/development-nir-detectable-black-plastic-packaging)).

## Users and context

| User | Need | Context |
| --- | --- | --- |
| Waste picker | Know which pile an item belongs in, and what it is worth, without reading or guessing | Streets, dumpsites and transfer points; sun, dust, rain; no power at work; low-cost phone at most |
| Cooperative or aggregator sorter | Check disputed items quickly; keep bales clean; train new members | Sorting shed or yard, hundreds to thousands of items per shift |
| Small recycler or buyer | Spot-check incoming bales before paying; reject PVC in PET | Receiving bay |
| Trainer, NGO or researcher | A shared, open reference for resin identification and a log of what is collected | Workshops, studies, WasteWise-ml data collection |

## Constraints

- Garage-buildable prototype, about $150 USD in parts, using off-the-shelf modules and 3D-printed parts.
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

- Which users to work with first, and through which partner (a waste picker organization, a cooperative, or a university lab)? Proposed, awaiting Amish.
- Which region's resin mix and price structure should set the first classifier and price table? Proposed, awaiting Amish.
- Is the $150 target the price a cooperative would pay, or should the target be lower for individual pickers? Proposed, awaiting Amish.

## User research and co-design

This design is for communities the author is not part of, so requirements come from the people who will use it.

- [ ] Identify a local partner organization (Helpful Engineering network, NGO or university)
- [ ] Run co-design sessions with intended users; record who, where and what was learned
- [ ] Validate load, distance, terrain and cost assumptions in the field
- [ ] Revise requirements (REQ) from findings before freezing the design

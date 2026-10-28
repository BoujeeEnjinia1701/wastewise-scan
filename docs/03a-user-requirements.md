---
doc_id: WSC-URS-001
title: WasteWise Scan user requirements
project: WasteWise Scan
doc_type: User requirements
version: "0.1"
status: Draft
date: '2026-10-24'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-24'
    author: Amish Chadha
    change: First user requirements (kit 1.8 upgrade), drawn from the users and stakeholders in WSC-PRB-001 v0.5 Tables 1 and 2
---

# WasteWise Scan user requirements

What users need, written from their side. Product requirements that meet these needs are in WSC-PRS-001 (`03-requirements.md`) and the links are in the traceability matrix WSC-RTM-001 (`03b-traceability.md`). The needs come from the users and stakeholders in WSC-PRB-001 Tables 1 and 2. None has yet been confirmed in a co-design session with the first candidate partner (a member-owned waste picker cooperative, first candidate SWaCH in Pune, decided by Amish on 2026-10-02), so every priority is a proposal. Method: STANDARDS section 22.

Table 1. User requirements.

| ID | Category | Title | Need | Priority | Source |
| --- | --- | --- | --- | --- | --- |
| UR-001 | Performance | Right resin | When I scan a plastic item I am told whether it is PET, HDPE, PP, PS or PVC, and it is right almost every time it gives an answer | High | Waste picker; cooperative sorter; small recycler or buyer (PRB Table 1) |
| UR-002 | Performance | Quick | The answer comes in about a second, so checking doubtful items does not slow work paid by weight | High | Waste picker; cooperative sorter (PRB Table 1) |
| UR-003 | Performance | Honest unknown | When it cannot tell, for black, wet or very thin items, it says "unknown" rather than guessing, and it is never used to judge whether waste is safe to handle | High | Small recycler or buyer; cooperative (PRB Table 1, Out of scope) |
| UR-004 | Environment and durability | Works in the sun | It works outdoors in strong sun at streets, dumpsites and yards | High | Waste picker (PRB Table 1 context) |
| UR-005 | Logistics | Lasts a shift | It lasts a full shift with no power at the work site and charges from a phone charger | High | Waste picker; cooperative (PRB constraints) |
| UR-006 | Usability | One hand, light | I can hold it in one hand, press one button and carry it all shift | High | Waste picker (PRB constraints) |
| UR-007 | Usability | No reading needed | I can read the result at arm's length in sun without reading text: colour, icon and resin code, in my own language | High | Waste picker; trainer (PRB constraints, literacy) |
| UR-008 | Usability | Our price grade | It shows the grade our buyer pays for, from a price table the cooperative sets and edits, offline | High | Cooperative; small recycler or buyer (PRB Table 1) |
| UR-009 | Performance | A record of scans | The cooperative can keep and export a record of what was scanned, for training and for disputes | Medium | Cooperative; trainer, NGO or researcher (PRB Table 1) |
| UR-010 | Environment and durability | Survives handling | It survives drops, dust, rain and heat in daily use | High | Waste picker; cooperative (PRB constraints) |
| UR-011 | Maintenance | Easy to keep right | A quick self-check keeps it accurate, and it tells me when a check is due | Medium | Cooperative sorter (PRB Table 1) |
| UR-012 | Cost | Affordable to a cooperative | A cooperative can afford a shared scanner (USD 150 value-engineering target, decided 2026-10-02) | High | Cooperative; NGOs (PRB constraints) |
| UR-013 | Performance | Works with the phone app | Items it cannot resolve can be passed to WasteWise-ml on a phone, and the two records join | Medium | Cooperative; WasteWise-ml (PRB prior work, Stakeholders) |
| UR-014 | Safety | Safe invisible light | The invisible infrared light cannot harm my eyes or anyone near me | High | Waste picker; municipality (PRB Table 2) |
| UR-015 | Safety | Safe battery | The battery is safe to carry, drop and charge in a hot climate | High | Waste picker; cooperative (PRB constraints) |
| UR-016 | Deployment and assembly | Built locally | A local maker or makerspace can build and repair it from off-the-shelf modules and printed parts | Medium | Trainer, NGO or researcher; Helpful Engineering makers (PRB constraints, Stakeholders) |
| UR-017 | Regulatory | Our data, our consent | Scan records and spectra stay on the device unless we agree to share them, on terms our organization co-owns | Medium | Cooperative; waste pickers (WSC-DDR-002, decided 2026-10-02) |

Categories: deployment and assembly, performance, usability, safety, environment and durability, logistics, maintenance, cost, regulatory. Priorities: High, Medium, Low.

---
doc_id: WSC-REG-001
title: WasteWise Scan regulatory and standards register
project: WasteWise Scan
doc_type: Regulatory and standards register
version: "0.1"
status: Draft
date: '2026-10-24'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-24'
    author: Amish Chadha
    change: First regulatory and standards register (kit 1.8 upgrade), for a first pilot with a waste picker cooperative in Pune, India; India waste rules cited through the focus-area register of WasteWise-ml (WML-REG-001)
---

# WasteWise Scan regulatory and standards register

Which standards and regulations apply, where, and what is needed, for a first pilot in Pune, India (first candidate partner SWaCH, decided 2026-10-02). The scanner is a battery-powered handheld with invisible infrared LEDs and a radio-capable controller board; it advises on resin and never certifies material or judges whether waste is safe. The items that need work before any product claim are eye safety (IEC 62471, met by estimate only), the lithium-ion cell (BIS registration of cells to IS 16046 Part 2), radio approval of the controller board in India (WPC), and battery and e-waste producer duties if units are ever supplied. Standards shared with WasteWise-ml (the Circular Materials focus area) are cited from its register, WML-REG-001. Not legal advice; anything marked "to assess" needs a qualified reviewer before any product claim. Method: STANDARDS section 23.

Table 1. Regulatory and standards register.

| # | Standard or regulation | Jurisdiction | What it covers | Applicability to this design | Owner (role) | Status |
| --- | --- | --- | --- | --- | --- | --- |
| R1 | IEC 62471:2006 (EN 62471), photobiological safety of lamps and lamp systems | International | Risk groups (exempt, 1 to 3) for optical radiation from lamps and LEDs, including infrared to the eye | Eight NIR and SWIR LEDs pulsed about 14 ms each per scan; PR-014 targets the exempt group | Design lead | Met by design on paper (WSC-CAL-001 H: 3.9 W/m2 at 200 mm against 100 W/m2); limits to confirm against the purchased standard and LED datasheets; measurement at TRL 4 |
| R2 | Hardware limit on LED on-time (practice that keeps R1 true under a firmware fault) | Design practice | A stuck-on LED at the shroud rim could exceed the corneal limit over long exposures | Required by PR-014 and WSC-PRC-001 Safety | Electronics lead | Applies; to design at TRL 4 (monostable or RC limit on each driver) |
| R3 | IS 16046 (Part 2):2018, equivalent to IEC 62133-2:2017, safety of portable sealed secondary lithium cells and batteries; BIS Compulsory Registration Scheme | India | Cell and battery safety tests; registration of cells sold in India | The protected 18650 cell (BOM line 8) | Procurement (partner) | To assess: buy a cell registered with BIS under this standard (PR-015); which cell categories the scheme lists is to confirm on the BIS site |
| R4 | UN Manual of Tests and Criteria, section 38.3, transport of lithium cells | International | Tests before lithium cells or equipment containing them are shipped | Shipping cells or assembled scanners | Procurement | To assess (not checked in this session): buy cells with a UN 38.3 test summary |
| R5 | Wireless Planning and Coordination (WPC) Equipment Type Approval for equipment in delicensed bands | India | Devices using 2.4 GHz Wi-Fi or Bluetooth need ETA; an end product made in India needs no separate ETA if its RF module already has one and is fitted unmodified (Granite River Labs guide) | The ESP32-S3 display board has a 2.4 GHz radio; the firmware keeps it off, but the module is radio equipment | Procurement (partner) | To assess: buy a board whose module holds an ETA certificate, or confirm the radio-off case with a qualified reviewer |
| R6 | Battery Waste Management Rules, 2022 (notified 2022-08-24) | India | Extended producer responsibility for all battery types including portable; collection and recycling, no landfill or incineration (pv magazine India) | Only if scanners with cells are supplied in India; each used cell goes to a battery collection route | Project lead; partner | To assess before any supply; applies to the partner's disposal of used cells now |
| R7 | E-Waste (Management) Rules, 2022 | India | Electrical and electronic equipment at end of life | The scanner itself at end of life | Project lead; partner | To assess (cited through WML-REG-001 G5; not checked in this session) |
| R8 | Solid Waste Management Rules, 2026 | India | Segregation at source and handling of dry recyclables; special care waste | The site where the scanner is used; the scanner never decides whether an item is special care waste | Partner (site operator) | Applies to the site (cited through WML-REG-001 G1) |
| R9 | ASTM D7611/D7611M-21, resin identification coding | International | The resin codes moulded on plastic items | The codes the scanner displays (PR-001, PR-007) | Design lead | Applies (reference) |
| R10 | IEC 60529, degrees of protection by enclosures (IP code) | International | IP54 target of PR-010 | Shell gasket, sealed button, window | Design lead | To verify at TRL 4 (spray test); the standard is cited by number only, not purchased |
| R11 | Digital Personal Data Protection Act, 2023, and Rules, 2025 | India | Personal data in digital form | Scan records hold no personal data by design; a pair ID joins to WasteWise-ml photos, which may | Data lead with the partner | Does not apply to the scanner's own record by design; joint records to assess (cited through WML-REG-001 G2) |
| R12 | RoHS-type substance restrictions (India E-Waste Rules carry RoHS limits) | India | Hazardous substances in electrical equipment | Bought boards and LEDs | Procurement | To assess (not checked in this session) |
| R13 | Medical, food-contact or hazardous-material claims | Any | Certifying material grade or safety | Out of scope: the scanner gives sorting advice only (WSC-PRB-001, Out of scope; WSC-PRC-001 Safety) | Project lead | Does not apply by design; keep the claim out of all user material |

Status: to assess, applies, does not apply, met by design, certification needed later.

## Sources

- BAuA. *Photobiological Safety of Light Emitting Diodes (LEDs)*. Report F 2115, 2013 (EN 62471 exempt group and risk groups 1 to 3). https://baua.de/EN/Service/Publications/Report/F2115. Checked 2026-10-25.
- Bureau of Indian Standards. IS 16046 (Part 2):2018 test report format (title: safety requirements for portable sealed secondary cells, part 2 lithium systems; equivalent to IEC 62133-2:2017). https://www.bis.gov.in/wp-content/uploads/2026/03/UTRF_16046_2_2018.pdf. Checked 2026-10-25.
- Granite River Labs. "A Guide to WPC and ETA Certification." https://www.graniteriverlabs.com/en-us/market-access-services/country/india/wpc-mark. Checked 2026-10-25.
- pv magazine India. "Government notifies Battery Waste Management Rules, 2022." 2022-08-25. https://www.pv-magazine-india.com/?p=10815. Checked 2026-10-25.
- WasteWise-ml regulatory and standards register WML-REG-001 v0.1 (Solid Waste Management Rules, 2026; DPDP Act and Rules; E-Waste Rules), the Circular Materials focus-area register.
- ASTM D7611/D7611M-21, as cited in WSC-PRB-001. https://store.astm.org/d7611_d7611m-21.html.

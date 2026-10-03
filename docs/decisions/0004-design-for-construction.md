---
doc_id: WSC-DDR-004
title: WasteWise Scan design for construction
project: WasteWise Scan
doc_type: Design decision record
version: "0.3"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-02'
  author: Amish Chadha
  change: Changes that make the concept physically buildable, with the reason for each; made under Amish's 2026-09-30 instruction and open for his review
- version: "0.2"
  date: '2026-10-02'
  author: Amish Chadha
  change: Accepted by Amish on 2026-10-02 (A2), with A1 decided as option (a)
- version: "0.3"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Decision A1 carried into the model: 2.0 mm shell walls, 238 g and 258 g with the cap; record stays Draft"
---

# 0004: Design for construction

- **Date:** 2026-10-02
- **Status:** accepted. Amish, 2026-10-02: "APPROVED: The open decisions from the last wave (TremorTrace to ZeerBox) came in after the review and aren't on the page either." This approves the recommendation written for each open decision in the design decisions register (WSC-DEC-001 v0.1): the changes in Tables 1 and 2 are accepted as made (A2), and A1 is decided as recorded in Table 3. The record stays Draft.

## Context

On 2026-09-30 Amish asked for every repo to carry an illustrated build plan and wrote: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." The TRL 3 model of WasteWise Scan (WSC-DDR-003) showed what the scanner does, and its optics drove the calculation note, but most of its parts had no fixing, two parts overlapped, and two parts could not do their job as drawn. Checking the model with build123d (part overlaps, contacts and clearances) found the twelve problems below. Two of them (the button hole and the USB-C socket) had already been noted in the review of 2026-09-26.

The changes keep what the scanner does: the same body size (160 x 62 x 34 mm), the same optical geometry (detector 22 mm from the item, LEDs on a 20 mm circle tilted 23°, 25 mm window, 18 mm shroud with a 42 mm rim), the same electronics, cell, display, button position, sun hood walls and calibration method. Nothing here changes the pitch or the safety case. Every change is in `cad/src/model.py`, which now runs 312 constructability checks (`python cad/src/model.py --check`): no two of the 25 components overlap, the 25 contacts that must exist do exist, and 11 clearances hold. All 312 pass.

## Decision

*Table 1. Changes made to the model, the BOM and the calculations.*

| # | Problem in the concept | Change made | Why this way |
| --- | --- | --- | --- |
| P1 | The two shells had no fixing, no seal and nothing to line them up, although the BOM listed screws, inserts and a gasket. | Four M3 x 20 screws from below through counterbored bosses at 68 mm each side of centre and 20 mm out, into brass heat-set inserts in matching bosses in the top shell. A 2.5 mm strip of 1.5 mm closed-cell foam on the rim, squeezed to 0.6 mm; the top shell rim starts 0.6 mm higher so the body stays 34 mm tall. A 1.2 x 2.6 mm tongue on the bottom shell locates the top shell. | The bosses meet face to face, so tightening the screws cannot crush the gasket past 0.6 mm. Screws from below keep the top face clean for the display and hood. |
| P2 | The window sat in a 25.4 mm hole through the floor with no ledge: nothing held it in. | The window is pinched between the lip of the shroud flange (22 mm opening) below and the baffle tube of the head block above. | One clamp holds window, shroud and head block. The baffle tube already had to reach the glass to block crosstalk. |
| P3 | The shroud touched the underside of the body with no fixing. | A flange 47 mm across and 2.5 mm thick on the top of the shroud, held by three M3 x 10 screws with washers on a 40 mm circle, through the floor into inserts in the head block. | The circle is large enough that the screw heads and washers clear the cone; the shroud is a wear part and now comes off with three screws. |
| P4 | The LED holder floated 2.5 mm above nothing, and the amplifier board floated 1.2 mm above the holder. | The holder becomes an optical head block, 36 mm across and 7.2 mm tall, standing on the floor with the amplifier board on its top face: three lugs with M3 inserts, the baffle tube built in, a bore that seats the photodiode, LED pockets open at the top for the leads, and two M2.5 inserts for the board. | The block fills the gap the concept left, so every optical part is located by one printed part and clamped by P3. |
| P5 | The baffle bore (5.6 mm) was wider than the photodiode can (5.4 mm), so the can would drop onto the window. | A step 4 mm up the body with a 4 mm aperture below it; the can sits on the step. | The detector plane stays 4 mm up, 22 mm from the item, so the optics calculations are unchanged. |
| P6 | The cell cradle was an open trough sized for a 65 mm cell, with no contacts and nothing to stop the cell lifting or sliding out, while the BOM calls for a protected cell, which is about 69 mm long. | The cradle is printed with the bottom shell: two 1.5 mm rails and two end walls 75 mm apart that carry a bought spring and flat contact pair, for a 69 mm cell. A printed strap (10 x 8 mm PETG) across the cell, on two M3 x 25 screws into inserts in floor bosses. The cell moves 6 mm toward the head end. | The strap carries the 553 N corner-drop load at about 38 MPa, 1.3 times under the strength of printed PETG [J4]. It sits outside the display board, where there is room for its depth. Moving the cell makes room for P7. |
| P7 | The USB-C socket overlapped the tail wall and had no mount. | A small USB-C power board on a printed seat on the floor, its socket mouth in the tail wall opening, fixed with a dot of glue. | Uses the existing opening; no screws needed for a part that is only pushed on. |
| P8 | The display board floated under the ceiling with no fixing. | A printed display frame with lips under the board's long edges and four ears, held by four M3 x 8 screws into inserts in four top shell bosses; 0.5 mm foam tape on the lips. | The board has no mounting holes; the frame holds it by its edges and keeps the lips clear of the cell below. |
| P9 | The 16 mm button sat over a 13 mm hole and overlapped the shell. | A 16.2 mm hole for a panel-mount 16 mm button, with its nut tightened up against the ceiling inside. | Standard panel-mount fitting; seals with the button's own washer. |
| P10 | The slide power switch in BOM line 11 was not in the model. | A panel slide switch on the inside of the right-hand wall, 50 mm behind the centre, actuator through a 7 x 3.5 mm slot, two M2 screws and nuts. | Reachable by the thumb of the hand not holding the grip, and away from the cell and strap. |
| P11 | The sun hood was "clip-on" but had nothing to clip to. | Two clip legs 40 mm long down the sides of the top shell, each with a lip that snaps under a 1 x 1 mm rib printed on the shell side. The plate is trimmed to the legs and the frame round the display opening. | No tools; the walls that shade the screen are unchanged, so the legibility result [I3] stands. Width over the legs is 68.4 mm; R6 allows the hood beyond the body size. |
| P12 | The calibration cap (44 mm bore) was loose on the 42 mm rim, so nothing held it in storage, and it was 1 mm too deep, so the rim never touched the 38 mm PTFE disc, which was also narrower than the rim. | Cap 46 mm across and 20 mm tall with a 41.6 mm bore that grips the TPU rim; PTFE disc 41 mm. Pushed on, the rim rests on the disc and the cap mouth stops 0.5 mm short of the flange. | The white reference is now read at the same distance as an item, which is what the calibration needs, and the cap stays on in a pocket. |

*Table 2. Knock-on changes.*

| Item | Change | Reason |
| --- | --- | --- |
| Mass | 254 g, 274 g with the cap (was 209 g and 229 g) [A3]. R6 (250 g) moves from met to **not met**, 24 g over with the cap. | Bosses, cradle walls, display frame, strap and hood legs add about 25 g of PETG; the fixings allowance rises from 10 to 25 g for 17 steel screws and 15 brass inserts. |
| Cost | BOM lines 1, 3, 7, 9 to 14 and 16 respecified, lines 9, 10 and 16 repriced, lines 17 (display frame), 18 (cell strap) and 19 (shell gasket) added: USD 167.50. Value-engineering target USD 150 (`budget_usd`, unchanged): USD 17.50 over the target [K2]. | Parts added for construction, net USD 3.50. |
| Calculations | WSC-CAL-001 v0.3: masses from the new model volumes, fixings allowance, new line J4 (strap), cost against the value-engineering target [K2]. Optics, power, timing, sunlight and display results unchanged. | Follows the model. |
| Drawing | WSC-DWG-001 Rev P4; making sketches WSC-DWG-101 to 109 added. | Follows the model. |
| Documents | WSC-PRC-001 v0.5 and WSC-REQ-001 v0.5: mass, cost, components and R6 and R12 status updated. | Follows the model. |

*Table 3. Decided by Amish, 2026-10-02.*

| # | Question | Options | Recommendation |
| --- | --- | --- | --- |
| A1 | R6 is now not met: 274 g with the cap against 250 g (254 g without it). | (a) shell walls 2.0 mm instead of 2.5 mm, keeping the bosses and ribs (saves about 20 g; the drop case R10 is then checked at TRL 4); (b) count R6 without the cap, which stores on the shroud but can be left in a pocket (254 g, still 4 g over); (c) accept about 275 g and restate R6. | (a), and weigh the first prototype at TRL 4 before deciding on (b) or (c). **Decided by Amish, 2026-10-02: (a).** R6 stays not met (about 254 g with the cap, 4 g over) until the prototype is weighed; (b) is not used because the cap is carried for backing clear items. The 2.0 mm walls are now in the model (v0.3 of this record): 238 g, 258 g with the cap, 8 g over, because the shells saved 17 g rather than about 20 g (WSC-CAL-001 v0.4, A3). |
| A2 | Whether to accept the changes P1 to P12 as the constructable design. | Accept; accept with changes; reject. | Accept. **Decided by Amish, 2026-10-02: accepted as made.** |

*Table 4. Carried into the model, 2026-10-02 (A1).*

| Item | Change | Reason |
| --- | --- | --- |
| Shell walls | Both shells 2.0 mm (was 2.5 mm); bosses, ribs, tongue and gasket unchanged. The model's 314 checks pass, including a new check that the wall is at least 1.6 mm and the tongue fits inside it. | Decision A1, option (a) |
| Parts that follow | The display frame is 12 mm tall (was 11.5 mm) because the ceiling is 0.5 mm higher; the cell strap legs stand 0.5 mm taller; the shell prints with five perimeters. | The thinner floor and ceiling |
| Mass | Top shell 42 g, bottom shell 47 g (were 51 g and 56 g); scanner 238 g, 258 g with the cap [A3]. | Model volumes |
| Drawings | WSC-DWG-001 Rev P5; making sketches WSC-DWG-101 and 105 and the shell pictures regenerated. | Follows the model |
| Drop case | Cell load unchanged (about 550 N); thin shell corners checked in the drop test at TRL 4 (R10). | Decision A1 |

## Consequences

- `design_state: constructable` in `project.yaml`. The build plan WSC-BLD-001 shows every component and step in pictures generated from the model (`cad/src/build_plan_media.py`).
- Requirement status (WSC-CAL-001 v0.3): 1 not met (R6, mass), 3 at risk (R1, R7, R13), 2 not verifiable at TRL 3 (R3, R10), 7 met; R12 is reported against the value-engineering target, USD 17.50 over.
- The photoreal renders (`media/render-*.png`), `media/card.png` and `media/social-preview.png` and the appearance model `cad/src/product_model.py` differ from the constructable design where it shows from outside: the hood has no clip legs and the shell sides no ribs, and the cap is the concept's 48 x 24 mm. Their shroud flange and screw heads were appearance details that the design now carries. They need regenerating on Amish's Mac, where Blender is.
- Open questions about parts still to be bought are listed in the design decisions register, WSC-DEC-001.

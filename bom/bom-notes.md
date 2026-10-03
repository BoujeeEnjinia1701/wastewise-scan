# BOM notes

Every line of `bom/bom.csv` is priced (TRL 3). Prices are catalog-level estimates with a supplier or supplier type; no quotes have been requested. Items 1 to 14 and 16 to 18 match the numbered callouts in `media/exploded.png`; items 15 and 19 are not shown there. `docs/04-calcs/sizing.py` reads the BOM and prints the total (WSC-CAL-001, K1).

| Group | Items | Cost |
| --- | --- | --- |
| Optics (LEDs and photodiode) | 3, 4 | $92.00 |
| Electronics and power | 2, 5, 8, 9, 11 | $43.00 |
| Housing, window, shroud, hood, calibration and construction parts | 1, 6, 7, 10, 12, 13, 14, 15, 17, 18, 19 | $26.50 |
| Hardware and consumables | 16 | $6.00 |
| **Total** | 1 to 19 | **$167.50** |

Value-engineering target: USD 150 (`budget_usd`, a hypothetical control target, not a limit; Amish, 2026-10-01). Estimated cost of the constructable design: USD 167.50 (USD 17.50 over the target). The SWIR LEDs are the largest and least certain cost. Cost drivers and savings worth trying are in the design decisions register (`docs/06-design-decisions.md`).

Changes for construction (2026-10-02, WSC-DDR-004, open for Amish's review): lines 1, 3, 7, 10 to 14 and 16 respecified; line 9 is now cell contacts and a USB-C board ($3.00, the cradle is printed with the bottom shell); line 10 repriced to $5.00 and line 16 to $6.00; lines 17 (display frame), 18 (cell strap) and 19 (shell gasket) added. Items 17 to 19 are modeled; the exploded view shows 16 (screws), 17 and 18.

Shell walls 2.0 mm (2026-10-02, decision on R6): lines 1 and 10 now print about 33 cm3 (42 g) and 37 cm3 (47 g), together 17 g lighter, and their prices stay at $3.00 and $5.00 because filament is a small share of each line; the total stays $167.50. Scanner mass is 238 g, 258 g with the cap (WSC-CAL-001 A3).

Changes at TRL 3: item 5 specifies a 47 kOhm transimpedance gain (set by the sunlight calculation). On 2026-09-25 (WSC-DDR-003) item 14, the sun hood, was added; the calibration cap (item 12) is now printed in black PETG so it can back clear items in sun; the resin reference chips and the hardware lines moved from 14 and 15 to 15 and 16.

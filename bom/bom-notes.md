# BOM notes

Every line of `bom/bom.csv` is priced (TRL 3). Prices are catalog-level estimates with a supplier or supplier type; no quotes have been requested. Items 1 to 14 match the numbered callouts in `media/exploded.png`; items 15 and 16 are not modeled. `docs/04-calcs/sizing.py` reads the BOM and prints the total (WSC-CAL-001, K1).

| Group | Items | Cost |
| --- | --- | --- |
| Optics (LEDs and photodiode) | 3, 4 | $92.00 |
| Electronics and power | 2, 5, 8, 9, 11 | $44.00 |
| Housing, window, shroud, hood and calibration | 1, 6, 7, 10, 12, 13, 14, 15 | $23.00 |
| Hardware and consumables | 16 | $5.00 |
| **Total** | 1 to 16 | **$164.00** |

Budget check: `budget_usd` is $150. Amish decided on 2026-09-25 (WSC-DDR-001 D2) to keep $150 as the volume target and accept about $163 for the first prototype, and then accepted the clip-on sun hood (WSC-DDR-003 D10), which adds $1.00. The total of $164.00 is 9.3 % over the volume target and within the accepted prototype figure (R12). The SWIR LEDs are the largest and least certain cost.

Changes at TRL 3: item 5 specifies a 47 kOhm transimpedance gain (set by the sunlight calculation). On 2026-09-25 (WSC-DDR-003) item 14, the sun hood, was added; the calibration cap (item 12) is now printed in black PETG so it can back clear items in sun; the resin reference chips and the hardware lines moved from 14 and 15 to 15 and 16.

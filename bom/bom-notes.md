# BOM notes

Every line of `bom/bom.csv` is priced (TRL 3). Prices are catalog-level estimates with a supplier or supplier type; no quotes have been requested. Items 1 to 13 match the numbered callouts in `media/exploded.png`; items 14 and 15 are not modeled. `docs/04-calcs/sizing.py` reads the BOM and prints the total (WSC-CAL-001, K1).

| Group | Items | Cost |
| --- | --- | --- |
| Optics (LEDs and photodiode) | 3, 4 | $92.00 |
| Electronics and power | 2, 5, 8, 9, 11 | $44.00 |
| Housing, window, shroud and calibration | 1, 6, 7, 10, 12, 13, 14 | $22.00 |
| Hardware and consumables | 15 | $5.00 |
| **Total** | 1 to 15 | **$163.00** |

Budget check: `budget_usd` is $150. Amish decided on 2026-09-25 (WSC-DDR-001 D2) to keep $150 as the volume target and accept about $163 for the first prototype, so the total is 8.7 % over the volume target and within the accepted prototype figure (R12). The SWIR LEDs are the largest and least certain cost.

Changes at TRL 3: item 5 now specifies a 47 kOhm transimpedance gain (set by the sunlight calculation); supplier types and model-derived volumes and masses were added. No line was added or removed, and the total is unchanged.

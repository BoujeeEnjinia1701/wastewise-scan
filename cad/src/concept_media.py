"""WasteWise Scan concept media (TRL 3), built from the parametric model in cad/src/model.py.

Run from the repo root:  python cad/src/concept_media.py
Proportions and main parts only; not for fabrication.

Axes: X along the body (scan head at +X), Y across the body, Z up.
The shroud rim rests on the item being scanned at Z = SHROUD_TIP.
"""
import sys
import shutil
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build123d import Box, Cylinder, Pos, Rot
from concept import Part, render_all
from build123d import Compound
from model import PARAMS as P, components, CHOSEN

Z_TOP = P["body_h"]
SHROUD_TIP = -P["shroud_h"]
# kit 1.9: the concept media show the detailed D3 model of the current design (components(CHOSEN)), grouped by
# BOM line so the exploded view's callouts match bom/bom.csv
GROUPS = [  # (BOM line, label, colour, explode)
    (1, "Top shell", "#E5E7EB", (0, 0, 95)),
    (2, "ESP32-S3 display board", "#0F766E", (0, 0, 62)),
    (3, "LED ring in the optical head block", "#C2410C", (0, 0, 22)),
    (4, "InGaAs photodiode", "#D4A017", (0, 0, 40)),
    (5, "Amplifier and ADC board", "#15803D", (0, 0, 60)),
    (6, "Borosilicate windows (LED ring and detector)", "#BFDBFE", (0, 0, -26)),
    (7, "Black TPU light shroud", "#1F2937", (0, 0, -58)),
    (8, "18650 Li-ion cell", "#7C3AED", (0, 0, 32)),
    (9, "Cell contacts and USB-C board", "#2563EB", (0, 0, 18)),
    (10, "Bottom shell and grip", "#9CA3AF", (0, 0, 0)),
    (11, "Scan button and power switch", "#F59E0B", (0, 0, 128)),
    (12, "Calibration cap (black)", "#374151", (0, 0, -45)),
    (13, "White PTFE reference disc", "#F9FAFB", (0, 0, 0)),
    (14, "Clip-on sun hood", "#475569", (0, 0, 118)),
    (16, "Screws, washers, nuts and inserts", "#111827", (0, 0, -95)),
    (17, "Display frame", "#0E7490", (0, 0, 78)),
    (18, "Cell strap", "#B45309", (0, 0, 48)),
    (19, "Shell gasket", "#16A34A", (0, 0, 40)),
]
comp = [q for q in components(CHOSEN) if q["kind"] != "context"]
parts = []
for bom, label, col, ex in GROUPS:
    shapes = [q["shape"] for q in comp if q.get("bom") == bom]
    if shapes:
        parts.append(Part(label, Compound(children=shapes), col, bom, ex))

# Context for scale (hero only): a hand on the grip and a flat HDPE crate panel being scanned.
palm = Pos(-60, 0, Z_TOP + 11) * Box(48.0, 80.0, 22.0)
fingers = Pos(-60, -37, Z_TOP - 9) * Box(44.0, 14.0, 42.0)
thumb = Pos(-22, 36, Z_TOP - 6) * Rot(0, 90, 0) * Cylinder(9.0, 64.0)
wrist = Pos(-125, 0, Z_TOP + 13) * Rot(0, 90, 0) * Cylinder(29.0, 90.0)
panel = Pos(0, -30, SHROUD_TIP - 3.0) * Box(260.0, 190.0, 6.0)
context = [Part("Hand", palm + thumb + fingers + wrist, "#C8CDD3"),
           Part("HDPE crate panel", panel, "#93C5FD")]

render_all(
    parts, project="WasteWise Scan", title="Handheld resin scanner concept", dwg_no="WSC-DWG-010",
    key_figures=["8 NIR/SWIR bands, 850 to 1,650 nm", "Scan about 0.64 s (WSC-CAL-001)",
                 "Body 160 x 62 x 34 mm, about 239 g, 259 g with cap (WSC-CAL-001)",
                 "About 22 h per charge on one 18650 (WSC-CAL-001)",
                 "$167.50 in parts, prototype (priced BOM)"],
    date="2026-10-24", scale_figure=False, context=context,
    flow={"title": "item flow per 100 mixed plastic items (all values estimates)", "unit": "%",
          "stages": [("Mixed items", 100), ("Scanned", 100), ("Spectrum usable", 88),
                     ("Resin + price grade", 78)],
          "losses": [(1, "Black or dark\n(reads unknown)", 12),
                     (2, "Low confidence\n(WasteWise-ml or hand check)", 10)]},
)

media = Path(__file__).resolve().parents[2] / "media"
for d in media.glob("_views*"):
    shutil.rmtree(d, ignore_errors=True)

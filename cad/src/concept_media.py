"""WasteWise Scan concept massing model and media (TRL 2).

Run from the repo root:  python cad/src/concept_media.py
Proportions and main parts only; not for fabrication.

Axes: X along the body (scan head at +X), Y across the body, Z up.
The shroud rim rests on the item being scanned at Z = SHROUD_TIP.
"""
import sys
import shutil
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
from build123d import Box, Cylinder, Cone, Pos, Rot, Axis, fillet
from concept import Part, render_all

L, W = 160.0, 62.0            # body length and width, mm
Z_SPLIT, Z_TOP = 16.0, 34.0   # shell split line and top of body
WALL = 2.5
HEAD_X = 55.0                 # optical axis position along the body
SHROUD_H = 18.0
SHROUD_TIP = -SHROUD_H


def shell(z0, z1, open_top):
    h = z1 - z0
    outer = Pos(0, 0, z0 + h / 2) * Box(L, W, h)
    outer = fillet(outer.edges().filter_by(Axis.Z), 10.0)
    zin = z0 + h / 2 + (WALL / 2 if open_top else -WALL / 2)
    inner = Pos(0, 0, zin) * Box(L - 2 * WALL, W - 2 * WALL, h - WALL + 0.01)
    inner = fillet(inner.edges().filter_by(Axis.Z), 7.5)
    return outer - inner


bottom = shell(0.0, Z_SPLIT, open_top=True) - Pos(HEAD_X, 0, 1.0) * Cylinder(13.0, 4.0)
top = shell(Z_SPLIT, Z_TOP, open_top=False) - Pos(-10, 0, Z_TOP - 1) * Box(46.0, 24.0, 4.0) \
    - Pos(35, 0, Z_TOP - 1) * Cylinder(6.5, 4.0)
display_board = Pos(-10, 0, 27.0) * Box(62.0, 26.0, 9.5)
battery = Pos(-30, 0, 12.0) * Rot(0, 90, 0) * Cylinder(9.25, 65.0)
led_ring = Pos(HEAD_X, 0, 5.0) * (Cylinder(12.0, 2.0) - Cylinder(7.0, 2.2))
photodiode = Pos(HEAD_X, 0, 6.0) * Cylinder(3.0, 4.0)
charger = Pos(20, 0, 4.5) * Box(22.0, 18.0, 2.0)
amp_board = Pos(HEAD_X, 0, 10.5) * Box(28.0, 28.0, 1.6)
window = Pos(HEAD_X, 0, 1.0) * Cylinder(12.5, 2.0)
shroud = Pos(HEAD_X, 0, -SHROUD_H / 2) * (Cone(21.0, 15.0, SHROUD_H) - Cone(18.0, 12.5, SHROUD_H + 0.02))
button = Pos(35, 0, Z_TOP + 1.5) * Cylinder(6.0, 5.0)
cap_disc = Pos(-20, -85, SHROUD_TIP + 3.0) * Cylinder(19.0, 2.0)
cap = Pos(-20, -85, SHROUD_TIP + 11.0) * (Cylinder(23.0, 22.0) - Pos(0, 0, 2.0) * Cylinder(20.5, 22.0))

parts = [
    Part("Top shell", top, "#E5E7EB", 1, (0, 0, 95)),
    Part("ESP32-S3 display board", display_board, "#0F766E", 2, (0, 0, 62)),
    Part("LED ring, 8 NIR bands", led_ring, "#C2410C", 3, (0, 0, 22)),
    Part("InGaAs photodiode", photodiode, "#D4A017", 4, (0, 0, 40)),
    Part("Amplifier and ADC board", amp_board, "#15803D", 5, (0, 0, 60)),
    Part("Borosilicate window", window, "#BFDBFE", 6, (0, 0, -26)),
    Part("Black TPU light shroud", shroud, "#1F2937", 7, (0, 0, -58)),
    Part("18650 Li-ion cell", battery, "#7C3AED", 8, (0, 0, 32)),
    Part("Cell holder and USB-C", charger, "#2563EB", 9, (0, 0, 18)),
    Part("Bottom shell and grip", bottom, "#9CA3AF", 10, (0, 0, 0)),
    Part("Scan button", button, "#F59E0B", 11, (0, 0, 128)),
    Part("Calibration cap", cap, "#374151", 12, (0, 0, -45)),
    Part("White PTFE reference disc", cap_disc, "#F9FAFB", 13, (0, 0, 0)),
]

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
    key_figures=["8 NIR/SWIR bands, 850 to 1,650 nm", "Scan about 0.6 s (estimate)",
                 "Body 160 x 62 x 34 mm, about 170 g (estimate)",
                 "About 17 h per charge on one 18650 (estimate)",
                 "About $163 in parts (indicative)"],
    date="2026-09-25", scale_figure=False, context=context,
    flow={"title": "item flow per 100 mixed plastic items (all values estimates)", "unit": "%",
          "stages": [("Mixed items", 100), ("Scanned", 100), ("Spectrum usable", 88),
                     ("Resin + price grade", 78)],
          "losses": [(1, "Black or dark\n(reads unknown)", 12),
                     (2, "Low confidence\n(WasteWise-ml or hand check)", 10)]},
)

media = Path(__file__).resolve().parents[2] / "media"
for d in media.glob("_views*"):
    shutil.rmtree(d, ignore_errors=True)

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
from model import PARAMS as P, parts as model_parts, cap_parts

Z_TOP = P["body_h"]
SHROUD_TIP = -P["shroud_h"]
m = model_parts(P)
c = cap_parts(P, at=(-20.0, -85.0, SHROUD_TIP))

parts = [
    Part("Top shell", m["top_shell"], "#E5E7EB", 1, (0, 0, 95)),
    Part("ESP32-S3 display board", m["display_board"], "#0F766E", 2, (0, 0, 62)),
    Part("LED ring in the optical head block", m["leds"] + m["led_holder"], "#C2410C", 3, (0, 0, 22)),
    Part("InGaAs photodiode", m["photodiode"], "#D4A017", 4, (0, 0, 40)),
    Part("Amplifier and ADC board", m["afe_board"] + m["afe_screws"], "#15803D", 5, (0, 0, 60)),
    Part("Borosilicate window", m["window"], "#BFDBFE", 6, (0, 0, -26)),
    Part("Black TPU light shroud", m["shroud"], "#1F2937", 7, (0, 0, -58)),
    Part("18650 Li-ion cell", m["cell"], "#7C3AED", 8, (0, 0, 32)),
    Part("Cell contacts and USB-C board", m["cell_contacts"] + m["usb_board"], "#2563EB", 9, (0, 0, 18)),
    Part("Bottom shell and grip", m["bottom_shell"], "#9CA3AF", 10, (0, 0, 0)),
    Part("Scan button and power switch", m["button"] + m["switch"], "#F59E0B", 11, (0, 0, 128)),
    Part("Calibration cap (black)", c["cal_cap"], "#374151", 12, (0, 0, -45)),
    Part("White PTFE reference disc", c["ptfe_disc"], "#F9FAFB", 13, (0, 0, 0)),
    Part("Clip-on sun hood", m["sun_hood"], "#475569", 14, (0, 0, 118)),
    Part("Screws", m["shell_screws"] + m["head_screws"] + m["frame_screws"] + m["strap_screws"], "#111827", 16, (0, 0, -95)),
    Part("Display frame", m["display_frame"], "#0E7490", 17, (0, 0, 78)),
    Part("Cell strap", m["cell_strap"], "#B45309", 18, (0, 0, 48)),
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
    key_figures=["8 NIR/SWIR bands, 850 to 1,650 nm", "Scan about 0.33 s (WSC-CAL-001)",
                 "Body 160 x 62 x 34 mm, about 254 g with hood (WSC-CAL-001)",
                 "About 22 h per charge on one 18650 (WSC-CAL-001)",
                 "$167.50 in parts, prototype (priced BOM)"],
    date="2026-10-02", scale_figure=False, context=context,
    flow={"title": "item flow per 100 mixed plastic items (all values estimates)", "unit": "%",
          "stages": [("Mixed items", 100), ("Scanned", 100), ("Spectrum usable", 88),
                     ("Resin + price grade", 78)],
          "losses": [(1, "Black or dark\n(reads unknown)", 12),
                     (2, "Low confidence\n(WasteWise-ml or hand check)", 10)]},
)

media = Path(__file__).resolve().parents[2] / "media"
for d in media.glob("_views*"):
    shutil.rmtree(d, ignore_errors=True)

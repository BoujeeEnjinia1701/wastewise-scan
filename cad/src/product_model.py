"""WasteWise Scan product model for photoreal renders (STANDARDS sections 12 and 24), TRL 3.

Every product part is components(CHOSEN) from cad/src/model.py as it is (the D3 model: shells, shroud, split
window, head block with its LEDs and photodiode, amplifier board, display board, cell, contacts, switch, button,
sun hood, every screw, washer, nut and insert, and the calibration cap with its PTFE disc). Nothing is restyled.
Two copies are returned:

- groups "shell", "internal" and "accessory": the scanner on its own, for the studio, exploded and detail views;
- group "site": the same parts placed in the right hand of a 1.75 m mannequin at a sorting table in a
  cooperative's yard, the shroud pressed on the lid of a closed HDPE crate, for the hero. Ground level is z = 0
  (photoreal --ground-z=0); the site structure is one part named "(site)" that reaches below the ground, and
  the mannequin is named "(scale)" so the camera frames the person and the scanner together.

APPEARANCE MODEL ONLY. CONCEPT, NOT FOR FABRICATION.

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]

from build123d import Box, Cylinder, Pos, Rot  # noqa: E402
import model as M  # noqa: E402
from cad_parts import part, break_edges  # noqa: E402

TITLE = "WasteWise Scan: handheld near-infrared plastic resin scanner"

_SITE = ["--scene=outdoor", "--ground=concrete", "--ground-z=0", "--sun=48,-70", "--lens=50"]
RENDER_VIEWS = [
    {"name": "hero", "groups": ["site", "context"], "explode": False, "el": 14, "az": -35, "args": _SITE,
     "note": "Site render in a sorting yard from the front right, a little above (about 14 deg elevation): a sorter "
             "(1.75 m figure for scale) presses the scanner's shroud on the lid of an HDPE crate at a sorting table, "
             "sun hood and display toward her"},
    {"name": "studio", "groups": ["shell", "internal", "accessory"], "explode": False, "el": 28, "az": -40,
     "note": "Studio render from the front right and above (about 28 deg elevation): the scanner on its black shroud, "
             "sun hood over the display, scan button, with the black calibration cap beside it"},
    {"name": "exploded", "groups": ["shell", "internal", "accessory"], "explode": True, "el": 24, "az": -55,
     "note": "Exploded view from the front right and above (about 24 deg elevation): top shell, display frame and board, "
             "button and hood above; head block with LEDs, photodiode and amplifier board, cell and strap in the bottom "
             "shell; windows, shroud and screws below; calibration cap beside"},
    {"name": "detail", "groups": ["shell", "internal"], "explode": False, "el": 20, "az": 145,
     "note": "Detail from below and the head end (about 20 deg elevation): the shroud, the LED window ring with the "
             "detector window in the baffle tube, and the slide switch"},
]

# Placement of the scanner in the sorter's right hand (mannequin "push" pose: hands at 1.0 m, 520 mm ahead).
HAND = (-171.0, -520.0, 1000.0)       # right-hand grip centre, from context_parts.mannequin_landmarks(1750, "push")
GRIP = (-40.0, 0.0, 17.0)             # grip point on the scanner's tail half, model coordinates


def _place(shape):
    """Turn the scanner so its head end points away from the sorter (-Y) and put its grip in her right hand."""
    gx, gy, gz = GRIP                   # Rot(0, 0, -90) takes (x, y, z) to (y, -x, z)
    return Pos(HAND[0] - gy, HAND[1] + gx, HAND[2] - gz) * Rot(0, 0, -90) * shape


def _site():
    """The sorting table with an HDPE crate and a few bottles, one solid that stands on and reaches below the
    concrete, and a sack of sorted bottles on the ground beside it."""
    shroud_tip_z = HAND[2] - GRIP[2] - M.PARAMS["shroud_h"]
    head = _place(Pos(M.PARAMS["head_x"], 0, 0) * Box(1, 1, 1)).bounding_box().center()
    tx, ty = head.X + 60.0, head.Y - 230.0          # table centre, under and ahead of the scan
    crate_h = 165.0
    top_z = shroud_tip_z - crate_h - 0.5            # table top so the closed crate's top meets the shroud rim
    t = Pos(tx, ty, top_z - 15.0) * Box(1200.0, 700.0, 30.0)
    for sx in (-1, 1):
        for sy in (-1, 1):
            t += Pos(tx + sx * 560, ty + sy * 310, (top_z - 30.0 - 60.0) / 2) * Box(50.0, 50.0, top_z - 30.0 + 60.0)
    crate = Pos(head.X, head.Y - 140.0, top_z + crate_h / 2) * Box(300.0, 400.0, crate_h)
    t += crate
    for i, (dx, dy) in enumerate([(260, -60), (320, 40), (380, -120), (-330, 90)]):
        t += Pos(tx + dx, ty + dy, top_z + 125.0) * Cylinder(40.0, 250.0)
    out = [part("Sorting table with crate and bottles (site)", break_edges(t, 2.0), "timber", kind="context", group="context",
                color="#8B6B47")]
    sack = Pos(tx + 900.0, ty + 250.0, 380.0) * Cylinder(330.0, 860.0)
    out.append(part("Woven sack of sorted bottles (site)", break_edges(sack, 40.0), "canvas", kind="context", group="context"))
    try:
        import context_parts
        man = context_parts.mannequin(1750.0, "push")
        out.append(part("Sorter 1.75 m (scale)", man, "skin", kind="context", group="context"))
    except Exception as e:   # scale context only; never block the product parts
        print("mannequin not added:", e)
    return out


def product_parts():
    parts = [p for p in M.components(M.CHOSEN) if p["kind"] != "context"]
    out = []
    for p in parts:
        out.append(dict(p))
        q = dict(p)
        q["shape"] = _place(p["shape"])
        q["group"] = "site"
        q["name"] = p["name"] + " (in use)"
        out.append(q)
    return out + _site()


if __name__ == "__main__":
    ps = product_parts()
    groups = {}
    for p in ps:
        groups[p["group"]] = groups.get(p["group"], 0) + 1
    print(len(ps), "parts;", groups)

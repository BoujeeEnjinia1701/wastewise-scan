"""WasteWise Scan product appearance model (build123d), TRL 3.

Finished-product look for photoreal renders: filleted shells, parting-line groove, TPU grip
overmold, display glass, sealed scan button, screws, USB-C port, lanyard tab and visible optics.
APPEARANCE MODEL ONLY: no tolerances, no fabrication detail. CONCEPT, NOT FOR FABRICATION.

Every main dimension and interface comes from PARAMS and derived() in model.py.
Axes as model.py: X along the body (scan head at +X), Y across, Z up, underside of the bottom
shell at Z = 0.

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build123d import (Axis, Box, Cone, Cylinder, Plane, Pos, RectangleRounded, RegularPolygon,
                       Rot, SlotOverall, Sphere, extrude, fillet)
from model import PARAMS, derived, parts as model_parts, cap_parts

# Colours (restrained product palette; accent from the kit)
C_TOP = "#E8EAED"
C_BOTTOM = "#9AA3AE"
C_GRIP = "#2B2F36"
C_ACCENT = "#0F766E"
C_SCREEN = "#22D3EE"
C_GLASS = "#1B232C"
C_WINDOW = "#DCEBF5"
C_BLACK = "#1C1F24"
C_METAL = "#B8BEC6"
C_PCB_BLACK = "#1A1D21"
C_PCB_GREEN = "#166534"
C_CHIP = "#111827"
C_CELL = "#1E40AF"
C_PTFE = "#F7F7F5"

# Appearance-only detail sizes (mm)
FIL_TOP = 4.0          # outer top edge fillet
FIL_BOT = 3.0          # outer bottom edge fillet
GROOVE_W = 0.6         # parting-line groove width
GROOVE_D = 0.6         # parting-line groove depth
GRIP_T = 1.0           # grip recess into the bottom shell
GRIP_PROUD = 0.4       # grip stands proud of the shell
GRIP_X = (-81.0, -8.0) # grip zone along X (tail half)
GRIP_Z = (3.2, 13.6)
SCREW_XY = [(-68.0, -20.0), (-68.0, 20.0), (68.0, -20.0), (68.0, 20.0)]


def _fillet_try(shape, edges, radii):
    """Fillet `edges` with the first radius that gives a valid solid; else return the input."""
    edges = list(edges)
    if not edges:
        return shape
    for r in radii:
        try:
            out = fillet(edges, r)
            if out.is_valid and out.volume > 0:
                return out
        except Exception:
            pass
    return shape


def _prism(L, W, r, z0, h, x=0.0, y=0.0):
    """Rounded-rectangle prism in plan, from z0 up by h."""
    r = max(min(r, min(L, W) / 2 - 0.01), 0.01)
    return Pos(x, y, z0) * extrude(RectangleRounded(L, W, r), amount=h)


def _stadium_x(w, h, x0, depth, z, y=0.0):
    """Stadium (w across Y, h in Z) extruded along +X from x0 by depth."""
    return Pos(x0, y, z) * extrude(Plane.YZ * SlotOverall(w, h), amount=depth)


def _top_edges(s):
    return s.faces().sort_by(Axis.Z)[-1].edges()


def _bottom_edges(s):
    return s.faces().sort_by(Axis.Z)[0].edges()


def _shells(P, D):
    L, W, H, t, r = P["body_l"], P["body_w"], P["body_h"], P["wall"], P["corner_r"]
    zs = P["z_split"]
    hx = P["head_x"]
    body = _prism(L, W, r, 0.0, H)
    body = _fillet_try(body, _top_edges(body), [FIL_TOP, 3.0, 2.0])
    body = _fillet_try(body, _bottom_edges(body), [FIL_BOT, 2.0, 1.0])
    body -= _prism(L - 2 * t, W - 2 * t, r - t, t, H - 2 * t)
    # parting-line groove
    groove = _prism(L + 2, W + 2, r + 1, zs - GROOVE_W / 2, GROOVE_W) - \
        _prism(L - 2 * GROOVE_D, W - 2 * GROOVE_D, r - GROOVE_D, zs - GROOVE_W, 2 * GROOVE_W)
    body -= groove
    bottom = body & Pos(0, 0, zs / 2) * Box(L + 10, W + 10, zs)
    top = body & Pos(0, 0, zs + (H - zs) / 2 + 1) * Box(L + 10, W + 10, H - zs + 2)

    # ---- bottom shell (BOM 10): grip recess, optics seat, screws, USB-C
    gx0, gx1 = GRIP_X
    gzh = GRIP_Z[1] - GRIP_Z[0]
    gzc = (GRIP_Z[0] + GRIP_Z[1]) / 2
    zone = Pos((gx0 + gx1 - gzh) / 2, 0, gzc) * Box(gx1 - gx0 - gzh / 2, W + 10, gzh)
    zone += Pos(gx1 - gzh / 2, 0, gzc) * Rot(90, 0, 0) * Cylinder(gzh / 2, W + 10)   # rounded front end
    inset = _prism(L - 2 * GRIP_T, W - 2 * GRIP_T, r - GRIP_T, -1, H)
    bottom -= zone & (_prism(L + 4, W + 4, r + 2, -1, H) - inset)
    grip = zone & (_prism(L + 2 * GRIP_PROUD, W + 2 * GRIP_PROUD, r + GRIP_PROUD, -1, H) - inset)
    # shallow grip ribs (grooves) on both sides
    for x in range(-66, -14, 7):
        for sy in (-1, 1):
            grip -= Pos(x, sy * (W / 2 + GRIP_PROUD), (GRIP_Z[0] + GRIP_Z[1]) / 2) * Box(1.6, 1.0, 7.0)

    # optical aperture and window seat exactly as model.py
    bottom -= Pos(hx, 0, P["wall"] / 2) * Cylinder(P["window_d"] / 2 - 1.5, P["wall"] + 1)
    bottom -= Pos(hx, 0, P["window_t"] / 2 + 0.5) * Cylinder(P["window_d"] / 2 + 0.2, P["window_t"] + 1)

    # screw bosses, counterbores and clearance holes
    for (x, y) in SCREW_XY:
        bh = zs - 0.5 - t
        bottom += Pos(x, y, t + bh / 2) * Cylinder(3.5, bh)
        bottom -= Pos(x, y, 0.9) * Cylinder(3.2, 1.8)
        bottom -= Pos(x, y, zs / 2) * Cylinder(1.7, zs + 2)

    # USB-C: stadium opening through tail wall (bottom shell and grip)
    usb_cut = _stadium_x(9.2, 3.6, -L / 2 - 3, 6.0, 8.0)
    bottom -= usb_cut
    grip -= usb_cut
    # shallow trim recess around the port in the grip
    grip -= _stadium_x(12.0, 6.0, -L / 2 - 2, 2.0, 8.0)

    # ---- top shell (BOM 1): display pocket and window, button hole, switch recess, lanyard tab
    bx = P["board_x"]
    pocket_l, pocket_w, pocket_d = P["disp_win_l"] + 4, P["disp_win_w"] + 4, 1.0
    top -= _prism(pocket_l, pocket_w, 3.0, H - pocket_d, 2.0, x=bx)
    top -= _prism(P["disp_win_l"], P["disp_win_w"], 1.5, H - 4.0, 4.0, x=bx)
    top -= Pos(P["button_x"], 0, H - 1.5) * Cylinder(8.4, 5.0)
    # slide power switch recess on the -Y side, toward the tail
    top -= Pos(-45.0, -W / 2, 22.5) * Box(13.0, 2.0, 5.0)
    top -= Pos(-45.0, -W / 2 + t, 22.5) * Box(8.0, 2.0 * t, 1.6)
    # lanyard tab at the tail
    tab = Pos(-L / 2 - 4.5, 0, 17.2 + 2.0) * Box(9.0, 12.0, 4.0) + Pos(-L / 2 - 9.0, 0, 17.2 + 2.0) * Cylinder(6.0, 4.0)
    tab -= Pos(-L / 2 - 9.5, 0, 19.2) * Box(3.2, 7.0, 6.0)
    tab = _fillet_try(tab, tab.edges().filter_by(Axis.Z, reverse=True), [1.0, 0.6])
    tab &= Pos(-L / 2 - 8, 0, 20) * Box(16.0, 20.0, 10.0)       # keep only outside the tail wall
    top += tab
    return bottom, top, grip


def product_parts(P=PARAMS):
    D = derived(P)
    m = model_parts(P)
    L, W, H, t = P["body_l"], P["body_w"], P["body_h"], P["wall"]
    hx, bx = P["head_x"], P["board_x"]
    out = []

    def add(name, shape, color, material, bom, group, explode):
        out.append({"name": name, "shape": shape, "color": color, "material": material,
                    "bom": bom, "group": group, "explode": tuple(float(v) for v in explode)})

    bottom, top, grip = _shells(P, D)
    add("Top shell", top, C_TOP, "plastic", 1, "shell", (0, 0, 72))
    add("Bottom shell", bottom, C_BOTTOM, "plastic", 10, "shell", (0, 0, 0))
    add("Grip overmold (TPU)", grip, C_GRIP, "rubber", 10, "shell", (0, 0, 0))

    # ---- display: glass cover, lit screen, module and board (BOM 2)
    glass = _prism(P["disp_win_l"] + 3.6, P["disp_win_w"] + 3.6, 2.8, H - 1.0, 0.8, x=bx)
    add("Display cover glass", glass, C_GLASS, "clear", 2, "shell", (0, 0, 84))
    bz0 = P["board_z"] - P["board_h"] / 2          # envelope bottom
    bz1 = P["board_z"] + P["board_h"] / 2          # envelope top
    pcb_t = 1.2
    screen = _prism(P["disp_win_l"] - 2, P["disp_win_w"] - 2, 0.8, bz1, 0.6, x=bx)
    add("Display screen (lit)", screen, C_SCREEN, "emissive", 2, "internal", (0, 0, 48))
    module = _prism(P["disp_win_l"] + 2, P["board_w"] - 1, 1.0, bz0 + pcb_t, bz1 - bz0 - pcb_t, x=bx)
    add("Display module", module, "#2A2F37", "plastic", 2, "internal", (0, 0, 48))
    pcb = _prism(P["board_l"], P["board_w"], 1.5, bz0, pcb_t, x=bx)
    add("ESP32-S3 board PCB", pcb, C_PCB_BLACK, "plastic", 2, "internal", (0, 0, 48))
    x0b, x1b = bx - P["board_l"] / 2, bx + P["board_l"] / 2
    comps = Pos(x0b + 4.0, 0, bz0 + pcb_t + 1.6) * Box(7.0, 9.0, 3.2)                  # board USB-C
    comps += Pos(x1b - 3.5, -7.0, bz0 + pcb_t + 0.75) * Box(3.5, 4.5, 1.5)             # buttons
    comps += Pos(x1b - 3.5, 7.0, bz0 + pcb_t + 0.75) * Box(3.5, 4.5, 1.5)
    comps += Pos(x1b - 3.5, 0, bz0 + pcb_t + 0.5) * Box(3.0, 3.0, 1.0)
    add("ESP32-S3 board components", comps, C_METAL, "metal", 2, "internal", (0, 0, 48))

    # ---- scan button (BOM 11): bezel collar and accent cap; slide power switch
    bxb = P["button_x"]
    bezel = Pos(bxb, 0, H + 0.75) * (Cylinder(11.0, 1.5) - Cylinder(8.4, 2.0))
    bezel = _fillet_try(bezel, _top_edges(bezel), [0.6, 0.4])
    add("Scan button bezel", bezel, C_GRIP, "plastic", 11, "shell", (0, 0, 92))
    cap_top = H + P["button_h"] - 1.0              # same top as model.py (z = 37)
    cap_bot = H - 0.8
    btn = Pos(bxb, 0, (cap_top + cap_bot) / 2) * Cylinder(P["button_d"] / 2, cap_top - cap_bot)
    btn = _fillet_try(btn, _top_edges(btn), [1.5, 1.0, 0.5])
    btn += Pos(bxb, 0, H - 4.0) * Cylinder(6.0, 6.0)   # plunger, as model.py
    add("Scan button", btn, C_ACCENT, "plastic", 11, "shell", (0, 0, 104))
    slider = Pos(-45.0, -W / 2 + 0.3, 22.5) * Box(5.0, 2.0, 3.0)
    slider -= Pos(-45.0, -W / 2 - 0.9, 22.5) * Box(0.8, 0.6, 4.0)
    slider = _fillet_try(slider, slider.edges().filter_by(Axis.Z), [0.5, 0.3])
    add("Slide power switch", slider, C_GRIP, "plastic", 11, "shell", (0, -16, 72))

    # ---- USB-C (BOM 9): socket body inside, dark insert in the tail opening
    usb_body = Pos(P["usb_x"] + 2.0, 0, 8.0) * Box(6.0, 9.0, 3.2)
    add("USB-C socket", usb_body, C_METAL, "metal", 9, "internal", (-14, 0, 14))
    ins = _stadium_x(9.0, 3.4, -L / 2 + 0.6, 2.5, 8.0)
    ins -= _stadium_x(8.0, 2.5, -L / 2 + 0.5, 1.2, 8.0)
    ins += Pos(-L / 2 + 1.6, 0, 8.0) * Box(1.2, 6.6, 0.7)
    add("USB-C port insert", ins, C_CHIP, "plastic", 9, "shell", (-22, 0, 0))

    # ---- screws (BOM 16, hardware) visible on the underside
    for i, (x, y) in enumerate(SCREW_XY):
        head = Pos(x, y, 0.3 + 0.75) * Cylinder(2.75, 1.5)
        head = _fillet_try(head, _bottom_edges(head), [0.4, 0.2])
        head -= Pos(x, y, 0.3) * extrude(RegularPolygon(1.45, 6), amount=1.0)
        head += Pos(x, y, 1.8 + 5.0) * Cylinder(1.5, 10.0)
        add(f"M3 screw {i + 1}", head, C_METAL, "metal", 16, "shell", (0, 0, -24))

    # ---- sun hood (BOM 14), as model.py, filleted
    hood = m["sun_hood"]
    hood = _fillet_try(hood, hood.edges().filter_by(Axis.Z), [1.0, 0.6])
    hood = _fillet_try(hood, _top_edges(hood), [0.8, 0.5])
    add("Clip-on sun hood", hood, C_BOTTOM, "plastic", 14, "shell", (0, 0, 112))

    # ---- optics
    add("Borosilicate window", m["window"], C_WINDOW, "clear", 6, "shell", (0, 0, -32))
    ro, rt, sh, sw = P["shroud_rim_d"] / 2, P["shroud_top_d"] / 2, P["shroud_h"], P["shroud_wall"]
    shroud = Pos(hx, 0, -sh / 2) * (Cone(ro, rt, sh) - Cone(ro - sw, rt - sw, sh + 0.02))
    shroud += Pos(hx, 0, -0.75) * (Cylinder(rt + 2.0, 1.5) - Cylinder(rt - sw, 2.0))
    shroud = _fillet_try(shroud, _bottom_edges(shroud), [1.2, 0.8, 0.5])
    add("Light shroud (black TPU)", shroud, C_BLACK, "rubber", 7, "shell", (0, 0, -62))
    add("LED holder ring", m["led_holder"], C_BLACK, "plastic", 3, "internal", (0, 0, 20))
    lenses = None
    tilt = D["led_tilt_deg"]
    for k in range(P["led_n"]):
        a = 360.0 * k / P["led_n"] + 22.5
        dome = Rot(0, 0, a) * Pos(P["led_ring_r"], 0, 0) * Rot(0, tilt, 0) * \
            (Pos(0, 0, -P["led_can_h"] / 2) * Sphere(P["led_can_d"] / 2 - 0.5))
        dome = Pos(hx, 0, P["led_z"]) * dome
        lenses = dome if lenses is None else lenses + dome
    add("LED emitters (8 bands)", m["leds"], C_METAL, "metal", 3, "internal", (0, 0, 20))
    add("LED lenses", lenses, "#F3E6C4", "clear", 3, "internal", (0, 0, 20))
    pd = Pos(hx, 0, P["pd_z"] + P["pd_can_h"] / 2) * Cylinder(P["pd_can_d"] / 2, P["pd_can_h"])
    pd += Pos(hx, 0, P["pd_z"] + 0.15) * Cylinder(1.6, 0.3)   # lens face
    add("InGaAs photodiode", pd, "#C9A227", "metal", 4, "internal", (0, 0, 32))
    baffle_h = P["pd_z"] - P["window_t"]
    baffle = Pos(hx, 0, P["window_t"] + baffle_h / 2) * (Cylinder(P["baffle_od"] / 2, baffle_h) - Cylinder(P["baffle_id"] / 2, baffle_h + 1))
    add("Photodiode baffle", baffle, C_BLACK, "plastic", 4, "internal", (0, 0, 32))

    # ---- amplifier and ADC board (BOM 5)
    afe = m["afe_board"]
    add("Amplifier and ADC board", afe, C_PCB_GREEN, "plastic", 5, "internal", (0, 0, 42))
    az = P["afe_z"] + P["afe_t"] / 2
    ac = Pos(hx + 6, 5, az + 0.5) * Box(5.0, 5.0, 1.0)
    ac += Pos(hx - 5, -6, az + 0.6) * Box(3.0, 5.0, 1.2)
    ac += Pos(hx + 6, -7, az + 0.4) * Box(2.0, 3.0, 0.8)
    ac += Pos(hx - P["afe_w"] / 2 + 2.5, 0, az + 1.25) * Box(2.5, 18.0, 2.5)
    add("AFE board components", ac, C_CHIP, "plastic", 5, "internal", (0, 0, 42))

    # ---- 18650 cell (BOM 8) and cradle (BOM 9)
    cl, cr, cx, cz = P["cell_l"], P["cell_d"] / 2, P["cell_x"], P["cell_z"]
    endc = 0.7
    wrap = Pos(cx, 0, cz) * Rot(0, 90, 0) * Cylinder(cr, cl - 2 * endc)
    wrap = _fillet_try(wrap, wrap.edges(), [0.5, 0.3])
    add("18650 cell wrap", wrap, C_CELL, "painted", 8, "internal", (0, 0, 30))
    caps = Pos(cx + cl / 2 - endc / 2, 0, cz) * Rot(0, 90, 0) * Cylinder(cr - 0.6, endc)
    caps += Pos(cx - cl / 2 + endc / 2, 0, cz) * Rot(0, 90, 0) * Cylinder(cr - 0.6, endc)
    add("18650 cell end caps", caps, C_METAL, "metal", 8, "internal", (0, 0, 30))
    cradle = Pos(cx, 0, t + 4.0) * Box(cl + 12, P["cell_d"] + 3, 8.0)
    cradle -= Pos(cx, 0, cz) * Rot(0, 90, 0) * Cylinder(cr + 0.3, cl + 20)
    cradle = _fillet_try(cradle, cradle.edges().filter_by(Axis.Z), [1.5, 0.8])
    add("Cell cradle", cradle, "#3A3F47", "plastic", 9, "internal", (0, 0, 14))

    # ---- accessories (lineup beside the device, not attached)
    c = cap_parts(P, at=(-20.0, -85.0, -P["shroud_h"]))
    cal = c["cal_cap"]
    cal = _fillet_try(cal, _bottom_edges(cal), [1.5, 1.0])
    cal = _fillet_try(cal, _top_edges(cal), [0.8, 0.5])
    add("Calibration cap", cal, C_BLACK, "plastic", 12, "accessory", (-10, -40, -30))
    disc = Pos(40.0, -85.0, -P["shroud_h"] + P["ptfe_t"] / 2) * Cylinder(P["ptfe_d"] / 2, P["ptfe_t"])
    disc = _fillet_try(disc, _top_edges(disc), [0.6, 0.3])
    add("PTFE reference disc", disc, C_PTFE, "plastic", 13, "accessory", (10, -40, -30))
    return out


if __name__ == "__main__":
    for p in product_parts():
        s = p["shape"]
        print(f"{p['name']:30s} {p['group']:9s} {p['material']:8s} valid={s.is_valid} vol={s.volume / 1000:7.2f} cm3")

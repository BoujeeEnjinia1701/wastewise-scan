"""WasteWise Scan parametric model (build123d), TRL 3.
Rev P2 (2026-09-25): clip-on sun hood over the display added (WSC-DDR-003).
Rev P3 (2026-10-02): made constructable (WSC-DDR-004): shell screws, bosses, tongue and gasket;
optical head block clamped by the shroud flange; window clamped between flange and baffle;
cradle with end walls and cell contacts for a protected cell, cell strap; display frame;
panel-mount button; slide switch; USB-C board seat; clip legs on the sun hood; calibration cap
sized so the shroud rim rests on the PTFE disc.

Run from the repo root:  python cad/src/model.py          exports STEP and STL
                         python cad/src/model.py --check  runs the constructability checks
Exports STEP and STL into cad/step and cad/stl. PRELIMINARY, NOT FOR FABRICATION.

Axes: X along the body (scan head at +X), Y across the body, Z up. The underside of the
bottom shell is Z = 0. The shroud rim rests on the item being scanned at Z = -shroud_h.

The calculation note WSC-CAL-001 (docs/04-calcs/sizing.py) imports PARAMS, derived() and
the part solids from this file, so the numbers there follow any change made here.
"""
import sys
from math import atan2, cos, degrees, radians, sin
from pathlib import Path

# Top-level parameters (mm). Edit these, not the geometry below.
PARAMS = {
    # body
    "body_l": 160.0,          # body length
    "body_w": 62.0,           # body width
    "z_split": 16.0,          # top of the bottom shell rim
    "gasket_t": 0.6,          # foam gasket squeezed thickness; the top shell rim starts above it
    "body_h": 34.0,           # top of body
    "wall": 2.0,              # shell wall and floor thickness (2.0 mm decided 2026-10-02, R6)
    "corner_r": 10.0,         # plan corner radius
    "tongue_t": 1.2,          # locating tongue on the bottom shell, inside the top shell wall
    "tongue_h": 2.6,          # height of the tongue above the bottom shell rim
    "shell_screw_xy": (68.0, 20.0),   # four M3 shell screws at (+-x, +-y), from below
    "boss_d": 7.0,            # screw boss diameter
    "insert_d": 4.0,          # hole for an M3 heat-set insert
    # scan head (optical axis)
    "head_x": 55.0,           # optical axis position along the body
    "window_d": 25.0,         # borosilicate LED window, outside diameter
    "window_t": 2.0,          # window thickness
    # fix F1 (2026-10-24, WSC-DEC-001): baffle extended through the glass, so LED light reflected by the
    # window's item-side surface cannot reach the detector (STEM check S12, WSC-CAL-001 C8)
    "win_hole_d": 8.4,        # core-drilled hole through the centre of the LED window
    "det_win_d": 5.8,         # separate detector window in the end of the baffle tube
    "tube_od": 8.0,           # baffle tube of the head block, down through the hole to the glass face
    "tube_bore": 6.0,         # bore in the end of the tube that takes the detector window
    "led_chan_d": 4.0,        # light channel from each LED face down through the head block to the window
    "shroud_h": 18.0,         # shroud depth below the body
    "shroud_rim_d": 42.0,     # outer diameter at the rim (item side)
    "shroud_top_d": 30.0,     # outer diameter at the body
    "shroud_wall": 3.0,
    "flange_d": 47.0,         # shroud clamping flange, against the underside of the body
    "flange_t": 2.5,
    "flange_id": 22.0,        # flange aperture; the flange lip holds the window from below
    "head_screw_r": 20.0,     # three M3 head screws on this radius, at 90, 210 and 330 deg
    # optics
    "pd_can_d": 5.4,          # photodiode TO-46 can diameter (1 mm active area)
    "pd_can_h": 4.0,
    "pd_z": 4.0,              # underside of the photodiode can (detector plane)
    "baffle_od": 7.0,         # (kit 1.7 baffle; replaced by tube_od under fix F1, kept for old scripts)
    "baffle_id": 4.0,
    "led_n": 8,               # number of LED bands
    "led_can_d": 5.4,         # TO-46 SWIR LED can diameter (some bands are 5 mm T-1 3/4)
    "led_can_h": 5.0,
    "led_ring_r": 10.0,       # LED pitch circle radius
    "led_z": 5.5,             # LED can center height
    "holder_od": 36.0,        # printed optical head block (LED holder)
    "holder_id": 5.6,         # bore that takes the photodiode can
    "afe_w": 28.0,            # amplifier and ADC board, square
    "afe_t": 1.6,
    "afe_z": 10.5,            # board center height; the board sits on top of the head block
    "afe_screw": (12.0, 12.0),  # two M2.5 screws at (+x, +-y) from the optical axis
    # electronics and power
    "board_l": 62.0,          # ESP32-S3 display board (T-Display-S3 class), assumed envelope
    "board_w": 26.0,
    "board_h": 9.5,
    "board_x": -10.0,
    "board_z": 26.5,
    "frame_wall": 2.0,        # printed display frame around the board
    "frame_z0": 20.0,         # underside of the display frame lips and ears
    "frame_screws": ((-30.0, 19.0), (10.0, 19.0)),  # four M3 screws at (x, +-y)
    "disp_win_l": 46.0,       # display window in the top shell
    "disp_win_w": 24.0,
    # sun hood over the display (WSC-DDR-003 D10): clip-on, three walls, open toward the user (tail, -X)
    "hood_h": 20.0,           # wall height above the top shell
    "hood_wall": 2.0,
    "hood_base_t": 1.5,       # frame plate that sits on the top shell
    "hood_leg_l": 40.0,       # clip legs down both sides of the top shell
    "rib_z": 28.0,            # underside of the clip ribs on the top shell sides
    "cell_d": 18.5,           # protected 18650 cell (button top, about 69 mm long)
    "cell_l": 69.0,
    "cell_x": -24.0,
    "cell_z": 12.0,
    "cradle_end_t": 3.0,      # cradle end walls that carry the contacts (side rails 1.5 mm)
    "spring_l": 4.0,          # spring contact, compressed length
    "strap_x": -54.0,         # cell strap across the cell, outside the display board
    "strap_w": 11.0,          # fix F3 (2026-10-24): 11 x 10 mm, was 10 x 8 mm (peak drop load, WSC-CAL-001 J4)
    "strap_t": 10.0,
    "strap_cbore": 2.0,       # fix F3: screw heads sit in 6.2 mm counterbores 2 mm deep, so the head clears the ceiling
    "usb_x": -76.0,           # USB-C socket at the tail wall
    "switch_x": -50.0,        # slide power switch in the right-hand side wall (-Y)
    "switch_z": 9.0,
    "button_x": 35.0,
    "button_d": 16.0,         # sealed 16 mm panel-mount push button (thread diameter)
    "button_bezel_d": 19.0,
    "button_h": 4.0,          # height above the top shell (bezel and cap)
    # calibration cap (stored on the shroud)
    "cap_od": 46.0,
    "cap_h": 20.0,
    "cap_wall": 2.2,
    "ptfe_d": 41.0,
    "ptfe_t": 3.0,
}


def derived(P=PARAMS):
    """Numbers the calculation note and the drawing use."""
    z_item = -P["shroud_h"]
    d_pd = P["pd_z"] - z_item                          # detector plane to item
    tilt = degrees(atan2(P["led_ring_r"], P["led_z"] - z_item))   # LED axis tilt from vertical
    rim_id = P["shroud_rim_d"] - 2 * P["shroud_wall"]
    cav_l = P["cell_l"] + 1.0 + P["spring_l"] + 1.0   # cell, flat contact, spring, its plate
    return {
        "z_item": z_item,
        "d_pd_item": d_pd,
        "d_led_item": ((P["led_z"] - z_item) ** 2 + P["led_ring_r"] ** 2) ** 0.5,
        "led_tilt_deg": tilt,
        "rim_id": rim_id,
        "overall_h": P["body_h"] + P["button_h"] + P["shroud_h"],
        "overall_h_hood": P["body_h"] + P["hood_h"] + P["shroud_h"],
        "top_z0": P["z_split"] + P["gasket_t"],
        "ceiling": P["body_h"] - P["wall"],
        "holder_z0": P["wall"],
        "holder_z1": P["afe_z"] - P["afe_t"] / 2,
        "cav_l": cav_l,
        "cav_x0": P["cell_x"] - P["cell_l"] / 2 - P["spring_l"] - 1.0,   # inside face of the spring-end wall
        "cradle_w": P["cell_d"] + 3.0,
        "head_screws": [(P["head_x"] + P["head_screw_r"] * cos(radians(a)), P["head_screw_r"] * sin(radians(a)))
                        for a in (90.0, 210.0, 330.0)],
        "strap_y": P["cell_d"] / 2 + 5.25,                 # strap leg and boss centre, each side
    }


def _plan(P, L, W, r, z0, h):
    from build123d import Axis, Box, Pos, fillet
    b = Pos(0, 0, z0 + h / 2) * Box(L, W, h)
    return fillet(b.edges().filter_by(Axis.Z), r)


def _shell(P, z0, z1, open_top):
    from build123d import Pos
    L, W, t = P["body_l"], P["body_w"], P["wall"]
    h = z1 - z0
    outer = _plan(P, L, W, P["corner_r"], z0, h)
    inner = _plan(P, L - 2 * t, W - 2 * t, P["corner_r"] - t, z0 + (t if open_top else -0.01), h - t + 0.01)
    return outer - inner


def _cyl(x, y, z0, z1, d):
    from build123d import Cylinder, Pos
    return Pos(x, y, (z0 + z1) / 2) * Cylinder(d / 2, z1 - z0)


def _screw(x, y, z_head, head_d, head_h, length, d, up=True):
    """Pan-head screw: head below z_head (up=True, shank going up) or above it (up=False)."""
    s = 1 if up else -1
    head = _cyl(x, y, z_head - s * head_h, z_head, head_d) if up else _cyl(x, y, z_head, z_head + head_h, head_d)
    shank = _cyl(x, y, min(z_head, z_head + s * length), max(z_head, z_head + s * length), d - 0.1)
    return head + shank


def _fuse(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


def build_components(P=PARAMS):
    """Return {name: solid} for every component, in assembled position."""
    from build123d import Box, Cone, Cylinder, Pos, Rot
    D = derived(P)
    hx, t = P["head_x"], P["wall"]
    sx, sy = P["shell_screw_xy"]
    corners = [(a * sx, b * sy) for a in (1, -1) for b in (1, -1)]
    zt0, ceil = D["top_z0"], D["ceiling"]
    out = {}

    # ---------------------------------------------------------------- bottom shell
    bottom = _shell(P, 0.0, P["z_split"], open_top=True)
    # locating tongue inside the top shell wall
    L, W = P["body_l"] - 2 * t, P["body_w"] - 2 * t
    tt = P["tongue_t"]
    tongue = _plan(P, L, W, P["corner_r"] - t, P["z_split"], P["tongue_h"]) - \
        _plan(P, L - 2 * tt, W - 2 * tt, P["corner_r"] - t - tt, P["z_split"] - 0.01, P["tongue_h"] + 0.02)
    bottom += tongue
    for x, y in corners:   # shell screw bosses, counterbored from below
        bottom += _cyl(x, y, t - 0.01, P["z_split"], P["boss_d"])
        bottom -= _cyl(x, y, -0.1, P["z_split"] + 0.1, 3.4)
        bottom -= _cyl(x, y, -0.1, 3.2, 6.2)
    # cell cradle printed with the shell: side walls below the cell centre, end walls carrying the contacts
    cw, ce = D["cradle_w"], P["cradle_end_t"]
    x0, x1 = D["cav_x0"], D["cav_x0"] + D["cav_l"]
    cradle = None
    for s in (1, -1):      # two side rails, 1.5 mm thick, up to 1.5 mm below the cell centre
        rail = Pos((x0 + x1) / 2, s * (cw / 2 - 0.75), t + 4.0) * Box(x1 - x0, 1.5, 8.0)
        cradle = rail if cradle is None else cradle + rail
    for xe in (x0 - ce / 2, x1 + ce / 2):
        cradle += Pos(xe, 0, (t + 18.0) / 2) * Box(ce, cw, 18.0 - t)
    cradle -= Pos((x0 + x1) / 2, 0, P["cell_z"]) * Rot(0, 90, 0) * Cylinder(P["cell_d"] / 2 + 0.2, x1 - x0)
    for xe in (x0 - ce / 2, x1 + ce / 2):   # wire slot in each end wall
        cradle -= Pos(xe, 0, 16.0) * Box(ce + 1, 4.0, 4.0)
    bottom += cradle
    # cell strap bosses
    for s in (1, -1):
        bottom += _cyl(P["strap_x"], s * D["strap_y"], t - 0.01, t + 4.0, P["boss_d"])
        bottom -= _cyl(P["strap_x"], s * D["strap_y"], t, t + 4.1, P["insert_d"])
    # USB-C board seat
    bottom += Pos(-72.15, 0, (t + 4.8) / 2) * Box(10.3, 14.0, 4.8 - t)
    # optics: window hole and head screw holes
    bottom -= _cyl(hx, 0, -0.1, t + 0.1, P["window_d"] + 0.4)
    for x, y in D["head_screws"]:
        bottom -= _cyl(x, y, -0.1, t + 0.1, 3.4)
    # USB-C opening at the tail, slide switch slot and screw holes in the -Y wall
    bottom -= Pos(-P["body_l"] / 2 + t / 2, 0, 8.0) * Box(t + 1, 9.5, 3.8)
    sw = P["switch_x"]
    bottom -= Pos(sw, -P["body_w"] / 2 + t / 2, P["switch_z"]) * Box(7.0, t + 1, 3.5)
    for dx in (-7.5, 7.5):
        bottom -= Pos(sw + dx, -P["body_w"] / 2 + t / 2, P["switch_z"]) * Rot(90, 0, 0) * Cylinder(1.2, t + 1)
    out["bottom_shell"] = bottom

    # ---------------------------------------------------------------- gasket (squeezed foam strip on the rim)
    out["gasket"] = _plan(P, P["body_l"], P["body_w"], P["corner_r"], P["z_split"], P["gasket_t"]) - \
        _plan(P, L, W, P["corner_r"] - t, P["z_split"] - 0.01, P["gasket_t"] + 0.02)

    # ---------------------------------------------------------------- top shell
    top = _shell(P, zt0, P["body_h"], open_top=False)
    top -= Pos(P["board_x"], 0, P["body_h"] - 1) * Box(P["disp_win_l"], P["disp_win_w"], 4.0)
    top -= _cyl(P["button_x"], 0, ceil - 0.1, P["body_h"] + 0.1, P["button_d"] + 0.2)
    for x, y in corners:   # shell screw bosses reach down to the bottom shell bosses (gasket stop)
        top += _cyl(x, y, P["z_split"], ceil + 0.01, P["boss_d"])
        top -= _cyl(x, y, P["z_split"] - 0.1, P["z_split"] + 8.0, P["insert_d"])
    for fx, fy in P["frame_screws"]:
        for s in (1, -1):
            top += _cyl(fx, s * fy, P["frame_z0"] + 2.5, ceil + 0.01, P["boss_d"])
            top -= _cyl(fx, s * fy, P["frame_z0"] + 2.4, P["frame_z0"] + 9.5, P["insert_d"])
    for s in (1, -1):      # clip ribs for the sun hood legs
        top += Pos(P["board_x"], s * (P["body_w"] / 2 + 0.5 - 0.01), P["rib_z"] + 0.5) * Box(P["hood_leg_l"] - 4, 1.02, 1.0)
    out["top_shell"] = top

    # ---------------------------------------------------------------- sun hood with clip legs
    hl, hw, ht, hh = P["disp_win_l"] + 2 * P["hood_wall"], P["disp_win_w"] + 2 * P["hood_wall"], P["hood_base_t"], P["hood_h"]
    hz = P["body_h"]
    leg_in = P["body_w"] / 2 + 1.2          # inner face of each leg, 0.2 clear of the rib
    plate_w = 2 * (leg_in + 2.0)
    hood = Pos(P["board_x"], 0, hz + ht / 2) * (Box(P["hood_leg_l"], plate_w, ht) - Box(P["disp_win_l"], P["disp_win_w"], ht + 1))
    hood += Pos(P["board_x"], 0, hz + ht / 2) * (Box(hl, hw, ht) - Box(P["disp_win_l"], P["disp_win_w"], ht + 1))
    for sy_ in (-1, 1):
        hood += Pos(P["board_x"], sy_ * (P["disp_win_w"] / 2 + P["hood_wall"] / 2), hz + hh / 2) * Box(hl, P["hood_wall"], hh)
        legz0 = P["rib_z"] - 1.5
        hood += Pos(P["board_x"], sy_ * (leg_in + 1.0), (legz0 + hz + ht) / 2) * Box(P["hood_leg_l"], 2.0, hz + ht - legz0)
        hood += Pos(P["board_x"], sy_ * (P["body_w"] / 2 + 0.1 + 0.55), legz0 + 0.65) * Box(P["hood_leg_l"], 1.1 + 0.02, 1.3)
    hood += Pos(P["board_x"] + P["disp_win_l"] / 2 + P["hood_wall"] / 2, 0, hz + hh / 2) * Box(P["hood_wall"], hw, hh)
    out["sun_hood"] = hood

    # ---------------------------------------------------------------- display board and its frame
    bz0 = P["board_z"] - P["board_h"] / 2
    out["display_board"] = Pos(P["board_x"], 0, P["board_z"]) * Box(P["board_l"], P["board_w"], P["board_h"])
    fw = P["frame_wall"]
    il, iw = P["board_l"] + 0.4, P["board_w"] + 0.4
    fz0 = P["frame_z0"]
    frame = None
    for s in (1, -1):      # side walls with lips under the board edges
        wall = Pos(P["board_x"], s * (iw / 2 + fw / 2), (fz0 + ceil) / 2) * Box(il + 2 * fw, fw, ceil - fz0)
        lip = Pos(P["board_x"], s * (iw / 2 - 1.0), (fz0 + bz0) / 2) * Box(il, 2.0 + 0.02, bz0 - fz0)
        frame = wall + lip if frame is None else frame + wall + lip
    for s in (1, -1):      # end walls above the cell
        frame += Pos(P["board_x"] + s * (il / 2 + fw / 2), 0, (bz0 + ceil) / 2) * Box(fw, iw + 0.02, ceil - bz0)
    for fx, fy in P["frame_screws"]:
        for s in (1, -1):
            ear = Pos(fx, s * (iw / 2 + fw + 3.5 - 0.01), fz0 + 1.25) * Box(7.0, 7.0, 2.5)
            frame += ear
            frame -= _cyl(fx, s * fy, fz0 - 0.1, fz0 + 2.6, 3.4)
    out["display_frame"] = frame

    # ---------------------------------------------------------------- cell, contacts, strap
    out["cell"] = Pos(P["cell_x"], 0, P["cell_z"]) * Rot(0, 90, 0) * Cylinder(P["cell_d"] / 2, P["cell_l"])
    xc0 = D["cav_x0"]
    contacts = Pos(xc0 + 0.5, 0, P["cell_z"]) * Box(1.0, 12.0, 12.0)
    contacts += Pos(xc0 + 1.0 + P["spring_l"] / 2, 0, P["cell_z"]) * Rot(0, 90, 0) * Cylinder(3.0, P["spring_l"])
    contacts += Pos(xc0 + D["cav_l"] - 0.5, 0, P["cell_z"]) * Box(1.0, 12.0, 12.0)
    out["cell_contacts"] = contacts
    ctop = P["cell_z"] + P["cell_d"] / 2
    syy = D["strap_y"]
    strap = Pos(P["strap_x"], 0, ctop + P["strap_t"] / 2) * Box(P["strap_w"], 2 * syy + 7.0, P["strap_t"])
    for s in (1, -1):
        strap += Pos(P["strap_x"], s * syy, (t + 4.0 + ctop) / 2) * Box(P["strap_w"], 4.0, ctop - t - 4.0)
        strap -= _cyl(P["strap_x"], s * syy, t + 3.9, ctop + P["strap_t"] + 0.1, 3.4)
        strap -= _cyl(P["strap_x"], s * syy, ctop + P["strap_t"] - P["strap_cbore"], ctop + P["strap_t"] + 0.1, 6.2)
    out["cell_strap"] = strap
    # USB-C board on its seat, socket mouth in the tail wall opening
    usb = Pos(-72.15, 0, 5.6) * Box(10.3, 12.0, 1.6)
    usb += Pos(-P["body_l"] / 2 + 3.7, 0, 8.0) * Box(7.4, 9.0, 3.2)
    out["usb_board"] = usb
    # slide switch: plate against the inside of the -Y wall, body behind it, actuator through the slot
    ywi = -P["body_w"] / 2 + t
    swp = Pos(P["switch_x"], ywi + 0.3, P["switch_z"]) * Box(20.0, 0.6, 6.0)
    swp -= Pos(P["switch_x"] - 7.5, ywi + 0.3, P["switch_z"]) * Rot(90, 0, 0) * Cylinder(1.1, 1.0)
    swp -= Pos(P["switch_x"] + 7.5, ywi + 0.3, P["switch_z"]) * Rot(90, 0, 0) * Cylinder(1.1, 1.0)
    swp += Pos(P["switch_x"], ywi + 0.6 + 3.0, P["switch_z"]) * Box(10.0, 6.0, 6.0)
    swp += Pos(P["switch_x"], -P["body_w"] / 2 + t - 3.5 / 2, P["switch_z"]) * Box(3.0, 3.5, 2.0)   # actuator, 1 mm proud
    out["switch"] = swp

    # ---------------------------------------------------------------- optics
    # fix F1: an annular LED window and a separate detector window in the end of the baffle tube
    led_win = _cyl(hx, 0, 0.0, P["window_t"], P["window_d"]) - _cyl(hx, 0, -0.1, P["window_t"] + 0.1, P["win_hole_d"])
    det_win = _cyl(hx, 0, 0.0, P["window_t"], P["det_win_d"])
    out["window"] = led_win + det_win
    ro, rt, sh, sw_ = P["shroud_rim_d"] / 2, P["shroud_top_d"] / 2, P["shroud_h"], P["shroud_wall"]
    shroud = Pos(hx, 0, -sh / 2) * (Cone(ro, rt, sh) - Cone(ro - sw_, rt - sw_, sh + 0.02))
    flange = _cyl(hx, 0, -P["flange_t"], 0.0, P["flange_d"]) - _cyl(hx, 0, -P["flange_t"] - 0.1, 0.1, P["flange_id"])
    shroud += flange
    shroud -= _cyl(hx, 0, -P["flange_t"] - 0.01, 0.01, P["flange_id"])
    for x, y in D["head_screws"]:
        shroud -= _cyl(x, y, -P["flange_t"] - 0.1, 0.1, 3.4)
    out["shroud"] = shroud
    hz0, hz1 = D["holder_z0"], D["holder_z1"]
    holder = _cyl(hx, 0, hz0, hz1, P["holder_od"])
    for x, y in D["head_screws"]:   # lugs for the head screws
        a = atan2(y, x - hx)
        holder += _cyl(x, y, hz0, hz1, 7.0)
        holder += Pos(hx + (P["head_screw_r"] - 3.0) * cos(a), (P["head_screw_r"] - 3.0) * sin(a), (hz0 + hz1) / 2) * \
            Rot(0, 0, degrees(a)) * Box(6.0, 7.0, hz1 - hz0)
        holder -= _cyl(x, y, hz0 - 0.1, hz0 + 6.0, P["insert_d"])
    holder += _cyl(hx, 0, 0.0, hz0 + 0.01, P["tube_od"])                     # fix F1: baffle tube down through the glass
    holder -= _cyl(hx, 0, -0.1, P["window_t"], P["tube_bore"])                # bore for the detector window
    holder -= _cyl(hx, 0, P["window_t"] - 0.01, P["pd_z"], P["baffle_id"])    # aperture under the photodiode
    holder -= _cyl(hx, 0, P["pd_z"], hz1 + 0.1, P["holder_id"])                # bore for the photodiode can
    ax_, ay_ = P["afe_screw"]
    for s in (1, -1):
        holder -= _cyl(hx + ax_, s * ay_, hz1 - 5.0, hz1 + 0.1, 3.5)
    leds = None
    for k in range(P["led_n"]):
        a = 360.0 * k / P["led_n"] + 22.5
        place = Pos(hx, 0, P["led_z"]) * Rot(0, 0, a) * Pos(P["led_ring_r"], 0, 0) * Rot(0, D["led_tilt_deg"], 0)
        led = place * Cylinder(P["led_can_d"] / 2, P["led_can_h"])
        holder -= place * Pos(0, 0, 4.0) * Cylinder(P["led_can_d"] / 2 + 0.1, P["led_can_h"] + 8.0)
        holder -= place * Pos(0, 0, -P["led_can_h"] / 2 - 3.0 + 0.01) * Cylinder(P["led_chan_d"] / 2, 6.0)   # light channel to the window
        leds = led if leds is None else leds + led
    out["led_holder"] = holder
    out["leds"] = leds
    out["photodiode"] = Pos(hx, 0, P["pd_z"] + P["pd_can_h"] / 2) * Cylinder(P["pd_can_d"] / 2, P["pd_can_h"])
    afe = Pos(hx, 0, P["afe_z"]) * Box(P["afe_w"], P["afe_w"], P["afe_t"])
    for s in (1, -1):
        afe -= _cyl(hx + ax_, s * ay_, hz1 - 0.1, hz1 + P["afe_t"] + 0.1, 2.8)
    out["afe_board"] = afe

    # ---------------------------------------------------------------- scan button (panel mount, nut inside)
    bx = P["button_x"]
    btn = _cyl(bx, 0, P["body_h"], P["body_h"] + 2.0, P["button_bezel_d"])
    btn += _cyl(bx, 0, P["body_h"] + 2.0, P["body_h"] + P["button_h"], 12.0)
    btn += _cyl(bx, 0, 20.0, P["body_h"], P["button_d"])
    btn += Pos(bx, 0, ceil - 1.5) * Cylinder(10.0, 3.0)        # nut, against the ceiling
    out["button"] = btn

    # ---------------------------------------------------------------- fixings
    out["shell_screws"] = _fuse([_screw(x, y, 3.2, 5.5, 3.0, 20.0, 3.0) for x, y in corners])
    fl = -P["flange_t"]
    hs = []
    for x, y in D["head_screws"]:
        hs.append(_cyl(x, y, fl - 0.5, fl, 7.0) + _screw(x, y, fl - 0.5, 5.5, 2.0, 10.0 + 0.5, 3.0))
    out["head_screws"] = _fuse(hs)
    out["frame_screws"] = _fuse([_screw(fx, s * fy, P["frame_z0"], 5.5, 2.0, 8.0, 3.0)
                                 for fx, fy in P["frame_screws"] for s in (1, -1)])
    out["strap_screws"] = _fuse([_screw(P["strap_x"], s * syy, ctop + P["strap_t"] - P["strap_cbore"], 5.5, 1.8, 25.0, 3.0, up=False)
                                 for s in (1, -1)])
    out["afe_screws"] = _fuse([_screw(hx + ax_, s * ay_, hz1 + P["afe_t"], 4.5, 1.7, 6.0, 2.5, up=False) for s in (1, -1)])
    swf = []
    for dx in (-7.5, 7.5):
        xx = P["switch_x"] + dx
        swf.append(Pos(xx, -P["body_w"] / 2 - 0.6, P["switch_z"]) * Rot(90, 0, 0) * Cylinder(1.9, 1.2))
        swf.append(Pos(xx, -P["body_w"] / 2 + 2.5, P["switch_z"]) * Rot(90, 0, 0) * Cylinder(0.95, 5.0))
        swf.append(Pos(xx, ywi + 0.6 + 0.8, P["switch_z"]) * Rot(90, 0, 0) * Cylinder(2.0, 1.6))
    out["switch_screws"] = _fuse(swf)
    return out


def parts(P=PARAMS):
    """All components in assembled position (the calculation note and the drawing use this)."""
    return build_components(P)


def cap_parts(P=PARAMS, at=(0.0, 0.0, 0.0)):
    """Calibration cap and PTFE disc, open side up, base at `at`."""
    from build123d import Cylinder, Pos
    x, y, z = at
    r, h, t = P["cap_od"] / 2, P["cap_h"], P["cap_wall"]
    tb = 2.0
    cap = Pos(x, y, z + h / 2) * (Cylinder(r, h) - Pos(0, 0, tb) * Cylinder(r - t, h))
    disc = Pos(x, y, z + tb + P["ptfe_t"] / 2) * Cylinder(P["ptfe_d"] / 2, P["ptfe_t"])
    return {"cal_cap": cap, "ptfe_disc": disc}


def cap_on_shroud(P=PARAMS):
    """The cap pushed over the shroud: the rim rests on the PTFE disc."""
    z = -P["shroud_h"] - P["ptfe_t"] - 2.0
    return cap_parts(P, at=(P["head_x"], 0.0, z))


def scanner(P=PARAMS):
    from build123d import Compound
    return Compound(children=list(parts(P).values()))


def assembly(P=PARAMS):
    from build123d import Compound
    return Compound(children=list(parts(P).values()) + list(cap_parts(P, at=(-20.0, -85.0, -P["shroud_h"])).values()))


# ------------------------------------------------------------------ kit 1.9 interface (STANDARDS section 24)
# OPTIONS, PRINCIPLES, CHOSEN, OPTION_VIEWS and components(option), each part a cad_parts.part() dict at
# detail level D3. Option A is the design above (build_components) with every bought part, screw, washer,
# nut and heat-set insert as its own solid; option B (WSC-OPT-001) shares the body and swaps the optical head.
sys.path[:0] = [str(Path(__file__).resolve().parent), str(Path(__file__).resolve().parents[2] / ".kit")]

TITLE = "WasteWise Scan"
OPTIONS = {"A": "Eight-band LED scanner", "B": "Tunable-filter spectrometer"}
PRINCIPLES = {
    "A": "Eight NIR and SWIR LEDs from 850 to 1,650 nm flash in turn on the item and one InGaAs photodiode "
         "reads each reflection; a classifier on the band ratios names the resin.",
    "B": "Two small tungsten lamps light the item with a broad spectrum and a MEMS Fabry-Perot tunable filter "
         "on an InGaAs detector sweeps 1,550 to 1,850 nm, reading a continuous spectrum across the polymer bands.",
}
CHOSEN = "A"
OPTION_VIEWS = {k: {"el": 24, "az": -50, "scale": "none", "keep_context": True} for k in OPTIONS}
ALLOWED_CONTACTS = []

# option B overrides (WSC-OPT-001): taller head block for the TO-5 sensor, driver board above it
PARAMS_B = dict(PARAMS, afe_z=13.5, fpi_flange_d=9.2, fpi_body_d=8.2, fpi_h=6.5, fpi_z=4.5,
                lamp_r=11.0, lamp_z=3.0, lamp_bulb_d=5.0, lamp_bulb_l=9.0)

_CACHE = {}


def _built(key, P):
    if key not in _CACHE:
        _CACHE[key] = build_components(P)
    return _CACHE[key]


def _parts_lib():
    import cad_parts as cp
    import wws_parts as wp
    return cp, wp


def _common(P, C, bom):
    """Body, display, power and fixings shared by both options (positions from build_components)."""
    cp, wp = _parts_lib()
    from build123d import Pos, Rot, RegularPolygon, extrude
    D = derived(P)
    hx, t = P["head_x"], P["wall"]
    sx, sy = P["shell_screw_xy"]
    corners = [(a * sx, b * sy) for a in (1, -1) for b in (1, -1)]
    b = (lambda n: n) if bom else (lambda n: None)
    out = []

    def add(name, shape, mat, kind="made", bomn=None, group="shell", explode=(0, 0, 0), color=None):
        out.append(cp.part(name, shape, mat, kind=kind, bom=bomn, group=group, explode=explode, color=color))

    # made parts (PETG unless noted); kit MATERIALS has no PETG, TPU or PTFE: HDPE density stands in (REVIEW)
    add("Top shell", C["top_shell"], "hdpe_natural", bomn=b(1), explode=(0, 0, 95), color="#E5E7EB")
    add("Bottom shell and grip", C["bottom_shell"], "hdpe_natural", bomn=b(10), color="#9CA3AF")
    add("Shell gasket (EPDM foam)", C["gasket"], "epdm", kind="bought", bomn=b(19), explode=(0, 0, 40))
    add("Clip-on sun hood", C["sun_hood"], "hdpe_natural", bomn=b(14), explode=(0, 0, 130), color="#475569")
    add("Display frame", C["display_frame"], "hdpe_natural", bomn=b(17), group="internal", explode=(0, 0, 70), color="#0E7490")
    add("Cell strap", C["cell_strap"], "hdpe_natural", bomn=b(18), group="internal", explode=(0, 0, 48), color="#B45309")
    add("Light shroud (TPU)", C["shroud"], "epdm", bomn=b(7), explode=(0, 0, -60))
    # windows (fix F1): annular LED window and detector window, borosilicate, edges broken
    led_win = _cyl(hx, 0, 0.0, P["window_t"], P["window_d"]) - _cyl(hx, 0, -0.1, P["window_t"] + 0.1, P["win_hole_d"])
    add("LED window (borosilicate ring)", wp.eased(led_win, 0.2), "glass", kind="bought", bomn=b(6), explode=(0, 0, -30))
    add("Detector window (borosilicate)", wp.eased(_cyl(hx, 0, 0.0, P["window_t"], P["det_win_d"]), 0.2), "glass",
        kind="bought", bomn=b(6), explode=(0, 0, -36))

    # display board (T-Display-S3 class), envelope from PARAMS, modelled as its main parts
    bx, bz0 = P["board_x"], P["board_z"] - P["board_h"] / 2
    bl, bw = P["board_l"], P["board_w"]
    ex = (0, 0, 62)
    add("Display board PCB", Pos(bx, 0, bz0) * wp.pcb(bl, bw, 1.2, holes=[(s1 * 28.0, s2 * 10.5, 2.2) for s1 in (1, -1) for s2 in (1, -1)]),
        "hdpe_recycled", kind="bought", bomn=b(2), group="internal", explode=ex, color="#1A1D21")
    add("ESP32-S3 module", Pos(bx - 5, 0, bz0 + 1.2) * wp.smd_box(18.0, 20.0, 2.3), "stainless", kind="bought", bomn=b(2), group="internal", explode=ex)
    disp = wp.eased(Pos(bx + 1, 0, bz0 + 3.5 + 2.65) * __import__("build123d").Box(48.0, 25.0, 5.3), 0.3)
    add("IPS display module", disp, "matte_black", kind="bought", bomn=b(2), group="internal", explode=ex)
    glass = wp.eased(Pos(bx + 1, 0, bz0 + 8.8 + 0.35) * __import__("build123d").Box(48.0, 25.0, 0.7), 0.15)
    add("Display cover glass", glass, "glass", kind="bought", bomn=b(2), group="internal", explode=ex)
    add("USB-C receptacle on the display board", Pos(bx - bl / 2 + 3.7, 0, bz0 + 1.2 + 1.63) * Rot(0, 0, 180) * wp.usb_c_receptacle(),
        "stainless", kind="bought", bomn=b(2), group="internal", explode=ex)
    for s in (1, -1):
        add("Display board button", Pos(bx + 25, s * 9.0, bz0 + 1.2) * wp.smd_box(3.0, 4.0, 1.5), "matte_black", kind="bought",
            bomn=b(2), group="internal", explode=ex)

    # power: cell, contacts, USB-C power board, switch
    xc0 = D["cav_x0"]
    add("18650 Li-ion cell, protected", Pos(P["cell_x"], 0, P["cell_z"]) * wp.cell_18650(P["cell_d"], P["cell_l"]),
        "aluminium", kind="bought", bomn=b(8), group="internal", explode=(0, 0, 32), color="#1E40AF")
    add("Cell contact, negative plate", Pos(xc0, 0, P["cell_z"]) * wp.contact_plate(), "stainless", kind="bought", bomn=b(9), group="internal", explode=(0, 0, 18))
    add("Cell contact spring", Pos(xc0 + 1.0, 0, P["cell_z"]) * wp.spring_contact(5.0, 1.0, P["spring_l"]), "stainless", kind="bought",
        bomn=b(9), group="internal", explode=(0, 0, 18))
    add("Cell contact, positive plate", Pos(xc0 + D["cav_l"] - 1.0, 0, P["cell_z"]) * wp.contact_plate(), "stainless", kind="bought",
        bomn=b(9), group="internal", explode=(0, 0, 18))
    add("USB-C power board PCB", Pos(-72.15, 0, 4.8) * wp.pcb(10.3, 12.0, 1.6), "hdpe_recycled", kind="bought", bomn=b(9),
        group="internal", explode=(0, 0, 18), color="#1D4ED8")
    add("USB-C power receptacle", Pos(-P["body_l"] / 2 + 3.7, 0, 8.0) * Rot(0, 0, 180) * wp.usb_c_receptacle(), "stainless",
        kind="bought", bomn=b(9), group="internal", explode=(0, 0, 18))
    add("Slide power switch", C["switch"], "matte_black", kind="bought", bomn=b(11), group="internal", explode=(0, -20, 0))

    # scan button: bezel, cap and threaded body; hexagonal panel nut under the ceiling
    bxn, ceil = P["button_x"], D["ceiling"]
    btn = _cyl(bxn, 0, P["body_h"], P["body_h"] + 2.0, P["button_bezel_d"]) + \
        _cyl(bxn, 0, P["body_h"] + 2.0, P["body_h"] + P["button_h"], 12.0) + _cyl(bxn, 0, 20.0, P["body_h"], P["button_d"])
    add("Sealed 16 mm scan button", btn, "hdpe_natural", kind="bought", bomn=b(11), explode=(0, 0, 128), color="#F59E0B")
    nut = Pos(bxn, 0, ceil - 3.0) * (extrude(RegularPolygon(10.0, 6), 3.0) - Pos(0, 0, 1.5) * __import__("build123d").Cylinder(8.1, 3.2))
    add("Button panel nut M16", nut, "zinc_plated", kind="fastener", bomn=b(11), group="internal", explode=(0, 0, 110))

    # fixings: every screw, washer, nut and heat-set insert (BOM line 16)
    F = lambda name, shape, mat="zinc_plated", ex=(0, 0, 0), grp="internal": add(name, shape, mat, kind="fastener", bomn=b(16), group=grp, explode=ex)
    for x, y in corners:
        F("M3x20 pan head screw (shell)", Pos(x, y, 3.2) * Rot(180, 0, 0) * wp.pan_screw(3.0, 20.0), ex=(0, 0, -95), grp="shell")
        F("M3 heat-set insert (shell boss)", Pos(x, y, 16.7) * wp.heat_set_insert(4.0, 5.7, 3.0), "brass", ex=(0, 0, 95))
    fl = -P["flange_t"]
    for x, y in D["head_screws"]:
        F("M3 washer (shroud flange)", Pos(x, y, fl - 0.5) * wp.washer_small(3.0), ex=(0, 0, -80), grp="shell")
        F("M3x10 pan head screw (shroud and head block)", Pos(x, y, fl - 0.5) * Rot(180, 0, 0) * wp.pan_screw(3.0, 10.0), ex=(0, 0, -90), grp="shell")
        F("M3 heat-set insert (head block lug)", Pos(x, y, D["holder_z0"] + 0.05) * wp.heat_set_insert(4.0, 5.7, 3.0), "brass", ex=(0, 0, 22))
    for fx, fy in P["frame_screws"]:
        for s in (1, -1):
            F("M3x8 pan head screw (display frame)", Pos(fx, s * fy, P["frame_z0"]) * Rot(180, 0, 0) * wp.pan_screw(3.0, 8.0), ex=(0, 0, 70))
            F("M3 heat-set insert (frame boss)", Pos(fx, s * fy, P["frame_z0"] + 2.6) * wp.heat_set_insert(4.0, 5.7, 3.0), "brass", ex=(0, 0, 95))
    ctop = P["cell_z"] + P["cell_d"] / 2
    for s in (1, -1):
        F("M3x25 low head screw (cell strap)", Pos(P["strap_x"], s * D["strap_y"], ctop + P["strap_t"] - P["strap_cbore"]) * wp.pan_screw(3.0, 25.0, 5.5, 1.8), ex=(0, 0, 60))
        F("M3 heat-set insert (strap boss)", Pos(P["strap_x"], s * D["strap_y"], t + 0.05) * wp.heat_set_insert(4.0, 3.9, 3.0), "brass")
    ywall = -P["body_w"] / 2
    for dx in (-7.5, 7.5):
        xx = P["switch_x"] + dx
        F("M2x6 pan head screw (switch)", Pos(xx, ywall, P["switch_z"]) * Rot(90, 0, 0) * wp.pan_screw(2.0, 6.0), ex=(0, -20, 0), grp="shell")
        F("M2 hex nut (switch)", Pos(xx, ywall + t + 0.6, P["switch_z"]) * Rot(-90, 0, 0) * wp.hex_nut_small(2.0), ex=(0, -20, 0))
    return out


def _afe_screws(P, bom):
    cp, wp = _parts_lib()
    from build123d import Pos
    D = derived(P)
    hx, (ax_, ay_) = P["head_x"], P["afe_screw"]
    hz1 = D["holder_z1"]
    out = []
    for s in (1, -1):
        out.append(cp.part("M2.5x6 pan head screw (board)", Pos(hx + ax_, s * ay_, hz1 + P["afe_t"]) * wp.pan_screw(2.5, 6.0), "zinc_plated",
                           kind="fastener", bom=16 if bom else None, group="internal", explode=(0, 0, 70)))
        out.append(cp.part("M2.5 heat-set insert (head block)", Pos(hx + ax_, s * ay_, hz1 - 4.1) * wp.heat_set_insert(3.5, 4.0, 2.5), "brass",
                           kind="fastener", bom=16 if bom else None, group="internal", explode=(0, 0, 40)))
    return out


def _board(P, extra_holes, parts, bom, bomn, name):
    """Amplifier or driver board: perfboard square on the head block with its parts on top."""
    cp, wp = _parts_lib()
    from build123d import Pos
    D = derived(P)
    hx, (ax_, ay_), w = P["head_x"], P["afe_screw"], P["afe_w"]
    z = D["holder_z1"]
    holes = [(ax_, s * ay_, 2.8) for s in (1, -1)] + extra_holes
    out = [cp.part(name, Pos(hx, 0, z) * wp.pcb(w, w, P["afe_t"], holes=holes, r=1.0), "hdpe_recycled", kind="bought",
                   bom=bomn if bom else None, group="internal", explode=(0, 0, 60), color="#166534")]
    zt = z + P["afe_t"]
    for pname, shape, (x, y), mat in parts:
        out.append(cp.part(pname, Pos(hx + x, y, zt) * shape, mat, kind="bought", bom=bomn if bom else None, group="internal", explode=(0, 0, 60)))
    return out


def _option_a(bom=True):
    cp, wp = _parts_lib()
    from build123d import Pos, Rot
    P = PARAMS
    C = _built("A", P)
    D = derived(P)
    hx = P["head_x"]
    out = _common(P, C, bom)
    b = (lambda n: n) if bom else (lambda n: None)
    out.append(cp.part("Optical head block (black PETG)", C["led_holder"], "matte_black", bom=b(3), group="internal", explode=(0, 0, 22)))
    for k in range(P["led_n"]):
        a = 360.0 * k / P["led_n"] + 22.5
        place = Pos(hx, 0, P["led_z"]) * Rot(0, 0, a) * Pos(P["led_ring_r"], 0, 0) * Rot(0, D["led_tilt_deg"], 0)
        led = place * Pos(0, 0, -P["led_can_h"] / 2) * wp.to_can(P["led_can_d"], 4.7, P["led_can_h"], window_d=2.5, lead_l=1.5)
        nm = [850, 940, 1050, 1200, 1300, 1450, 1550, 1650][k]
        out.append(cp.part(f"LED {nm} nm (TO-46)", led, "stainless", kind="bought", bom=b(3), group="internal", explode=(0, 0, 40)))
    out.append(cp.part("InGaAs photodiode (TO-46)", Pos(hx, 0, P["pd_z"]) * wp.to_can(P["pd_can_d"], 4.7, P["pd_can_h"], window_d=2.0, lead_l=4.0),
                       "stainless", kind="bought", bom=b(4), group="internal", explode=(0, 0, 48)))
    import math
    lead_holes = [(1.27 * math.cos(math.radians(90 + i * 120)), 1.27 * math.sin(math.radians(90 + i * 120)), 0.9) for i in range(3)]
    parts = [("Transimpedance op-amp (SOIC-8)", wp.ic(4.9, 3.9, 1.5, 4, 1.27), (-7.0, 7.0), "matte_black"),
             ("24-bit ADC (TSSOP-16)", wp.ic(5.0, 4.4, 1.0, 8, 0.6), (-7.0, -7.0), "matte_black"),
             ("Wire header, 6 pins", wp.header(6, body_h=2.5, pin_up=3.0), (-12.0, 0.0), "matte_black")]
    parts += [(f"LED switch MOSFET {i + 1}", wp.smd_box(2.9, 1.3, 1.0), (5.0, -8.75 + 2.5 * i), "matte_black") for i in range(8)]
    out += _board(P, lead_holes, parts, bom, 5, "Amplifier and ADC board (perfboard)")
    out += _afe_screws(P, bom)
    # calibration cap and PTFE disc, stored beside the scanner (as in the assembly STEP)
    cps = cap_parts(P, at=(-20.0, -85.0, -P["shroud_h"]))
    out.append(cp.part("Calibration cap (black PETG)", cps["cal_cap"], "matte_black", bom=b(12), group="accessory", explode=(0, -40, 0)))
    out.append(cp.part("White PTFE reference disc", wp.eased(cps["ptfe_disc"], 0.3), "hdpe_natural", kind="bought", bom=b(13),
                       group="accessory", explode=(0, -40, 30), color="#F9FAFB"))
    return out


def _head_b(P):
    """Option B optical head block: lugs, baffle tube through the glass, bore for the TO-5 sensor, two lamp pockets."""
    from build123d import Pos, Rot, Box, Cylinder
    from math import atan2, cos, degrees, sin
    D = derived(P)
    hx = P["head_x"]
    hz0, hz1 = D["holder_z0"], D["holder_z1"]
    h = _cyl(hx, 0, hz0, hz1, P["holder_od"])
    for x, y in D["head_screws"]:
        a = atan2(y, x - hx)
        h += _cyl(x, y, hz0, hz1, 7.0)
        h += Pos(hx + (P["head_screw_r"] - 3.0) * cos(a), (P["head_screw_r"] - 3.0) * sin(a), (hz0 + hz1) / 2) * Rot(0, 0, degrees(a)) * Box(6.0, 7.0, hz1 - hz0)
        h -= _cyl(x, y, hz0 - 0.1, hz0 + 6.0, P["insert_d"])
    h += _cyl(hx, 0, 0.0, hz0 + 0.01, P["tube_od"])
    h -= _cyl(hx, 0, -0.1, P["window_t"], P["tube_bore"])
    h -= _cyl(hx, 0, P["window_t"] - 0.01, P["fpi_z"], P["baffle_id"])
    h -= _cyl(hx, 0, P["fpi_z"], hz1 + 0.1, P["fpi_flange_d"] + 0.2)
    ax_, ay_ = P["afe_screw"]
    for s in (1, -1):
        h -= _cyl(hx + ax_, s * ay_, hz1 - 5.0, hz1 + 0.1, 3.5)
    tilt = degrees(atan2(P["lamp_r"], P["lamp_z"] + P["shroud_h"]))
    places = []
    for a in (0.0, 180.0):
        place = Pos(hx, 0, P["lamp_z"]) * Rot(0, 0, a) * Pos(P["lamp_r"], 0, 0) * Rot(0, tilt, 0)
        h -= place * Pos(0, 0, 10.0) * Cylinder(P["lamp_bulb_d"] / 2 + 1.2, 20.2)   # fix F4: room for an aluminium sleeve
        h -= place * Pos(0, 0, -3.0) * Cylinder(2.0, 6.0)
        places.append(place)
    return h, places


def _option_b():
    cp, wp = _parts_lib()
    from build123d import Pos
    import math
    P = PARAMS_B
    C = _built("B", P)
    hx = P["head_x"]
    out = _common(P, C, bom=False)
    head, places = _head_b(P)
    out.append(cp.part("Optical head block B (black PETG)", head, "matte_black", group="internal", explode=(0, 0, 22)))
    from build123d import Sketch, Circle, extrude
    for i, pl in enumerate(places):
        out.append(cp.part(f"Tungsten lamp {i + 1} (T-1 3/4)", pl * wp.mini_lamp(P["lamp_bulb_d"], P["lamp_bulb_l"], 6.0), "glass",
                           kind="bought", group="internal", explode=(0, 0, 40)))
        # fix F4 (independent review): an aluminium sleeve with a 0.2 mm air gap keeps the hot bulb off the PETG block
        sleeve = extrude(Sketch() + Circle(P["lamp_bulb_d"] / 2 + 1.2) - Circle(P["lamp_bulb_d"] / 2 + 0.2), P["lamp_bulb_l"])
        out.append(cp.part(f"Aluminium lamp sleeve {i + 1}", pl * wp.eased(sleeve, 0.2), "aluminium", group="internal", explode=(0, 0, 32)))
    out.append(cp.part("MEMS-FPI spectrum sensor (TO-5 class)", Pos(hx, 0, P["fpi_z"]) * wp.to_can(P["fpi_flange_d"], P["fpi_body_d"], P["fpi_h"],
                       window_d=3.0, leads=4, lead_l=4.0, lead_pcd=5.08), "stainless", kind="bought", group="internal", explode=(0, 0, 48)))
    lead_holes = [(2.54 * math.cos(math.radians(90 + i * 90)), 2.54 * math.sin(math.radians(90 + i * 90)), 0.9) for i in range(4)]
    parts = [("Boost inductor (filter tuning supply)", wp.smd_box(4.0, 4.0, 2.0), (-8.0, 7.0), "matte_black"),
             ("Filter driver and DAC (TSSOP-16)", wp.ic(5.0, 4.4, 1.0, 8, 0.6), (-8.0, -7.0), "matte_black"),
             ("Transimpedance op-amp (SOIC-8)", wp.ic(4.9, 3.9, 1.5, 4, 1.27), (6.0, 7.0), "matte_black"),
             ("24-bit ADC (TSSOP-16)", wp.ic(5.0, 4.4, 1.0, 8, 0.6), (6.0, -7.0), "matte_black"),
             ("Lamp switch MOSFET 1", wp.smd_box(2.9, 1.3, 1.0), (-1.0, 10.5), "matte_black"),
             ("Lamp switch MOSFET 2", wp.smd_box(2.9, 1.3, 1.0), (-1.0, -10.5), "matte_black"),
             ("Wire header, 6 pins", wp.header(6, body_h=2.5, pin_up=3.0), (-12.0, 0.0), "matte_black")]
    out += _board(P, lead_holes, parts, False, None, "Filter driver and ADC board (perfboard)")
    out += _afe_screws(P, False)
    cps = cap_parts(P, at=(-20.0, -85.0, -P["shroud_h"]))
    out.append(cp.part("Calibration cap (black PETG)", cps["cal_cap"], "matte_black", group="accessory"))
    out.append(cp.part("White PTFE reference disc", wp.eased(cps["ptfe_disc"], 0.3), "hdpe_natural", kind="bought", group="accessory", color="#F9FAFB"))
    return out


def _hand():
    """A relaxed right hand and forearm lying beside the scanner on the item surface, for scale only."""
    cp, _ = _parts_lib()
    import context_parts
    from build123d import Pos, Rot
    h = context_parts.forearm_hand("right", "flat")
    return cp.part("Hand (scale)", Pos(-30.0, 105.0, -PARAMS["shroud_h"] + 43.8) * Rot(0, 0, 180) * h, "skin", kind="context", group="context")


def components(option=CHOSEN):
    """cad_parts.part() dicts for one concept option, in assembled position (D3, STANDARDS section 24)."""
    if option == "A":
        parts = _option_a(bom=True)
    elif option == "B":
        parts = _option_b()
    else:
        raise KeyError(option)
    try:
        parts.append(_hand())
    except Exception as e:   # scale context only; never block the model
        print("hand not added:", e)
    return parts


# ------------------------------------------------------------------ constructability checks
TOUCH = [  # (a, b, why): these must touch (distance under 0.02 mm)
    ("bottom_shell", "gasket", "gasket lies on the bottom shell rim"),
    ("gasket", "top_shell", "top shell rim squeezes the gasket"),
    ("bottom_shell", "top_shell", "top shell bosses bottom out on the bottom shell bosses (gasket stop)"),
    ("bottom_shell", "shell_screws", "shell screw heads seat in the counterbores"),
    ("bottom_shell", "led_holder", "optical head block sits on the floor"),
    ("led_holder", "window", "baffle tube rests on the window"),
    ("shroud", "window", "shroud flange lip holds the window from below"),
    ("shroud", "bottom_shell", "shroud flange sits flat on the underside"),
    ("shroud", "head_screws", "washers under the shroud flange"),
    ("led_holder", "photodiode", "photodiode can sits on the step in the bore"),
    ("led_holder", "afe_board", "amplifier board sits on the head block"),
    ("afe_board", "afe_screws", "board screws clamp the amplifier board"),
    ("bottom_shell", "cell_contacts", "contacts in the cradle end walls"),
    ("cell", "cell_contacts", "cell between its contacts"),
    ("cell", "cell_strap", "strap holds the cell down"),
    ("bottom_shell", "cell_strap", "strap legs stand on their bosses"),
    ("cell_strap", "strap_screws", "strap screws clamp the strap"),
    ("bottom_shell", "usb_board", "USB-C board on its seat"),
    ("bottom_shell", "switch", "switch plate against the side wall"),
    ("switch", "switch_screws", "switch screws and nuts"),
    ("display_board", "display_frame", "board rests on the frame lips"),
    ("display_frame", "top_shell", "frame against the ceiling and its bosses"),
    ("display_frame", "frame_screws", "frame screws under the ears"),
    ("top_shell", "button", "button bezel on the top shell, nut under the ceiling"),
    ("top_shell", "sun_hood", "hood plate on the top shell"),
]
APART = [  # (a, b, min gap mm, why)
    ("cell", "display_board", 0.3, "cell clear of the display board"),
    ("cell", "bottom_shell", 0.1, "cell clear of the cradle bore"),
    ("leds", "window", 0.05, "LED cans clear of the glass"),
    ("display_board", "top_shell", 0.2, "display glass clear of the ceiling (foam tape fills it)"),
    ("led_holder", "button", 5.0, "button clear of the optics"),
    ("cell_strap", "top_shell", 0.1, "strap clear of the ceiling"),
    ("cell_strap", "display_frame", 5.0, "strap clear of the display frame"),
    ("afe_board", "button", 5.0, "button terminals clear of the amplifier board"),
]


def check(P=PARAMS, verbose=True):
    """Constructability checks: no two components overlap, required contacts exist, clearances hold."""
    C = build_components(P)
    ks = list(C)
    fails, n = [], 0
    for i, a in enumerate(ks):
        for b in ks[i + 1:]:
            n += 1
            try:
                v = (C[a] & C[b]).volume
            except Exception:
                v = 0.0
            if v > 0.05:
                fails.append(f"overlap {a} / {b}: {v:.2f} mm3")
    for a, b, why in TOUCH:
        n += 1
        d = C[a].distance_to(C[b])
        if d > 0.02:
            fails.append(f"no contact {a} / {b} ({why}): gap {d:.2f} mm")
    for a, b, g, why in APART:
        n += 1
        d = C[a].distance_to(C[b])
        if d < g:
            fails.append(f"too close {a} / {b} ({why}): {d:.2f} mm, need {g} mm")
    # the cap: the shroud rim rests on the PTFE disc and the cap mouth stays below the body
    cp = cap_on_shroud(P)
    n += 3
    if C["shroud"].distance_to(cp["ptfe_disc"]) > 0.02:
        fails.append("shroud rim does not reach the PTFE disc")
    top_cap = cp["cal_cap"].bounding_box().max.Z
    if top_cap > -P["flange_t"] - 0.5:
        fails.append(f"cap mouth at z {top_cap:.1f} hits the shroud flange")
    if (cp["cal_cap"].bounding_box().max.X - cp["cal_cap"].bounding_box().min.X) - 2 * P["cap_wall"] > P["shroud_rim_d"]:
        fails.append("cap bore larger than the shroud rim: no grip")
    # shell wall: at least four 0.4 mm perimeters, and the 1.2 mm tongue must sit inside it with room for the top shell wall
    n += 2
    if P["wall"] < 1.6:
        fails.append(f"shell wall {P['wall']} mm is under 1.6 mm (four perimeters)")
    if P["tongue_t"] > P["wall"] - 0.6:
        fails.append("locating tongue too thick for the shell wall")
    if verbose:
        print(f"{n} constructability checks, {len(fails)} failed")
        for f in fails:
            print("  FAIL", f)
    return n, fails


if __name__ == "__main__":
    if "--check" in sys.argv:
        n, f = check()
        sys.exit(1 if f else 0)
    from build123d import export_step, export_stl
    out = Path(__file__).resolve().parents[1]
    (out / "step").mkdir(exist_ok=True); (out / "stl").mkdir(exist_ok=True)
    ps = parts()
    cp = cap_parts()
    export_step(assembly(), str(out / "step" / "wastewise-scan-assembly.step"))
    for name in ("top_shell", "bottom_shell", "shroud", "led_holder", "sun_hood", "display_frame", "cell_strap"):
        export_step(ps[name], str(out / "step" / f"wastewise-scan-{name.replace('_', '-')}.step"))
        export_stl(ps[name], str(out / "stl" / f"wastewise-scan-{name.replace('_', '-')}.stl"), tolerance=0.15, angular_tolerance=0.3)
    export_step(cp["cal_cap"], str(out / "step" / "wastewise-scan-cal-cap.step"))
    export_stl(cp["cal_cap"], str(out / "stl" / "wastewise-scan-cal-cap.stl"), tolerance=0.15, angular_tolerance=0.3)
    D = derived()
    bb = scanner().bounding_box()
    print(f"scanner envelope {bb.size.X:.1f} x {bb.size.Y:.1f} x {bb.size.Z:.1f} mm; "
          f"detector to item {D['d_pd_item']:.1f} mm; LED tilt {D['led_tilt_deg']:.1f} deg")
    for k, v in {**ps, **cp}.items():
        print(f"  {k:16s} volume {v.volume / 1000:7.2f} cm3")

"""WasteWise Scan parametric model (build123d), TRL 3.

Run from the repo root:  python cad/src/model.py
Exports STEP and STL into cad/step and cad/stl. Massing-plus detail: correct interfaces
and main dimensions, not fabrication detail. PRELIMINARY, NOT FOR FABRICATION.

Axes: X along the body (scan head at +X), Y across the body, Z up. The underside of the
bottom shell is Z = 0. The shroud rim rests on the item being scanned at Z = -shroud_h.

The calculation note WSC-CAL-001 (docs/04-calcs/sizing.py) imports PARAMS, derived() and
the part solids from this file, so the numbers there follow any change made here.
"""
from math import atan2, degrees
from pathlib import Path

# Top-level parameters (mm). Edit these, not the geometry below.
PARAMS = {
    # body
    "body_l": 160.0,          # body length
    "body_w": 62.0,           # body width
    "z_split": 16.0,          # shell split line
    "body_h": 34.0,           # top of body
    "wall": 2.5,              # shell wall and floor thickness
    "corner_r": 10.0,         # plan corner radius
    # scan head (optical axis)
    "head_x": 55.0,           # optical axis position along the body
    "window_d": 25.0,         # borosilicate window diameter
    "window_t": 2.0,          # window thickness
    "shroud_h": 18.0,         # shroud depth below the body
    "shroud_rim_d": 42.0,     # outer diameter at the rim (item side)
    "shroud_top_d": 30.0,     # outer diameter at the body
    "shroud_wall": 3.0,
    # optics
    "pd_can_d": 5.4,          # photodiode TO-46 can diameter (1 mm active area)
    "pd_can_h": 4.0,
    "pd_z": 4.0,              # underside of the photodiode can (detector plane)
    "baffle_od": 7.0,         # baffle tube around the photodiode, down to the window
    "baffle_id": 5.6,
    "led_n": 8,               # number of LED bands
    "led_can_d": 5.4,         # TO-46 SWIR LED can diameter (some bands are 5 mm T-1 3/4)
    "led_can_h": 5.0,
    "led_ring_r": 10.0,       # LED pitch circle radius
    "led_z": 5.5,             # LED can center height
    "holder_od": 28.0,        # printed LED holder ring
    "holder_id": 7.4,
    "holder_h": 6.0,
    "afe_w": 28.0,            # amplifier and ADC board, square
    "afe_t": 1.6,
    "afe_z": 10.5,            # board center height
    # electronics and power
    "board_l": 62.0,          # ESP32-S3 display board (T-Display-S3 class), assumed envelope
    "board_w": 26.0,
    "board_h": 9.5,
    "board_x": -10.0,
    "board_z": 26.5,
    "disp_win_l": 46.0,       # display window in the top shell
    "disp_win_w": 24.0,
    "cell_d": 18.5,           # 18650 cell
    "cell_l": 65.0,
    "cell_x": -30.0,
    "cell_z": 12.0,
    "usb_x": -76.0,           # USB-C socket block at the tail wall
    "button_x": 35.0,
    "button_d": 16.0,         # sealed 16 mm push button (bezel)
    "button_h": 4.0,
    # calibration cap (stored on the shroud)
    "cap_od": 48.0,
    "cap_h": 24.0,
    "cap_wall": 2.0,
    "ptfe_d": 38.0,
    "ptfe_t": 3.0,
}


def derived(P=PARAMS):
    """Numbers the calculation note and the drawing use."""
    z_item = -P["shroud_h"]
    d_pd = P["pd_z"] - z_item                          # detector plane to item
    tilt = degrees(atan2(P["led_ring_r"], P["led_z"] - z_item))   # LED axis tilt from vertical
    rim_id = P["shroud_rim_d"] - 2 * P["shroud_wall"]
    return {
        "z_item": z_item,
        "d_pd_item": d_pd,
        "d_led_item": ((P["led_z"] - z_item) ** 2 + P["led_ring_r"] ** 2) ** 0.5,
        "led_tilt_deg": tilt,
        "rim_id": rim_id,
        "overall_h": P["body_h"] + P["button_h"] / 2 + P["shroud_h"],
    }


def _shell(P, z0, z1, open_top):
    from build123d import Box, Pos, Axis, fillet
    L, W, t = P["body_l"], P["body_w"], P["wall"]
    h = z1 - z0
    outer = Pos(0, 0, z0 + h / 2) * Box(L, W, h)
    outer = fillet(outer.edges().filter_by(Axis.Z), P["corner_r"])
    zin = z0 + h / 2 + (t / 2 if open_top else -t / 2)
    inner = Pos(0, 0, zin) * Box(L - 2 * t, W - 2 * t, h - t + 0.01)
    inner = fillet(inner.edges().filter_by(Axis.Z), P["corner_r"] - t)
    return outer - inner


def parts(P=PARAMS):
    """Return {name: solid} for every modeled part, in assembled position."""
    from build123d import Box, Cylinder, Cone, Pos, Rot
    D = derived(P)
    hx = P["head_x"]
    out = {}
    bottom = _shell(P, 0.0, P["z_split"], open_top=True)
    bottom -= Pos(hx, 0, P["wall"] / 2) * Cylinder(P["window_d"] / 2 - 1.5, P["wall"] + 1)   # optical aperture
    bottom -= Pos(hx, 0, P["window_t"] / 2 + 0.5) * Cylinder(P["window_d"] / 2 + 0.2, P["window_t"] + 1)  # window seat
    bottom -= Pos(-P["body_l"] / 2 + P["wall"] / 2, 0, 8.0) * Box(P["wall"] + 1, 9.5, 3.8)  # USB-C opening
    out["bottom_shell"] = bottom
    top = _shell(P, P["z_split"], P["body_h"], open_top=False)
    top -= Pos(P["board_x"], 0, P["body_h"] - 1) * Box(P["disp_win_l"], P["disp_win_w"], 4.0)
    top -= Pos(P["button_x"], 0, P["body_h"] - 1) * Cylinder(6.5, 4.0)
    out["top_shell"] = top
    out["display_board"] = Pos(P["board_x"], 0, P["board_z"]) * Box(P["board_l"], P["board_w"], P["board_h"])
    out["cell"] = Pos(P["cell_x"], 0, P["cell_z"]) * Rot(0, 90, 0) * Cylinder(P["cell_d"] / 2, P["cell_l"])
    cradle = Pos(P["cell_x"], 0, P["wall"] + 4.0) * Box(P["cell_l"] + 12, P["cell_d"] + 3, 8.0)
    cradle -= Pos(P["cell_x"], 0, P["cell_z"]) * Rot(0, 90, 0) * Cylinder(P["cell_d"] / 2 + 0.3, P["cell_l"] + 20)
    usb = Pos(P["usb_x"], 0, 8.0) * Box(8.0, 9.0, 3.2)
    out["cell_holder_usb"] = cradle + usb
    out["window"] = Pos(hx, 0, P["window_t"] / 2) * Cylinder(P["window_d"] / 2, P["window_t"])
    ro, rt, sh, sw = P["shroud_rim_d"] / 2, P["shroud_top_d"] / 2, P["shroud_h"], P["shroud_wall"]
    out["shroud"] = Pos(hx, 0, -sh / 2) * (Cone(ro, rt, sh) - Cone(ro - sw, rt - sw, sh + 0.02))
    holder_z = P["led_z"]
    holder = Pos(hx, 0, holder_z) * (Cylinder(P["holder_od"] / 2, P["holder_h"]) - Cylinder(P["holder_id"] / 2, P["holder_h"] + 1))
    leds = None
    for k in range(P["led_n"]):
        a = 360.0 * k / P["led_n"] + 22.5
        led = Rot(0, 0, a) * Pos(P["led_ring_r"], 0, 0) * Rot(0, D["led_tilt_deg"], 0) * Cylinder(P["led_can_d"] / 2, P["led_can_h"])
        led = Pos(hx, 0, P["led_z"]) * led
        holder -= led
        leds = led if leds is None else leds + led
    out["led_holder"] = holder
    out["leds"] = leds
    pd = Pos(hx, 0, P["pd_z"] + P["pd_can_h"] / 2) * Cylinder(P["pd_can_d"] / 2, P["pd_can_h"])
    baffle_h = P["pd_z"] - P["window_t"]
    baffle = Pos(hx, 0, P["window_t"] + baffle_h / 2) * (Cylinder(P["baffle_od"] / 2, baffle_h) - Cylinder(P["baffle_id"] / 2, baffle_h + 1))
    out["photodiode"] = pd + baffle
    out["afe_board"] = Pos(hx, 0, P["afe_z"]) * Box(P["afe_w"], P["afe_w"], P["afe_t"])
    out["button"] = Pos(P["button_x"], 0, P["body_h"] + P["button_h"] / 2 - 1.0) * Cylinder(P["button_d"] / 2, P["button_h"]) \
        + Pos(P["button_x"], 0, P["body_h"] - 4.0) * Cylinder(6.0, 6.0)
    return out


def cap_parts(P=PARAMS, at=(0.0, 0.0, 0.0)):
    """Calibration cap and PTFE disc, open side up, base at `at`."""
    from build123d import Cylinder, Pos
    x, y, z = at
    r, h, t = P["cap_od"] / 2, P["cap_h"], P["cap_wall"]
    cap = Pos(x, y, z + h / 2) * (Cylinder(r, h) - Pos(0, 0, t) * Cylinder(r - t, h))
    disc = Pos(x, y, z + t + P["ptfe_t"] / 2) * Cylinder(P["ptfe_d"] / 2, P["ptfe_t"])
    return {"cal_cap": cap, "ptfe_disc": disc}


def scanner(P=PARAMS):
    from build123d import Compound
    return Compound(children=list(parts(P).values()))


def assembly(P=PARAMS):
    from build123d import Compound
    return Compound(children=list(parts(P).values()) + list(cap_parts(P, at=(-20.0, -85.0, -P["shroud_h"])).values()))


if __name__ == "__main__":
    from build123d import export_step, export_stl
    out = Path(__file__).resolve().parents[1]
    (out / "step").mkdir(exist_ok=True); (out / "stl").mkdir(exist_ok=True)
    ps = parts()
    cp = cap_parts()
    export_step(assembly(), str(out / "step" / "wastewise-scan-assembly.step"))
    for name in ("top_shell", "bottom_shell", "shroud", "led_holder"):
        export_step(ps[name], str(out / "step" / f"wastewise-scan-{name.replace('_', '-')}.step"))
        export_stl(ps[name], str(out / "stl" / f"wastewise-scan-{name.replace('_', '-')}.stl"))
    export_step(cp["cal_cap"], str(out / "step" / "wastewise-scan-cal-cap.step"))
    export_stl(cp["cal_cap"], str(out / "stl" / "wastewise-scan-cal-cap.stl"))
    D = derived()
    bb = scanner().bounding_box()
    print(f"scanner envelope {bb.size.X:.1f} x {bb.size.Y:.1f} x {bb.size.Z:.1f} mm; "
          f"detector to item {D['d_pd_item']:.1f} mm; LED tilt {D['led_tilt_deg']:.1f} deg")
    for k, v in {**ps, **cp}.items():
        print(f"  {k:16s} volume {v.volume / 1000:7.2f} cm3")

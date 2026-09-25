"""WasteWise Scan general arrangement sheet WSC-DWG-001, Rev P1 (TRL 3).

Run from the repo root:  python cad/src/sheets.py
Writes cad/drawings/WSC-DWG-001.svg, .pdf and .png from the parametric model in
cad/src/model.py with .kit/drawing.py. Dimensions are taken from PARAMS and derived(), so
they follow any parameter change. The concept sheet in media/ is WSC-DWG-010.
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
from drawing import Sheet, _viewbox, _t, INK, MUTED  # noqa: E402
from model import PARAMS as P, derived, scanner, parts  # noqa: E402

DATE = "2026-09-25"


def views_of(part, workdir, hidden=("front", "top", "right")):
    """drawing.project_views, edge by edge, skipping degenerate edges."""
    from build123d import ExportSVG, LineType, Unit
    workdir = Path(workdir); workdir.mkdir(parents=True, exist_ok=True)
    bb = part.bounding_box()
    c = bb.center(); d = max(bb.size.X, bb.size.Y, bb.size.Z) * 10
    setups = {"front": ((c.X, c.Y - d, c.Z), (0, 0, 1)), "top": ((c.X, c.Y, c.Z + d), (0, 1, 0)),
              "right": ((c.X + d, c.Y, c.Z), (0, 0, 1)), "iso": ((c.X + d, c.Y - d, c.Z + d * 0.8), (0, 0, 1))}
    out = {}
    for name, (origin, up) in setups.items():
        visible, hid = part.project_to_viewport(origin, up, (c.X, c.Y, c.Z))
        ex = ExportSVG(unit=Unit.MM, line_weight=0.35)
        ex.add_layer("Visible", line_color=0x111827)
        ex.add_layer("Hidden", line_color=0x6B7280, line_type=LineType.ISO_DASH, line_weight=0.18)
        for layer, edges in (("Visible", visible), ("Hidden", hid if name in hidden else [])):
            for e in edges:
                try:
                    ex.add_shape(e, layer=layer)
                except (AssertionError, ValueError, ZeroDivisionError):
                    pass
        p = workdir / f"{name}.svg"
        ex.write(str(p))
        out[name] = p
    return out


def dim_h(x1, x2, y, text, above=True):
    a = 1.4
    ty = y - 1.0 if above else y + 3.2
    return [f'<line x1="{x1:.2f}" y1="{y:.2f}" x2="{x2:.2f}" y2="{y:.2f}" stroke="{INK}" stroke-width="0.18"/>',
            f'<path d="M{x1:.2f} {y:.2f} l{a} -0.5 l0 1 Z" fill="{INK}"/>',
            f'<path d="M{x2:.2f} {y:.2f} l{-a} -0.5 l0 1 Z" fill="{INK}"/>',
            _t((x1 + x2) / 2, ty, text, 2.3, 400, INK, "middle", mono=True)]


def dim_v(x, y1, y2, text, left=True):
    a = 1.4
    cx, cy = (x - 1.0 if left else x + 3.0), (y1 + y2) / 2
    return [f'<line x1="{x:.2f}" y1="{y1:.2f}" x2="{x:.2f}" y2="{y2:.2f}" stroke="{INK}" stroke-width="0.18"/>',
            f'<path d="M{x:.2f} {y1:.2f} l-0.5 {a} l1 0 Z" fill="{INK}"/>',
            f'<path d="M{x:.2f} {y2:.2f} l-0.5 {-a} l1 0 Z" fill="{INK}"/>',
            f'<g transform="rotate(-90 {cx:.2f} {cy:.2f})">{_t(cx, cy, text, 2.3, 400, INK, "middle", mono=True)}</g>']


def ext(x1, y1, x2, y2):
    return f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{MUTED}" stroke-width="0.13"/>'


def main():
    from build123d import Box, Compound, Pos
    D = derived(P)
    part = scanner(P)
    bb = part.bounding_box()
    work = ROOT / "cad" / "drawings" / "_views"
    views = views_of(part, work)
    hx = P["head_x"]
    slab = Pos(hx - 1.0, 0, 0) * Box(2.0, 200, 200)          # thin slice ending on the optical axis (section A-A)
    cuts = [c & slab for c in parts(P).values()]
    sec = Compound(children=[c for c in cuts if c is not None and c._wrapped is not None and c.volume > 1e-6])
    sviews = views_of(sec, work / "sec", hidden=())
    sbb = sec.bounding_box()

    s = Sheet(project="WasteWise Scan", title="General arrangement, handheld resin scanner", dwg_no="WSC-DWG-001", rev="P1",
              author="Amish Chadha", date=DATE, scale=1.0, theme="technical",
              material="PETG shells, TPU shroud, borosilicate window; bought parts per bom/bom.csv. PRELIMINARY, NOT FOR FABRICATION",
              revisions=[("P1", "Preliminary GA for TRL 3 (from cad/src/model.py)", DATE, "AC")])
    s._layers.append(_t(16, 29, "PRELIMINARY, NOT FOR FABRICATION", 3.2, 600, "#B45309"))
    k = 1.0
    L = []

    # top view at 1:1 (from +Z): X to the right, Y up the sheet
    tx, ty = 40.0, 48.0
    s.add_svg(views["top"], tx, ty, scale=k, label="Top view", sublabel="Scale 1:1")
    Xt = lambda mx: tx + (mx - bb.min.X) * k
    Yt = lambda my: ty + (bb.max.Y - my) * k
    L += [ext(Xt(bb.min.X), Yt(bb.max.Y) - 1, Xt(bb.min.X), Yt(bb.max.Y) - 10),
          ext(Xt(bb.max.X), Yt(bb.max.Y) - 1, Xt(bb.max.X), Yt(bb.max.Y) - 10)]
    L += dim_h(Xt(bb.min.X), Xt(bb.max.X), Yt(bb.max.Y) - 9, f"{P['body_l']:.0f} body")
    L += [ext(Xt(bb.min.X) - 1, Yt(bb.max.Y), Xt(bb.min.X) - 10, Yt(bb.max.Y)),
          ext(Xt(bb.min.X) - 1, Yt(bb.min.Y), Xt(bb.min.X) - 10, Yt(bb.min.Y))]
    L += dim_v(Xt(bb.min.X) - 8, Yt(bb.max.Y), Yt(bb.min.Y), f"{P['body_w']:.0f}")
    L += [ext(Xt(bb.min.X), Yt(bb.max.Y) - 1, Xt(bb.min.X), Yt(bb.max.Y) - 4), ext(Xt(hx), Yt(bb.max.Y) - 1, Xt(hx), Yt(bb.max.Y) - 4)]
    L += dim_h(Xt(bb.min.X), Xt(hx), Yt(bb.max.Y) - 3, f"{hx - bb.min.X:.0f} to optical axis")
    L.append(f'<line x1="{Xt(hx):.2f}" y1="{Yt(bb.max.Y) - 5:.2f}" x2="{Xt(hx):.2f}" y2="{Yt(bb.min.Y) + 5:.2f}" stroke="{INK}" '
             f'stroke-width="0.18" stroke-dasharray="4 1 0.8 1"/>')
    L += [_t(Xt(hx) + 1.5, Yt(bb.min.Y) + 5, "A", 3.2, 600, INK)]

    # front view at 1:1 (from -Y): X to the right, Z up
    fvw, fvh = _viewbox(Path(views["front"]).read_text())[2:]
    fx, fy = tx, ty + P["body_w"] + 30
    s.add_svg(views["front"], fx, fy, scale=k, label="Front view", sublabel="Scale 1:1")
    X = lambda mx: fx + (mx - bb.min.X) * k
    Z = lambda mz: fy + (bb.max.Z - mz) * k
    L += [ext(X(bb.max.X) + 1, Z(P["body_h"]), X(bb.max.X) + 10, Z(P["body_h"])),
          ext(X(bb.max.X) + 1, Z(0), X(bb.max.X) + 10, Z(0)),
          ext(X(hx + P["shroud_rim_d"] / 2) + 1, Z(D["z_item"]), X(bb.max.X) + 18, Z(D["z_item"]))]
    L += dim_v(X(bb.max.X) + 8, Z(P["body_h"]), Z(0), f"{P['body_h']:.0f}", left=False)
    L += dim_v(X(bb.max.X) + 16, Z(0), Z(D["z_item"]), f"{P['shroud_h']:.0f}", left=False)
    L += [ext(X(hx - P["shroud_rim_d"] / 2), Z(D["z_item"]) + 1, X(hx - P["shroud_rim_d"] / 2), Z(D["z_item"]) + 8),
          ext(X(hx + P["shroud_rim_d"] / 2), Z(D["z_item"]) + 1, X(hx + P["shroud_rim_d"] / 2), Z(D["z_item"]) + 8)]
    L += dim_h(X(hx - P["shroud_rim_d"] / 2), X(hx + P["shroud_rim_d"] / 2), Z(D["z_item"]) + 7, f"{P['shroud_rim_d']:.0f} rim dia", above=False)
    L.append(_t(X(bb.min.X), Z(D["z_item"]) + 1.5, "Item surface (shroud rim)", 2.2, 400, MUTED))

    # section A-A at 2:1 through the optical axis, looking from +X toward the tail
    ks = 2.0
    sx, sy = 212.0, 36.0
    s.add_svg(sviews["right"], sx, sy, scale=ks)
    vw, vh = [v * ks for v in _viewbox(Path(sviews["right"]).read_text())[2:]]
    Yr = lambda my: sx + (my - sbb.min.Y) * ks
    Zr = lambda mz: sy + (sbb.max.Z - mz) * ks
    L.append(_t(sx + vw / 2, sy + vh + 14, "SECTION A-A", 2.8, 600, INK, "middle"))
    L.append(_t(sx + vw / 2, sy + vh + 18, "Scale 2:1; on the optical axis, looking toward the tail", 2.2, 400, MUTED, "middle"))
    L.append(f'<line x1="{Yr(0):.2f}" y1="{Zr(P["body_h"]) - 3:.2f}" x2="{Yr(0):.2f}" y2="{Zr(D["z_item"]) + 3:.2f}" '
             f'stroke="{INK}" stroke-width="0.18" stroke-dasharray="4 1 0.8 1"/>')
    rw = P["window_d"] / 2
    L += [ext(Yr(-rw), Zr(0), Yr(-rw), Zr(D["z_item"]) + 6), ext(Yr(rw), Zr(0), Yr(rw), Zr(D["z_item"]) + 6)]
    L += dim_h(Yr(-rw), Yr(rw), Zr(D["z_item"]) + 5, f"{P['window_d']:.0f} window", above=False)
    L += [ext(Yr(sbb.min.Y) - 1, Zr(P["pd_z"]), Yr(sbb.min.Y) - 12, Zr(P["pd_z"])),
          ext(Yr(-D["rim_id"] / 2) - 1, Zr(D["z_item"]), Yr(sbb.min.Y) - 12, Zr(D["z_item"]))]
    L += dim_v(Yr(sbb.min.Y) - 10, Zr(P["pd_z"]), Zr(D["z_item"]), f"{D['d_pd_item']:.0f} detector to item")
    tags = [((0.0, P["afe_z"]), f"Amplifier and ADC board {P['afe_w']:.0f} x {P['afe_w']:.0f}"),
            ((0.0, P["pd_z"] + 2), f"InGaAs photodiode, TO-46, {P['pd_z']:.0f} above base"),
            ((P["led_ring_r"] * 0.7, P["led_z"]), f"8 LEDs on {2 * P['led_ring_r']:.0f} PCD, tilted {D['led_tilt_deg']:.0f} deg"),
            ((-3.2, 3.0), "Baffle tube 7 OD down to the window"),
            ((-(rw - 2), 1.0), f"Window {P['window_d']:.0f} x {P['window_t']:.0f} borosilicate"),
            ((-(P['shroud_rim_d'] / 2 - 2), D["z_item"] + 3), f"TPU shroud, {D['rim_id']:.0f} ID at the rim")]
    lx = sx + vw + 6
    for i, ((uy, wz), text) in enumerate(tags):
        tyy = sy + 6 + i * (vh - 10) / (len(tags) - 1)
        L.append(f'<line x1="{Yr(uy):.2f}" y1="{Zr(wz):.2f}" x2="{lx - 1:.2f}" y2="{tyy - 0.8:.2f}" stroke="{MUTED}" stroke-width="0.15"/>')
        L.append(f'<circle cx="{Yr(uy):.2f}" cy="{Zr(wz):.2f}" r="0.5" fill="{INK}"/>')
        L.append(_t(lx, tyy, text, 2.2, 400, INK))

    s._layers += L
    s.add_svg(views["iso"], 30, 214, 180, 42, label="Isometric view", sublabel="Not to scale")
    s.add_notes("Main dimensions and interfaces (mm)", [
        f"Body {P['body_l']:.0f} x {P['body_w']:.0f} x {P['body_h']:.0f}, shell split at {P['z_split']:.0f}; {bb.size.Z:.0f} high with button and shroud",
        f"Shroud {P['shroud_h']:.0f} deep, {P['shroud_rim_d']:.0f} dia at the rim; sets detector to item {D['d_pd_item']:.0f}",
        f"Display window {P['disp_win_l']:.0f} x {P['disp_win_w']:.0f} over a T-Display-S3 class board (envelope assumed)",
        f"18650 cell on the body axis, {P['cell_z']:.0f} above base; USB-C in the tail wall",
        f"Scan button {P['button_d']:.0f} dia, {P['button_x'] - P['board_x']:.0f} ahead of the display center",
        f"Cal. cap {P['cap_od']:.0f} OD x {P['cap_h']:.0f}, PTFE disc {P['ptfe_d']:.0f} x {P['ptfe_t']:.0f}; stores over the shroud",
        "Mass about 202 g, 222 g with cap (WSC-CAL-001 A3)",
        "Third-angle; X along the body, Z up; base of body Z = 0",
    ], x=226.8, y=166, width=190)
    out = s.save(ROOT / "cad" / "drawings" / "WSC-DWG-001")
    shutil.rmtree(work, ignore_errors=True)
    print(f"wrote {out} and .pdf, .png")


if __name__ == "__main__":
    main()

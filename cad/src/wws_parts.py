"""WasteWise Scan repo-specific parts for the kit 1.9 model (STANDARDS section 24). Nothing here is in .kit/.

`.kit/cad_parts.py` covers structural stock and ISO fasteners from M5 up. A handheld needs the small end:
ISO 7045 pan head screws from M2 to M3, ISO 4032 nuts and ISO 7089 washers at M2 and M3, brass heat-set
inserts, and the bought electronics (TO-46 and TO-5 cans, an 18650 cell, PCBs with their parts, a USB-C
receptacle, a miniature lamp). Every function returns a build123d solid in millimetres, built along +Z
from the origin unless its docstring says otherwise. Threads are drawn as plain shanks, as is usual in
assembly CAD. Sizes are the nominal catalogue values; bought envelopes are confirmed when parts are bought
(WSC-DEC-001, "To confirm when parts are bought").
"""
from __future__ import annotations

import math

from build123d import (Box, Cylinder, Pos, Rot, RegularPolygon, Sketch, Circle, RectangleRounded, Torus,
                       extrude, chamfer, fillet, Axis)

# ISO 7045 pan head (cross recess): d -> (head diameter dk, head height k)
PAN = {2.0: (4.0, 1.6), 2.5: (5.0, 1.75), 3.0: (5.6, 2.4)}
# ISO 4032 nut and ISO 7089 washer: d -> (nut across flats s, nut height m, washer outside d2, washer h)
SMALL = {2.0: (4.0, 1.6, 5.0, 0.3), 2.5: (5.0, 2.0, 6.0, 0.5), 3.0: (5.5, 2.4, 7.0, 0.5)}


def _try(op, shape, edges, r):
    try:
        out = op(edges, r)
        ok = out.is_valid() if callable(out.is_valid) else out.is_valid
        return out if ok else shape
    except Exception:
        return shape


def eased(shape, r=0.3):
    """Break every edge of a small part by r mm (fillet, else chamfer), as a moulded or cut part has."""
    out = _try(fillet, shape, shape.edges(), r)
    if out is shape:
        out = _try(chamfer, shape, shape.edges(), r)
    return out


def pan_screw(d, length, head_d=None, head_h=None):
    """ISO 7045 pan head screw, cross recess. Head bearing face on z = 0, head up to +k, shank down to -length."""
    dk, k = PAN[d]
    dk, k = head_d or dk, head_h or k
    head = Pos(0, 0, k / 2) * Cylinder(dk / 2, k)
    head = _try(fillet, head, head.edges().sort_by(Axis.Z)[-1:], k * 0.45)
    for a in (0, 90):
        head -= Pos(0, 0, k) * Rot(0, 0, a) * Box(dk * 0.55, d * 0.22, k * 0.9)
    shank = Pos(0, 0, -length / 2) * Cylinder(d * 0.97 / 2, length)
    shank = _try(chamfer, shank, shank.edges().sort_by(Axis.Z)[:1], d * 0.12)
    return head + shank


def hex_nut_small(d):
    """ISO 4032 hex nut M2 to M3 from z 0 to m, with its bore and a 30 degree chamfer."""
    s, m, _, _ = SMALL[d]
    prism = extrude(RegularPolygon(s / math.sqrt(3), 6), m)
    cap = Pos(0, 0, m / 2) * Cylinder(s / math.sqrt(3), m)
    cap = _try(chamfer, cap, cap.edges(), s / math.sqrt(3) - s / 2 * 0.96)
    return (prism & cap) - Pos(0, 0, m / 2) * Cylinder(d / 2, m + 0.2)


def washer_small(d):
    """ISO 7089 plain washer M2 to M3 from z 0 to h."""
    _, _, d2, h = SMALL[d]
    return extrude(Sketch() + Circle(d2 / 2) - Circle(d * 1.07 / 2), h)


def heat_set_insert(od, length, bore):
    """Brass heat-set insert: knurled sleeve from z 0 up to length (drawn at the hole size), threaded bore."""
    body = extrude(Sketch() + Circle(od / 2) - Circle(bore / 2), length)
    for z in (length * 0.3, length * 0.7):    # the two knurl grooves
        body -= Pos(0, 0, z) * (Cylinder(od / 2 + 0.1, length * 0.12) - Cylinder(od / 2 - 0.25, length * 0.12))
    return body


def to_can(flange_d, body_d, height, flange_t=0.5, window_d=None, leads=3, lead_l=4.0, lead_pcd=2.54):
    """TO-46 or TO-5 style metal can: optical window face on z = 0, can body up to height with the flange at
    the top (lead end), leads continuing up by lead_l on a pitch circle."""
    body = Pos(0, 0, (height - flange_t) / 2) * Cylinder(body_d / 2, height - flange_t)
    body = _try(fillet, body, body.edges().sort_by(Axis.Z)[:1], 0.3)
    fl = Pos(0, 0, height - flange_t / 2) * Cylinder(flange_d / 2, flange_t)
    can = body + fl
    if window_d:
        can -= Pos(0, 0, 0.1) * Cylinder(window_d / 2, 0.4)          # recessed glass window
        can += Pos(0, 0, 0.2) * Cylinder(window_d / 2, 0.2)
    for i in range(leads):
        a = math.radians(90 + i * 360 / leads)
        can += Pos(lead_pcd / 2 * math.cos(a), lead_pcd / 2 * math.sin(a), height + lead_l / 2) * Cylinder(0.225, lead_l)
    return can


def cell_18650(d=18.5, length=69.0, button_d=8.0, button_h=1.0):
    """Protected 18650 Li-ion cell along +X centred on the origin: negative can end at -X, positive button at +X."""
    body_l = length - button_h
    body = Pos(-button_h / 2, 0, 0) * Rot(0, 90, 0) * Cylinder(d / 2, body_l)
    body = _try(fillet, body, body.edges(), 0.8)
    body -= Pos(length / 2 - button_h - 0.6, 0, 0) * Rot(0, 90, 0) * (Cylinder(d / 2 + 0.1, 0.5) - Cylinder(d / 2 - 0.4, 0.5))  # crimp groove
    btn = Pos(length / 2 - button_h / 2, 0, 0) * Rot(0, 90, 0) * Cylinder(button_d / 2, button_h)
    return body + btn


def spring_contact(coil_d=5.0, wire_d=1.0, length=4.0, turns=4):
    """Compressed battery spring along +X from x 0 to length: stacked coils fused into one solid."""
    pitch = (length - wire_d) / (turns - 1)
    out = None
    for i in range(turns):
        t = Pos(wire_d / 2 + i * pitch, 0, 0) * Rot(0, 90, 0) * Torus(coil_d / 2 - wire_d / 2, wire_d * 0.62)
        out = t if out is None else out + t
    return out


def contact_plate(w=12.0, h=12.0, t=1.0, tab_h=4.0):
    """Flat battery contact plate in the YZ plane (thickness along X from 0), with a dimple and a solder tab up."""
    plate = Pos(t / 2, 0, 0) * Box(t, w, h)
    plate += Pos(t / 2, 0, h / 2 + tab_h / 2) * Box(t, 3.0, tab_h)
    plate -= Pos(t / 2, 0, h / 2 + tab_h - 1.5) * Rot(0, 90, 0) * Cylinder(0.6, t + 0.2)
    return eased(plate, 0.2)


def pcb(length, width, t=1.6, holes=(), r=1.0):
    """Printed circuit board in the XY plane from z 0 to t, holes [(x, y, d)] from the board centre."""
    sk = Sketch() + RectangleRounded(length, width, r)
    for x, y, d in holes:
        sk -= Pos(x, y) * Circle(d / 2)
    return extrude(sk, t)


def ic(length, width, height, pins_per_side=4, pitch=1.27):
    """Moulded IC package (SOIC or TSSOP) on z = 0 with gull-wing leads on its two long sides."""
    body = eased(Pos(0, 0, height / 2 + 0.1) * Box(length, width, height), 0.15)
    for i in range(pins_per_side):
        x = (i - (pins_per_side - 1) / 2) * pitch
        for s in (1, -1):
            body += Pos(x, s * (width / 2 + 0.35), 0.15) * Box(pitch * 0.35, 0.7, 0.3)
    return body


def usb_c_receptacle(length=7.4, w=8.94, h=3.26):
    """USB-C receptacle shell along +X (mouth at +X), centred on the origin: racetrack shell with its tongue."""
    outer = Rot(0, 90, 0) * extrude(RectangleRounded(h, w, h / 2 - 0.01), length)
    inner = Pos(0.6, 0, 0) * Rot(0, 90, 0) * extrude(RectangleRounded(h - 0.6, w - 0.6, h / 2 - 0.31), length)
    shell = outer - inner + Pos(length / 2 + 0.6, 0, 0) * Box(length - 1.2, w - 2.6, 0.7)
    return Pos(-length / 2, 0, 0) * shell


def mini_lamp(bulb_d=5.0, bulb_l=9.0, lead_l=6.0):
    """T-1 3/4 wire-lead tungsten lamp along +Z: glass bulb with a domed end at z 0, leads up from the pinch."""
    bulb = Pos(0, 0, bulb_l / 2) * Cylinder(bulb_d / 2, bulb_l)
    bulb = _try(fillet, bulb, bulb.edges().sort_by(Axis.Z)[:1], bulb_d * 0.45)
    bulb = _try(chamfer, bulb, bulb.edges().sort_by(Axis.Z)[-1:], 0.6)
    for s in (1, -1):
        bulb += Pos(s * 1.0, 0, bulb_l + lead_l / 2) * Cylinder(0.25, lead_l)
    return bulb


def smd_box(length, width, height, r=0.15):
    """Small SMD part (MOSFET, regulator, inductor) on z = 0 with eased edges."""
    return eased(Pos(0, 0, height / 2) * Box(length, width, height), min(r, height / 3))


def header(n, pitch=2.54, body_h=2.5, pin_up=3.0):
    """Single-row pin header along Y on z = 0: plastic strip and square pins."""
    body = eased(Pos(0, 0, body_h / 2) * Box(pitch, n * pitch, body_h), 0.2)
    for i in range(n):
        y = (i - (n - 1) / 2) * pitch
        body += Pos(0, y, body_h + pin_up / 2) * Box(0.64, 0.64, pin_up)
    return body

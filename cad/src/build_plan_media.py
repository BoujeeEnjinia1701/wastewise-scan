"""WasteWise Scan prototype build plan pictures (WSC-BLD-001, STANDARDS section 18).

Run from the repo root:  python cad/src/build_plan_media.py [overview|sheets|joints|steps|wiring ...]
A single picture can be drawn with  python cad/src/build_plan_media.py steps 5  (or joints 3, sheets 104).
With no argument it draws everything. Every picture is drawn from cad/src/model.py
(build_components), so the pictures and the model never disagree:
    docs/05-build-plan/overview.png        every component pulled apart, numbered in build order
    cad/drawings/WSC-DWG-101 to 109        making sketches for the printed and cut components
    docs/05-build-plan/joint-NN.png        close-ups of the joints that need explaining
    docs/05-build-plan/step-NN.png         one picture per assembly step
    docs/05-build-plan/wiring.png          block-level wiring with wire sizes (matplotlib)
Uses .kit/build_views.py. BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import build_views as bv  # noqa: E402
from build_views import Part  # noqa: E402
from model import PARAMS as P, build_components, derived, cap_parts, cap_on_shroud  # noqa: E402

OUT = ROOT / "docs" / "05-build-plan"
DWG = ROOT / "cad" / "drawings"
DATE = "2026-10-02"
D = derived(P)
C = build_components(P)
CAP = cap_on_shroud(P)
HX = P["head_x"]

COL = {"bottom": "#9CA3AF", "top": "#CBD5E1", "head": "#C2410C", "leds": "#7F1D1D", "pd": "#D4A017",
       "afe": "#15803D", "window": "#93C5FD", "shroud": "#1F2937", "contacts": "#A21CAF", "usb": "#1D4ED8",
       "switch": "#F59E0B", "board": "#4338CA", "frame": "#0E7490", "button": "#F59E0B", "cell": "#7C3AED",
       "strap": "#B45309", "gasket": "#16A34A", "screw": "#111827", "hood": "#475569", "cap": "#374151",
       "ptfe": "#E5E7EB", "insert": "#B7791F"}


def _fuse(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


S = lambda *ks: _fuse([C[k] for k in ks])  # noqa: E731


def part(name, shape, color, explode=(0, 0, 0), alpha=1.0):
    return Part(name, shape, color, None, tuple(explode), alpha)


def inserts(which):
    """Brass heat-set inserts (drawn for the pictures; in the model they are the holes in the bosses)."""
    from build123d import Cylinder, Pos
    pts = []
    sx, sy = P["shell_screw_xy"]
    if which == "top":
        pts = [(a * sx, b * sy, P["z_split"] + 0.2) for a in (1, -1) for b in (1, -1)]
        pts += [(fx, s * fy, P["frame_z0"] + 2.6) for fx, fy in P["frame_screws"] for s in (1, -1)]
    elif which == "head":
        pts = [(x, y, D["holder_z0"] + 0.1) for x, y in D["head_screws"]]
    elif which == "strap":
        pts = [(P["strap_x"], s * D["strap_y"], P["wall"] + 0.1) for s in (1, -1)]
    return _fuse([Pos(x, y, z + 2.5) * Cylinder(1.95, 5.0) for x, y, z in pts])


# ----------------------------------------------------------------- named components, in build order
def made():
    return {
        "bottom": part("Bottom shell with cradle", C["bottom_shell"], COL["bottom"]),
        "top": part("Top shell", C["top_shell"], COL["top"]),
        "head": part("Optical head block", C["led_holder"], COL["head"]),
        "leds": part("Eight LEDs", C["leds"], COL["leds"]),
        "pd": part("Photodiode", C["photodiode"], COL["pd"]),
        "afe": part("Amplifier board", S("afe_board", "afe_screws"), COL["afe"]),
        "window": part("Window", C["window"], COL["window"]),
        "shroud": part("Light shroud", C["shroud"], COL["shroud"]),
        "contacts": part("Cell contacts", C["cell_contacts"], COL["contacts"]),
        "usb": part("USB-C board", C["usb_board"], COL["usb"]),
        "switch": part("Slide switch", S("switch", "switch_screws"), COL["switch"]),
        "board": part("Display board", C["display_board"], COL["board"]),
        "frame": part("Display frame", S("display_frame", "frame_screws"), COL["frame"]),
        "button": part("Scan button", C["button"], COL["button"]),
        "cell": part("18650 cell", C["cell"], COL["cell"]),
        "strap": part("Cell strap", S("cell_strap", "strap_screws"), COL["strap"]),
        "gasket": part("Shell gasket", C["gasket"], COL["gasket"]),
        "screws": part("Shell and shroud screws", S("shell_screws", "head_screws"), COL["screw"]),
        "hood": part("Sun hood", C["sun_hood"], COL["hood"]),
        "cap": part("Calibration cap", CAP["cal_cap"], COL["cap"]),
        "ptfe": part("PTFE reference disc", CAP["ptfe_disc"], COL["ptfe"]),
    }


ORDER = ["bottom", "top", "head", "leds", "pd", "afe", "window", "shroud", "contacts", "usb", "switch", "board",
         "frame", "button", "cell", "strap", "gasket", "screws", "hood", "cap", "ptfe"]


# ----------------------------------------------------------------- overview
def overview():
    M = made()
    off = {"bottom": (0, 0, 0), "top": (0, 0, 170), "head": (0, 0, 40), "leds": (0, 0, 62), "pd": (28, 0, 75),
           "afe": (0, 0, 98), "window": (0, 0, -30), "shroud": (0, 0, -62), "contacts": (0, -70, 20),
           "usb": (-30, -70, 0), "switch": (0, -70, -10), "board": (0, 0, 125), "frame": (0, 0, 105),
           "button": (0, 0, 215), "cell": (0, 0, 45), "strap": (0, 0, 75), "gasket": (0, 0, 145),
           "screws": (0, -75, -95), "hood": (0, 0, 240), "cap": (0, 0, -185), "ptfe": (0, 0, -128)}
    parts = []
    for k in ORDER:
        p = M[k]
        p.explode = off[k]
        parts.append(p)
    return bv.overview(parts, OUT / "overview.png", "WasteWise Scan prototype: every component, pulled apart",
                       subtitle="Numbered in build order. Seen from the front right and above; the scan head is at the right",
                       elev=20, azim=-62, size=(11, 9), dpi=150, key=True)


# ----------------------------------------------------------------- making sketches
def sheets(only=None):
    from build123d import Pos, Rot
    M = made()
    base = dict(project="WasteWise Scan", date=DATE)
    out = []

    def want(n):
        return only is None or str(n) in only

    if want(101):
        out.append(bv.component_sheet(
            Part("Bottom shell", C["bottom_shell"], COL["bottom"]), [M["shroud"], M["window"]],
            dwg_no="WSC-DWG-101", title="WasteWise Scan bottom shell: making sketch", material="PETG, 3D printed",
            inset_view=(40, -60),
            notes=["Print open side up, 0.2 mm layers, 6 perimeters (2.5 mm walls), 40 % infill.",
                   "Outside 160 x 62 x 16 mm, 10 mm corner radius; floor and walls 2.5 mm.",
                   "Tongue 1.2 x 2.6 mm stands up inside the rim; it locates the top shell.",
                   "Window hole 25.4 mm on the scan axis, 55 mm ahead of the centre.",
                   "Three 3.4 mm holes round it on a 40 mm circle for the shroud screws.",
                   "Four shell bosses 7 mm at 68 mm each side of centre, 20 mm out:",
                   "  3.4 mm through, 6.2 mm counterbore 3.2 mm deep from below.",
                   "Cell cradle: two 1.5 mm rails and two 3 mm end walls 75 mm apart.",
                   "Two strap bosses beside the cradle take M3 inserts (4 mm hole).",
                   "Tail wall: USB-C opening 9.5 x 3.8 mm, 8 mm up; seat inside for the board.",
                   "Right wall: switch slot 7 x 3.5 mm and two 2.4 mm holes 15 mm apart.",
                   "Check: the top shell drops over the tongue without force."],
            **base))
    if want(102):
        out.append(bv.component_sheet(
            Part("Top shell", C["top_shell"], COL["top"]), [M["bottom"], M["hood"]],
            dwg_no="WSC-DWG-102", title="WasteWise Scan top shell: making sketch", material="PETG, 3D printed",
            view_shape=Pos(0, 0, -D["top_z0"]) * C["top_shell"], inset_view=(28, -60),
            notes=["Print upside down (top face on the bed), same settings as the bottom shell.",
                   "Outside 160 x 62 x 17.4 mm; it sits on the gasket 16.6 mm up the body.",
                   "Display window 46 x 24 mm centred 10 mm behind the body centre.",
                   "Button hole 16.2 mm, 35 mm ahead of the body centre.",
                   "Four shell bosses reach down to meet the bottom shell bosses; they stop",
                   "  the gasket being squeezed below 0.6 mm. Press an M3 insert in each.",
                   "Four frame bosses at 30 mm behind and 10 mm ahead of centre, 19 mm",
                   "  out each side; press an M3 insert in each.",
                   "Two clip ribs 36 x 1 x 1 mm on the outside of the side walls, 28 mm up",
                   "  the body; the sun hood legs snap under them.",
                   "Inserts: soldering iron at about 230 C, push square, flush with the boss.",
                   "Check: each insert is square and flush; the ribs are unbroken."],
            **base))
    if want(103):
        out.append(bv.component_sheet(
            Part("Optical head block", C["led_holder"], COL["head"]), [M["bottom"], M["window"], M["afe"]],
            dwg_no="WSC-DWG-103", title="WasteWise Scan optical head block: making sketch", material="Black PETG, 3D printed",
            view_shape=Pos(-HX, 0, -D["holder_z0"]) * C["led_holder"], inset_view=(55, -60),
            notes=["Print in black PETG, top face on the bed, 0.1 mm layers, 100 % infill.",
                   "Disc 36 mm across, 7.2 mm tall, with three lugs for the shroud screws",
                   "  on a 40 mm circle; press an M3 insert into each lug from below.",
                   "Eight LED pockets 5.6 mm on a 20 mm circle, each tilted 23 degrees",
                   "  inward so the beams meet on the item; leads come out of the top.",
                   "Centre bore 5.6 mm for the photodiode can, with a step 4 mm up the",
                   "  body; below the step a 4 mm aperture and a baffle tube 7 mm across",
                   "  that stands 0.5 mm proud of the underside and rests on the window.",
                   "Two 3.5 mm holes 12 mm each side for M2.5 inserts (amplifier board).",
                   "Ream the LED pockets and the bore with a 5.6 mm drill by hand.",
                   "Check: each LED can slides in and stops square; the bore is black inside."],
            **base))
    if want(104):
        out.append(bv.component_sheet(
            Part("Light shroud", C["shroud"], COL["shroud"]), [M["bottom"], M["window"], M["head"]],
            dwg_no="WSC-DWG-104", title="WasteWise Scan light shroud: making sketch", material="Black TPU 95A, 3D printed",
            view_shape=Pos(-HX, 0, P["shroud_h"]) * C["shroud"], inset_view=(-35, -60),
            notes=["Print in black TPU 95A, flange on the bed, slow (about 20 mm/s).",
                   "Flange 47 mm across and 2.5 mm thick, with a 22 mm hole; the lip of the",
                   "  flange holds the window up into the body.",
                   "Cone 18 mm deep from the body: 30 mm across at the flange, 42 mm at the",
                   "  rim, 3 mm wall; 36 mm inside at the rim.",
                   "Three 3.4 mm holes on a 40 mm circle, at 90, 210 and 330 degrees",
                   "  (the first one toward the left side of the body).",
                   "Fit: three M3 x 10 screws with washers through the flange and the floor",
                   "  into the head block inserts. Snug only: TPU creeps if overtightened.",
                   "The shroud wears; it is replaced with the same three screws.",
                   "Check: the rim sits flat on a sheet of glass with no light under it."],
            **base))
    if want(105):
        out.append(bv.component_sheet(
            Part("Display frame", C["display_frame"], COL["frame"]), [M["top"], M["board"]],
            dwg_no="WSC-DWG-105", title="WasteWise Scan display frame: making sketch", material="PETG, 3D printed",
            view_shape=Pos(-P["board_x"], 0, -P["frame_z0"]) * C["display_frame"], inset_view=(-50, -60),
            notes=["Print with the lips and ears on the bed; the end walls bridge 26 mm.",
                   "Inside 62.4 x 26.4 mm, walls 2 mm, 11.5 mm tall to the shell ceiling.",
                   "Lips 2 mm wide under both long edges of the board, 1.75 mm thick.",
                   "Four ears 7 x 7 x 2.5 mm with 3.4 mm holes, 19 mm each side of the",
                   "  centre line, 30 mm behind and 10 mm ahead of the body centre.",
                   "Stick 0.5 mm foam tape on the lips so the board cannot rattle.",
                   "Fit: the display board drops in face up; the frame then goes into the",
                   "  upturned top shell with four M3 x 8 screws into the frame bosses.",
                   "The screen sits 0.25 mm under the shell ceiling, behind the window.",
                   "Check: the board drops in without force and the screen is centred."],
            **base))
    if want(106):
        out.append(bv.component_sheet(
            Part("Cell strap", C["cell_strap"], COL["strap"]), [M["bottom"], M["cell"]],
            dwg_no="WSC-DWG-106", title="WasteWise Scan cell strap: making sketch", material="PETG, 3D printed, 100 % infill",
            view_shape=Pos(-P["strap_x"], 0, -P["wall"] - 4.0) * C["cell_strap"], inset_view=(40, -60),
            notes=["Print on its side (the 10 mm face on the bed), 100 % infill.",
                   "A bridge 10 mm wide: top bar 33 x 8 mm, two legs 4 mm thick and",
                   "  14.75 mm tall, 29 mm apart between centres.",
                   "3.4 mm hole down through each leg and the bar.",
                   "Fit: the bar lies on top of the cell, 46 mm from the cell's spring end;",
                   "  the legs stand on the two strap bosses beside the cradle.",
                   "Two M3 x 25 low-head screws down through the strap into the inserts.",
                   "It holds the cell down in a drop: about 550 N at 1.3 times margin.",
                   "Check: the cell cannot lift and the screw heads are below 31 mm."],
            **base))
    if want(107):
        out.append(bv.component_sheet(
            Part("Sun hood", C["sun_hood"], COL["hood"]), [M["top"], M["bottom"], M["button"]],
            dwg_no="WSC-DWG-107", title="WasteWise Scan sun hood: making sketch", material="PETG, 3D printed",
            view_shape=Pos(-P["board_x"], 0, -P["body_h"]) * C["sun_hood"], inset_view=(30, -55),
            notes=["Print upside down on the wall tops, with support under the plate.",
                   "Plate 1.5 mm thick with the 46 x 24 mm display opening.",
                   "Walls 20 mm tall and 2 mm thick on both sides and the head end of the",
                   "  opening; the tail end is open toward the user.",
                   "Two clip legs 40 mm long, 2 mm thick, down both sides of the top shell;",
                   "  a lip on each leg snaps under the rib on the shell side.",
                   "Plate 68.4 mm across at the legs; legs 0.2 mm clear of the ribs.",
                   "Fit: press straight down until both lips click under the ribs. To take",
                   "  it off, spread the legs with the thumbs and lift.",
                   "Check: it does not lift when the scanner is shaken face down."],
            **base))
    if want(108):
        out.append(bv.component_sheet(
            Part("Calibration cap", S_cap(), COL["cap"]), [M["shroud"], M["bottom"]],
            dwg_no="WSC-DWG-108", title="WasteWise Scan calibration cap and PTFE disc: making sketch",
            material="Black PETG cap, 3D printed; PTFE sheet 3 mm",
            view_shape=Pos(-HX, 0, P["shroud_h"] + P["ptfe_t"] + 2.0) * S_cap(), inset_view=(20, -60),
            notes=["Cap: print open end up in black PETG, 100 % infill so no light passes.",
                   "46 mm across, 20 mm tall, floor 2 mm, bore 41.6 mm.",
                   "Disc: cut 41 mm from 3 mm white PTFE sheet with a knife and file;",
                   "  sand the top face matte with 400 grit; do not touch it after.",
                   "Press the disc into the cap, sanded face up; a drop of glue at the edge.",
                   "Fit: the cap pushes over the shroud; the bore grips the 42 mm rim and",
                   "  the rim rests on the disc, as it rests on an item when scanning.",
                   "The cap mouth stops 0.5 mm below the shroud flange.",
                   "Check: pushed fully on, the rim touches the disc all round."],
            **base))
    if want(109):
        out.append(bv.component_sheet(
            Part("Amplifier board", C["afe_board"], COL["afe"]), [M["head"], M["leds"], M["pd"]],
            dwg_no="WSC-DWG-109", title="WasteWise Scan amplifier board: making sketch", material="Perfboard, 2.54 mm pitch, 1.6 mm",
            view_shape=Pos(-HX, 0, -D["holder_z1"]) * C["afe_board"], inset_view=(45, -60),
            notes=["Cut 28 x 28 mm of perfboard; file the edges square.",
                   "Drill two 2.8 mm holes 12 mm from the scan axis toward the head end,",
                   "  12 mm each side, for M2.5 x 6 screws into the head block.",
                   "Hold the board on the head block with the LEDs and photodiode in their",
                   "  pockets and mark where every lead comes through; open those holes.",
                   "Build the amplifier, the 24-bit converter and the LED switches on the",
                   "  top face as the wiring picture shows; keep the photodiode input short.",
                   "The LED switches include a hardware limit on how long an LED can stay on.",
                   "Check: every lead passes through without bending the LED or photodiode."],
            **base))
    return out


def S_cap():
    return CAP["cal_cap"] + CAP["ptfe_disc"]


def joint_at(parts, pts, out, title, subtitle, elev, azim, size=(8, 6), dpi=160, cut=None):
    """bv.joint with the leader points given (one 3D point per part, on a face the camera sees)."""
    import numpy as np
    import matplotlib.pyplot as plt
    if cut:
        parts = bv._cut(parts, cut)
    W, H = int(size[0] * dpi), int(size[1] * dpi * bv.PIC_HEIGHT)
    img, proj, verts = bv._raster([(p, p.color, p.alpha, (0, 0, 0)) for p in parts], elev, azim, W, H)
    fig, ax = bv._frame(size, dpi, title, subtitle)
    ax.imshow(img, interpolation="bilinear")
    bv._draw_labels(ax, proj, [np.asarray(q, float) for q in pts], [p.name for p in parts], W, H)
    fig.savefig(out, facecolor="white"); plt.close(fig)
    return out


# ----------------------------------------------------------------- joints
def win(sh, x0, x1, y0, y1, z0, z1):
    from build123d import Box, Pos
    return sh & (Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0))


def joints(only=None):
    out = []

    def want(n):
        return only is None or str(n) in only
    if want(1):   # optical head clamp, cut through the axis
        b = (HX - 24, HX + 21, -14, 0.01, -8, 14)
        out.append(joint_at([
            part("Bottom shell floor", win(C["bottom_shell"], *b), COL["bottom"]),
            part("Optical head block", win(C["led_holder"], *b), COL["head"]),
            part("Photodiode on its step", win(C["photodiode"], *b), COL["pd"]),
            part("Amplifier board", win(C["afe_board"], *b), COL["afe"]),
            part("Window", win(C["window"], *b), COL["window"]),
            part("Shroud flange", win(C["shroud"], *b), COL["shroud"]),
            part("M3 screw and washer into an insert", win(C["head_screws"], *b), "#64748B")],
            [(HX - 21, 0, 1.2), (HX - 14, 0, 6), (HX, 0, 6), (HX + 5, 0, 10.5), (HX + 8, 0, 1.0), (HX - 19, 0, -1.2), (HX - 17.3, -10, -4.5)],
            OUT / "joint-01.png", "Joint 1: the optical head, cut through the scan axis",
            "The window is pinched between the shroud flange lip below and the baffle tube above",
            elev=12, azim=72))
    if want(2):   # shell joint at a screw
        sx, sy = P["shell_screw_xy"]
        b = (sx - 12, sx + 12, sy - 20, sy + 12, -1, 34.5)
        out.append(bv.joint([
            part("Bottom shell, boss and tongue", win(C["bottom_shell"], *b), COL["bottom"]),
            part("Foam gasket", win(C["gasket"], *b), COL["gasket"]),
            part("Top shell and its boss", win(C["top_shell"], *b), COL["top"]),
            part("M3 x 20 screw from below", win(C["shell_screws"], *b), COL["screw"]),
            part("Brass insert", win(inserts("top"), *b), COL["insert"])],
            OUT / "joint-02.png", "Joint 2: the shells meet (head end, left corner, cut open)",
            subtitle="The bosses meet and stop the squeeze; the gasket seals the rim; the tongue locates the halves",
            cut="+X", elev=15, azim=-130, size=(8, 6)))
    if want(3):   # cell in cradle with strap and contacts
        x0 = D["cav_x0"] - 4
        b = (x0, x0 + 30, -20, 20, 2.0, 32)
        out.append(bv.joint([
            part("Bottom shell cradle and boss", win(C["bottom_shell"], *b), COL["bottom"]),
            part("Spring contact", win(C["cell_contacts"], *b), COL["contacts"]),
            part("18650 cell", win(C["cell"], *b), COL["cell"]),
            part("Cell strap", win(C["cell_strap"], *b), COL["strap"]),
            part("M3 x 25 screws", win(C["strap_screws"], *b), COL["screw"])],
            OUT / "joint-03.png", "Joint 3: cell, spring contact and strap (tail end of the cradle, cut open)",
            subtitle="Cut along the cell. The end wall carries the contact; the strap stops the cell lifting in a drop",
            cut="-Y", elev=22, azim=65, size=(8, 6)))
    if want(4):   # display frame ear on its boss, cut
        fx, fy = P["frame_screws"][1]
        b = (fx - 12, fx + 12, -fy - 8, 2, 16.5, 34.2)
        out.append(joint_at([
            part("Top shell, boss and insert", win(C["top_shell"], *b), COL["top"]),
            part("Display frame, lip and ear", win(C["display_frame"], *b), COL["frame"]),
            part("Display board", win(C["display_board"], fx - 3, fx + 12, -fy - 8, 2, 16.5, 34.2), COL["board"]),
            part("M3 x 8 screw", win(C["frame_screws"], *b), COL["screw"])],
            [(fx, -fy + 3.2, 28), (fx, -fy - 2.5, 21), (fx, -6, 27), (fx, -fy, 19)],
            OUT / "joint-04.png", "Joint 4: display board in its frame (cut across the body)",
            "The board rests on the lips; the ear screws up into the boss; the screen sits under the window",
            cut="-X", elev=-12, azim=-35))
    if want(5):   # hood clip
        b = (-14, -6, 20, 36, 24, 42)
        out.append(bv.joint([
            part("Top shell ceiling, side wall and rib", win(C["top_shell"], *b), COL["top"]),
            part("Sun hood plate, clip leg and lip", win(C["sun_hood"], *b), COL["hood"])],
            OUT / "joint-05.png", "Joint 5: sun hood clip leg (left side, cut across)",
            subtitle="The lip on the leg snaps under the 1 mm rib; 0.2 mm clearance all round",
            elev=8, azim=-170, size=(8, 6)))
    if want(6):   # button, as a thin slice through its axis
        bx = P["button_x"]
        sl = lambda sh, z0, z1: win(sh, bx - 14, bx + 14, -3, 0.01, z0, z1)  # noqa: E731
        out.append(joint_at([
            part("Top shell", sl(C["top_shell"], 18, 39), COL["top"]),
            part("Button cap and bezel, seal under it", sl(C["button"], 34.0, 39), COL["button"]),
            part("Threaded body", sl(C["button"], 31.5, 34.0) + sl(C["button"], 18, 28.5), "#92400E"),
            part("Nut, up against the ceiling", sl(C["button"], 28.5, 31.5), "#374151")],
            [(bx - 12, 0, 33), (bx + 2, 0, 37.0), (bx - 4, 0, 24), (bx + 9, 0, 30)],
            OUT / "joint-06.png", "Joint 6: scan button through the top shell (slice through its axis)",
            "Bezel and seal on top; the nut tightens up against the ceiling from inside",
            elev=6, azim=80))
    if want(7):   # cap
        b = (HX - 26, HX + 26, -26, 0.01, -24, 4)
        out.append(joint_at([
            part("Bottom shell", win(C["bottom_shell"], HX - 26, HX + 26, -15, 0.01, -24, 4), "#D1D5DB"),
            part("Shroud", win(C["shroud"], *b), COL["shroud"]),
            part("Window", win(C["window"], *b), COL["window"]),
            part("Calibration cap", win(CAP["cal_cap"], *b), "#B6C0CE"),
            part("PTFE disc", win(CAP["ptfe_disc"], *b), "#F8FAFC")],
            [(HX - 20, 0, 1.2), (HX - 16.2, 0, -8), (HX - 4, 0, 1.0), (HX + 21.9, 0, -11), (HX + 6, 0, -19.6)],
            OUT / "joint-07.png", "Joint 7: calibration cap on the shroud (cut through the scan axis)",
            "The bore grips the rim; the rim rests on the PTFE disc as it rests on an item. The black cap is drawn light here",
            elev=12, azim=72))
    if want(8):   # tail: USB-C and switch
        b = (-81, -38, -34, 8, 1.5, 15)
        out.append(bv.joint([
            part("Bottom shell, board seat", win(C["bottom_shell"], *b), COL["bottom"]),
            part("USB-C board", win(C["usb_board"], *b), COL["usb"]),
            part("Slide switch, M2 screws and nuts", win(S("switch", "switch_screws"), *b), COL["switch"]),
            part("Cradle and spring contact", win(C["cell_contacts"], *b), COL["contacts"])],
            OUT / "joint-08.png", "Joint 8: USB-C board and slide switch at the tail (from inside)",
            subtitle="Socket mouth flush with the tail wall; switch plate on the inside of the right wall",
            elev=35, azim=60, size=(8, 6)))
    return out


# ----------------------------------------------------------------- assembly steps
def steps(only=None):
    M = made()
    out = []

    def st(n, done, new, title, sub, **kw):
        if only is None or str(n) in only:
            out.append(bv.step(done, new, OUT / f"step-{n:02d}.png", f"Step {n}: {title}", subtitle=sub, **kw))

    def mv(p, e):
        return Part(p.name, p.shape, p.color, None, tuple(e), p.alpha)

    from build123d import Pos, Rot
    flip = lambda sh: Rot(180, 0, 0) * Pos(0, 0, -P["body_h"]) * sh  # noqa: E731  (top shell upside down on the bench)
    top_up = part("Top shell, upside down", flip(C["top_shell"]), COL["top"])
    st(1, [top_up], [mv(part("Eight M3 inserts", flip(inserts("top")), COL["insert"]), (0, 0, 25))],
       "heat-set inserts into the top shell",
       "Top shell upside down on the bench; iron at about 230 °C; also 3 in the head block and 2 in the strap bosses",
       elev=50, azim=-60)
    head = part("Optical head block", C["led_holder"] + inserts("head"), COL["head"])
    st(2, [head], [mv(M["leds"], (0, 0, 25)), mv(M["pd"], (0, 0, 40))], "LEDs and photodiode into the head block",
       "Each can pushed in from the top until it stops square, in the band order marked on the block",
       elev=40, azim=-60, label_done=True)
    st(3, [head, M["leds"], M["pd"]], [mv(M["afe"], (0, 0, 25))], "amplifier board onto the head block",
       "Leads through their holes; two M2.5 x 6 screws; then solder every lead and trim",
       elev=35, azim=-60, label_done=False)
    bot = M["bottom"]
    optics = part("Head block with LEDs and board", S("led_holder", "leds", "photodiode", "afe_board", "afe_screws"), COL["head"])
    st(4, [bot], [mv(M["window"], (0, 0, -30)), mv(optics, (0, 0, 40))], "window and head block into the bottom shell",
       "Window up into its hole from below; head block down onto the floor, lugs over the three holes",
       elev=25, azim=-60, label_done=False)
    inside = [bot, part("Window", C["window"], COL["window"]), optics]
    st(5, inside, [mv(M["shroud"], (0, 0, -30)), mv(part("Three M3 x 10 screws and washers", C["head_screws"], COL["screw"]), (0, 0, -60))],
       "shroud and head screws from below",
       "Bottom shell held on its side; three screws through the flange and floor into the head block, snug",
       elev=-30, azim=-60, label_done=False)
    st(6, inside, [mv(M["contacts"], (0, 0, 30)), mv(M["usb"], (0, 0, 30)), mv(M["switch"], (0, -30, 0))],
       "contacts, USB-C board and slide switch",
       "Contacts into the end-wall slots; USB-C board on its seat with a dot of glue; switch on two M2 screws",
       elev=35, azim=-55, label_done=False)
    fr = part("Display frame", flip(C["display_frame"]), COL["frame"])
    st(7, [top_up, part("Inserts", flip(inserts("top")), COL["insert"])],
       [mv(part("Display board, face down", flip(C["display_board"]), COL["board"]), (0, 0, 22)),
        mv(fr, (0, 0, 48)), mv(part("Four M3 x 8 screws", flip(C["frame_screws"]), COL["screw"]), (0, 0, 75))],
       "display board and frame into the top shell",
       "Top shell upside down; board face down over the window, frame over it; four screws into the inserts",
       elev=50, azim=-60, label_done=False)
    st(8, [top_up, fr], [mv(part("Scan button and nut", flip(C["button"]), COL["button"]), (0, 0, -25))],
       "scan button into the top shell",
       "Button in from the outside with its seal; nut tightened from inside, by hand plus a quarter turn",
       elev=-35, azim=-60, label_done=False)
    st(9, inside + [M["contacts"], M["usb"], M["switch"]], [mv(M["cell"], (0, 0, 30)), mv(M["strap"], (0, 0, 55))],
       "cell and strap",
       "Only after safety stops S1 to S4: cell into the cradle, negative end on the spring at the tail; strap on two M3 x 25 screws",
       elev=30, azim=-55, label_done=False)
    lower = inside + [M["contacts"], M["usb"], M["switch"], M["cell"], M["strap"]]
    st(10, lower, [mv(M["gasket"], (0, 0, 25))], "gasket onto the rim",
       "Foam tape on the rim, outside the tongue, ends butted at the tail; no tape across a boss",
       elev=35, azim=-55, label_done=False)
    upper = part("Top shell with display, frame and button", S("top_shell", "display_board", "display_frame", "frame_screws", "button"), "#7DA7D9")
    st(11, lower + [M["gasket"]], [mv(upper, (0, 0, 45)), mv(part("Four M3 x 20 screws", C["shell_screws"], COL["screw"]), (0, 0, -40))],
       "close the shells",
       "Leads tucked clear; top shell down over the tongue; four screws from below until the bosses meet",
       elev=20, azim=-55, label_done=False)
    closed = [part("Closed scanner", S("bottom_shell", "top_shell", "shroud", "button", "head_screws", "shell_screws", "gasket"), COL["bottom"])]
    st(12, closed, [mv(M["hood"], (0, 0, 30))], "clip on the sun hood",
       "Straight down over the display until both legs click under the ribs",
       elev=25, azim=-55, label_done=False)
    st(13, closed + [M["hood"]], [mv(part("Calibration cap with PTFE disc", S_cap(), COL["cap"]), (0, 0, -35))],
       "calibration cap onto the shroud",
       "Pushed on until the rim rests on the disc; this is also how it is stored",
       elev=-20, azim=-55, label_done=False)
    return out


# ----------------------------------------------------------------- wiring
def wiring():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch
    fig = plt.figure(figsize=(12, 7.2), dpi=150)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 120); ax.set_ylim(0, 72); ax.set_axis_off()
    INK, MUT = "#111827", "#4B5563"
    ax.text(2, 70, "WasteWise Scan prototype: block-level wiring", fontsize=13, fontweight="bold", color=INK, va="top")
    ax.text(2, 66.6, "Bought modules and one hand-built perfboard; no circuit board is laid out. Stranded or solid tinned copper as listed.",
            fontsize=8.5, color=MUT, va="top")
    ax.text(2, 1.5, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color="#B45309")
    ax.text(118, 1.5, "github.com/BoujeeEnjinia1701/wastewise-scan", fontsize=7, color="#0F766E", ha="right", family="monospace")
    B = {}

    def blk(key, x, y, w, h, title, sub, color):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3", fc="white", ec=color, lw=1.8))
        ax.text(x + w / 2, y + h - 1.4, title, ha="center", va="top", fontsize=9, fontweight="bold", color=INK)
        ax.text(x + w / 2, y + h - 4.3, sub, ha="center", va="top", fontsize=7.2, color=MUT, linespacing=1.3)
        B[key] = (x, y, w, h)

    def wire(pts, color, lw=2.0):
        xs, ys = zip(*pts)
        ax.plot(xs, ys, color=color, lw=lw, solid_capstyle="round", zorder=1)

    def lab(x, y, text, color, ha="left"):
        ax.text(x, y, text, fontsize=7.2, color=color, ha=ha, va="center", zorder=3,
                bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none"))
    RED, BLU, GRY = "#B91C1C", "#1D4ED8", "#6B7280"
    blk("usb", 3, 46, 15, 11, "USB-C board", "power only,\nin the tail wall", "#1D4ED8")
    blk("cell", 3, 24, 15, 13, "18650 cell", "protected, 3.6 V,\nin the cradle\ncontacts", "#7C3AED")
    blk("sw", 26, 24, 13, 10, "Slide switch", "in the right\nside wall", "#F59E0B")
    blk("board", 47, 38, 24, 21, "Display board", "ESP32-S3 with 1.9 in\nscreen and on-board\nLi-ion charger\n(T-Display-S3 class)", "#0F766E")
    blk("btn", 47, 14, 13, 10, "Scan button", "16 mm,\nnormally open", "#F59E0B")
    blk("afe", 82, 30, 24, 29, "Amplifier board", "transimpedance amp,\n47 k feedback, 24-bit\nconverter, 8 LED\nswitches with a\nhardware on-time\nlimit", "#15803D")
    blk("opt", 84, 8, 20, 14, "Optical head", "8 LEDs, 850 to\n1,650 nm; InGaAs\nphotodiode", "#C2410C")
    wire([(18, 52), (47, 52)], RED); lab(30, 54, "5 V and 0 V, 0.25 mm²", RED, "center")
    wire([(18, 30), (26, 30)], RED); lab(22, 32.4, "0.25 mm²", RED, "center")
    wire([(39, 30), (43, 30), (43, 42), (47, 42)], RED); lab(42.4, 37.5, "battery\ninput,\n0.25 mm²", RED, "right")
    wire([(71, 54), (82, 54)], RED); lab(76.5, 57.2, "3.3 V, 0 V,\n0.25 mm²", RED, "center")
    wire([(71, 46), (82, 46)], BLU); lab(76.5, 48.2, "SPI + ready", BLU, "center")
    wire([(71, 41), (82, 41)], BLU); lab(76.5, 43.2, "LED select", BLU, "center")
    wire([(53.5, 24), (53.5, 38)], GRY, 1.2); lab(54.2, 31, "button to GPIO,\n0.14 mm²", GRY)
    wire([(94, 22), (94, 30)], GRY, 1.4); lab(94.8, 26, "LED and photodiode leads,\nsoldered straight through", GRY)
    ax.text(3, 9.6, "Signal wires 0.14 mm² (26 AWG). Keep the photodiode input on the board, under 10 mm long and away from the LED switches.",
            fontsize=7.4, color=MUT)
    ax.text(3, 6.2, "Safety: the cell goes in only after stops S1 to S4. The LED on-time limit is in hardware and the firmware cannot override it.",
            fontsize=7.6, color="#B45309", fontweight="bold")
    out = OUT / "wiring.png"
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, facecolor="white"); plt.close(fig)
    return out


if __name__ == "__main__":
    args = sys.argv[1:] or ["overview", "sheets", "joints", "steps", "wiring"]
    fns = {"overview": overview, "sheets": sheets, "joints": joints, "steps": steps, "wiring": wiring}
    what, only = args[0], (args[1:] or None)
    if len(args) > 1 and args[1] in fns:      # several groups, all pictures in each
        for w in args:
            print(w, "->", fns[w]())
    elif what in ("overview", "wiring"):
        print(what, "->", fns[what]())
    else:
        print(what, "->", fns[what](only) if only else fns[what]())

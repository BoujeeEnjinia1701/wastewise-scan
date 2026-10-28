"""WasteWise Scan STEM check, WSC-STM-001 (STANDARDS section 20).

Run from the repo root:  python docs/04-calcs/stem_check.py
Writes docs/04-calcs/stem_results.csv, which docs/01b-stem-check.md quotes row by row. Option A numbers are
taken from the calculation note's script (docs/04-calcs/sizing.py, WSC-CAL-001), run here silently, so the
STEM check and the CAL never disagree. Option B (WSC-OPT-001) numbers are first-order estimates made here;
every assumption is in the B_ASSUMPTIONS block. A check is a first-order screen, never a replacement for the CAL.
"""
import contextlib
import io
import runpy
import sys
from math import exp, pi
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
from stem_check import Check, WITHIN, PLAUSIBLE  # noqa: E402

with contextlib.redirect_stdout(io.StringIO()):
    S = runpy.run_path(str(ROOT / "docs" / "04-calcs" / "sizing.py"), run_name="sizing")
P, A, D = S["P"], S["A"], S["D"]

c = Check(ROOT / "docs" / "04-calcs" / "stem_results.csv")


def assumed(note, closed_by=None):
    """Downgrade the row just added to Plausible: its check passes, but it rests on assumed inputs that only
    measurement can confirm (independent review of 2026-10-24). closed_by=None keeps the row open."""
    r = c.rows[-1]
    r["verdict"] = PLAUSIBLE
    r["check"] += f"; {note}"
    r["closed_by"] = closed_by or ""


h_, c_, k_ = 6.626e-34, 2.998e8, 1.381e-23


def planck_share(l0_nm, l1_nm, T, n=600):
    """Share of black-body emission between two wavelengths (numerical integral of Planck's law)."""
    def b(lam):
        return 1.0 / (lam ** 5 * (exp(h_ * c_ / (lam * k_ * T)) - 1.0))
    def integ(a, z, m):
        dx = (z - a) / m
        return sum(b(a + (i + 0.5) * dx) for i in range(m)) * dx
    return integ(l0_nm * 1e-9, l1_nm * 1e-9, n) / integ(0.2e-6, 30e-6, 20000)


# ------------------------------------------------------------------ option A (the current design)
c.cited("S1", "Common resins absorb at C-H overtone and combination bands near 1,150 to 1,250 nm, 1,370 to 1,420 nm and 1,650 to "
        "1,765 nm, at positions that differ between PET, HDPE, PP, PS and PVC", "Chemistry", "Analytical",
        "Near-infrared spectroscopy of polymers (Neo et al. 2022, review); open Plastic Scanner prior work",
        "Band positions used in WSC-CAL-001 B4; discrete-band identification shown by Plastic Scanner", WITHIN)
r1650, c1650, above = S["band"](1650, S["LED_FWHM"][1650])
c.cited("S2", f"A standard InGaAs photodiode responds from about 900 to 1,700 nm; the 1,650 nm band is seen with its centroid at "
        f"{c1650:.0f} nm and {above * 100:.0f} % of its signal at or above 1,650 nm", "Physics", "Optics and radiation",
        "InGaAs band gap cutoff near 1,700 nm at room temperature; responsivity curve of WSC-CAL-001 Table 1",
        f"Band integral of a Gaussian LED times the responsivity [B1, B2]: centroid {c1650:.0f} nm", WITHIN, closed_by="WSC-CAL-001 B2")
c.claim("S3", "Signal-to-noise ratio on the weakest band in shade (clear item, 8 conversions in 4 cycles) is at least 600, enough to "
        "resolve 0.5 % reflectance differences at 3 sigma (fix F2)", "Physics", "Electromagnetism and circuits",
        "Shot noise 2qIB and Johnson noise 4kTB/R of the transimpedance stage plus ADC noise", S["worst_snr"], A["min_snr"], "",
        rule="above", closed_by="WSC-CAL-001 C4")
v_sun = S["I_amb"] * A["Rf"]
c.claim("S4", "Sunlight through a clear item at 100 klx keeps the 47 kOhm amplifier inside the 2.048 V ADC range",
        "Physics", "Optics and radiation", "Diffuse transmission and view factor of the 36 mm rim; Ohm's law",
        round(v_sun, 3), A["adc_fs"], "V", closed_by="WSC-CAL-001 D1, D2")
c.claim("S5", "Ambient error on a clear item backed with the black cap is under 0.5 % of the 1,650 nm signal",
        "Physics", "Optics and radiation", "Interleaved dark subtraction; 10^-3 of the through-light left by the cap",
        round(S["err_b"] / S["V1650b"] * 100, 3), A["err_limit"] * 100, "%", closed_by="WSC-CAL-001 D6")
assumed("rests on the assumed cap leak (10^-3) and ambient change (1 % per 10 ms), to measure at TRL 4", "WSC-CAL-001 D6 (fix F2); cap opacity at TRL 4")
c.claim("S6", "Ambient error on an opaque item is under 0.5 % of the 1,650 nm signal", "Physics", "Optics and radiation",
        "Rim leak of 10^-3 of the clear-item case", round(S["err_opq"] / S["V1650o"] * 100, 3), A["err_limit"] * 100, "%",
        closed_by="WSC-CAL-001 D5")
assumed("rests on the assumed rim leak; the black TPU shroud's near-infrared opacity is to confirm", "WSC-CAL-001 D5; shroud opacity at TRL 4")
c.claim("S7", "The dark-level rule refuses an unbacked clear item in sun (dark level above 0.71 times the weakest band)",
        "Engineering and technology", "Sensing resolution", "Error budget: 0.5 % limit over the drift of 1 % per 10 ms in a 7 ms gap",
        round(S["I_amb"] * A["Rf"] / S["V1650c"], 0), S["k_prompt"], "times the band reading", rule="above", closed_by="WSC-CAL-001 D7")
c.claim("S8", "Button to result in 1.5 s or less", "Engineering and technology", "Control",
        "Timing budget: 4 cycles of 17 readings of 2 ms settling plus 2 conversions at 330 samples/s, plus classification and display (fix F2)",
        round(S["t_scan"] / 1000, 2), 1.5, "s", closed_by="WSC-CAL-001 E2")
c.claim("S9", "One 3,000 mAh cell lasts an 8 h shift at 4 scans per minute", "Engineering and technology", "Power and link budgets",
        "Energy balance: 80 % of 10.8 Wh over the average draw; an 85 % efficient 3.3 V converter still leaves "
        f"{S['life'] * 0.85:.1f} h", round(S["life"], 1), A["shift_h"], "h", rule="above", closed_by="WSC-CAL-001 F2")
c.cited("S10", "A protected 18650 Li-ion cell of 3,000 mAh at 3.6 V stores about 10.8 Wh and is charged at 0 to 45 C only",
        "Chemistry", "Electrochemistry and batteries", "Cell capacity times nominal voltage; IEC 62133-2 (IS 16046 Part 2) cell safety practice",
        "3.0 Ah x 3.6 V = 10.8 Wh; the 45 C charge limit is the usual Li-ion maker limit, to confirm on the chosen cell's datasheet",
        WITHIN, closed_by="WSC-CAL-001 F2; WSC-REG-001 R3")
c.claim("S11", "The 8 MB log partition holds at least 10,000 scans of 64 bytes", "Mathematics", "Units and dimensional analysis",
        "8 x 1,048,576 B / 64 B; a margin of 13 times covers file system overhead", round(S["n_log"]), 10000, "scans", rule="above", closed_by="WSC-CAL-001 G1")
c.claim("S12", "LED light reflected inside the window reaches the detector at under 0.5 % of the signal after the open-air reading, "
        "with the window offset changing 10 % between readings (PR-017)", "Physics", "Optics and radiation",
        "Fresnel reflection (4 % per uncoated surface); geometric optics of the baffle through the glass (fix F1); leak through the tube wall",
        round(S["CROSSTALK"]["after"] * 100, 4), A["err_limit"] * 100, "%")
assumed("10 % before fix F1 (Fails, fix proposed); after it the glass path is closed by geometry and the wall leak rests on assumed "
        "values (wall opacity 2e-02 or better needed), to confirm on a coupon and a built head at TRL 4")
c.cited("S13", "Carbon-black items reflect about 4 % in the near infrared and read 'unknown' below the 0.08 reflectance threshold",
        "Chemistry", "Materials and polymer chemistry", "Carbon black absorbs across the near infrared (WRAP, black plastic packaging)",
        f"Black item returns {S['black_ratio'] * 100:.0f} % of a typical item; separated with SNR over {S['worst_snr'] * A['rho_black'] / A['rho_clear']:.0f} [C6]; an unbacked clear item (0.10) sits close to the threshold and may read 'unknown', which is the safe side",
        WITHIN, closed_by="WSC-CAL-001 C6")
c.claim("S14", "Corneal irradiance of the brightest LED at 200 mm is inside the IEC 62471 exempt group (100 W/m2)", "Physics",
        "Optics and radiation", "Radiant intensity over distance squared; IEC 62471 exempt limit for infrared radiation to the eye",
        round(S["E200"], 2), 100.0, "W/m2", closed_by="WSC-CAL-001 H2")
assumed("limit values as understood from IEC 62471, standard not purchased; 241 W/m2 at the rim if an LED sticks on, so the hardware on-time limit is required",
        "WSC-CAL-001 H2; limits to confirm against the standard text")
c.claim("S15", "Weighted retinal thermal radiance of the 850 nm LED is under the IEC 62471 exempt limit (weak visual stimulus)",
        "Biology", "Human physiology and biomechanics", "Retinal thermal hazard of near-infrared sources, IEC 62471",
        round(S["L_eff"] / S["L_lim"] * 100, 1), 100.0, "% of the limit", closed_by="WSC-CAL-001 H3")
assumed("limit values as understood from IEC 62471, standard not purchased", "WSC-CAL-001 H3; limits to confirm against the standard text")
c.claim("S16", "The sun hood gives at least 3:1 display contrast on the part of the screen it shades in 100 klx sun",
        "Physics", "Optics and radiation", "Contrast ratio with diffuse screen reflection of sky light (15 klx)",
        round(S["cr_shade"], 1), A["cr_needed"], ":1", rule="above", closed_by="WSC-CAL-001 I2 to I4")
assumed("screen reflectance of 2 % is assumed; a glossy screen reflects sky light specularly (reviewer: about 2:1), so PR-007 stays at risk",
        "WSC-CAL-001 I2 to I4; outdoor check at TRL 4")
c.order_of_magnitude("S17", "A 1.2 m drop on a shell corner with about 1 mm of crush decelerates the scanner at about 1,200 g",
                     "Physics", "Mechanics and statics", claimed=1200, estimate=A["drop_h"] / A["stop_shell_m"], unit="g",
                     law="Work-energy: deceleration = drop height / stopping distance")
assumed("mean deceleration from an assumed 1 mm crush; the peak of a half-sine pulse is 1.57 times higher (used in S18); crush to measure in the drop test at TRL 4")
c.claim("S18", "The printed PETG cell strap stays below the bending strength of printed PETG under the corner-drop cell load",
        "Physics", "Strength of materials", "Simply supported beam, central peak load: stress = F L / (4 Z); printed PETG about 50 MPa along the layers",
        round(S["sig"], 1), A["petg_strength"], "MPa", margin=0.3)
assumed(f"11 x 10 mm strap at the half-sine peak (fix F3); the 10 x 8 mm strap reached {S['sig_old']:.0f} MPa (Fails, fix proposed); "
        "rests on the assumed crush (S17), drop test at TRL 4")
c.cited("S19", "With LED output falling 0.4 %/C, the 5 % drift warning trips after about 12.5 C of change", "Engineering and technology",
        "Sensing resolution", "Linear temperature coefficient (typical for SWIR LEDs; assumed in WSC-CAL-001 Table 1)",
        f"0.05 / 0.004 = {S['dT']:.1f} C [J3]; the coefficient is assumed, SWIR LEDs may drift more and shift in wavelength on the steep "
        "1,650 nm detector edge, and a uniform drift cancels in the band ratios while a band-to-band difference does not", PLAUSIBLE)
c.cited("S20", "PVC in a PET stream spoils the batch because PVC degrades well below PET melt-processing temperatures", "Chemistry",
        "Materials and polymer chemistry", "Thermal dehydrochlorination of PVC releases HCl; PET is melt-processed hot (polymer handbooks)",
        "Qualitative claim in WSC-PRB-001; the scanner only reports PVC, it does not depend on the temperatures", WITHIN)
c.order_of_magnitude("S21", "Sunlight at about 100 klx carries about 300 W/m2 between 900 and 1,700 nm", "Mathematics",
                     "Orders of magnitude", claimed=A["E_sun_band"], estimate=1000.0 * planck_share(900, 1700, 5778), unit="W/m2",
                     law="About 1,000 W/m2 global irradiance at 100 to 120 klx, times the share of a 5,778 K black body between 900 and 1,700 nm "
                         "(Planck's law, computed here; atmospheric water bands lower it a little)", closed_by="WSC-CAL-001 D1")
c.claim("S22", "The 34 mm body thickness sits in the 32 to 51 mm handle range for a hand grip; the 62 mm width is held like a phone "
        "for a light pressing task", "Biology", "Ergonomics", "NIOSH 2004-164 handle diameter for single-handle power tools",
        P["body_h"], 32.0, "mm", rule="above", margin=0.1)
c.cited("S23", "Eight discrete bands classify the five resins at 95 % or better on clean, non-black items (PR-001)", "Mathematics",
        "Statistics and uncertainty", "Paper band study: linear discriminant analysis on log band ratios of approximate reference spectra",
        f"Not shown at the assumed scatter: {S['acc8'] * 100:.1f} % at 1.5 % band scatter, {S['sens'][0.010] * 100:.1f} % at 1.0 %; PE against PP "
        f"{min(S['confpe'][0, 0], S['confpe'][1, 1]) * 100:.0f} % [B4 to B7]; approximate spectra, train and test from one generator, no "
        "'other' class; needs real item scatter of about 1 % or less; settled only by a labelled item set at TRL 4", PLAUSIBLE)

# ------------------------------------------------------------------ option B (tunable-filter spectrometer), first order
B_ASSUMPTIONS = {
    "fpi_band": (1550.0, 1850.0),   # nm, MEMS-FPI sensor range (Hamamatsu C13272 series, cited in WSC-OPT-001)
    "fpi_fwhm": 20.0,               # nm, spectral resolution (assumed; to assess from the datasheet)
    "lamp_w": 0.58, "lamp_n": 2,    # W each, 5 V 115 mA T-1 3/4 lamp (assumed class)
    "lamp_rad_eff": 0.85,           # share of electrical power radiated (tungsten filament, typical)
    "T_fil": 2400.0,                # K, filament temperature at rated voltage (assumed)
    "lamp_dist": 0.024,             # m, lamp to the item spot
    "det_area": 1.0e-6,             # m2, effective aperture of the filter and detector (assumed)
    "det_omega": 0.1,               # sr, acceptance solid angle of the filter (assumed, about +-10 deg)
    "resp": 1.0,                    # A/W near 1,700 nm (extended-response detector inside the sensor, assumed)
    "bw_hz": 50.0,                  # Hz, noise bandwidth per wavelength step
    "Rf": 1.0e7,                    # Ohm, transimpedance gain
    "points": 100, "step_ms": 5.0, "lamp_warm_ms": 150.0, "scan_s_per_min": 4.0,
    "base_w": 0.39,                 # W, option A's average draw without LEDs (WSC-CAL-001 F2, 108 mA at 3.6 V)
}
BA = B_ASSUMPTIONS
share = planck_share(*BA["fpi_band"], BA["T_fil"])
c.claim("S30", "Option B: a 2,400 K tungsten filament radiates at least 10 % of its output between 1,550 and 1,850 nm",
        "Physics", "Thermodynamics", "Planck's law, numerical integral", round(share * 100, 1), 10.0, "%", rule="above")
c.cited("S31", "Option B: the MEMS-FPI sensor's 1,550 to 1,850 nm range covers the PE and PP first-overtone bands from 1,680 to 1,765 nm",
        "Physics", "Optics and radiation", "Hamamatsu C13272 series range 1,550 to 1,850 nm (Photonics Online datasheet notice)",
        "1,680 to 1,765 nm lies inside 1,550 to 1,850 nm", WITHIN)
slice_w = BA["lamp_w"] * BA["lamp_rad_eff"] * share * BA["fpi_fwhm"] / (BA["fpi_band"][1] - BA["fpi_band"][0])
E_slice = BA["lamp_n"] * slice_w / (4 * pi * BA["lamp_dist"] ** 2)
P_det = A["rho_clear"] * E_slice / pi * BA["det_area"] * BA["det_omega"]
I_det = P_det * BA["resp"]
i_n = (2 * 1.602e-19 * I_det * BA["bw_hz"] + 4 * k_ * 300 / BA["Rf"] * BA["bw_hz"]) ** 0.5
snr_b = I_det / i_n
c.claim("S32", "Option B: signal-to-noise ratio of at least 200 per 20 nm step on a clear item in shade", "Physics",
        "Electromagnetism and circuits", "Lamp irradiance per spectral slice, Lambertian item, shot and Johnson noise",
        round(snr_b), 200.0, "", rule="above", margin=0.0)
t_b = BA["lamp_warm_ms"] / 1000 + BA["points"] * BA["step_ms"] / 1000 + 0.09
c.cited("S33", f"Option B: button to result in about {t_b:.2f} s, under 1.5 s", "Engineering and technology", "Control",
        "Lamp warm-up plus a 100-point filter sweep at an assumed 5 ms per step",
        f"{t_b:.2f} s; the filter settling time per step is to assess from the sensor datasheet", PLAUSIBLE)
c.cited("S34", "Option B: the five resins can be told apart from 1,550 to 1,850 nm alone", "Chemistry", "Analytical",
        "First-overtone C-H bands of PE and PP and the aromatic bands of PET and PS lie in this range; PVC's features are weaker",
        "Plausible from the band positions of WSC-CAL-001 B4; PVC and PET need a labelled item set", PLAUSIBLE)
e_scan = BA["lamp_n"] * BA["lamp_w"] * t_b
p_b = BA["base_w"] + e_scan * BA["scan_s_per_min"] / 60.0
life_b = A["cap_mah"] / 1000 * A["v_cell"] * A["usable"] / p_b
c.claim("S35", "Option B: one 3,000 mAh cell lasts an 8 h shift with the lamps", "Engineering and technology", "Power and link budgets",
        "Energy balance with the lamp energy per scan", round(life_b, 1), 8.0, "h", rule="above")
c.cited("S36", "Option B: the lamps stay clear of softening the black PETG head block (glass transition about 80 C)", "Physics",
        "Heat transfer", f"Average lamp power {e_scan * BA['scan_s_per_min'] / 60:.3f} W; bulb glass reaches well above 80 C during each scan",
        "Fails, fix proposed at first (bulb 0.2 mm from PETG, independent review); fix F4 in the option B model: each bulb sits in an "
        "aluminium sleeve with a 0.2 mm air gap, which spreads the heat to the block; sleeve temperature to confirm", PLAUSIBLE)

state = c.write()
for r in c.rows:
    print(f"{r['id']:4s} {r['verdict']:32s} {r['check']}")
print("B numbers:", f"share {share:.3f}; P_det {P_det * 1e9:.2f} nW; I {I_det * 1e9:.2f} nA; SNR {snr_b:.0f}; t {t_b:.2f} s; life {life_b:.1f} h")

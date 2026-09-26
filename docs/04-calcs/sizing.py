"""WasteWise Scan sizing calculations, WSC-CAL-001 (TRL 3).

Run from the repo root:  python docs/04-calcs/sizing.py
Prints every number that WSC-CAL-001 (docs/04-calcs/01-sizing.md) quotes, each on a line
tagged like [C3]. Geometry comes from cad/src/model.py (PARAMS, derived() and the part
solids), so the note, the STEP files and drawing WSC-DWG-001 use the same dimensions. The BOM
total is read from bom/bom.csv and the budget from project.yaml. These are first-principles
estimates for a paper proof of concept; every assumption is set in the ASSUMPTIONS block.
v0.2 (2026-09-25): decisions of WSC-DDR-003 applied (sun hood, backing step and dark-level
prompt for clear items, open-air crosstalk reading, paper check of LED modulation).
"""
import csv
import sys
from math import atan, cos, degrees, exp, log, pi, radians, sqrt
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "cad" / "src"))
from model import PARAMS as P, derived, parts, cap_parts, scanner  # noqa: E402

D = derived(P)
q_e, k_B, T_K = 1.602e-19, 1.381e-23, 300.0

# ------------------------------------------------------------------ ASSUMPTIONS
BANDS = [850, 940, 1050, 1200, 1300, 1450, 1550, 1650]          # nm, decided band set (DDR-001 D4)
LED_MW = {850: 15.0, 940: 15.0, 1050: 4.0, 1200: 2.0, 1300: 2.0, 1450: 1.5, 1550: 1.5, 1650: 1.0}   # radiant power at 100 mA, mW
LED_FWHM = {850: 40, 940: 50, 1050: 60, 1200: 80, 1300: 90, 1450: 100, 1550: 110, 1650: 120}        # nm
# Standard InGaAs PIN responsivity, A/W (typical curve shape; confirm from the chosen part's datasheet)
RESP = [(800, 0.05), (900, 0.35), (1000, 0.65), (1300, 0.90), (1550, 0.95), (1620, 0.90),
        (1680, 0.50), (1720, 0.05), (1760, 0.0)]
A = {
    "pd_active_d": 1.0e-3,      # m, photodiode active diameter
    "T_window": 0.92,           # borosilicate, one pass, uncoated (two surfaces)
    "R_fresnel": 0.04,          # one uncoated glass surface, near normal incidence
    "spot_r": 8.0e-3,           # m, radius of the illuminated spot on the item (LED beam at about 24 mm)
    "rho_white": 0.9, "rho_item": 0.5, "rho_clear": 0.10, "rho_black": 0.04,   # diffuse reflectance
    "led_half_angle": 10.0,     # deg, narrowest LED beam considered (worst case for eye safety)
    "led_off_axis_rel": 0.25,   # relative intensity 23 deg off the LED axis (window crosstalk path)
    "adc_rate": 330.0,          # samples/s, ADS1220 class, normal mode
    "adc_noise_uv": 5.0,        # µV rms per conversion at gain 1 (assumed, conservative)
    "adc_fs": 2.048,            # V, internal reference
    "rail_v": 3.3,              # TIA output swing limit
    "n_avg": 4,                 # conversions averaged per reading
    "settle_ms": 2.0,           # LED switch-on and TIA settling
    "classify_ms": 20.0, "display_ms": 50.0, "debounce_ms": 20.0,
    "Rf_concept": 1.0e6,        # TIA feedback, TRL 2 concept
    "Rf": 47.0e3,               # TIA feedback, sized here for sunlight through clear items
    "E_sun_band": 300.0,        # W/m2 of sunlight in the 900 to 1,700 nm band at about 100 klx
    "T_diffuse_clear": 0.30,    # diffuse transmittance of a clear or translucent item wall (worst case)
    "leak_opaque": 1.0e-3,      # fraction of the clear-item case that leaks past the rim on an opaque, curved item
    "ambient_drift": 0.01,      # relative change of ambient light per 10 ms from hand movement (assumed)
    "dark_gap_ms": 7.0,         # time between a band reading and the mean of its two dark readings
    "min_snr": 200.0,           # needed to resolve 0.5 % reflectance differences
    "err_limit": 0.005,         # largest acceptable ambient error, relative to the band signal (0.5 %)
    "leak_backed": 1.0e-3,      # fraction of the clear-item through-light left when the item is backed with the black cap
    "mod_hz": 2000.0,           # LED modulation frequency for the synchronous demodulation option (paper check only)
    "xtalk_change": 0.10,       # assumed change of the window crosstalk from dirt or scratches between open-air readings
    # power
    "i_mcu_ma": 45.0, "i_display_ma": 60.0, "i_afe_ma": 3.0,        # ESP32-S3 at 240 MHz, radio off; display at full backlight
    "i_led_ma": 100.0, "v_cell": 3.6, "cap_mah": 3000.0, "usable": 0.80,
    "scans_per_min": 4.0, "shift_h": 8.0, "charge_ma": 500.0, "charge_overhead": 1.2,
    # logging
    "record_b": 64, "log_partition_mb": 8.0, "csv_row_b": 140,
    # masses
    "rho_petg": 1.27, "rho_tpu": 1.21, "rho_glass": 2.23, "rho_ptfe": 2.20,   # g/cm3
    "m_cell": 47.0, "m_board": 15.0, "m_leds": 4.0, "m_pd": 0.5, "m_afe": 5.0,
    "m_button": 5.0, "m_usb": 2.0, "m_fixings": 10.0,
    # display legibility
    "disp_nits": 400.0, "disp_black_nits": 0.4, "screen_rho": 0.02,   # diffuse-equivalent screen reflectance
    "sun_angles": (30, 45, 60, 75),   # deg, sun direction from the screen normal, for the hood check
    "E_sun_lux": 100e3, "E_shade_lux": 15e3, "cr_needed": 3.0,
    # drop and temperature
    "drop_h": 1.2, "stop_shell_m": 1.0e-3, "stop_tpu_m": 10.0e-3,
    "led_tc": -0.004,           # 1/°C, relative LED output change (SWIR LEDs, assumed)
    "drift_limit": 0.05,
}


def say(tag, text):
    print(f"[{tag}] {text}")


def resp(lam):
    for (l0, r0), (l1, r1) in zip(RESP, RESP[1:]):
        if l0 <= lam <= l1:
            return r0 + (r1 - r0) * (lam - l0) / (l1 - l0)
    return 0.0


def band(lam0, fwhm, step=1.0):
    """Gaussian LED spectrum times detector responsivity. Returns (mean responsivity, detected centroid, share above 1,650 nm)."""
    s = fwhm / 2.3548
    lams = [lam0 - 4 * s + i * step for i in range(int(8 * s / step) + 1)]
    w = [exp(-0.5 * ((l - lam0) / s) ** 2) for l in lams]
    det = [wi * resp(l) for wi, l in zip(w, lams)]
    r_mean = sum(det) / sum(w)
    centroid = sum(d * l for d, l in zip(det, lams)) / sum(det)
    above = sum(d for d, l in zip(det, lams) if l >= 1650) / sum(det)
    return r_mean, centroid, above


STATUS = {}

# ------------------------------------------------------------------ A. geometry and mass
print("A. Geometry and mass (R6)")
ps = parts(P)
cp = cap_parts(P)
bb = scanner(P).bounding_box()
body_l, body_w, body_h = P["body_l"], P["body_w"], P["body_h"]
say("A1", f"Body {body_l:.0f} x {body_w:.0f} x {body_h:.0f} mm; overall with hood, button and shroud {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f} mm; "
          f"shroud {P['shroud_h']:.0f} mm deep, rim {P['shroud_rim_d']:.0f} mm outside and {D['rim_id']:.0f} mm inside; "
          f"sun hood {P['hood_h']:.0f} mm above the top shell")
vol = {k: v.volume / 1000.0 for k, v in {**ps, **cp}.items()}
m = {
    "Top shell (PETG)": vol["top_shell"] * A["rho_petg"],
    "Bottom shell (PETG)": vol["bottom_shell"] * A["rho_petg"],
    "Shroud (TPU)": vol["shroud"] * A["rho_tpu"],
    "LED holder (PETG)": vol["led_holder"] * A["rho_petg"],
    "Cell cradle (PETG) and USB-C": vol["cell_holder_usb"] * A["rho_petg"] + A["m_usb"],
    "Window (borosilicate)": vol["window"] * A["rho_glass"],
    "18650 cell": A["m_cell"],
    "Display board": A["m_board"],
    "Sun hood (PETG)": vol["sun_hood"] * A["rho_petg"],
    "LEDs, photodiode, AFE board": A["m_leds"] + A["m_pd"] + A["m_afe"],
    "Button and switch": A["m_button"],
    "Fixings, gasket, wire": A["m_fixings"],
}
m_scanner = sum(m.values())
m_cap = vol["cal_cap"] * A["rho_petg"] + vol["ptfe_disc"] * A["rho_ptfe"]
for k, v in m.items():
    say("A2", f"  {k:32s} {v:6.1f} g")
say("A3", f"Scanner {m_scanner:.0f} g; cap with PTFE disc {m_cap:.0f} g; total {m_scanner + m_cap:.0f} g (R6 limit 250 g)")
fit = body_l <= 170 and body_w <= 65 and body_h <= 40
STATUS["R6"] = ("Met" if (m_scanner + m_cap) <= 250 and fit else "Not met",
                f"{m_scanner:.0f} g ({m_scanner + m_cap:.0f} g with cap); {body_l:.0f} x {body_w:.0f} x {body_h:.0f} mm", "250 g; 170 x 65 x 40 mm")

# ------------------------------------------------------------------ B. band coverage
print("B. Band coverage and detector response (R1)")
bandinfo = {}
for lam in BANDS:
    r, c, above = band(lam, LED_FWHM[lam])
    bandinfo[lam] = r
    say("B1", f"  {lam:5d} nm, FWHM {LED_FWHM[lam]:3d} nm: mean responsivity {r:.2f} A/W, detected centroid {c:6.0f} nm")
r, c, above = band(1650, LED_FWHM[1650])
say("B2", f"1,650 nm band: detected centroid {c:.0f} nm; {above * 100:.0f} % of the detected signal lies at 1,650 nm or above; "
          f"responsivity at 1,700 nm {resp(1700):.2f} A/W and at 1,720 nm {resp(1720):.2f} A/W")
in_2nd = [l for l in BANDS if 1150 <= l <= 1250]
say("B3", f"Bands inside the 1,150 to 1,250 nm C-H second-overtone region: {in_2nd}; inside 1,650 to 1,750 nm: only the short edge of 1,650 nm")
STATUS["R1"] = ("At risk", f"8 bands; 1,650 nm band detected centroid {c:.0f} nm, {above * 100:.0f} % of its signal at or above 1,650 nm",
                "95 % correct, 5 resins")

# ------------------------------------------------------------------ C. signal and noise
print("C. Optical signal, crosstalk and noise (R1, R3)")
A_det = pi * (A["pd_active_d"] / 2) ** 2
d = D["d_pd_item"] / 1000.0
g_coll = A_det / (pi * (A["spot_r"] ** 2 + d ** 2))        # Lambertian disc of radius spot_r, on axis
say("C1", f"Detector {A['pd_active_d'] * 1e3:.1f} mm dia, {d * 1e3:.0f} mm from the item; collection factor {g_coll:.2e} per unit reflectance")
enbw = A["adc_rate"] / 2 / A["n_avg"]
v_adc = A["adc_noise_uv"] * 1e-6 / sqrt(A["n_avg"])


def signal(lam, rho, Rf):
    P_det = LED_MW[lam] * 1e-3 * A["T_window"] ** 2 * rho * g_coll
    I = P_det * bandinfo[lam]
    return P_det, I, I * Rf


def noise(I_total, Rf):
    i_n = sqrt(2 * q_e * I_total * enbw + 4 * k_B * T_K / Rf * enbw)
    return sqrt((i_n * Rf) ** 2 + v_adc ** 2)


worst_snr = 1e9
for lam in BANDS:
    Pw, Iw, Vw = signal(lam, A["rho_white"], A["Rf"])
    _, Ic, Vc = signal(lam, A["rho_clear"], A["Rf"])
    snr_c = Vc / noise(Ic, A["Rf"])
    worst_snr = min(worst_snr, snr_c)
    say("C2", f"  {lam:5d} nm: white {Pw * 1e6:6.2f} µW, {Iw * 1e6:5.3f} µA, {Vw * 1e3:6.2f} mV at {A['Rf'] / 1e3:.0f} kΩ; "
              f"clear item {Vc * 1e3:5.2f} mV, SNR {snr_c:6.0f} (shade)")
lam_max = max(BANDS, key=lambda l: signal(l, A["rho_white"], 1.0)[1])
_, Imax, _ = signal(lam_max, A["rho_white"], A["Rf_concept"])
say("C3", f"Concept 1 MΩ gain in shade: strongest band ({lam_max} nm) on white {Imax * 1e6:.2f} µA gives {Imax * A['Rf_concept']:.2f} V "
          f"({'saturates' if Imax * A['Rf_concept'] > A['rail_v'] else 'within'} a {A['rail_v']} V rail)")
say("C4", f"Worst-case SNR in shade (clear item, 4 averages, {A['Rf'] / 1e3:.0f} kΩ): {worst_snr:.0f}; needed {A['min_snr']:.0f}")
# window crosstalk: LED light reflected by the window's outer (item-side) surface into the detector
led_r, led_z, pd_z = P["led_ring_r"], P["led_z"], P["pd_z"]
L_img = sqrt(led_r ** 2 + (led_z + pd_z) ** 2) / 1000.0     # image of the LED in the z = 0 surface to the detector
omega = 2 * pi * (1 - cos(radians(15.0)))
x_ratio = (A["led_off_axis_rel"] * A["R_fresnel"] * A_det / L_img ** 2 / omega) / (A["T_window"] ** 2 * A["rho_item"] * g_coll)
say("C5", f"Window crosstalk through the glass under the baffle: path {L_img * 1e3:.1f} mm, about {x_ratio * 100:.0f} % of the "
          f"signal from a 0.5-reflectance item (order of magnitude)")
black_ratio = A["rho_black"] / A["rho_item"]
resid = x_ratio * A["xtalk_change"]
say("C7", f"Open-air reading in the calibration routine removes the fixed crosstalk offset; a {A['xtalk_change'] * 100:.0f} % change of that offset "
          f"from window dirt leaves about {resid * 100:.0f} % of the signal; to stay under {A['err_limit'] * 100:.1f} % the offset must stay within "
          f"{A['err_limit'] / x_ratio * 100:.1f} % of itself between open-air readings")
say("C6", f"Black item (reflectance {A['rho_black']}) returns {black_ratio * 100:.0f} % of a typical item's signal; "
          f"an 'unknown' threshold at mean reflectance 0.08 separates it with SNR over {worst_snr * A['rho_black'] / A['rho_clear']:.0f}")
STATUS["R3"] = ("Not verifiable at TRL 3", "black items fall below the 0.08 reflectance threshold; wrong-result rate needs item data", "2 % or fewer wrong")

# ------------------------------------------------------------------ D. sunlight
print("D. Sunlight and stray light (R4)")
a_rim = D["rim_id"] / 2 / 1000.0
view = a_rim ** 2 / (a_rim ** 2 + d ** 2)
r_sun = 0.8
P_amb = A["E_sun_band"] * A["T_diffuse_clear"] * A_det * view
I_amb = P_amb * r_sun
say("D1", f"Clear item in direct sun: light through the item fills the {D['rim_id']:.0f} mm rim; view factor {view:.2f}; "
          f"{P_amb * 1e6:.1f} µW, {I_amb * 1e6:.1f} µA at the detector")
say("D2", f"At 1 MΩ that is {I_amb * A['Rf_concept']:.1f} V (saturated); at {A['Rf'] / 1e3:.0f} kΩ it is {I_amb * A['Rf']:.2f} V "
          f"({'within' if I_amb * A['Rf'] < A['adc_fs'] else 'over'} the {A['adc_fs']} V ADC range)")
_, _, V1650c = signal(1650, A["rho_clear"], A["Rf"])
ratio = I_amb * A["Rf"] / V1650c
err = A["ambient_drift"] * (A["dark_gap_ms"] / 10.0) * I_amb * A["Rf"]
say("D3", f"Ambient is {ratio:.0f} times the 1,650 nm signal from a clear item; a {A['ambient_drift'] * 100:.0f} % change per 10 ms "
          f"leaves {err * 1e3:.1f} mV after interleaved dark subtraction, against {V1650c * 1e3:.2f} mV of signal")
snr_sun = V1650c / sqrt(noise(I_amb + 0, A["Rf"]) ** 2)
say("D4", f"Shot-noise-limited SNR in sun, clear item, 1,650 nm: {snr_sun:.0f}; the ambient drift error, not noise, sets the limit")
err_opq = err * A["leak_opaque"]
_, _, V1650o = signal(1650, A["rho_item"], A["Rf"])
say("D5", f"Opaque item (rim leak {A['leak_opaque']:.0e} of the clear case): drift error {err_opq * 1e6:.1f} µV against {V1650o * 1e3:.2f} mV, "
          f"{err_opq / V1650o * 100:.2f} % of signal")
# D6: decided option (b): back clear and translucent items with the (black) calibration cap
rho_backed = A["rho_clear"] + A["T_diffuse_clear"] ** 2 * A["rho_white"]
_, _, V1650b = signal(1650, rho_backed, A["Rf"])
err_b = err * A["leak_backed"]
say("D6", f"Clear item backed with the cap (PTFE behind the wall, black cap outside): effective reflectance {rho_backed:.2f}, "
          f"1,650 nm signal {V1650b * 1e3:.2f} mV; through-light cut to {A['leak_backed']:.0e}; drift error {err_b * 1e6:.1f} µV, "
          f"{err_b / V1650b * 100:.2f} % of signal (limit {A['err_limit'] * 100:.1f} %)")
k_prompt = A["err_limit"] / (A["ambient_drift"] * A["dark_gap_ms"] / 10.0)
say("D7", f"Firmware rule: show 'shade or back with cap' instead of a result when the mean dark level exceeds {k_prompt:.2f} times the "
          f"weakest band reading. Clear unbacked in sun {I_amb * A['Rf'] / V1650c:.0f} (prompt); backed {I_amb * A['Rf'] * A['leak_backed'] / V1650b:.2f}; "
          f"opaque {I_amb * A['Rf'] * A['leak_opaque'] / V1650o:.2f} (result shown)")
gap_mod = 1000.0 / A["mod_hz"] / 2
err_mod = A["ambient_drift"] * (gap_mod / 10.0) * I_amb * A["Rf"]
say("D8", f"Paper check of option (a), LEDs modulated at {A['mod_hz'] / 1000:.0f} kHz: light-to-dark gap {gap_mod:.2f} ms; clear unbacked item in sun "
          f"still leaves {err_mod / V1650c * 100:.0f} % of the 1,650 nm signal; needs an ADC of {4 * A['mod_hz'] / 1000:.0f} kS/s or more or an analog demodulator")
r4_ok = err_b / V1650b <= A["err_limit"] and err_opq / V1650o <= A["err_limit"]
STATUS["R4"] = ("Met" if r4_ok else "Not met",
                f"opaque {err_opq / V1650o * 100:.2f} %, clear backed with cap {err_b / V1650b * 100:.2f} % of signal; clear unbacked in sun refused by the dark-level prompt",
                "same result in 100 klx sun; clear items backed with the cap")

# ------------------------------------------------------------------ E. timing
print("E. Scan timing (R2)")
t_conv = 1000.0 / A["adc_rate"]
t_read = A["settle_ms"] + A["n_avg"] * t_conv
n_read = len(BANDS) + (len(BANDS) + 1)            # each band between two dark readings
t_scan = n_read * t_read + A["classify_ms"] + A["display_ms"] + A["debounce_ms"]
say("E1", f"One reading {t_read:.1f} ms ({A['settle_ms']:.0f} ms settle plus {A['n_avg']} conversions of {t_conv:.2f} ms); "
          f"{n_read} readings (8 bands, 9 interleaved darks) {n_read * t_read:.0f} ms")
say("E2", f"Button to result {t_scan:.0f} ms ({t_scan / 1000:.2f} s) against 1.5 s")
STATUS["R2"] = ("Met" if t_scan <= 1500 else "Not met", f"{t_scan / 1000:.2f} s", "1.5 s")

# ------------------------------------------------------------------ F. power
print("F. Power and battery (R5)")
led_j = len(BANDS) * A["i_led_ma"] / 1000 * 3.7 * t_read / 1000
led_ma = led_j * A["scans_per_min"] / 60.0 / A["v_cell"] * 1000
i_tot = A["i_mcu_ma"] + A["i_display_ma"] + A["i_afe_ma"] + led_ma
wh = A["cap_mah"] / 1000 * A["v_cell"]
life = A["cap_mah"] * A["usable"] / i_tot
say("F1", f"LED energy {led_j * 1000:.0f} mJ per scan, {led_ma:.2f} mA average at {A['scans_per_min']:.0f} scans per minute")
say("F2", f"Average draw {i_tot:.0f} mA ({i_tot * A['v_cell'] / 1000:.2f} W); cell {wh:.1f} Wh, {A['usable'] * 100:.0f} % usable; "
          f"life {life:.1f} h against {A['shift_h']:.0f} h")
t_charge = A["cap_mah"] / A["charge_ma"] * A["charge_overhead"]
say("F3", f"USB charge time about {t_charge:.1f} h at {A['charge_ma']:.0f} mA (board charger, assumed)")
STATUS["R5"] = ("Met" if life >= A["shift_h"] else "Not met", f"{life:.1f} h", "8 h")

# ------------------------------------------------------------------ G. logging
print("G. Log storage (R9)")
n_log = A["log_partition_mb"] * 1024 * 1024 / A["record_b"]
say("G1", f"{A['record_b']} B per record; 10,000 scans = {10000 * A['record_b'] / 1024:.0f} kB; "
          f"a {A['log_partition_mb']:.0f} MB log partition holds {n_log:,.0f} scans; CSV export of 10,000 rows about "
          f"{10000 * A['csv_row_b'] / 1e6:.1f} MB")
STATUS["R9"] = ("Met" if n_log >= 10000 else "Not met", f"{n_log:,.0f} scans", "10,000 scans")

# ------------------------------------------------------------------ H. eye safety
print("H. Eye safety (R14)")
om = 2 * pi * (1 - cos(radians(A["led_half_angle"])))
I_max = max(LED_MW.values()) * 1e-3 / om
E200 = I_max / 0.2 ** 2
E24 = I_max / (D["d_led_item"] / 1000.0) ** 2
duty = t_read / 1000 * A["scans_per_min"] / 60.0
field = pi * (0.011 * 0.2 / 2) ** 2
L_eff = I_max / field * 10 ** ((700 - 850) / 500)
L_lim = 6000 / 0.011
say("H1", f"Brightest LED (850 nm, {max(LED_MW.values()):.0f} mW, ±{A['led_half_angle']:.0f}°): {I_max * 1e3:.0f} mW/sr")
say("H2", f"Corneal irradiance {E200:.1f} W/m2 at 200 mm and {E24:.0f} W/m2 at the shroud rim if held on; "
          f"{E24 * duty:.2f} W/m2 time-averaged at {A['scans_per_min']:.0f} scans per minute; exempt limit 100 W/m2")
say("H3", f"Retinal thermal (weak visual stimulus), 850 nm: weighted radiance {L_eff:.0f} W/(m2 sr) against {L_lim:.0f}, "
          f"{L_eff / L_lim * 100:.1f} % of the exempt limit")
STATUS["R14"] = ("Met" if E200 < 100 and E24 * duty < 100 and L_eff < L_lim else "Not met",
                 f"{E200:.1f} W/m2 at 200 mm; {L_eff / L_lim * 100:.1f} % of retinal limit", "IEC 62471 exempt")

# ------------------------------------------------------------------ I. display
print("I. Display legibility (R7)")
def cr(lux):
    Lr = lux * A["screen_rho"] / pi
    return (A["disp_nits"] + Lr) / (A["disp_black_nits"] + Lr), Lr
cr_sun, Lr_sun = cr(A["E_sun_lux"])
cr_shade, Lr_shade = cr(A["E_shade_lux"])
say("I1", f"Direct sun {A['E_sun_lux'] / 1e3:.0f} klx: reflected {Lr_sun:.0f} cd/m2 on a {A['disp_nits']:.0f} cd/m2 screen, contrast {cr_sun:.1f}:1 "
          f"(needed {A['cr_needed']:.0f}:1)")
say("I2", f"Screen shaded from the sun ({A['E_shade_lux'] / 1e3:.0f} klx sky light): contrast {cr_shade:.1f}:1")
# I3: decided option (a): clip-on sun hood, walls on both sides and at the head end, open toward the user
from math import tan
ws, lh, hh = P["disp_win_w"], P["disp_win_l"], P["hood_h"]
full_side, full_head = degrees(atan(ws / hh)), degrees(atan(lh / hh))
fr = []
for ang in A["sun_angles"]:
    f_side = min(1.0, hh * tan(radians(ang)) / ws)
    f_head = min(1.0, hh * tan(radians(ang)) / lh)
    fr.append(f"{ang} deg: {f_side * 100:.0f} % (side), {f_head * 100:.0f} % (head)")
say("I3", f"Sun hood {hh:.0f} mm high over a {lh:.0f} x {ws:.0f} mm window: screen fully shaded when the sun is at least {full_side:.0f} deg "
          f"from the screen normal on a side, or {full_head:.0f} deg on the head end; open toward the user. Shaded share: " + "; ".join(fr))
say("I4", f"Shaded part of the screen {cr_shade:.1f}:1; sun over the open side or near the screen normal still gives {cr_sun:.1f}:1")
STATUS["R7"] = ("At risk", f"{cr_shade:.1f}:1 where the hood shades the screen; {cr_sun:.1f}:1 with the sun near the screen normal or over the open side",
                f"{A['cr_needed']:.0f}:1 in direct sun")

# ------------------------------------------------------------------ J. drop and temperature
print("J. Drop and temperature (R10, R11)")
g = 9.81
decel_shell = A["drop_h"] / A["stop_shell_m"]
decel_tpu = A["drop_h"] / A["stop_tpu_m"]
m_tot = (m_scanner) / 1000
say("J1", f"Drop {A['drop_h']} m: impact {m_tot * g * A['drop_h']:.1f} J; about {decel_shell:.0f} g on a shell corner "
          f"({A['stop_shell_m'] * 1e3:.0f} mm crush), about {decel_tpu:.0f} g on the shroud ({A['stop_tpu_m'] * 1e3:.0f} mm)")
say("J2", f"Cell retention needed on a corner drop {A['m_cell'] / 1000 * g * decel_shell:.0f} N; display board {A['m_board'] / 1000 * g * decel_shell:.0f} N")
dT = A["drift_limit"] / abs(A["led_tc"])
say("J3", f"LED output drifts {abs(A['led_tc']) * 100:.1f} %/°C: the 5 % drift warning trips after about {dT:.1f} °C change since the last white reference")
STATUS["R10"] = ("Not verifiable at TRL 3", f"corner drop about {decel_shell:.0f} g; cell needs {A['m_cell'] / 1000 * g * decel_shell:.0f} N retention", "1.2 m drop, IP54, 0 to 45 °C")
STATUS["R11"] = ("Met", f"PTFE cap reference; 5 % drift after about {dT:.0f} °C", "check in 10 s; warn at 5 %")

PROTO_ACCEPTED = 164.0   # USD: $163 accepted by Amish on 2026-09-25 (WSC-DDR-001 D2) plus the $1 sun hood (WSC-DDR-003)
# ------------------------------------------------------------------ K. cost
print("K. Cost (R12)")
rows = list(csv.DictReader((ROOT / "bom" / "bom.csv").open()))
total = sum(float(r["qty"]) * float(r["unit_cost_usd"]) for r in rows)
budget = float(yaml.safe_load((ROOT / "project.yaml").read_text())["budget_usd"])
optics = sum(float(r["qty"]) * float(r["unit_cost_usd"]) for r in rows if r["item"].startswith(("3 ", "4 ")))
say("K1", f"BOM {len(rows)} lines, total ${total:.2f}; budget_usd ${budget:.0f} (volume target); "
          f"{(total / budget - 1) * 100:+.1f} %; LEDs and photodiode ${optics:.2f} ({optics / total * 100:.0f} %)")
STATUS["R12"] = ("Met" if total <= PROTO_ACCEPTED else "Not met", f"${total:.2f} prototype", "about $164 prototype (accepted plus hood); $150 volume target")

# ------------------------------------------------------------------ L. requirement table
print("L. Requirement status")
STATUS["R8"] = ("Met", "price table on the device, offline", "editable local grades")
STATUS["R13"] = ("At risk", "shared record decided on this side (WSC-DDR-002 v0.2); not yet adopted by WasteWise-ml", "shared documented format")
order = ["Not met", "At risk", "Not verifiable at TRL 3", "Met"]
for rid in sorted(STATUS, key=lambda k: int(k[1:])):
    s, v, t = STATUS[rid]
    say("L1", f"  {rid:4s} {s:24s} value: {v}; target: {t}")
for s in order:
    ids = [k for k in sorted(STATUS, key=lambda k: int(k[1:])) if STATUS[k][0] == s]
    say("L2", f"{s}: {len(ids)} ({', '.join(ids) if ids else 'none'})")

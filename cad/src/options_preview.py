"""Provisional shaded preview of the concept options picture, media/options.png (WSC-OPT-001).

Run from the repo root:  python cad/src/options_preview.py
`python .kit/options.py` renders the kit 1.9 options picture in Blender Cycles on the coordinator's machine and
overwrites this file. Until then `render.py --check` still needs the picture, so this script draws each option's
D3 model (components(option) from cad/src/model.py, the same parts the fidelity check reads) with the kit's
shaded matplotlib renderer, at one scale, with the same hand beside each scanner. The header says it is a
preview, so it is never mistaken for the final render. Repo-specific helper; nothing here is in .kit/.
"""
import sys
import tempfile
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]

import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from PIL import Image  # noqa: E402
import concept  # noqa: E402
import model as M  # noqa: E402

INK, MUTED, ACCENT, WARN = "#111827", "#4B5563", "#0F766E", "#B45309"


def panel(key, path):
    parts = [concept.Part(p["name"], p["shape"], p["color"], p.get("bom")) for p in M.components(key)]
    v = M.OPTION_VIEWS.get(key, {})
    concept._render(parts, path, elev=v.get("el", 24), azim=v.get("az", -50), size=(5, 5), dpi=160)
    return Image.open(path).convert("RGB")


def main():
    keys = list(M.OPTIONS)
    n = len(keys)
    with tempfile.TemporaryDirectory() as tmp:
        imgs = [panel(k, Path(tmp) / f"wastewise-scan-opt-{k}.png") for k in keys]
    fig = plt.figure(figsize=(5.2 * n, 6.6), dpi=160)
    fig.text(0.015, 0.975, f"{M.TITLE}: concept options", fontsize=13, fontweight="bold", color=INK, va="top")
    fig.text(0.015, 0.935, "CONCEPT OPTIONS, NOT FOR FABRICATION. PROVISIONAL SHADED PREVIEW of the D3 models; the Cycles "
             "render replaces it. Same scale and the same hand in both panels.", fontsize=7.5, color=WARN, va="top")
    fig.text(0.985, 0.975, "github.com/BoujeeEnjinia1701/wastewise-scan", fontsize=8, color=ACCENT, va="top", ha="right",
             family="monospace")
    for i, (k, im) in enumerate(zip(keys, imgs)):
        ax = fig.add_axes([i / n + 0.01, 0.2, 1 / n - 0.02, 0.68])
        ax.imshow(im)
        ax.axis("off")
        fig.text(i / n + 0.02, 0.17, f"Option {k}: {M.OPTIONS[k]}", fontsize=11, fontweight="bold", color=INK, va="top")
        fig.text(i / n + 0.02, 0.12, textwrap.fill(M.PRINCIPLES.get(k, ""), 52), fontsize=8.5, color=MUTED, va="top")
        if k == M.CHOSEN:
            fig.text((i + 1) / n - 0.02, 0.17, "CURRENT DESIGN", fontsize=8, fontweight="bold", color=ACCENT, va="top", ha="right")
    out = ROOT / "media" / "options.png"
    fig.savefig(out, facecolor="white")
    plt.close(fig)
    print(f"wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

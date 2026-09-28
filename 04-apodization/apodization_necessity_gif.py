"""
GIF — Why apodization? Three cases sequential:
  Case 1: noisy FID, no window  → high noise floor
  Case 2: truncated FID          → sinc wiggles (Gibbs)
  Case 3: noisy FID + window     → clean spectrum
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patheffects as pe
import matplotlib.gridspec as gridspec

# ── palette ───────────────────────────────────────────────────────────────────
BG        = "#080B10"
PANEL_BG  = "#0D1117"
GRID      = "#141A24"
TEXT      = "#C8CDD8"
TEXT_DIM  = "#3D4A5C"
FID_DIM   = "#1A2535"
WATERMARK = "#2D3748"

C1 = "#FF6B35"   # case 1 — orange/red  (problem: noise)
C2 = "#FF3CAC"   # case 2 — pink        (problem: truncation)
C3 = "#00E5FF"   # case 3 — cyan        (solution)

# ── load ──────────────────────────────────────────────────────────────────────
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

data = np.load(os.path.join(SCRIPT_DIR, "necessity_data.npz"))
t          = data["t"]
freqs      = data["freqs"]
window     = data["window"]
fids       = [data["fid_case1"], data["fid_case2"], data["fid_case3"]]
spectra    = [data["sp_case1"],  data["sp_case2"],  data["sp_case3"]]
n          = len(t)

zoom_lo, zoom_hi = 0, 20
fmask = (freqs >= zoom_lo) & (freqs <= zoom_hi)
fq_z  = freqs[fmask]

# global ylims
fid_ymax  = max(np.abs(fids[0]).max(), np.abs(fids[2]).max()) * 1.12
spec_ymax = max(sp[fmask].max() for sp in spectra) * 1.15

# truncation boundary marker
trunc_idx = int(0.08 * n)
t_trunc   = t[trunc_idx]

# ── case metadata ─────────────────────────────────────────────────────────────
cases = [
    {
        "color":   C1,
        "title":   "Case 1 — No apodization",
        "problem": "noise dominates late FID → elevated baseline",
        "fid_label": "noisy FID  (no window)",
        "annotation": "noise persists\nthroughout FID",
        "ann_xy": (1.5, 0.38),
        "arr_xy": (1.5, 0.12),
    },
    {
        "color":   C2,
        "title":   "Case 2 — Truncated FID",
        "problem": "sinc ringing  (truncation artifact)",
        "fid_label": "FID cut short  (hard truncation)",
        "annotation": "rectangular window\n→ sinc convolution\n→ ringing",
        "ann_xy": (14.5, 0.72),
        "arr_xy": (13.0, 0.55),
    },
    {
        "color":   C3,
        "title":   "Case 3 — With apodization  ✓",
        "problem": "",
        "fid_label": "noisy FID  (dim)  ×  window  (dashed)  =  weighted FID",
        "annotation": "smooth decay\n→ reduced ringing\n· better SNR appearance",
        "ann_xy": (14.5, 0.72),
        "arr_xy": (12.0, 0.60),
    },
]

# ── glow ──────────────────────────────────────────────────────────────────────
def glow(color, lw):
    return [
        pe.Stroke(linewidth=lw+8, foreground=color, alpha=0.07),
        pe.Stroke(linewidth=lw+3, foreground=color, alpha=0.17),
        pe.Normal(),
    ]

# ── figure ────────────────────────────────────────────────────────────────────
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9})

fig = plt.figure(figsize=(12, 7.4), dpi=100, facecolor=BG)
gs  = gridspec.GridSpec(
    2, 1, figure=fig,
    height_ratios=[1, 1.1],
    hspace=0.40,
    left=0.09, right=0.96,
    top=0.84, bottom=0.09,
)
ax_fid  = fig.add_subplot(gs[0])
ax_spec = fig.add_subplot(gs[1])

def style(ax, xlabel="", ylabel=""):
    ax.set_facecolor(PANEL_BG)
    for sp in ax.spines.values():
        sp.set_color("#1A2236"); sp.set_linewidth(0.8)
    ax.tick_params(colors=TEXT_DIM, labelsize=8, length=3)
    ax.grid(True, color=GRID, linewidth=0.5)
    if xlabel: ax.set_xlabel(xlabel, color=TEXT_DIM, fontsize=9, labelpad=4)
    if ylabel: ax.set_ylabel(ylabel, color=TEXT_DIM, fontsize=9, labelpad=4)

style(ax_fid,  xlabel="time  (s)",       ylabel="amplitude")
style(ax_spec, xlabel="frequency  (Hz)", ylabel="amplitude")

ax_fid.set_xlim(t[0], t[-1])
ax_fid.set_ylim(-fid_ymax, fid_ymax)
ax_spec.set_xlim(zoom_lo, zoom_hi)
ax_spec.set_ylim(0, spec_ymax)

# ── header ─────────────────────────────────────────────────────────────────────
fig.text(0.05, 0.957, "WHY APODIZATION?", color="#FFFFFF",
         fontsize=20, fontweight="bold", va="top",
         path_effects=[pe.Stroke(linewidth=5, foreground="#FFFFFF", alpha=0.12),
                       pe.Normal()])
fig.text(0.05, 0.913, "three scenarios — what goes wrong without it",
         color=TEXT_DIM, fontsize=10, va="top", style="italic")

ax_fid.set_title("FID  (time domain)", color=TEXT, fontsize=10,
                  fontweight="bold", loc="left", pad=6)
ax_spec.set_title("spectrum  (after Fourier Transform)", color=TEXT,
                   fontsize=10, fontweight="bold", loc="left", pad=6)

fig.text(0.965, 0.018, "nmrx.ir", color=WATERMARK, fontsize=12,
          fontweight="bold", ha="right", va="bottom")

# ── static raw FID (dim background) ───────────────────────────────────────────
ax_fid.plot(t, fids[0].real, color=FID_DIM, lw=0.7, zorder=1)

# ── dynamic artists ────────────────────────────────────────────────────────────
(fid_line,)  = ax_fid.plot([],  [], lw=1.5, zorder=3)
fid_fill     = [None]
(win_line,)  = ax_fid.plot([],  [], lw=1.8, ls="--", zorder=4, alpha=0.85)
(spec_line,) = ax_spec.plot([], [], lw=2.2, zorder=3)
spec_fill2   = [None]

# ── noise inset (Case 1 only) — shows tail of FID where noise dominates ──────
ax_inset = ax_fid.inset_axes([0.55, 0.55, 0.42, 0.40])
ax_inset.set_facecolor("#080F18")
for sp in ax_inset.spines.values():
    sp.set_color(C1); sp.set_linewidth(0.9)
ax_inset.tick_params(colors=TEXT_DIM, labelsize=7, length=2)
ax_inset.set_xlim(6.0, 8.2)
# inset ylim: just noise range
inset_ylim = 6.0
ax_inset.set_ylim(-inset_ylim, inset_ylim)
ax_inset.set_title("tail  (noise only)", color=C1, fontsize=7.5,
                    fontweight="bold", loc="center", pad=3)
ax_inset.axhline(0, color=TEXT_DIM, lw=0.4, alpha=0.4)
(inset_line,) = ax_inset.plot([], [], color=C1, lw=0.9,
                               path_effects=glow(C1, 0.9))
inset_visible = [False]

# truncation marker (case 2 only)
trunc_vline = ax_fid.axvline(x=t_trunc, color=C2, lw=1.2,
                               ls=(0,(4,3)), alpha=0.0, zorder=5)
trunc_label = ax_fid.text(
    t_trunc + 0.02, fid_ymax * 0.88, "cutoff",
    color=C2, fontsize=8.5, va="top", alpha=0.0,
    bbox=dict(facecolor=PANEL_BG, edgecolor=C2,
               linewidth=0.8, boxstyle="round,pad=0.35", alpha=0.0),
)

# case label box (top-left of FID)
case_label = ax_fid.text(
    0.02, 0.97, "", transform=ax_fid.transAxes,
    color=TEXT, fontsize=11, fontweight="bold", va="top", ha="left",
    bbox=dict(facecolor=PANEL_BG, edgecolor="#2A3448",
               linewidth=1.1, boxstyle="round,pad=0.5", alpha=0.93),
)
fid_sublabel = ax_fid.text(
    0.02, 0.72, "", transform=ax_fid.transAxes,
    color=TEXT_DIM, fontsize=8.5, va="top", ha="left", family="monospace",
)

# problem label (top of spectrum)
prob_label = ax_spec.text(
    0.98, 0.97, "", transform=ax_spec.transAxes,
    color=TEXT, fontsize=10, fontweight="bold", va="top", ha="right",
    bbox=dict(facecolor=PANEL_BG, edgecolor="#2A3448",
               linewidth=1.1, boxstyle="round,pad=0.5", alpha=0.93),
)

# annotation on spectrum (wiggles / noise etc.)
spec_ann = ax_spec.annotate(
    "", xy=(7.0, 0.5), xytext=(14.0, 0.7),
    xycoords=("data", "axes fraction"),
    textcoords=("data", "axes fraction"),
    color=TEXT, fontsize=8.5,
    bbox=dict(facecolor=PANEL_BG, edgecolor="#2A3448",
               linewidth=0.8, boxstyle="round,pad=0.4", alpha=0),
    arrowprops=dict(arrowstyle="-|>", color=TEXT_DIM, lw=1.0, alpha=0),
)

# progress dots
dots = []
labels_dot = ["1", "2", "3"]
for i in range(3):
    d = fig.text(0.5 + (i - 1) * 0.055, 0.005, f"●  {labels_dot[i]}",
                 color=TEXT_DIM, fontsize=10, ha="center", va="bottom")
    dots.append(d)

# ── timing ────────────────────────────────────────────────────────────────────
DRAW  = 45
HOLD  = 22
FADE  = 10
PHASE = DRAW + HOLD + FADE
TOTAL = 3 * PHASE + HOLD

def update(frame):
    ci        = min(frame // PHASE, 2)
    pf        = frame % PHASE
    c         = cases[ci]
    color     = c["color"]
    fid_data  = fids[ci]
    sp_data   = spectra[ci]

    if pf < DRAW:
        prog      = pf / DRAW
        alpha_out = 1.0
    elif pf < DRAW + HOLD:
        prog      = 1.0
        alpha_out = 1.0
    else:
        prog      = 1.0
        fade_t    = (pf - DRAW - HOLD) / FADE
        alpha_out = max(0.0, 1.0 - fade_t)

    n_show = max(1, int(prog * n))
    nf     = max(1, int(prog * fmask.sum()))

    # FID line
    fid_line.set_data(t[:n_show], fid_data.real[:n_show])
    fid_line.set_color(color)
    fid_line.set_alpha(alpha_out * 0.85)
    fid_line.set_path_effects(glow(color, 1.5))

    if fid_fill[0] is not None:
        fid_fill[0].remove()
    fid_fill[0] = ax_fid.fill_between(
        t[:n_show], fid_data.real[:n_show],
        color=color, alpha=0.05 * alpha_out, zorder=2)

    # window overlay (case 3 only) — show window shape + weighted FID
    if ci == 2:
        # show window envelope
        win_line.set_data(t[:n_show], window[:n_show] * fid_ymax * 0.88)
        win_line.set_color(C3)
        win_line.set_alpha(alpha_out * 0.75)
        win_line.set_path_effects(glow(C3, 1.8))
        # draw weighted FID (noisy_fid × window), not raw FID
        fid_line.set_data(t[:n_show], (fids[2].real * window)[:n_show])
        fid_line.set_color(C3)
        fid_line.set_alpha(alpha_out * 0.9)
    else:
        win_line.set_data([], [])

    # inset: show only for Case 1, fade in during hold phase
    if ci == 0 and prog > 0.7:
        a_inset = min((prog - 0.7) / 0.3, 1.0) * alpha_out
        ax_inset.set_visible(True)
        inset_mask = (t >= 6.0) & (t <= 8.2)
        inset_line.set_data(t[inset_mask], fids[0].real[inset_mask])
        inset_line.set_alpha(a_inset)
        ax_inset.patch.set_alpha(a_inset * 0.9)
        for sp in ax_inset.spines.values():
            sp.set_alpha(a_inset)
    else:
        ax_inset.set_visible(False)
        inset_line.set_data([], [])

    # truncation marker (case 2)
    trunc_alpha = alpha_out if ci == 1 else 0.0
    trunc_vline.set_alpha(trunc_alpha * 0.8)
    trunc_label.set_alpha(trunc_alpha)
    trunc_label.get_bbox_patch().set_alpha(trunc_alpha * 0.88)

    # spectrum
    spec_line.set_data(fq_z[:nf], sp_data[fmask][:nf])
    spec_line.set_color(color)
    spec_line.set_alpha(alpha_out)
    spec_line.set_path_effects(glow(color, 2.2))

    if spec_fill2[0] is not None:
        spec_fill2[0].remove()
    spec_fill2[0] = ax_spec.fill_between(
        fq_z[:nf], sp_data[fmask][:nf],
        color=color, alpha=0.08 * alpha_out, zorder=2)

    # labels
    case_label.set_text(c["title"])
    case_label.set_color(color)
    case_label.set_alpha(alpha_out)
    fid_sublabel.set_text(c["fid_label"])
    fid_sublabel.set_alpha(alpha_out * 0.75)

    prob_txt = f"⚠  {c['problem']}" if c["problem"] else "✓  reduced ringing  ·  better SNR appearance"
    prob_col = "#FF4444" if c["problem"] else "#44FF88"
    prob_label.set_text(prob_txt)
    prob_label.set_color(prob_col)
    prob_label.set_alpha(alpha_out if prog > 0.5 else 0.0)

    # annotation
    if prog > 0.85 and alpha_out > 0.3:
        a = min((prog - 0.85) / 0.15, 1.0) * alpha_out
        spec_ann.set_text(c["annotation"])
        spec_ann.set_color(color)
        spec_ann.xy        = c["arr_xy"]
        spec_ann.xyann     = c["ann_xy"]
        spec_ann.get_bbox_patch().set_alpha(0.88 * a)
        spec_ann.arrow_patch.set_alpha(a * 0.7)
    else:
        spec_ann.get_bbox_patch().set_alpha(0)
        spec_ann.arrow_patch.set_alpha(0)
        spec_ann.set_text("")

    # dots
    for i, d in enumerate(dots):
        if i < ci:
            d.set_color(TEXT_DIM); d.set_alpha(0.5)
        elif i == ci:
            d.set_color(color); d.set_alpha(alpha_out)
        else:
            d.set_color(TEXT_DIM); d.set_alpha(0.2)

    return [fid_line, win_line, spec_line,
            case_label, fid_sublabel, prob_label,
            trunc_vline, trunc_label, inset_line] + dots


ani = animation.FuncAnimation(
    fig, update, frames=TOTAL, interval=110, blit=False)

out = os.path.join(SCRIPT_DIR, "apodization_necessity.mp4")
ani.save(out, writer=animation.FFMpegWriter(fps=8, bitrate=1800,
         extra_args=["-vcodec", "libx264", "-pix_fmt", "yuv420p"]),
         savefig_kwargs={"facecolor": BG})
print(f"Saved → {out}")

# 04 — Apodization: Why Window Functions Matter

**See what happens to your spectrum when you ignore the tail of the FID.**

---

## The Idea

When an NMR instrument records a signal, it keeps listening long after the molecules have stopped talking.

The FID (Free Induction Decay) starts strong — real signal, real information.
But as time goes on, the signal decays. What remains is noise.

If you take that noisy tail and feed it directly into the Fourier Transform, it contaminates your spectrum.

The fix is **apodization**: multiplying the FID by a window function that smoothly suppresses the tail — like resting your finger on a guitar string after the note has already sounded.

> Apodization is not noise removal.
> It is a mathematical re-weighting of the FID in the time domain —
> with real consequences for linewidth, resolution, and spectral appearance.

---

## What This Visualization Shows

Three scenarios, compared side by side:

| Case | Setup | Problem |
|------|-------|---------|
| **1 — No apodization** | Full noisy FID, no window | Noise dominates the late FID → elevated spectral baseline |
| **2 — Truncated FID** | Hard cutoff at 8% of acquisition | Rectangular window → sinc convolution → ringing artifacts |
| **3 — With apodization** | Noisy FID × exponential window (LB = 0.2 Hz) | Reduced ringing · better SNR appearance (with linewidth cost) |

Each case shows the FID in the time domain and the resulting spectrum after Fourier Transform.

---

## Files

```
04-apodization/
├── generate_necessity_data.py     # generates the synthetic FID data
├── apodization_necessity_gif.py   # produces the animation
├── necessity_data.npz             # pre-generated data (numpy archive)
├── apodization_necessity.mp4      # output animation
└── README.md
```

---

## Reproducing the Animation

**1 — Install dependencies**

```bash
pip install numpy matplotlib scipy
```

You also need `ffmpeg` installed and on your PATH for `.mp4` output.
Download from: https://ffmpeg.org/download.html

**2 — Generate the data** *(skip if using the pre-generated `.npz`)*

```bash
python generate_necessity_data.py
```

**3 — Render the animation**

```bash
python apodization_necessity_gif.py
```

Output: `apodization_necessity.mp4`

---

## Data Details

The synthetic FID contains two complex Lorentzian signals:

| Parameter | Value |
|-----------|-------|
| Peak 1 | 7 Hz, amplitude 9.0 |
| Peak 2 | 10 Hz, amplitude 6.0 |
| T2* | 2.0 s |
| Noise | Complex Gaussian, σ = 1.5 |
| Points | 8192 |
| Dwell time | 1 ms |
| Frequency resolution | 0.122 Hz/pt |

All FIDs are **complex** (`complex128`) — consistent with real NMR acquisition.
FFT is applied to the full complex signal; the positive-frequency half is displayed.

---

## Scientific Notes

- **Case 2 uses the same noisy FID** as Cases 1 and 3 (truncated at 8%), so the comparison is fair across all three scenarios.
- **Apodization ≠ denoising.** The window multiplies both signal and noise. What changes is their relative contribution across the time axis.
- The exponential window used here adds LB = 0.2 Hz to the natural linewidth. This is visible as a small but real broadening of the peaks in Case 3.
- The term *Gibbs artifact* is avoided intentionally. What appears in Case 2 is **sinc ringing from rectangular windowing** (finite acquisition + hard truncation), not the Gibbs phenomenon in its strict mathematical sense.

---

## Related Visualizations

This is part of a series on apodization:

- `04-apodization` ← you are here — *why* apodization matters
- `05-apodization-tradeoff` *(coming)* — *how much* to apply: LB vs FWHM vs SNR

---

*Built alongside [nmrx.ir](https://nmrx.ir) — an open-source NMR analysis platform.*

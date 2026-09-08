# Larmor Precession in NMR — Bloch Equation Simulation

I thought I understood the Bloch equation. Then I tried to implement it.

The first version had five physics errors I couldn't see. This is version eight.

---

## What This Is

A Python animation of Larmor precession and the NMR signal chain — from equilibrium magnetization through a 90° RF pulse to FID acquisition and Fourier transform.

Built with `matplotlib`, `numpy`, and `scipy`. Renders to MP4 via `FFmpeg`.

---

## Physics

The simulation solves the **rotating-frame Bloch equation** using RK4:

```
dM/dt = γ(M × B_eff) − relaxation
```

Three stages:

| Stage | B_eff | Notes |
|-------|-------|-------|
| Pre-pulse | `[0, 0, 0]` | On resonance; M stays at equilibrium |
| RF pulse | `[0, −B₁, 0]` | γB₁t = π/2 → exact 90° flip |
| Post-pulse | `[0, 0, Δω/γ]` | Rotating-frame offset; FID decays with T₂ |

**Parameters:** B₀ = 9.4 T · ω₀/2π ≈ 400 MHz · T₁ = 1.5 s · T₂ = 0.8 s · Δf = 4.2 Hz

---

## What Was Fixed Across Versions

These are real errors, not style preferences:

- **v1–v2:** Lab-frame Bloch integration at 400 MHz with dt = 1/30 s — numerically invalid
- **v3–v4:** 3D visualization and FID came from two separate trajectories while claiming "Bloch simulation"
- **v5–v6:** RF pulse was an instantaneous manual rotation, not an integrated ODE
- **v7:** FFT included the pulse frames (180–210), not just the post-pulse FID
- **v8:** All fixed. Single rotating-frame trajectory. B₁(t) properly integrated. FFT from POST_PULSE onward.

---

## Known Simplifications

| Item | Status |
|------|--------|
| FID = Re[Mxy] only | Accepted simplification for visualization |
| RF pulse duration = 1s | Animation only — real ¹H pulse ≈ 10 µs, noted in video |
| Pre-pulse 3D = conceptual θ=22° | Labeled explicitly; Bloch gives M=[0,0,1] |
| Δf = 4.2 Hz | FPS-limited demo; 1 ppm at 400 MHz = 400 Hz |
| Hann-windowed FFT vs ideal Lorentzian | Not identical; analytical overlay shown for comparison |

---

## Output

The script produces two files:

```
larmor_silent_v8.mp4   — video only
larmor_with_tone_v8.mp4 — video + 432 Hz tone decaying with T₂
```

---

## Requirements

```bash
pip install numpy matplotlib scipy
# FFmpeg must be installed and on PATH
```

---

## Run

```bash
python larmor_v8.py
```

Renders 750 frames (25 s) at 30 FPS, 1980×1100 px, ~1 MB output.

---

## References

- Bloch, F. (1946). *Nuclear Induction.* Physical Review, 70(7–8), 460.
- Levitt, M. H. (2008). *Spin Dynamics.* Wiley.
- Ernst, R. R., Bodenhausen, G., Wokaun, A. (1987). *Principles of Nuclear Magnetic Resonance in One and Two Dimensions.* Oxford.

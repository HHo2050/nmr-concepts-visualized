# nmr-concepts-visualized

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Posts](https://img.shields.io/badge/Animations-1-orange?style=flat-square)
![nmrx.ir](https://img.shields.io/badge/Built_alongside-nmrx.ir-purple?style=flat-square)

Python animations for NMR and DSP concepts — built to make the math visible.

Each animation targets a specific phenomenon: aliasing, Fourier transform,
phase correction, baseline drift. The goal is not illustration for its own sake
but understanding the signal-level mechanics that determine whether an NMR
spectrum is trustworthy or not.

Each folder is self-contained. Download only what you need.

---

## Animations

### 02-1 — Nyquist Aliasing: Wagon Wheel Effect

![Nyquist Aliasing](02-nyquist-aliasing/nyquist_wheel.gif)

A car wheel spinning forward — but appearing to go backward.
The same math that places NMR peaks in the wrong position in the spectrum.

→ [Code + full breakdown](./02-nyquist-aliasing/)

---

## Background

These animations grew out of building [nmrx.ir](https://nmrx.ir) — an
open-source NMR analysis tool — and working through the signal processing
theory behind functions I was already using in code: autophase, baseline
correction, peak fitting. At some point the math became clearer through
animation than through equations alone.

The series covers the DSP foundations of NMR: sampling theory, Fourier
analysis, windowing, filtering, phase and baseline correction — and how
each one affects what you see (or misread) in the spectrum.

---

## Requirements

Each folder has its own README with exact dependencies.
Common base:

```bash
pip install matplotlib numpy pillow
```

---

## Author

Seyyed Mostafa Moosavi — Chemist with a focus on NMR signal processing and
chemoinformatics. Building nmrx.ir as an open-source NMR analysis platform.

[GitHub](https://github.com/HHo2050) · [nmrx.ir](https://nmrx.ir)
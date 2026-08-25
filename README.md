# NMR Concepts Visualized

> **Making NMR signal processing visible.**

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=flat-square\&logo=python\&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-2ea44f?style=flat-square)
![Animations](https://img.shields.io/badge/Animations-1-orange?style=flat-square)
![NMR](https://img.shields.io/badge/NMR-DSP-7c3aed?style=flat-square)

**NMR × DSP × Visual Thinking**

This project turns the signal-processing concepts behind NMR into short,
self-contained Python animations.

Not just pictures.

**The goal is to make the mathematics visible.**

---

## 🎬 Animations

### 02 — Nyquist Aliasing

**The Wagon Wheel Effect**

![Nyquist Aliasing](02-nyquist-aliasing/nyquist_wheel.gif)

A wheel is rotating forward.

But at the wrong sampling rate, it appears to rotate **backward**.

That isn't an optical trick.

It's **aliasing** — the same phenomenon that can make an NMR frequency
appear at the wrong position in a spectrum.

**→ [Explore the animation & mathematics](./02-nyquist-aliasing/)**

**▶ [Watch the demo](VIDEO_LINK_HERE)**

---

## 🧠 Why this project?

NMR processing is full of concepts that are mathematically simple but
difficult to visualize:

* Sampling & Nyquist limits
* Fourier transformation
* Window functions
* Filtering
* Phase correction
* Baseline distortion
* Frequency-domain artifacts

Equations describe these effects.

**Animations let you see them happen.**

The goal is to build an intuition for what is happening at the
**signal level** — before it becomes a peak, a spectrum, or an artifact.

---

## 🧪 From code to understanding

The project grew out of work on **[nmrx.ir](https://nmrx.ir)**,
an open-source NMR analysis platform.

While implementing functions such as:

```text
Autophasing
Baseline correction
Peak detection
Peak fitting
Fourier processing
```

the underlying DSP became increasingly important.

Some concepts were easier to understand by **watching the signal change**
than by reading another equation.

That's where this project started.

---

## 🗂️ Project structure

Each animation is intentionally self-contained:

```text
nmr-concepts-visualized/
│
├── 02-nyquist-aliasing/
│   ├── nyquist_car_v4.py
│   ├── nyquist_wheel.gif
│   └── README.md
│
└── README.md
```

You can explore or run an individual concept without needing the rest
of the repository.

---

## ⚙️ Requirements

Most animations use:

```bash
pip install matplotlib numpy pillow
```

Each folder contains its own README with the exact dependencies and
instructions required for that animation.

---

## 🔬 The bigger picture

This is a growing visual library for the DSP foundations of NMR.

```text
Sampling
   ↓
Fourier Transform
   ↓
Windowing
   ↓
Filtering
   ↓
Phase
   ↓
Baseline
   ↓
Peak Detection
   ↓
Quantitative NMR
```

The long-term goal is simple:

> **Make the signal-processing mechanics of NMR intuitive enough to see
> before you calculate them.**

---

## 👨‍🔬 Author

**Seyyed Mostafa Moosavi**

Chemist focused on **NMR signal processing and chemoinformatics**.

Building **[nmrx.ir](https://nmrx.ir)** as an open-source NMR analysis platform.

[GitHub](https://github.com/HHo2050) · [nmrx.ir](https://nmrx.ir)

---

### Built with Python · NMR · DSP · Curiosity

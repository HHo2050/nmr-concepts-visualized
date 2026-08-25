# NMR Concepts Visualized

> **See the signal. Understand the math.**

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=flat-square\&logo=python\&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-2ea44f?style=flat-square)
![Animations](https://img.shields.io/badge/Visualizations-Growing-orange?style=flat-square)
![NMR](https://img.shields.io/badge/NMR-DSP-7c3aed?style=flat-square)

**NMR × DSP × Computational Analysis**

A growing collection of Python animations that make the mathematics and
signal-level mechanics behind **NMR data processing** visible.

Not illustration for its own sake.

**The goal is understanding.**

---

## 🎬 Visual Library

Some NMR and DSP concepts are difficult to understand from equations alone.

This project turns those concepts into short, visual experiments — showing
what actually happens to a signal when it is sampled, transformed, processed,
or misinterpreted.

A single concept may be explored through **multiple visualizations**, each
showing a different side of the same underlying mechanism.

The library is intentionally open-ended.

New visualizations will be added as interesting concepts, problems, and
connections emerge across **NMR, DSP, and computational analysis**.

> **No fixed curriculum. No filler. Just useful ideas made visual.**

---

## 🧪 Current Visualizations

### 01 — Nyquist Aliasing

#### 🌊 Frequency Aliasing

A simple signal-level demonstration of what happens when a frequency is
sampled below the Nyquist limit.

The original signal and its sampled representation reveal how a frequency
can become indistinguishable from a different, lower-frequency signal.

**NMR connection:**
The same principle explains why signals outside the observable bandwidth
can fold back into the spectrum.

→ **[Explore the visualization](./01-nyquist-aliasing/)**

---

#### 🚗 Wagon Wheel Effect

A wheel rotates forward.

But when viewed through discrete samples, it can appear to rotate backward.

This familiar visual phenomenon is a direct and intuitive demonstration of
**aliasing**.

The same mathematics appears in NMR when a signal is sampled too slowly and
its frequency is observed at the wrong position.

→ **[Explore the visualization](./02-nyquist-aliasing/)**

---

## 🧠 Why Visualize NMR?

NMR processing contains a lot of mathematics that normally stays hidden
behind software:

* Sampling
* Fourier transformation
* Windowing
* Filtering
* Phase correction
* Baseline correction
* Frequency-domain artifacts
* Peak detection
* Quantitative analysis

A spectrum can look perfectly reasonable while the underlying signal
processing has introduced an artifact.

Understanding **why** something happens is therefore just as important as
knowing **which button to press**.

This project is an attempt to make those mechanisms visible.

---

## 🔬 From Signal to Spectrum

At its core, the project follows the computational path of NMR data:

```text
                 NMR Signal
                     │
                     ▼
                 Sampling
                     │
                     ▼
              Digital Signal
                     │
                     ▼
            Signal Processing
                     │
                     ▼
            Fourier Transform
                     │
                     ▼
                  Spectrum
                     │
                     ▼
              Interpretation
```

Every step introduces assumptions.

Every assumption can affect what we see.

The animations focus on making those transformations easier to reason about.

---

## ⚠️ When Processing Goes Wrong

Many spectral problems are not caused by the chemistry.

They can come from the way the signal was **sampled or processed**.

```text
Sampling
    │
    ├── insufficient bandwidth
    │          ↓
    │       Aliasing
    │
    ├── inappropriate processing
    │          ↓
    │       Artifacts
    │
    └── distorted signal
               ↓
         Misinterpretation
```

Understanding these failure modes is particularly important when moving from
visual inspection toward **quantitative NMR and computational analysis**.

---

## 🗂️ Project Structure

Each visualization is designed to be as self-contained as possible.

```text
nmr-concepts-visualized/
│
├── 01-...
│   ├── animation.py
│   ├── animation.gif
│   └── README.md
│
├── 02-...
│   ├── animation.py
│   ├── animation.gif
│   └── README.md
│
├── ...
│
└── README.md
```

A concept may contain **multiple visualizations**.

For example:

```text
Nyquist Aliasing
├── Frequency-domain / waveform demonstration
└── Wagon Wheel demonstration
```

The numbering reflects the order in which material is added.

It is **not a fixed curriculum or publication roadmap**.

That allows the library to grow naturally as new ideas and useful
visualizations emerge.

---

## ⚙️ Requirements

Most visualizations use Python with a small set of scientific libraries:

```bash
pip install matplotlib numpy pillow
```

Individual directories may have additional dependencies.

Check the `README.md` inside each visualization for its exact requirements
and execution instructions.

---

## ▶️ Running a Visualization

Enter the directory of the visualization you want to explore:

```bash
cd <visualization-directory>
```

Install its dependencies and run the provided Python script:

```bash
python <script>.py
```

The generated animation will be saved according to the configuration
specified by that visualization.

---

## 🎯 Design Philosophy

### 1. Make the invisible visible

Signal processing often involves transformations that are mathematically
obvious but visually abstract.

Animations expose those transformations.

### 2. Start with intuition

The viewer should understand the phenomenon visually before being asked to
follow the mathematics.

### 3. Keep the mathematics honest

The visual explanation should simplify the concept — **not distort it**.

### 4. Connect everything back to NMR

These are not generic DSP animations.

The purpose is to understand the signal-processing mechanisms that ultimately
affect NMR data and spectral interpretation.

---

## 🌐 Why This Exists

The project grew out of work on **[nmrx.ir](https://nmrx.ir)**, an open-source
NMR analysis platform.

While working with functions such as Fourier processing, phase correction,
baseline correction, peak detection, and quantitative analysis, it became
clear that many of the underlying concepts are easier to understand when
they can be **seen happening**.

This repository is a companion visual layer to that work.

---

## 🔭 Bigger Picture

The project sits at the intersection of:

**NMR × DSP × Computational Analysis × Machine Learning**

with a particular interest in understanding how signal-level information
propagates through the computational pipeline.

The long-term direction is not simply to create more animations.

It is to build a visual intuition for the computational foundations that
support modern NMR analysis.

---

## 👨‍🔬 Author

**Seyyed Mostafa Moosavi**

Chemist focused on **NMR signal processing and chemoinformatics**.

Building **[nmrx.ir](https://nmrx.ir)** as an open-source NMR analysis platform.

**[GitHub](https://github.com/HHo2050)** · **[nmrx.ir](https://nmrx.ir)**

---

## 📜 License

This project is released under the **MIT License**.

---

### Built with Python · NMR · DSP · Curiosity

> **See the signal. Understand the math.**

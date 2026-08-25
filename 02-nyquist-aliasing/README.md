# NMR Concepts Visualized

> **See the signal. Understand the math.**

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=flat-square\&logo=python\&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-2ea44f?style=flat-square)
![NMR](https://img.shields.io/badge/NMR-DSP-7c3aed?style=flat-square)
![nmrx.ir](https://img.shields.io/badge/Built_alongside-nmrx.ir-00A693?style=flat-square)

Python animations for **NMR, DSP, and computational signal analysis** — built to make the mathematics visible.

---

## 🚗 02 — Nyquist Aliasing

### The Wagon Wheel Effect

> **Why can a wheel spin forward… while your eyes see it moving backward?**

![Nyquist Aliasing — Wagon Wheel Effect](02-nyquist-aliasing/nyquist_wheel.gif)

**🎬 Watch the video → [Wagon Wheel Effect — Nyquist Aliasing](VIDEO_LINK_HERE)**

A car wheel is rotating **forward**.

Then something strange happens:

**the wheel appears to rotate backward.**

Nothing about the wheel changed.

**The sampling did.**

This is the **Nyquist aliasing effect** — the same mathematical phenomenon that can make an NMR signal appear at the **wrong frequency**.

---

## 🧠 The idea

The wheel has **6 spokes**.

That means the visual pattern repeats every:

**60°**

At a sufficiently slow rotation, consecutive frames represent the true motion.

But when the rotation becomes too fast relative to the sampling rate, the next frame can be interpreted as a small movement in the opposite direction.

The result:

|                | True motion | Sampled motion | Perception   |
| -------------- | ----------: | -------------: | ------------ |
| 🟢 **TRUE**    |  −20°/frame |     −20°/frame | Forward      |
| 🔴 **ALIASED** |  −52°/frame |      +8°/frame | **Backward** |

> **The samples are real.
> The interpretation is wrong.**

---

## 📐 The mathematics

For a periodic pattern, the observed motion can be written as:

```text
alias = true − round(true / period) × period
```

For the aliased case:

```text
alias = −52 − round(−52 / 60) × 60
      = −52 − (−60)
      = +8°/frame
```

The wheel is **actually rotating −52°/frame**.

But because the visual pattern repeats every **60°**, the sampled frames are indistinguishable from a wheel rotating **+8°/frame**.

That is aliasing.

---

## 🧪 Why NMR?

The wagon-wheel effect is not merely a visual illusion.

It is an intuitive demonstration of the same sampling principle behind
**frequency aliasing in NMR**.

An NMR signal is sampled discretely:

```text
Continuous signal
       ↓
    Sampling
       ↓
 Discrete samples
       ↓
      FFT
       ↓
   Spectrum
```

If a signal contains frequencies beyond the **Nyquist limit**, those frequencies can fold back into the observable spectral range.

A peak can therefore appear at a frequency that is **different from its true frequency**.

### 🚗 → 📡

| Wagon Wheel              | NMR                  |
| ------------------------ | -------------------- |
| Rotation frequency       | Signal frequency     |
| Camera frames            | NMR samples          |
| Spoke periodicity        | Sampling periodicity |
| Apparent backward motion | Aliased frequency    |
| Faster camera            | Faster sampling      |

---

## 🔬 The NMR connection

The sampling interval is the **dwell time**:

```text
Δt = 1 / SW
```

where `SW` is the spectral width.

Increasing the spectral width decreases the dwell time and therefore increases the sampling rate.

The basic Nyquist requirement is:

```text
SW ≥ 2 × fmax
```

where `fmax` is the highest frequency that needs to be represented.

### The same problem — different system.

**Wheel:**
Fast rotation + insufficient sampling → apparent backward motion

**NMR:**
High-frequency signal + insufficient sampling → frequency aliasing

---

## 🎬 Animation

| Property   | Value           |
| ---------- | --------------- |
| Resolution | `1200 × 675 px` |
| Frame rate | `10 FPS`        |
| Duration   | `~22 s`         |

```text
00–07 s   →   True forward rotation
07–10 s   →   Transition
10–19 s   →   Aliased / apparent backward rotation
19–22 s   →   End
```

---

## ⚙️ Run it yourself

### Install

```bash
pip install matplotlib numpy pillow
```

### Run

```bash
python nyquist_car_v4.py
```

The GIF is saved to the path defined by `out_path` at the bottom of the script.

Change that path to your preferred directory before running.

---

## 🎯 The takeaway

> **Aliasing doesn't change the signal.
> It changes what the samples allow you to see.**

A wheel can appear to rotate backward.

An NMR peak can appear at the wrong frequency.

**Same mathematics. Different system.**

---

## 🔗 Explore the project

**[← Back to NMR Concepts Visualized](../)**

A growing visual library exploring the signal-processing foundations of NMR:

**NMR × DSP × Computational Analysis**

---

### Built with Python · NMR · DSP · Visual Thinking

# 🚗 02 — Nyquist Aliasing: The Wagon Wheel Effect

> **Why can a wheel spin forward… while your eyes see it moving backward?**

![Wagon Wheel Aliasing Animation](nyquist_aliasing.gif)

### 🎯 One visual. One illusion. One fundamental DSP concept.

A car wheel is rotating **forward**.

Then, as the sampling rate changes, something strange happens:

**the wheel appears to rotate backward.**

Nothing about the wheel changed.

The **sampling** did.

This is the **Nyquist aliasing effect** — the same mathematical phenomenon that can make an NMR signal appear at the **wrong frequency**.

---

## 🧠 What you're seeing

The wheel has **6 spokes**, so identical visual patterns repeat every:

**60°**

When the wheel rotates slowly enough, every frame correctly represents its motion.

But when the rotation becomes too fast relative to the sampling rate, the next frame can look as if the wheel has moved **slightly backward**.

The motion has been **aliased**.

|                | True motion | Sampled motion | What we see  |
| -------------- | ----------: | -------------: | ------------ |
| 🟢 **TRUE**    |  −20°/frame |     −20°/frame | Forward      |
| 🔴 **ALIASED** |  −52°/frame |      +8°/frame | **Backward** |

The animation makes the invisible mathematics visible.

---

## 📐 The mathematics

Aliasing can be expressed as:

```text
alias = true − round(true / period) × period
```

For the aliased case:

```text
alias = −52 − round(−52 / 60) × 60
      = −52 − (−60)
      = +8°/frame
```

The wheel is **actually moving −52°/frame**.

But because the pattern repeats every 60°, the sampled frames are indistinguishable from a wheel moving **+8°/frame**.

### The important idea

> **The samples are real.
> The interpretation is wrong.**

---

## 🧪 Why this matters in NMR

The wagon-wheel effect isn't just a camera illusion.

It is the same principle behind **frequency aliasing in NMR**.

An NMR signal is sampled at discrete time intervals:

```text
Continuous signal
       ↓
   Sampling
       ↓
Discrete points
       ↓
   FFT / Spectrum
       ↓
Observed frequency
```

If the signal contains frequencies beyond the **Nyquist limit**, those frequencies fold back into the observable spectral range.

A peak can therefore appear at a frequency that is **not its true frequency**.

### 🚗 Wheel → 📡 NMR

| Wagon wheel              | NMR                    |
| ------------------------ | ---------------------- |
| Rotation frequency       | Signal frequency       |
| Camera frames            | NMR samples            |
| Spoke periodicity        | Sampling periodicity   |
| Apparent backward motion | Folded/aliased peak    |
| Increase frame rate      | Increase sampling rate |

---

## 🔬 The NMR fix

The sampling interval is the **dwell time**:

```text
Δt = 1 / SW
```

where **SW** is the spectral width.

To reduce aliasing:

> **Increase the spectral width → decrease the dwell time → sample faster.**

The goal is to satisfy the **Nyquist criterion**:

```text
SW ≥ 2 × highest frequency
```

---

## 🎬 Animation

**Resolution:** `1200 × 675 px`
**Frame rate:** `10 FPS`
**Duration:** `~22 s`

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

Change that path if you want to save the animation elsewhere.

---

## 💡 The takeaway

> **Aliasing doesn't change the signal.
> It changes what the samples allow you to see.**

And that's why a wheel can appear to spin backward —

and why an NMR peak can appear in the wrong place.

---

### Part of

**[nmr-concepts-visualized](https://github.com/HHo2050/nmr-concepts-visualized)**

Visualizing **NMR, DSP, and signal-processing concepts** through Python animations.

**02 / Nyquist Aliasing**
`NMR × DSP × Visual Thinking`

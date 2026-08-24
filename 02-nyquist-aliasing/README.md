\# 02 — Nyquist Aliasing: Wagon Wheel Effect



\## What this animation shows



A car wheel spinning forward — but appearing to go backward.

This is not a visual trick. It is aliasing: the same mathematical

phenomenon that places NMR peaks in the wrong position in the spectrum.



\## Physics of the animation



The wheel has 6 spokes (spoke period = 60°/frame).



| Phase | True rotation | Displayed rotation | Perceived direction |

|---|---|---|---|

| A — TRUE | −20°/frame (CW) | −20°/frame | Forward ✓ |

| B — ALIASED | −52°/frame (CW) | +8° to +14°/frame (CCW) | Backward ✗ |



Alias formula:

&#x20;   alias = true − round(true / spoke\_period) × spoke\_period

&#x20;   alias = −52 − (−60) = +8°/frame → appears to rotate backward



\## NMR connection



A fast NMR signal sampled with too long a dwell time folds back

into the spectrum — indistinguishable from a real peak.

The fix: increase spectral width (SW), which shortens dwell time (1/SW).



\## Output



\- Resolution: 1200 × 675 px

\- Frame rate: 10 FPS

\- Duration: \~22 seconds (7s forward / 3s transition / 9s aliased / 3s end)



\## Requirements



```bash

pip install matplotlib numpy pillow

```



\## How to run



```bash

python nyquist\_car\_v4.py

```



Output GIF saves to the path defined in `out\_path` at the bottom of the script.

Change it to your preferred directory before running.



\## Part of

\[nmr-concepts-visualized](https://github.com/HHo2050/nmr-concepts-visualized)

— visualizing NMR and DSP concepts with Python.


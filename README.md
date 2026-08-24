\# nmr-concepts-visualized



Python animations for NMR and DSP concepts — built to make the math visible.



Each animation targets a specific phenomenon: aliasing, Fourier transform,

phase correction, baseline drift. The goal is not illustration for its own sake

but understanding the signal-level mechanics that determine whether an NMR

spectrum is trustworthy or not.



Each folder is self-contained. Download only what you need.



\---



\## Background



These animations grew out of building \[nmrx.ir](https://nmrx.ir) — an

open-source NMR analysis tool — and working through the signal processing

theory behind functions I was already using in code: autophase, baseline

correction, peak fitting. At some point the math became clearer through

animation than through equations alone.



The series covers the DSP foundations of NMR: sampling theory, Fourier

analysis, windowing, filtering, phase and baseline correction — and how

each one affects what you see (or misread) in the spectrum.



\---



\## Posts



| # | Concept | Folder | LinkedIn |

|---|---|---|---|

| 02-1 | Nyquist Aliasing — Wagon Wheel Effect | \[02-nyquist-aliasing](./02-nyquist-aliasing/) | \[Post](#) |



More coming. Each post links to its folder.



\---



\## Requirements



Each folder has its own README with exact dependencies.

Common base:



```bash

pip install matplotlib numpy pillow

```



\---



\## Author



Seyyed Mostafa Moosavi — Chemist with a focus on NMR signal processing and

chemoinformatics. Building nmrx.ir as an open-source NMR analysis platform.



\[GitHub](https://github.com/HHo2050) · \[nmrx.ir](https://nmrx.ir)


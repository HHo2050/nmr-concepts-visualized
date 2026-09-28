import numpy as np

np.random.seed(7)
n_points = 8192
dwell_time = 1e-3
t = np.arange(n_points) * dwell_time

fid_clean = (
    9.0 * np.exp(1j * 2 * np.pi * 7.0  * t) * np.exp(-t / 2.0) +
    6.0 * np.exp(1j * 2 * np.pi * 10.0 * t) * np.exp(-t / 2.0)
)
noise = (1.5/np.sqrt(2)) * (np.random.randn(n_points) + 1j*np.random.randn(n_points))
noisy_fid = fid_clean + noise

freqs_full = np.fft.fftfreq(n_points, d=dwell_time)
freqs = freqs_full[freqs_full >= 0]

# case 1: noisy FID, no window → high noise floor
fid_case1 = noisy_fid.copy()

# case 2: noisy FID hard-truncated at 8% → sinc ringing
idx = int(0.08 * n_points)
fid_case2 = np.zeros(n_points, dtype=complex)
fid_case2[:idx] = noisy_fid[:idx]

# case 3: noisy FID + exponential window (lb=0.2 Hz) → reduced ringing
lb = 0.2
window = np.exp(-np.pi * lb * t)
fid_case3 = noisy_fid * window

def sp(fid):
    return np.abs(np.fft.fft(fid))[:n_points//2]

np.savez("/home/claude/necessity_data.npz",
    t=t, freqs=freqs, window=window,
    fid_case1=fid_case1,
    fid_case2=fid_case2,
    fid_case3=fid_case3,
    sp_case1=sp(fid_case1),
    sp_case2=sp(fid_case2),
    sp_case3=sp(fid_case3),
)

zoom = (freqs >= 0) & (freqs <= 20)
for name, s in [("no_window", sp(fid_case1)),
                ("truncated", sp(fid_case2)),
                ("windowed",  sp(fid_case3))]:
    print(f"{name:12s}  peak={s[zoom].max():.0f}")
print("Done.")

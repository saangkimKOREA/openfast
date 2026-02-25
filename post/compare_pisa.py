import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from openfast_toolbox.io import FASTOutputFile


# -----------------------------
# USER SETTINGS
# -----------------------------
BASE_FILE = "../results/run_base.outb"
K10_FILE  = "../results/run_k10_k1.outb"
CHANNEL   = "PtfmSurge_[m]"   # change if needed
TSTART    = 50.0              # ignore startup transient


# -----------------------------
# Helper Functions
# -----------------------------
def load_df(path):
    df = FASTOutputFile(path).toDataFrame()
    return df


def compute_stats(t, x):
    x = x - np.mean(x)
    dt = np.median(np.diff(t))
    fs = 1.0 / dt

    n = len(x)
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(n, dt)

    i = np.argmax(np.abs(X[1:])) + 1
    f_dom = f[i]

    rms = np.sqrt(np.mean(x**2))
    peak = np.max(np.abs(x))

    return rms, peak, f_dom


# -----------------------------
# Load Data
# -----------------------------
base = load_df(BASE_FILE)
k10  = load_df(K10_FILE)

t0 = base["Time_[s]"].values
x0 = base[CHANNEL].values

t1 = k10["Time_[s]"].values
x1 = k10[CHANNEL].values

mask0 = t0 >= TSTART
mask1 = t1 >= TSTART

rms0, peak0, f0 = compute_stats(t0[mask0], x0[mask0])
rms1, peak1, f1 = compute_stats(t1[mask1], x1[mask1])

summary = pd.DataFrame({
    "Case": ["Base", "K x10"],
    "RMS":  [rms0, rms1],
    "Peak": [peak0, peak1],
    "DominantFreq_Hz": [f0, f1],
})

print("\nComparison Summary:\n")
print(summary)


# -----------------------------
# Plot
# -----------------------------
plt.figure()
plt.plot(t0, x0, label="Base")
plt.plot(t1, x1, label="K x10", alpha=0.8)
plt.xlabel("Time [s]")
plt.ylabel(CHANNEL)
plt.legend()
plt.grid(True)
plt.show()

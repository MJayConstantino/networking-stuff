"""Activity 3: signals as sums of sine waves.

The program builds the two Fourier-series approximations required by the
activity, saves plots for the required term counts, and also saves a plot for
the term count entered by the user.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


sample_rate = 48_000
duration = 2
frequency = 1
angular_frequency = 2 * np.pi * frequency

try:
    number_of_terms = int(input("Enter the number of harmonic terms N: "))
    if number_of_terms < 1:
        raise ValueError
except ValueError:
    print("N must be a positive whole number.")
    raise SystemExit

time = np.linspace(0, duration, sample_rate * duration, endpoint=False)
sine_signal = np.zeros_like(time)
cosine_signal = np.zeros_like(time)

for k in range(1, number_of_terms + 1):
    harmonic = 2 * k - 1
    sine_signal += np.sin(harmonic * angular_frequency * time) / harmonic
    cosine_signal += np.cos(harmonic * angular_frequency * time) / harmonic**2

cosine_signal *= 8 / np.pi**2

plots_directory = Path("plots")
plots_directory.mkdir(exist_ok=True)

sine_figure, sine_axis = plt.subplots(figsize=(10, 4))
sine_axis.plot(time, sine_signal, color="blue")
sine_axis.set_title(f"Odd Sine Harmonics, N = {number_of_terms}")
sine_axis.set_xlabel("Time (seconds)")
sine_axis.set_ylabel("Amplitude")
sine_axis.grid(True)
sine_figure.tight_layout()
sine_figure.savefig(
    plots_directory / f"sine_N{number_of_terms}.png",
    dpi=200,
)

cosine_figure, cosine_axis = plt.subplots(figsize=(10, 4))
cosine_axis.plot(time, cosine_signal, color="orange")
cosine_axis.set_title(f"Odd Cosine Harmonics, N = {number_of_terms}")
cosine_axis.set_xlabel("Time (seconds)")
cosine_axis.set_ylabel("Amplitude")
cosine_axis.grid(True)
cosine_figure.tight_layout()
cosine_figure.savefig(
    plots_directory / f"cosine_N{number_of_terms}.png",
    dpi=200,
)

plt.show()
plt.close(sine_figure)
plt.close(cosine_figure)

print(f"Plots saved in: {plots_directory.resolve()}")

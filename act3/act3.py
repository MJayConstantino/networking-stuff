"""Activity 3: signals as sums of sine waves.

The program builds the two Fourier-series approximations required by the
activity, saves plots for the required term counts, and also saves a plot for
the term count entered by the user.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


SAMPLE_RATE = 48_000
DURATION = 2.0
FUNDAMENTAL_FREQUENCY = 1.0
REQUIRED_N_VALUES = (4, 8, 100, 1_000, 2_000)
DEFAULT_OUTPUT_DIRECTORY = Path(__file__).resolve().parent / "plots"


def create_time_array() -> np.ndarray:
    """Return two seconds of samples at the required 48 kHz sample rate."""
    number_of_samples = int(SAMPLE_RATE * DURATION)
    return np.linspace(0, DURATION, number_of_samples, endpoint=False)


def validate_number_of_terms(number_of_terms: int) -> int:
    """Return a valid positive harmonic-term count or raise ValueError."""
    if number_of_terms < 1:
        raise ValueError("The number of harmonic terms must be at least 1.")
    return number_of_terms


def odd_sine_series(time: np.ndarray, number_of_terms: int) -> np.ndarray:
    """Compute sum sin((2k-1)wt)/(2k-1) for k = 1 to N."""
    validate_number_of_terms(number_of_terms)
    angular_frequency = 2 * np.pi * FUNDAMENTAL_FREQUENCY
    signal = np.zeros_like(time)

    for k in range(1, number_of_terms + 1):
        harmonic = 2 * k - 1
        signal += np.sin(harmonic * angular_frequency * time) / harmonic

    return signal


def odd_cosine_series(time: np.ndarray, number_of_terms: int) -> np.ndarray:
    """Compute (8/pi^2) sum cos((2k-1)wt)/(2k-1)^2 for k = 1 to N."""
    validate_number_of_terms(number_of_terms)
    angular_frequency = 2 * np.pi * FUNDAMENTAL_FREQUENCY
    signal = np.zeros_like(time)

    for k in range(1, number_of_terms + 1):
        harmonic = 2 * k - 1
        signal += np.cos(harmonic * angular_frequency * time) / harmonic**2

    return (8 / np.pi**2) * signal


def ideal_waveform(series_name: str, time: np.ndarray) -> np.ndarray:
    """Return the ideal waveform approached by a series as N increases."""
    phase = np.mod(time * FUNDAMENTAL_FREQUENCY, 1.0)

    if series_name == "sine":
        # The unscaled series in the handout approaches +/- pi/4.
        return (np.pi / 4) * np.sign(np.sin(2 * np.pi * phase))

    if series_name == "cosine":
        # The positive odd cosine series approaches a triangle wave.
        return 1 - 4 * np.minimum(phase, 1 - phase)

    raise ValueError(f"Unknown series name: {series_name}")


def save_plot(
    time: np.ndarray,
    signal: np.ndarray,
    number_of_terms: int,
    series_name: str,
    output_path: Path,
) -> None:
    """Save one composite waveform plot with its ideal limiting waveform."""
    if series_name == "sine":
        title = "Odd Sine Harmonics"
        color = "#1D4ED8"
        ideal_label = "Ideal square-wave limit"
    elif series_name == "cosine":
        title = "Odd Cosine Harmonics"
        color = "#EA580C"
        ideal_label = "Ideal triangle-wave limit"
    else:
        raise ValueError(f"Unknown series name: {series_name}")

    highest_harmonic = 2 * number_of_terms - 1
    figure, axis = plt.subplots(figsize=(10, 4.4))
    axis.plot(
        time,
        ideal_waveform(series_name, time),
        color="#94A3B8",
        linewidth=1.2,
        linestyle="--",
        label=ideal_label,
    )
    axis.plot(
        time,
        signal,
        color=color,
        linewidth=1.35,
        label=f"Composite series, N = {number_of_terms}",
    )
    axis.set_title(f"{title} | N = {number_of_terms}", fontsize=14, fontweight="bold")
    axis.set_xlabel("Time (seconds)")
    axis.set_ylabel("Amplitude")
    axis.set_xlim(0, DURATION)
    axis.grid(True, alpha=0.25)
    axis.legend(loc="upper right")
    axis.text(
        0.01,
        0.03,
        f"Highest included harmonic: {highest_harmonic}f0 = "
        f"{highest_harmonic * FUNDAMENTAL_FREQUENCY:.0f} Hz",
        transform=axis.transAxes,
        fontsize=9,
        color="#334155",
    )
    figure.tight_layout()
    figure.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close(figure)


def save_series_plots(
    time: np.ndarray,
    number_of_terms: int,
    output_directory: Path,
    *,
    filename_prefix: str = "",
) -> tuple[Path, Path]:
    """Compute and save the sine and cosine plots for one value of N."""
    validate_number_of_terms(number_of_terms)
    output_directory.mkdir(parents=True, exist_ok=True)

    sine_path = output_directory / f"{filename_prefix}odd_sine_N{number_of_terms}.png"
    cosine_path = output_directory / f"{filename_prefix}odd_cosine_N{number_of_terms}.png"

    save_plot(
        time,
        odd_sine_series(time, number_of_terms),
        number_of_terms,
        "sine",
        sine_path,
    )
    save_plot(
        time,
        odd_cosine_series(time, number_of_terms),
        number_of_terms,
        "cosine",
        cosine_path,
    )
    return sine_path, cosine_path


def save_required_plots(time: np.ndarray, output_directory: Path) -> list[Path]:
    """Generate the ten plots requested by the activity handout."""
    paths: list[Path] = []
    for number_of_terms in REQUIRED_N_VALUES:
        paths.extend(save_series_plots(time, number_of_terms, output_directory))
    return paths


def prompt_for_number_of_terms() -> int:
    """Ask the user for a positive number of harmonic terms."""
    while True:
        raw_value = input("Enter the number of harmonic terms N: ").strip()
        try:
            return validate_number_of_terms(int(raw_value))
        except ValueError:
            print("Please enter a positive whole number, such as 4 or 100.")


def parse_arguments() -> argparse.Namespace:
    """Parse optional command-line settings while retaining the required prompt."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--terms",
        type=int,
        help="Use this value of N instead of prompting for it.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIRECTORY,
        help="Directory where PNG plots are saved.",
    )
    parser.add_argument(
        "--skip-required",
        action="store_true",
        help="Only save plots for the selected N; do not regenerate all required plots.",
    )
    return parser.parse_args()


def main() -> None:
    """Run the activity's plot generation workflow."""
    arguments = parse_arguments()
    number_of_terms = (
        validate_number_of_terms(arguments.terms)
        if arguments.terms is not None
        else prompt_for_number_of_terms()
    )
    time = create_time_array()

    selected_paths = save_series_plots(
        time,
        number_of_terms,
        arguments.output_dir,
        filename_prefix="selected_",
    )
    required_paths: list[Path] = []
    if not arguments.skip_required:
        required_paths = save_required_plots(time, arguments.output_dir)

    print(f"Saved {len(selected_paths) + len(required_paths)} plot(s) to {arguments.output_dir}")
    for path in [*selected_paths, *required_paths]:
        print(f"- {path}")


if __name__ == "__main__":
    main()

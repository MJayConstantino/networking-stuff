# SE 4143 Activity 3

This repository contains the Python implementation for **Signals as Sums of
Sine Waves - Fourier Series in Data Communication**.

## Requirements

- Python 3.10 or newer
- NumPy
- Matplotlib

The script uses a 48 kHz sample rate and a 1 Hz fundamental frequency over two
seconds. It generates the odd-sine and odd-cosine Fourier-series plots required
by the activity.

## Setup on Windows PowerShell

From the repository root:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install --upgrade pip
py -m pip install -r requirements.txt
```

If PowerShell blocks activation, run the script directly through the virtual
environment instead:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Run

The normal run asks for `N`, saves plots for that selected value, and generates
the ten required plots for `N = 4, 8, 100, 1000, 2000`:

```powershell
py act3\act3.py
```

For a non-interactive run, provide `N` on the command line:

```powershell
py act3\act3.py --terms 100
```

Plots are written to `act3\plots\`. To generate only the selected pair of
plots, add `--skip-required`.

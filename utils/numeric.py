"""Numerical helpers."""
import numpy as np
import pandas as pd


def safe_log10(series: pd.Series) -> pd.Series:
    s = pd.to_numeric(series, errors="coerce")
    return np.log10(s.where(s > 0))


def safe_slider_range(low: float, high: float, val: float) -> tuple[float, float, float]:
    low, high, val = float(low), float(high), float(val)
    if low == high or high <= low:
        low, high = val - 0.01, val + 0.01
    val = max(low, min(high, val))
    return low, high, val
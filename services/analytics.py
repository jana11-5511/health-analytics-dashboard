"""Correlation analytics shared across views."""
import pandas as pd
import streamlit as st

from config import PREDICTOR_MAP
from utils.text import clean_cause_name


@st.cache_data(show_spinner=False)
def predictor_correlations(panel: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for pred in PREDICTOR_MAP:
        if pred in panel.columns and "life_expectancy" in panel.columns:
            s = panel[[pred, "life_expectancy"]].dropna()
            if len(s) > 3:
                rows.append({
                    "Variable":    PREDICTOR_MAP[pred],
                    "col_orig":    pred,
                    "Correlación": round(s[pred].corr(s["life_expectancy"]), 3),
                })
    return pd.DataFrame(rows).dropna().sort_values("Correlación")


@st.cache_data(show_spinner=False)
def cause_correlations(death: pd.DataFrame, le: pd.DataFrame) -> pd.DataFrame:
    cause_cols = [c for c in death.columns if "Rate per 100k" in c]
    if "Code" not in death.columns or "Code" not in le.columns:
        return pd.DataFrame(columns=["Causa", "Correlación", "col_orig"])

    le_mean    = le.groupby("Code", as_index=False)["life_expectancy"].mean()
    death_mean = death.groupby("Code", as_index=False)[cause_cols].mean(numeric_only=True)
    merged     = pd.merge(death_mean, le_mean, on="Code", how="inner")

    rows = []
    for col in cause_cols:
        tmp = merged[[col, "life_expectancy"]].dropna()
        if len(tmp) > 3:
            rows.append({
                "Causa":       clean_cause_name(col),
                "Correlación": round(tmp[col].corr(tmp["life_expectancy"]), 3),
                "col_orig":    col,
            })
    return (pd.DataFrame(rows).dropna().sort_values("Correlación")
            if rows else pd.DataFrame(columns=["Causa", "Correlación", "col_orig"]))
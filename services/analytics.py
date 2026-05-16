"""Correlation analytics shared across views."""
import numpy as np
import pandas as pd
import streamlit as st

from config import PREDICTOR_MAP
from utils.text import clean_cause_name


@st.cache_data(show_spinner=False)
def predictor_correlations(panel: pd.DataFrame) -> pd.DataFrame:
    """
    Correlación bivariada (Pearson) entre cada predictor y la esperanza de vida.

    Se calcula sobre la media 2000-2019 por país (cross-sectional), espejo del
    notebook §3.3-§3.7. Esto es importante: las observaciones país-año del
    mismo país no son independientes (la EV de Mali en 2010 está muy correlada
    con la de Mali en 2011), así que correlar sobre el panel completo infla
    artificialmente los coeficientes.

    Caso especial PIB: se aplica log10 antes de Pearson porque la relación
    PIB↔EV es la curva de Preston (cóncava). Pearson sobre PIB raw subestima
    la fuerza real de la asociación — el notebook §3.3 reporta r ≈ +0.83
    sobre log10(PIB), no sobre PIB raw.
    """
    if "Code" not in panel.columns or "life_expectancy" not in panel.columns:
        return pd.DataFrame(columns=["Variable", "col_orig", "Correlación"])

    # Media 2000-2019 por país: una fila por país. Espejo de
    # `get_mean_data` del notebook §3.
    panel_mean = (
        panel.groupby("Code", as_index=False)
             .mean(numeric_only=True)
    )

    rows = []
    for pred in PREDICTOR_MAP:
        if pred not in panel_mean.columns:
            continue

        s = panel_mean[[pred, "life_expectancy"]].dropna()
        if len(s) <= 3:
            continue

        x = s[pred]
        y = s["life_expectancy"]

        # log10 solo para PIB (curva de Preston). Pobreza, gasto sanitario y
        # coberturas vacunales se mantienen sin transformar — son aproximada-
        # mente lineales con la EV en el rango del panel.
        if pred == "gdp_per_capita":
            x = np.log10(x.clip(lower=1))   # clip defensivo por si hay 0 o negativos

        rows.append({
            "Variable":    PREDICTOR_MAP[pred],
            "col_orig":    pred,
            "Correlación": round(x.corr(y), 3),
        })

    if not rows:
        return pd.DataFrame(columns=["Variable", "col_orig", "Correlación"])

    return pd.DataFrame(rows).dropna().sort_values("Correlación")


@st.cache_data(show_spinner=False)
def cause_correlations(death: pd.DataFrame, le: pd.DataFrame) -> pd.DataFrame:
    """
    Correlación cross-sectional entre cada causa de muerte y la esperanza de vida.
    Media 2000-2019 por país (espejo del notebook §3.8). Sin cambios respecto a
    la versión anterior — esta función ya estaba bien.
    """
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

"""OLS regression pipeline (Modelo Socioeconómico).

Métricas de generalización (R² CV, RMSE CV, R² test, RMSE test) se calculan
sobre el split por país. Pero los COEFICIENTES y la CALCULADORA usan un
modelo reentrenado sobre el panel completo (mismo enfoque que el notebook
§5.6 / §5.7 con `model_se_full`). Esto alinea los valores expuestos al
usuario con los reportados en el notebook.
"""
from dataclasses import dataclass

import numpy as np
import pandas as pd
import streamlit as st
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import (
    GroupKFold,
    GroupShuffleSplit,
    cross_val_score,
    train_test_split,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from config import PREDICTOR_MAP
from utils.numeric import safe_log10


@dataclass
class ModelResult:
    # Modelo entrenado sobre el panel completo (148 países, 1.460 obs).
    # Es el que expone la app al usuario en coeficientes, calculadora y
    # diagnóstico de residuos — espejo de `model_se_full` del notebook §5.6.
    model_full: LinearRegression
    scaler_full: StandardScaler
    df_full: pd.DataFrame
    full_pred: np.ndarray
    coef_full: pd.Series

    # Métricas de generalización (modelo del train, no se expone al usuario)
    rmse_train: float
    rmse_test: float
    rmse_cv: float
    rmse_cv_sd: float
    r2_train: float
    r2_test: float
    r2_cv: float
    r2_cv_sd: float

    # Estructura del panel
    features: list
    available_preds: list


def _prepare_features(panel: pd.DataFrame) -> tuple[pd.DataFrame, list, list]:
    available = [p for p in PREDICTOR_MAP if p in panel.columns]
    keep = available + [
        c for c in ("Entity", "Code", "Year", "life_expectancy") if c in panel.columns
    ]
    df = panel[keep].copy().dropna(subset=available + ["life_expectancy"])

    if "gdp_per_capita" in df.columns:
        df["gdp_log"] = safe_log10(df["gdp_per_capita"])

    features = [p for p in available if p != "gdp_per_capita"]
    if "gdp_per_capita" in available:
        features.append("gdp_log")
    features = [c for c in features if c in df.columns]
    return df, features, available


def _split(df: pd.DataFrame, features: list) -> tuple:
    """
    Split por país: ningún país aparece simultáneamente en train y test.
    Espejo del split usado en el notebook §5.5 (GroupShuffleSplit con
    test_size=0.2 y random_state=42).
    """
    X = df[features].values
    y = df["life_expectancy"].values

    if "Code" in df.columns:
        splitter = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
        train_idx, test_idx = next(splitter.split(X, y, groups=df["Code"].values))
        return X[train_idx], X[test_idx], y[train_idx], y[test_idx]

    # Fallback defensivo si no hay columna Code
    X_tr, X_te, y_tr, y_te = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    return X_tr, X_te, y_tr, y_te


@st.cache_resource(show_spinner="Entrenando modelo de Machine Learning...")
def train_model(panel: pd.DataFrame) -> ModelResult | None:
    df, features, available = _prepare_features(panel)
    if not features or len(df) <= 10:
        return None

    X = df[features].values
    y = df["life_expectancy"].values

    # ── (1) MÉTRICAS DE GENERALIZACIÓN ────────────────────────────────────
    # Split por país para obtener R²/RMSE test honestos.
    X_tr, X_te, y_tr, y_te = _split(df, features)

    scaler_tr = StandardScaler()
    X_tr_s = scaler_tr.fit_transform(X_tr)
    X_te_s = scaler_tr.transform(X_te)

    model_tr = LinearRegression().fit(X_tr_s, y_tr)
    yp_tr = model_tr.predict(X_tr_s)
    yp_te = model_tr.predict(X_te_s)

    # Validación cruzada honesta: GroupKFold(5) + Pipeline (scaler dentro
    # de cada fold). Espejo del notebook §5.5.
    pipe = Pipeline([
        ("scaler", StandardScaler()),
        ("model", LinearRegression()),
    ])
    cv = GroupKFold(n_splits=5)
    groups = df["Code"].values if "Code" in df.columns else None

    rmse_scores = -cross_val_score(
        pipe, X, y, groups=groups, cv=cv,
        scoring="neg_root_mean_squared_error",
    )
    r2_scores = cross_val_score(
        pipe, X, y, groups=groups, cv=cv, scoring="r2",
    )

    # ── (2) MODELO OPERATIVO — entrenado sobre TODO el panel ──────────────
    # Es el modelo expuesto al usuario: coeficientes, calculadora, residuos.
    # Equivalente a `model_se_full` del notebook §5.6.
    scaler_full = StandardScaler().fit(X)
    X_full_s = scaler_full.transform(X)
    model_full = LinearRegression().fit(X_full_s, y)
    full_pred = model_full.predict(X_full_s)

    coef_full = pd.Series(model_full.coef_, index=features)

    return ModelResult(
        model_full=model_full,
        scaler_full=scaler_full,
        df_full=df,
        full_pred=full_pred,
        coef_full=coef_full,
        rmse_train=float(np.sqrt(mean_squared_error(y_tr, yp_tr))),
        rmse_test=float(np.sqrt(mean_squared_error(y_te, yp_te))),
        rmse_cv=float(rmse_scores.mean()),
        rmse_cv_sd=float(rmse_scores.std(ddof=1)),
        r2_train=float(r2_score(y_tr, yp_tr)),
        r2_test=float(r2_score(y_te, yp_te)),
        r2_cv=float(r2_scores.mean()),
        r2_cv_sd=float(r2_scores.std(ddof=1)),
        features=features,
        available_preds=available,
    )


def predict_life_expectancy(mr: ModelResult, inputs: dict) -> float:
    """Predict from a dict of raw predictor values, usando el modelo full."""
    inp = pd.DataFrame([inputs])
    if "gdp_per_capita" in inp.columns:
        inp["gdp_log"] = safe_log10(inp["gdp_per_capita"])
        if inp["gdp_log"].isna().any() and "gdp_log" in mr.df_full.columns:
            inp["gdp_log"] = inp["gdp_log"].fillna(mr.df_full["gdp_log"].median())
        inp = inp.drop(columns=["gdp_per_capita"])

    for col in mr.features:
        if col not in inp.columns:
            inp[col] = mr.df_full[col].median()

    pred = mr.model_full.predict(mr.scaler_full.transform(inp[mr.features]))[0]
    return float(np.clip(pred, 40, 90))



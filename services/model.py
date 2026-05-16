"""OLS regression pipeline (Modelo Socioeconómico)."""
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
    model: LinearRegression
    scaler: StandardScaler
    train_pred: np.ndarray
    test_pred: np.ndarray
    rmse_train: float
    rmse_test: float
    rmse_cv: float
    rmse_cv_sd: float          # ← NUEVO: desviación entre folds del RMSE CV
    r2_train: float
    r2_test: float
    r2_cv: float               # ← NUEVO: R² CV honesto (antes hardcodeado "~0.66")
    r2_cv_sd: float            # ← NUEVO: desviación entre folds del R² CV
    resid_std: float
    coef: pd.Series
    df_train: pd.DataFrame
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
    test_size=0.2 y random_state=42). Esto evita el leakage país-año que
    infla las métricas cuando el modelo ve otros años del mismo país.
    """
    X = df[features].values
    y = df["life_expectancy"].values

    if "Code" in df.columns:
        splitter = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
        train_idx, test_idx = next(splitter.split(X, y, groups=df["Code"].values))
        return (
            X[train_idx], X[test_idx],
            y[train_idx], y[test_idx],
            df.iloc[train_idx].copy(),
        )

    # Fallback defensivo si el panel no trae columna Code
    X_tr, X_te, y_tr, y_te, idx_tr, _ = train_test_split(
        X, y, np.arange(len(y)), test_size=0.2, random_state=42
    )
    return X_tr, X_te, y_tr, y_te, df.iloc[idx_tr].copy()


@st.cache_resource(show_spinner="Entrenando modelo de Machine Learning...")
def train_model(panel: pd.DataFrame) -> ModelResult | None:
    df, features, available = _prepare_features(panel)
    if not features or len(df) <= 10:
        return None

    X_tr, X_te, y_tr, y_te, df_train = _split(df, features)

    scaler = StandardScaler()
    X_tr_s = scaler.fit_transform(X_tr)
    X_te_s = scaler.transform(X_te)

    model = LinearRegression().fit(X_tr_s, y_tr)
    train_pred = model.predict(X_tr_s)
    test_pred = model.predict(X_te_s)

    # Validación cruzada honesta:
    #  - GroupKFold(5) por país → ningún país comparte train y test del mismo fold.
    #  - Pipeline → el StandardScaler se ajusta DENTRO de cada fold sobre su propio
    #    train, no sobre el dataset completo (esto evita el data leakage del scaler).
    # Espejo del CV usado en el notebook §5.5.
    pipe = Pipeline([
        ("scaler", StandardScaler()),
        ("model", LinearRegression()),
    ])
    cv = GroupKFold(n_splits=5)
    groups = df["Code"].values if "Code" in df.columns else None

    rmse_scores = -cross_val_score(
        pipe, df[features].values, df["life_expectancy"].values,
        groups=groups, cv=cv, scoring="neg_root_mean_squared_error",
    )
    r2_scores = cross_val_score(
        pipe, df[features].values, df["life_expectancy"].values,
        groups=groups, cv=cv, scoring="r2",
    )

    return ModelResult(
        model=model,
        scaler=scaler,
        train_pred=train_pred,
        test_pred=test_pred,
        rmse_train=float(np.sqrt(mean_squared_error(y_tr, train_pred))),
        rmse_test=float(np.sqrt(mean_squared_error(y_te, test_pred))),
        rmse_cv=float(rmse_scores.mean()),
        rmse_cv_sd=float(rmse_scores.std(ddof=1)),
        r2_train=float(r2_score(y_tr, train_pred)),
        r2_test=float(r2_score(y_te, test_pred)),
        r2_cv=float(r2_scores.mean()),
        r2_cv_sd=float(r2_scores.std(ddof=1)),
        resid_std=float(np.std(y_tr - train_pred)),
        coef=pd.Series(model.coef_, index=features),
        df_train=df_train,
        features=features,
        available_preds=available,
    )


def predict_life_expectancy(mr: ModelResult, inputs: dict) -> float:
    """Predict from a dict of raw predictor values."""
    inp = pd.DataFrame([inputs])
    if "gdp_per_capita" in inp.columns:
        inp["gdp_log"] = safe_log10(inp["gdp_per_capita"])
        if inp["gdp_log"].isna().any() and "gdp_log" in mr.df_train.columns:
            inp["gdp_log"] = inp["gdp_log"].fillna(mr.df_train["gdp_log"].median())
        inp = inp.drop(columns=["gdp_per_capita"])

    for col in mr.features:
        if col not in inp.columns:
            inp[col] = mr.df_train[col].median()

    pred = mr.model.predict(mr.scaler.transform(inp[mr.features]))[0]
    return float(np.clip(pred, 40, 90))


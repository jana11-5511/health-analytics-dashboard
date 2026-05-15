"""Ridge regression pipeline."""
from dataclasses import dataclass

import numpy as np
import pandas as pd
import streamlit as st
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.preprocessing import StandardScaler

from config import PREDICTOR_MAP
from utils.numeric import safe_log10


@dataclass
class ModelResult:
    model: Ridge
    scaler: StandardScaler
    train_pred: np.ndarray
    test_pred: np.ndarray
    rmse_train: float
    rmse_test: float
    rmse_cv: float
    r2_train: float
    r2_test: float
    resid_std: float
    coef: pd.Series
    df_train: pd.DataFrame
    features: list
    available_preds: list


def _prepare_features(panel: pd.DataFrame) -> tuple[pd.DataFrame, list, list]:
    available = [p for p in PREDICTOR_MAP if p in panel.columns]
    keep = available + [c for c in ("Entity", "Code", "Year", "life_expectancy") if c in panel.columns]
    df = panel[keep].copy().dropna(subset=available + ["life_expectancy"])

    if "gdp_per_capita" in df.columns:
        df["gdp_log"] = safe_log10(df["gdp_per_capita"])

    features = [p for p in available if p != "gdp_per_capita"]
    if "gdp_per_capita" in available:
        features.append("gdp_log")
    features = [c for c in features if c in df.columns]
    return df, features, available


def _split(df: pd.DataFrame, features: list) -> tuple:
    X = df[features].values
    y = df["life_expectancy"].values

    if "Year" in df.columns:
        split_year = df["Year"].quantile(0.8)
        train_mask = df["Year"] <= split_year
        return X[train_mask], X[~train_mask], y[train_mask], y[~train_mask], df[train_mask].copy()

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

    model = Ridge(alpha=1.0).fit(X_tr_s, y_tr)
    train_pred = model.predict(X_tr_s)
    test_pred  = model.predict(X_te_s)

    cv_scores = cross_val_score(
        Ridge(alpha=1.0),
        scaler.fit_transform(df[features].values),
        df["life_expectancy"].values,
        cv=5, scoring="neg_root_mean_squared_error",
    )

    return ModelResult(
        model=model,
        scaler=scaler,
        train_pred=train_pred,
        test_pred=test_pred,
        rmse_train=float(np.sqrt(mean_squared_error(y_tr, train_pred))),
        rmse_test=float(np.sqrt(mean_squared_error(y_te, test_pred))),
        rmse_cv=float(-cv_scores.mean()),
        r2_train=float(r2_score(y_tr, train_pred)),
        r2_test=float(r2_score(y_te, test_pred)),
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
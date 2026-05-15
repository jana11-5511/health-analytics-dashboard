"""Model diagnostics view."""
import pandas as pd
import streamlit as st

from charts.base import DEFAULT_CONFIG
from charts.bars import signed_bar
from charts.scatter import gdp_scatter
from components.layout import page_header, section_header
from config import PREDICTOR_MAP
from services.analytics import predictor_correlations
from services.model import ModelResult
from utils.text import wrap_title


def _correlation_chart(corr_df: pd.DataFrame):
    corr_df = corr_df.copy()
    corr_df["Variable_wrap"] = corr_df["Variable"].apply(lambda t: wrap_title(t, 22))
    return signed_bar(
        corr_df, value_col="Correlación", label_col="Variable_wrap",
        height=380, x_title="Correlación de Pearson",
        hovertemplate="%{customdata}<br>r = %{x:+.2f}<extra></extra>",
        customdata=corr_df["Variable"],
    )


def _coefficient_chart(mr: ModelResult):
    coef = mr.coef.copy()
    coef.index = [PREDICTOR_MAP.get(i, i) for i in coef.index]
    coef = coef.sort_values().reset_index()
    coef.columns = ["Variable", "Coef"]
    return signed_bar(
        coef, value_col="Coef", label_col="Variable",
        height=300, x_title="Impacto relativo en Años (Estandarizado)",
        value_fmt="{:+.2f}",
        hovertemplate="<b>%{y}</b><br>Coeficiente: %{x:+.3f}<extra></extra>",
    )


def render(le: pd.DataFrame, panel: pd.DataFrame, mr: ModelResult | None) -> None:
    page_header(
        "Modelo",
        "Relación entre predictores estructurales y esperanza de vida: correlaciones, "
        "importancia de variables y ajuste del modelo.",
    )

    if mr is None:
        st.warning("Datos insuficientes para el modelo.")
        return

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("R² en datos de Test", f"{mr.r2_test:.3f}", f"Train R²: {mr.r2_train:.3f}")
    c2.metric("Predictores", f"{len(mr.available_preds)}", "variables en el modelo")
    c3.metric("Observaciones", f"{len(mr.df_train):,}", "filas país-año")
    c4.metric("Error (RMSE Test)", f"{mr.rmse_test:.2f} años", "en predicción final")

    corr_df = predictor_correlations(panel)
    left, right = st.columns([1, 1], gap="large")

    with left:
        section_header("Ranking de correlaciones con la EV", "Análisis Bivariante")
        if not corr_df.empty:
            st.plotly_chart(_correlation_chart(corr_df),
                            use_container_width=True, config=DEFAULT_CONFIG)
            section_header("Importancia de variables (Modelo Ridge)",
                           "Coeficientes estandarizados")
            st.plotly_chart(_coefficient_chart(mr),
                            use_container_width=True, config=DEFAULT_CONFIG)

    with right:
        section_header("Relación PIB per cápita – esperanza de vida", "Dispersión")
        pm = gdp_panel_data(panel, le)
        if pm is not None and len(pm):
            st.plotly_chart(gdp_scatter(pm), use_container_width=True, config=DEFAULT_CONFIG)    )


def _gdp_panel(panel: pd.DataFrame, le: pd.DataFrame):
    required = {"gdp_per_capita", "life_expectancy", "Code"}
    if not required.issubset(panel.columns):
        return None

    pm = panel.groupby("Code", as_index=False).mean(numeric_only=True)
    pm = pm.merge(le[["Code", "Entity"]].drop_duplicates(), on="Code", how="left")
    pm["gdp_log"] = safe_log10(pm["gdp_per_capita"])
    pm = pm.dropna(subset=["gdp_log", "life_expectancy", "Entity"])
    return gdp_scatter(pm) if len(pm) else None


def render(le: pd.DataFrame, panel: pd.DataFrame, mr: ModelResult | None) -> None:
    page_header(
        "Modelo",
        "Relación entre predictores estructurales y esperanza de vida: correlaciones, "
        "importancia de variables y ajuste del modelo.",
    )

    if mr is None:
        st.warning("Datos insuficientes para el modelo.")
        return

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("R² en datos de Test", f"{mr.r2_test:.3f}", f"Train R²: {mr.r2_train:.3f}")
    c2.metric("Predictores", f"{len(mr.available_preds)}", "variables en el modelo")
    c3.metric("Observaciones", f"{len(mr.df_train):,}", "filas país-año")
    c4.metric("Error (RMSE Test)", f"{mr.rmse_test:.2f} años", "en predicción final")

    corr_df = predictor_correlations(panel)
    left, right = st.columns([1, 1], gap="large")

    with left:
        section_header("Ranking de correlaciones con la EV", "Análisis Bivariante")
        if not corr_df.empty:
            st.plotly_chart(_correlation_chart(corr_df),
                            use_container_width=True, config=DEFAULT_CONFIG)

            section_header("Importancia de variables (Modelo Ridge)",
                           "Coeficientes estandarizados")
            st.plotly_chart(_coefficient_chart(mr),
                            use_container_width=True, config=DEFAULT_CONFIG)

    with right:
        section_header("Relación PIB per cápita – esperanza de vida", "Dispersión")
        fig = _gdp_panel(panel, le)
        if fig is not None:
            st.plotly_chart(fig, use_container_width=True, config=DEFAULT_CONFIG)

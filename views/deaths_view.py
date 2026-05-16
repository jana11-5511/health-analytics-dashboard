"""Causes of death view."""
import pandas as pd
import streamlit as st

from charts.base import DEFAULT_CONFIG
from charts.bars import horizontal_bar, signed_bar
from charts.scatter import residual_plot
from components.layout import info_box, page_header, section_header
from services.analytics import cause_correlations
from services.model import ModelResult
from styles.theme import ACCENT_3, NEG
from utils.text import categorize_cause, wrap_title


def _top_causes_chart(df: pd.DataFrame, color: str, x_range: tuple) -> "go.Figure":
    return horizontal_bar(
        x=df["Correlación"],
        y=[wrap_title(t, 25) for t in df["Causa"]],
        colors=color,
        text=[f"{v:.3f}" for v in df["Correlación"]],
        height=320, x_title="Correlación", x_range=x_range,
        add_zero_line=True,
        hovertemplate="%{customdata}<br>r = %{x:.3f}<extra></extra>",
        customdata=df["Causa"],
        margin=dict(l=10, r=40, t=10, b=40),
    )


def _category_chart(corr_df: pd.DataFrame) -> "go.Figure":
    corr_df = corr_df.copy()
    corr_df["Categoría"] = corr_df["Causa"].apply(categorize_cause)
    cat = (corr_df.groupby("Categoría", as_index=False)["Correlación"]
                  .mean(numeric_only=True)
                  .sort_values("Correlación"))
    return signed_bar(
        cat, value_col="Correlación", label_col="Categoría",
        height=480, x_title="Correlación media con la EV",
        positive_color=ACCENT_3, negative_color=NEG,
        hovertemplate="<b>%{y}</b><br>Correlación media: %{x:+.3f}<extra></extra>",
    )


def _residuals_frame(le: pd.DataFrame, mr: ModelResult) -> pd.DataFrame:
    """
    Residuos sobre el panel completo (espejo del notebook §5.6, no del
    train del split). Cada fila es un país-año.
    """
    resid = mr.df_full.copy()
    if "Entity" not in resid.columns:
        resid = resid.merge(le[["Code", "Entity"]].drop_duplicates(), on="Code", how="left")
    resid["pred"]     = mr.full_pred
    resid["residual"] = resid["life_expectancy"] - resid["pred"]
    return resid


def render(le: pd.DataFrame, panel: pd.DataFrame, death: pd.DataFrame, mr) -> None:
    page_header(
        "Causas de Muerte",
        "Correlaciones entre las principales causas de muerte y la esperanza de vida. "
        "Los datasets de suicidios y homicidios se analizaron pero no se incluyeron como "
        "predictores: la correlación con la EV es moderada y ambas variables presentan "
        "problemas de subnotificación en países de renta baja.",
    )
    corr_df = cause_correlations(death, le)
    top_neg = corr_df.head(5) if not corr_df.empty else pd.DataFrame()
    top_pos = (corr_df.tail(5).sort_values("Correlación", ascending=True)
               if not corr_df.empty else pd.DataFrame())

    c1, c2 = st.columns(2, gap="large")
    with c1:
        section_header("Causas con mayor impacto negativo", "Vulnerabilidad Sanitaria")
        info_box(
            "Enfermedades infecciosas y materno-infantiles típicas de sistemas sanitarios "
            "frágiles. Afectan a edades tempranas y reducen drásticamente la esperanza de "
            "vida al nacer."
        )
        if not top_neg.empty:
            st.plotly_chart(_top_causes_chart(top_neg, NEG, (-1.05, 0.1)),
                            use_container_width=True, config=DEFAULT_CONFIG)
    with c2:
        section_header("Causas con mayor impacto positivo", "Sesgo de Supervivencia")
        info_box(
            "Sesgo de supervivencia: las enfermedades crónico-degenerativas (cáncer, demencias, "
            "cardiovasculares) correlacionan positivamente con la EV porque solo se observan en "
            "poblaciones que ya han superado la mortalidad prematura. Morir de cáncer a los 80 "
            "es indicador de un sistema que ha erradicado causas de muerte evitables. "
            "La correlación no implica causalidad."
        )
        if not top_pos.empty:
            st.plotly_chart(_top_causes_chart(top_pos, ACCENT_3, (-0.1, 1.05)),
                            use_container_width=True, config=DEFAULT_CONFIG)

    st.markdown("<br>", unsafe_allow_html=True)
    left, right = st.columns([1, 1], gap="large")
    with left:
        section_header("Ranking completo — correlación de todas las causas", "Agrupado")
        info_box(
            "Correlación media de Pearson agrupada en 7 macro-categorías. "
            "Valores negativos señalan categorías asociadas a sistemas sanitarios vulnerables."
        )
        if not corr_df.empty:
            st.plotly_chart(_category_chart(corr_df),
                            use_container_width=True, config=DEFAULT_CONFIG)
    with right:
        section_header("Análisis de residuales del modelo", "Identificación de Outliers")
        info_box(
            "Un residual positivo indica que el país rinde por encima de lo que predice "
            "el modelo. Un residual negativo apunta a debilidades estructurales no captadas."
        )
        if mr and mr.features and len(mr.df_full) > 0:
            st.plotly_chart(residual_plot(_residuals_frame(le, mr), mr.rmse_cv),
                            use_container_width=True, config=DEFAULT_CONFIG)


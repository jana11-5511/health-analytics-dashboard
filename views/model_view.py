"""Model diagnostics view."""
import pandas as pd
import streamlit as st

from charts.base import DEFAULT_CONFIG
from charts.bars import signed_bar
from charts.scatter import gdp_scatter
from components.layout import page_header, section_header
from config import PREDICTOR_LABEL_OVERRIDE, PREDICTOR_MAP
from services.analytics import predictor_correlations
from services.model import ModelResult
from utils.numeric import safe_log10
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
    # Coeficientes del modelo entrenado sobre el panel completo (espejo
    # del notebook §5.6 con `model_se_full`, no del train del split).
    coef = mr.coef_full.copy()
    label_map = {**PREDICTOR_MAP, **PREDICTOR_LABEL_OVERRIDE}
    coef.index = [label_map.get(i, i) for i in coef.index]
    coef = coef.sort_values()

    return signed_bar(
        pd.DataFrame({"Variable": coef.index, "Coeficiente": coef.values}),
        value_col="Coeficiente", label_col="Variable",
        height=380, x_title="Coeficiente estandarizado (Beta)",
        hovertemplate="<b>%{y}</b><br>Beta = %{x:+.3f}<extra></extra>",
    )


def render(le: pd.DataFrame, panel: pd.DataFrame, mr) -> None:
    page_header(
        "Mecanismo del Modelo",
        "Análisis de la capacidad predictiva y estructura del modelo socioeconómico "
        "con validación cruzada por bloques (GroupKFold por país).",
    )

    if mr is None:
        st.warning("No se pudo inicializar el modelo matemático debido a la falta de variables.")
        return

    # Tarjetas métricas con el RMSE CV y R² CV real como contexto.
    c1, c2, c3, c4 = st.columns(4)
    c1.metric(
        "R² CV GroupKFold(5)",
        f"{mr.r2_cv:.3f}",
        f"Test split por país: {mr.r2_test:.3f}",
    )
    c2.metric(
        "Predictores socioeconómicos",
        f"{len(mr.available_preds)}",
        "variables en el modelo",
    )
    c3.metric(
        "Observaciones",
        f"{len(mr.df_full):,}",
        "filas país-año (panel completo)",
    )
    c4.metric(
        "RMSE CV GroupKFold(5)",
        f"{mr.rmse_cv:.2f} años",
        f"Test split por país: {mr.rmse_test:.2f} años",
    )

    corr_df = predictor_correlations(panel)
    left, right = st.columns([1, 1], gap="large")

    with left:
        section_header("Ranking de correlaciones con la EV", "Análisis Bivariante")
        if not corr_df.empty:
            st.plotly_chart(
                _correlation_chart(corr_df),
                use_container_width=True, config=DEFAULT_CONFIG,
            )
        section_header(
            "Importancia de variables (Modelo Socioeconómico)",
            "Coeficientes estandarizados",
        )
        st.plotly_chart(
            _coefficient_chart(mr),
            use_container_width=True, config=DEFAULT_CONFIG,
        )

    with right:
        section_header("El efecto cóncavo del ingreso económico", "Curva de Preston")
        # El scatter del notebook usa datos de panel completo (espejo del §3.3)
        st.plotly_chart(
            gdp_scatter(mr.df_full),
            use_container_width=True, config=DEFAULT_CONFIG,
        )


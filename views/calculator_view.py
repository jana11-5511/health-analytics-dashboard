"""Interactive calculator view."""
import streamlit as st

from components.layout import page_header, section_header
from components.prediction_card import render_prediction_card
from config import PREDICTOR_MAP
from services.model import ModelResult, predict_life_expectancy
from utils.numeric import safe_slider_range


def _render_sliders(mr: ModelResult) -> dict:
    """Render one slider per predictor and return their current values."""
    sliders: dict = {}
    for pred in mr.available_preds:
        if pred not in mr.df_train.columns:
            continue

        default = float(mr.df_train[pred].median())
        q05     = float(mr.df_train[pred].quantile(0.05))
        q95     = float(mr.df_train[pred].quantile(0.95))
        low, high, val = safe_slider_range(q05, q95, default)

        step = max((high - low) / 100, 0.01)
        if pred == "gdp_per_capita":
            step = max(step, 1.0)

        label = PREDICTOR_MAP.get(pred, pred)
        st.markdown(
            f"<div style='font-size:0.9rem; font-weight:600; margin-top:0.5rem;'>{label}</div>",
            unsafe_allow_html=True,
        )
        sliders[pred] = st.slider(
            label, low, high, val, float(step),
            key=f"calc_{pred}", label_visibility="collapsed",
        )
    return sliders


def render(le, panel, mr: ModelResult | None) -> None:
    page_header(
        "Calculadora",
        "Herramienta interactiva para simular la esperanza de vida según los "
        "predictores estructurales del modelo.",
    )

    if mr is None:
        st.warning("Datos insuficientes para el modelo.")
        return

    section_header("Calculadora interactiva del modelo", "Simulación en tiempo real")

    left, right = st.columns([1, 1], gap="large")

    with left:
        st.markdown("**Ajusta las variables estructurales**")
        inputs = _render_sliders(mr)

    with right:
        with st.spinner("Calculando predicción..."):
            pred       = predict_life_expectancy(mr, inputs)
            global_avg = float(le[le["Year"] == 2019]["life_expectancy"].mean())
            render_prediction_card(pred, global_avg, mr)
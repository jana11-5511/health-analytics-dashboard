"""Sidebar navigation and model summary."""
import pandas as pd
import streamlit as st
from config import PAGES
from services.model import ModelResult
from styles.theme import ACCENT_2


def _init_state() -> None:
    if "page" not in st.session_state or st.session_state.page not in PAGES:
        st.session_state.page = PAGES[0]


def _stats_row(label: str, value: str, *, highlight: bool = False) -> str:
    color = ACCENT_2 if highlight else "rgba(255,255,255,0.75)"
    weight = "700" if highlight else "400"
    return (
        f'<div style="display:flex;justify-content:space-between;margin-bottom:0.4rem;">'
        f'<span style="font-size:0.75rem;color:rgba(255,255,255,0.40);font-weight:600;">{label}</span>'
        f'<span style="font-size:0.75rem;font-weight:{weight};color:{color};">{value}</span>'
        f'</div>'
    )


def render_sidebar(df: pd.DataFrame, mr: ModelResult | None) -> str:
    _init_state()

    with st.sidebar:
        # ── Capçalera ──────────────────────────────────────────────────────
        st.markdown(
            '<div style="padding-bottom:1rem;">'
            '<div style="font-size:1.45rem;font-weight:900;color:#ffffff;'
            'letter-spacing:-0.03em;line-height:1.1;">OMS · Health Analytics</div>'
            '<div style="font-size:0.82rem;color:rgba(255,255,255,0.50);'
            'font-weight:500;margin-top:0.25rem;">Inteligencia sobre Esperanza de Vida</div>'
            '</div>',
            unsafe_allow_html=True,
        )

        # ── Navegació ──────────────────────────────────────────────────────
        st.markdown('<span class="sb-section-label">Navegación</span>', unsafe_allow_html=True)
        st.radio("nav", list(PAGES), key="page", label_visibility="collapsed")

        # Separador visual sense div buit
        st.write("")
        st.write("")

        st.markdown(
            '<hr style="border:none;border-top:1px solid rgba(255,255,255,0.10);margin:0.5rem 0;">',
            unsafe_allow_html=True,
        )

        # ── Estadístiques del model ────────────────────────────────────────
        n_paises = df["Code"].nunique() if "Code" in df.columns else "N/D"
        year_range = (
            f"{int(df['Year'].min())} – {int(df['Year'].max())}"
            if "Year" in df.columns
            else "2000 – 2019"
        )

        def fmt(v: float) -> str:
            return f"{v:.2f}" if mr else "—"

        rmse_tr = fmt(mr.rmse_train) if mr else "—"
        rmse_te = fmt(mr.rmse_test)  if mr else "—"
        rmse_cv = fmt(mr.rmse_cv)    if mr else "—"

        stats_html = (
            '<div style="padding-bottom:1rem;">'
            '<div style="font-size:0.6rem;font-weight:700;text-transform:uppercase;'
            'letter-spacing:0.1em;color:rgba(255,255,255,0.28);margin-bottom:0.7rem;">'
            'Rendimiento del Modelo</div>'
            + _stats_row("Países", str(n_paises))
            + _stats_row("Período", year_range)
            + _stats_row("RMSE Train", f"{rmse_tr} años")
            + _stats_row("RMSE Test",  f"{rmse_te} años", highlight=True)
            + _stats_row("CV 5-fold",  f"{rmse_cv} años")
            + '</div>'
        )
        st.markdown(stats_html, unsafe_allow_html=True)

    return st.session_state.page

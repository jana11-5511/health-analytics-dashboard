"""Global exploration view."""
import pandas as pd
import streamlit as st

from charts.base import DEFAULT_CONFIG
from charts.bars import horizontal_bar
from charts.maps import animated_choropleth
from charts.timeseries import life_expectancy_evolution
from components.layout import page_header, section_header
from styles.theme import ACCENT_3


def _render_top10(le_2019: pd.DataFrame) -> None:
    top10 = le_2019.nlargest(10, "life_expectancy")[["Entity", "life_expectancy"]] \
                   .sort_values("life_expectancy")
    n = len(top10)
    blues = ([f"rgba(8,145,178,{0.45 + 0.55 * i / (n - 1)})" for i in range(n)]
             if n > 1 else [ACCENT_3])
    fig = horizontal_bar(
        x=top10["life_expectancy"], y=top10["Entity"], colors=blues,
        text=[f"{v:.1f}" for v in top10["life_expectancy"]],
        height=360, x_range=(75, 92),
        hovertemplate="%{y}<br>EV: %{x:.1f} años<extra></extra>",
        margin=dict(l=10, r=30, t=10, b=20),
    )
    st.plotly_chart(fig, use_container_width=True, config=DEFAULT_CONFIG)


def render(le: pd.DataFrame) -> None:
    page_header(
        "Exploración Global",
        "Mapa mundial, evolución temporal y distribución de la esperanza de vida entre 2000 y 2019. "
        "Mapa y rankings sobre cobertura completa de OWID (~235 países). "
        "El modelo predictivo se entrena sobre el panel restringido de 148 países (ver pestaña Modelo).",
    )

    le_2019 = le[le["Year"] == 2019]
    le_2000 = le[le["Year"] == 2000]
    media_19 = le_2019["life_expectancy"].mean()
    media_00 = le_2000["life_expectancy"].mean()
    max_row = le_2019.loc[le_2019["life_expectancy"].idxmax()]
    min_row = le_2019.loc[le_2019["life_expectancy"].idxmin()]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("EV media global 2019", f"{media_19:.1f}", f"+{media_19 - media_00:.1f} vs 2000")
    c2.metric("País más longevo", max_row["Entity"], f"{max_row['life_expectancy']:.1f} años")
    c3.metric("País menos longevo", min_row["Entity"], f"{min_row['life_expectancy']:.1f} años")
    c4.metric("Brecha máxima",
              f"{(max_row['life_expectancy'] - min_row['life_expectancy']):.1f} años")

    section_header("Mapa mundial interactivo", "Distribución geográfica")
    st.plotly_chart(animated_choropleth(le), use_container_width=True, config=DEFAULT_CONFIG)

    left, right = st.columns([1, 1], gap="large")

    with left:
        section_header("Top 10 países — mayor esperanza de vida (2019)", "Ranking")
        _render_top10(le_2019)

    with right:
        section_header("Evolución EV media global (2000–2019)", "Tendencia Temporal")
        evol = le.groupby("Year", as_index=False)["life_expectancy"].mean()
        evol = evol[evol["Year"] <= 2019]
        st.plotly_chart(life_expectancy_evolution(evol),
                        use_container_width=True, config=DEFAULT_CONFIG)

"""Choropleth maps."""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from styles.theme import ACCENT, ACCENT_3, BG, FONT_FAMILY, MAP_COLOR_SCALE, TRANSPARENT_BG

_FRAME_DURATION = 550
_TRANSITION_DURATION = 300


def _style_animation_controls(fig: go.Figure) -> None:
    if fig.layout.updatemenus:
        for btn in fig.layout.updatemenus[0].buttons:
            if btn.args and len(btn.args) > 1 and isinstance(btn.args[1], dict):
                btn.args[1]["frame"] = {"duration": _FRAME_DURATION, "redraw": True}
                btn.args[1]["transition"] = {"duration": _TRANSITION_DURATION, "easing": "cubic-in-out"}

        fig.layout.updatemenus[0].update(dict(
            type="buttons", direction="left", showactive=False,
            x=0.1, xanchor="right", y=-0.1, yanchor="top",
            pad=dict(t=2, r=6, b=2, l=0),
            bgcolor="rgba(0,0,0,0)", bordercolor="rgba(0,0,0,0)", borderwidth=0,
            font=dict(family=FONT_FAMILY, size=15, color=ACCENT),
        ))

    if fig.layout.sliders:
        fig.layout.sliders[0].update(dict(
            x=0.14, xanchor="left", y=-0.04, yanchor="top",
            len=0.82, pad=dict(t=8, b=10),
            bgcolor="#E2E8F0", bordercolor="rgba(0,0,0,0)", borderwidth=0,
            tickcolor="#CBD5E1", ticklen=4,
            font=dict(family=FONT_FAMILY, size=11, color="#64748B"),
            activebgcolor=ACCENT,
            currentvalue=dict(
                prefix="Año  ",
                font=dict(family=FONT_FAMILY, size=13, color=ACCENT_3),
                offset=10, xanchor="left",
            ),
            transition=dict(duration=_TRANSITION_DURATION, easing="cubic-in-out"),
        ))
        for step in fig.layout.sliders[0].steps:
            if step.args and len(step.args) > 1 and isinstance(step.args[1], dict):
                step.args[1]["frame"] = {"duration": _FRAME_DURATION, "redraw": True}
                step.args[1]["transition"] = {"duration": _TRANSITION_DURATION, "easing": "cubic-in-out"}


@st.cache_data(show_spinner=False)
def animated_choropleth(le: pd.DataFrame) -> go.Figure:
    df_map = le[le["Year"].between(2000, 2019)].sort_values("Year")
    lo, hi = df_map["life_expectancy"].quantile(0.02), df_map["life_expectancy"].quantile(0.98)

    fig = px.choropleth(
        df_map.dropna(subset=["Code"]),
        locations="Code", color="life_expectancy", hover_name="Entity",
        animation_frame="Year", color_continuous_scale=MAP_COLOR_SCALE,
        projection="natural earth", range_color=[lo, hi],
        labels={"life_expectancy": "Años"},
    )
    fig.update_traces(
        hovertemplate="<b>%{hovertext}</b><br><span style='color:#94A3B8'>Esperanza de vida</span><br>"
                      "<span style='font-weight:700;color:#0891b2'>%{z:.1f} años</span><extra></extra>",
        marker_line_color="#CBD5E1", marker_line_width=0.4,
    )

    fig.update_layout(
        height=520,
        margin=dict(l=0, r=0, t=10, b=10),
        paper_bgcolor=TRANSPARENT_BG, plot_bgcolor=TRANSPARENT_BG,
        font=dict(family=FONT_FAMILY, color="#334155"),
        coloraxis_colorbar=dict(
            title=dict(text="Años", font=dict(size=12, color="#64748B")),
            thickness=10, len=0.72, x=0.98,
            tickfont=dict(size=11, color="#334155"),
            outlinewidth=0, ticks="outside", ticklen=3,
        ),
    )

    _style_animation_controls(fig)

    fig.update_geos(
        bgcolor=TRANSPARENT_BG, showocean=True, oceancolor=BG,
        showlakes=True, lakecolor=BG, showland=True, landcolor="#EEF2F7",
        showcoastlines=True, coastlinecolor="#CBD5E1", coastlinewidth=0.5,
        showcountries=True, countrycolor="#CBD5E1", countrywidth=0.3,
        showframe=False,
    )
    return fig
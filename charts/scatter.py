"""Scatter and residual plots."""
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import scipy.stats as stats

from charts.base import apply_base_layout
from styles.theme import ACCENT_3, GDP_COLOR_SCALE, LINE, MUTED, WARN


def gdp_scatter(pm: pd.DataFrame) -> go.Figure:
    fig = px.scatter(
        pm, x="gdp_log", y="life_expectancy", hover_name="Entity",
        color="life_expectancy", color_continuous_scale=GDP_COLOR_SCALE,
        trendline="ols", trendline_color_override=ACCENT_3, opacity=0.85,
    )
    fig.update_traces(
        selector=dict(mode="markers"),
        marker=dict(size=9, line=dict(width=0.8, color="#0c4a6e")),
        hovertemplate="<b>%{hovertext}</b><br>PIB (log₁₀): %{x:.2f}<br>EV: %{y:.1f} años<extra></extra>",
    )

    _, _, r, _, _ = stats.linregress(pm["gdp_log"], pm["life_expectancy"])
    fig.add_annotation(
        x=pm["gdp_log"].max() - 0.3, y=pm["life_expectancy"].min() + 3,
        text=f"<b>R² = {r**2:.3f}</b>", showarrow=False,
        font=dict(size=12, color=ACCENT_3),
        bgcolor="white", bordercolor=LINE, borderwidth=1, borderpad=6,
    )

    apply_base_layout(fig, height=450, margin=dict(l=10, r=20, t=10, b=40))
    fig.update_layout(coloraxis_showscale=False)
    fig.update_xaxes(showgrid=False, title="PIB per cápita (log₁₀ USD)")
    fig.update_yaxes(showgrid=True, gridcolor=LINE, title="Esperanza de vida (años)")
    return fig


def residual_plot(resid: pd.DataFrame, rmse_train: float) -> go.Figure:
    threshold = resid["residual"].std() * 4
    to_label = resid[resid["residual"].abs() > threshold]
    colors = np.where(resid["residual"] >= 0, ACCENT_3, WARN)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=resid["pred"], y=resid["residual"], mode="markers",
        marker=dict(size=5, color=colors, opacity=0.75),
        hovertemplate="<b>%{customdata}</b><br>Predicción: %{x:.1f} años<br>"
                      "Residual: %{y:.1f} años<extra></extra>",
        customdata=resid["Entity"] if "Entity" in resid.columns else resid["Code"],
        showlegend=False,
    ))

    if "Entity" in to_label.columns:
        for _, row in to_label.iterrows():
            fig.add_annotation(
                x=row["pred"], y=row["residual"], text=row["Entity"],
                showarrow=False, font=dict(size=9, color=MUTED),
                yshift=12 if row["residual"] > 0 else -12,
            )

    fig.add_hrect(y0=-rmse_train, y1=rmse_train, fillcolor="rgba(8,145,178,0.05)",
                  line_width=0, annotation_text=f"±RMSE ({rmse_train:.1f})",
                  annotation_position="right", annotation_font_size=9)
    fig.add_hline(y=0, line_color="#CBD5E1", line_width=1, line_dash="dot", layer="below")

    apply_base_layout(fig, height=480, margin=dict(l=10, r=30, t=10, b=50))
    fig.update_xaxes(title="Esperanza de vida predicha (años)", showgrid=False,
                     tickformat=".1f", nticks=7)
    fig.update_yaxes(title="Residual (real − predicho)", gridcolor=LINE,
                     tickformat=".1f", nticks=6, side="left")
    return fig
"""Time series charts."""
import pandas as pd
import plotly.graph_objects as go

from charts.base import apply_base_layout
from styles.theme import ACCENT, ACCENT_3, LINE, SURFACE


def life_expectancy_evolution(evol: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=evol["Year"], y=evol["life_expectancy"], mode="lines+markers",
        line=dict(color=ACCENT_3, width=2.5),
        marker=dict(size=6, color=ACCENT, line=dict(width=1.5, color=SURFACE)),
        fill="tozeroy", fillcolor="rgba(8,145,178,0.07)",
        hovertemplate="Año %{x}<br>EV media %{y:.1f} años<extra></extra>",
    ))

    max_row = evol.loc[evol["life_expectancy"].idxmax()]
    fig.add_annotation(
        x=max_row["Year"], y=max_row["life_expectancy"],
        text=f"<b>{max_row['life_expectancy']:.1f}</b>",
        showarrow=True, arrowhead=2, arrowcolor=ACCENT_3,
        font=dict(size=11, color=ACCENT_3),
        bgcolor="white", bordercolor=ACCENT_3, borderwidth=1, borderpad=4,
        ay=-30, ax=10,
    )

    apply_base_layout(fig, height=360, margin=dict(l=20, r=20, t=10, b=40))
    fig.update_xaxes(showgrid=False, range=[1999.5, 2019.5],
                     tickvals=list(range(2000, 2020, 2)))
    fig.update_yaxes(range=[55, 80], showgrid=True, gridcolor=LINE, title="Años")
    return fig
"""Reusable bar chart builders."""
import pandas as pd
import plotly.graph_objects as go

from charts.base import apply_base_layout
from styles.theme import ACCENT_3, LINE, NEG


def horizontal_bar(
    *, x, y, colors, text, height: int = 360,
    x_title: str = "", x_range: tuple | None = None,
    margin: dict | None = None, hovertemplate: str | None = None,
    customdata=None, add_zero_line: bool = False,
) -> go.Figure:
    fig = go.Figure(go.Bar(
        x=x, y=y, orientation="h",
        marker_color=colors, marker_line_width=0,
        text=text, textposition="outside",
        hovertemplate=hovertemplate or "%{y}<br>%{x}<extra></extra>",
        customdata=customdata,
    ))
    if add_zero_line:
        fig.add_vline(x=0, line_width=1, line_color="#CBD5E1")

    apply_base_layout(fig, height=height, margin=margin or dict(l=10, r=30, t=10, b=30))
    fig.update_xaxes(showgrid=False, title=x_title, showline=False, zeroline=False,
                     range=list(x_range) if x_range else None)
    fig.update_yaxes(showgrid=False, title="", showline=False, zeroline=False, automargin=True)
    return fig


def signed_bar(df: pd.DataFrame, value_col: str, label_col: str, *,
               height: int = 380, x_title: str = "Correlación",
               positive_color: str = ACCENT_3, negative_color: str = NEG,
               value_fmt: str = "{:+.2f}", padding_ratio: float = 0.18,
               hovertemplate: str | None = None, customdata=None) -> go.Figure:
    """Bar chart where bar color reflects sign of value."""
    colors = [positive_color if v >= 0 else negative_color for v in df[value_col]]
    x_min, x_max = df[value_col].min(), df[value_col].max()
    pad = (x_max - x_min) * padding_ratio if x_max != x_min else 0.1

    return horizontal_bar(
        x=df[value_col], y=df[label_col], colors=colors,
        text=[value_fmt.format(v) for v in df[value_col]],
        height=height, x_title=x_title,
        x_range=(x_min - pad, x_max + pad),
        add_zero_line=True,
        hovertemplate=hovertemplate, customdata=customdata,
    )
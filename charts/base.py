"""Plotly defaults shared across chart modules."""
import plotly.graph_objects as go

from styles.theme import FONT_FAMILY, LINE, TRANSPARENT_BG

DEFAULT_CONFIG = {"displayModeBar": "hover"}


def apply_base_layout(fig: go.Figure, *, height: int, margin: dict | None = None,
                      showlegend: bool = False) -> go.Figure:
    """Apply consistent layout settings to a Plotly figure."""
    fig.update_layout(
        height=height,
        margin=margin or dict(l=10, r=20, t=10, b=40),
        paper_bgcolor=TRANSPARENT_BG,
        plot_bgcolor=TRANSPARENT_BG,
        font=dict(family=FONT_FAMILY),
        showlegend=showlegend,
    )
    return fig


def clean_axes(fig: go.Figure, *, x_grid: bool = False, y_grid: bool = False,
               x_title: str = "", y_title: str = "") -> go.Figure:
    fig.update_xaxes(showgrid=x_grid, gridcolor=LINE, title=x_title,
                     showline=False, zeroline=False, automargin=True)
    fig.update_yaxes(showgrid=y_grid, gridcolor=LINE, title=y_title,
                     showline=False, zeroline=False, automargin=True)
    return fig
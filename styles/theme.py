"""Centralized design tokens: colors, spacing, scales."""

# Core palette
NEG      = "#64748b"
POS      = "#06b6d4"
BG       = "#F0F7FA"
SURFACE  = "#FFFFFF"
TEXT     = "#0F172A"
MUTED    = "#64748B"
ACCENT   = "#06b6d4"
ACCENT_2 = "#22d3ee"
ACCENT_3 = "#0891b2"
ACCENT_4 = "#14b8a6"
PURPLE   = "#8b5cf6"
LINE     = "#E2E8F0"
WARN     = "#f59e0b"

# Color scales
MAP_COLOR_SCALE = [
    [0.00, "#EFF6FF"],
    [0.25, "#B3D1ED"],
    [0.50, "#4FBFD9"],
    [0.75, "#118AB2"],
    [1.00, "#012641"],
]

GDP_COLOR_SCALE = [
    [0.00, "#0c4a6e"],
    [0.50, "#0369a1"],
    [1.00, "#0ea5e9"],
]

# Plotly layout defaults
FONT_FAMILY = "Inter, sans-serif"
UNIFIED_MARGIN = dict(l=50, r=20, t=20, b=50)
TRANSPARENT_BG = "rgba(0,0,0,0)"
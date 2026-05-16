"""Health Analytics · OMS — main entry point."""
import os
import sys

# Assegurem la ruta de cerca del projecte
root_path = os.path.dirname(os.path.abspath(__file__))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

import streamlit as st
from components.sidebar import render_sidebar
from config import PAGE_CONFIG
from services.data_loader import load_data
from services.model import train_model
from styles.css import inject_global_css

# Importem cada vista de manera individual
import views.calculator_view as calculator_view
import views.deaths_view as deaths_view
import views.global_view as global_view
import views.model_view as model_view

_ROUTES = {
    "Exploración global": lambda le, panel, death, mr: global_view.render(le),
    "Modelo":              lambda le, panel, death, mr: model_view.render(le, panel, mr),
    "Calculadora":         lambda le, panel, death, mr: calculator_view.render(le, panel, mr),
    "Causas de muerte":    lambda le, panel, death, mr: deaths_view.render(le, panel, death, mr),
}


def main() -> None:
    st.set_page_config(**PAGE_CONFIG)
    inject_global_css()

    le, panel, death = load_data()
    mr = train_model(panel)

    if True:
        page = render_sidebar(panel, mr)
        _ROUTES[page](le, panel, death, mr)


if __name__ == "__main__":
    main()

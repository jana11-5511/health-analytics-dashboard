"""Data loading and cleaning."""
import pandas as pd
import streamlit as st

from config import DATA_PATH, LIFE_EXPECTANCY_COL


@st.cache_data(show_spinner=False)
def load_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Load and normalize the three core datasets."""
    try:
        le    = pd.read_csv(f"{DATA_PATH}life_expectancy_clean.csv")
        panel = pd.read_csv(f"{DATA_PATH}panel_model_final.csv")
        death = pd.read_csv(f"{DATA_PATH}deaths_by_cause_clean.csv")
    except FileNotFoundError as e:
        st.error(f"❌ Archivo de datos no encontrado: {e.filename}. Verifica el DATA_PATH.")
        st.stop()

    for df in (le, panel):
        if LIFE_EXPECTANCY_COL in df.columns:
            df.rename(columns={LIFE_EXPECTANCY_COL: "life_expectancy"}, inplace=True)

    return le, panel, death
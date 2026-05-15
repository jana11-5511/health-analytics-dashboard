"""Application-wide configuration and constants."""

DATA_PATH = "./"

PAGE_CONFIG = {
    "page_title": "Health Analytics · OMS",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
}

PAGES = ("Exploración global", "Modelo", "Calculadora", "Causas de muerte")

PREDICTOR_MAP = {
    "gdp_per_capita":          "PIB per cápita",
    "health_spending_pct_gdp": "Gasto en Salud (% PIB)",
    "share_below_6_85":        "Pob. bajo umbral pobreza (%)",
    "DTP3":                    "Inmunización DTP3 (%)",
    "MCV1":                    "Inmunización Sarampión (%)",
}

LIFE_EXPECTANCY_COL = "Period life expectancy at birth - Sex: all - Age: 0"
"""Application-wide configuration and constants."""

DATA_PATH = "./"

PAGE_CONFIG = {
    "page_title": "Health Analytics · OMS",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
}

PAGES = ("Exploración global", "Modelo", "Calculadora", "Causas de muerte")

PREDICTOR_MAP = {
    "gdp_per_capita":          "PIB per cápita (USD PPP, log",
    "health_spending_pct_gdp": "Gasto en Salud (% PIB)",
    "share_below_6_85":        "Pob. bajo umbral pobreza (%)",
    "DTP3":                    "Inmunización DTP3 (%)",
    "MCV1":                    "MCV1 -  Sarampión (%)",
}

PREDICTOR_LABEL_OVERRIDE = {\n    "gdp_log": "PIB per cápita (USD PPP, log)",\n}\n\nLIFE_EXPECTANCY_COL

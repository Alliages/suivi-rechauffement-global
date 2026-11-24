"""
Paramètres centralisés du pipeline.

Toutes les constantes (sources, périodes, méthode, palette et libellés des
rendus) sont regroupées ici pour qu'une évolution de Copernicus ne demande de
modifier qu'un seul fichier. index.html reçoit sa palette via series.json.
"""
from pathlib import Path

# --------------------------------------------------------------------------
# Chemins
# --------------------------------------------------------------------------
ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"            # données versionnées (petites)
CACHE_DIR = ROOT_DIR / ".cache"         # téléchargements bruts (non versionnés)
SITE_SRC_FILES = ["index.html", "vendor", "VERSION"]  # page web et version, à la racine du dépôt
SITE_OUT_DIR = ROOT_DIR / "_site"       # page assemblée, publiée sur GitHub Pages

MONTHLY_CSV = DATA_DIR / "era5_global_monthly.csv"
TRENDS_CSV = DATA_DIR / "trends.csv"
IPCC_CSV = DATA_DIR / "ipcc_sr15.csv"
META_JSON = DATA_DIR / "meta.json"
SERIES_JSON = DATA_DIR / "series.json"  # tout-en-un lu par la page web
CONTENT_JSON = DATA_DIR / "content.json"  # texte des onglets (FAQ, glossaire…) lu par la page

# --------------------------------------------------------------------------
# Sources de données (publiques, sans compte)
# --------------------------------------------------------------------------
# Série quotidienne de la température moyenne mondiale à 2 m (ERA5), publiée
# par Copernicus Climate Pulse. Colonnes attendues : date, 2t, clim_91-20,
# ano_91-20, status (FINAL / PRELIMINARY). Lignes de commentaire préfixées par #.
DAILY_SERIES_URL = (
    "https://sites.ecmwf.int/data/climatepulse/data/series/"
    "era5_daily_series_2t_global.csv"
)
# Enveloppe des projections GIEC SR15 utilisée par l'outil officiel
# (colonnes : year, min_t, max_t). Fichier fixe, téléchargé une seule fois.
IPCC_URL = (
    "https://apps.climate.copernicus.eu/global-temperature-trend-monitor/"
    "ipcc-projections-sr15.csv"
)

# --------------------------------------------------------------------------
# Méthode (reprise du notebook C3S « Global temperature trend monitor »)
# --------------------------------------------------------------------------
# Écart moyen entre la référence 1991-2020 et la période préindustrielle
# 1850-1900, par mois (janvier → décembre), en °C. Source : documentation du
# bulletin climatique C3S, valeurs reprises du notebook officiel.
MONTHLY_OFFSETS = [0.96, 0.96, 0.95, 0.91, 0.87, 0.83,
                   0.80, 0.80, 0.81, 0.85, 0.89, 0.93]

TREND_YEARS = 30          # longueur de la fenêtre de tendance
WINDOW_MONTHS = TREND_YEARS * 12 + 1   # 361 valeurs, comme le notebook
TARGET_WARMING = 1.5      # seuil de l'accord de Paris (°C)
FIRST_TREND_YEAR = 2000   # première fenêtre annuelle du curseur
LAST_MONTHLY_STEPS = 12   # nb de pas mensuels en fin de curseur

# --------------------------------------------------------------------------
# Bornes d'affichage
# --------------------------------------------------------------------------
PLOT_X_RANGE = ("1970-01-01", "2062-01-01")        # rendus matplotlib
PLOT_Y_RANGE = (-0.23, 2.25)
IPCC_YEARS = (1970, 2062)
IPCC_LIKELY_RANGE = ("2030-01-01", "2052-12-31")   # « likely » GIEC à 1,5 °C
X_VIEW = ("1950-01-01", "2055-01-01")              # axe x de la page web
GRID_STEP = 0.5                                    # grille horizontale (°C)

# --------------------------------------------------------------------------
# Rendu Python (render.py)
# --------------------------------------------------------------------------
DEFAULT_SIZE_PX = (1280, 720)
DPI = 100
LAST_FRAME_HOLD_MS = 2500     # pause sur la dernière image du GIF
RENDER_COLORS = {
    "ipcc": "#f7d2b8",        # enveloppe GIEC (pêche, comme l'original)
    "series": "#e8762c",      # anomalies observées
    "series_light": "#f2b48a",
    "window": "#c4471b",      # fenêtre de 30 ans
    "trend": "#941333",       # tendance (rouge C3S)
    "target": "#333333",
    "grid": "#9a9a9a",
    "text": "#222222",
}
# La palette de la page (index.html) passe par series.json ; les variantes
# « _transparent » sont écrites en rgba/rgb pour Plotly.
PAGE_COLORS = {
    "accent": "#af1d29",
    "orange": "#ff6800",
    "orange_transparent": "rgba(255, 104, 0, 0.30)",
    "peach": "rgb(244, 174, 142)",
    "peach_transparent": "rgba(244, 174, 142, 0.2)",
    "likely": "#d84a63",
    "grid": "#CCCCCC",
    "zeroline": "#444444",
}
LABELS = {
    "fr": {
        "title": "Réchauffement mondial et seuil de 1,5 °C",
        "ylabel": "Anomalie vs 1850-1900 (°C)",
        "ipcc": "Projections GIEC (SR15)",
        "likely": "Fourchette GIEC 1,5 °C (2030-2052)",
        "series": "Anomalie mensuelle ERA5",
        "window": "Fenêtre de 30 ans",
        "trend": "Tendance linéaire 30 ans",
        "crossing": "Atteinte de 1,5 °C",
        "from": "Extrapolé depuis",
        "reach": "1,5 °C atteint vers",
        "warming": "Réchauffement (tendance)",
        "month": "Mois",
        "anomaly": "Anomalie",
        "source": "Données : ERA5 / Copernicus C3S (Climate Pulse) · Méthode : C3S Global Temperature Trend Monitor",
        "prelim": "provisoire",
    },
    "en": {
        "title": "Global warming and the 1.5 °C threshold",
        "ylabel": "Anomaly vs 1850-1900 (°C)",
        "ipcc": "IPCC projections (SR15)",
        "likely": "IPCC 1.5 °C likely range (2030-2052)",
        "series": "ERA5 monthly anomaly",
        "window": "30-year window",
        "trend": "30-year linear trend",
        "crossing": "1.5 °C reached",
        "from": "Extrapolated from",
        "reach": "1.5 °C reached around",
        "warming": "Warming (trend)",
        "month": "Month",
        "anomaly": "Anomaly",
        "source": "Data: ERA5 / Copernicus C3S (Climate Pulse) · Method: C3S Global Temperature Trend Monitor",
        "prelim": "preliminary",
    },
}

# --------------------------------------------------------------------------
# Contrôles qualité avant publication
# --------------------------------------------------------------------------
ANOMALY_BOUNDS = (-1.5, 3.5)        # anomalie préindustrielle plausible (°C)
MAX_FINAL_REVISION = 0.05           # révision max tolérée d'un mois « final » (°C)

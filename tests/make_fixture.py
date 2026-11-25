"""
Génère des fichiers factices au format Climate Pulse et GIEC, pour tester
le pipeline hors ligne. Les valeurs sont synthétiques, pas réelles.

    python tests/make_fixture.py <dossier>
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

# Paramètres de la série synthétique
START, END = "1940-01-01", "2026-11-20"
TREND_PER_YEAR = 0.012        # °C/an jusqu'en 1975
TREND_PER_YEAR_RECENT = 0.022 # °C/an après 1975
NOISE = 0.12
PRELIMINARY_DAYS = 60


def make_daily(path: Path, seed: int = 0) -> None:
    rng = np.random.default_rng(seed)
    dates = pd.date_range(START, END, freq="D")
    yrs_since_1975 = np.clip((dates - pd.Timestamp("1975-01-01")).days / 365.25, 0, None)
    yrs_before = np.clip((dates - pd.Timestamp("1975-01-01")).days / 365.25, None, 0)
    ano = TREND_PER_YEAR_RECENT * yrs_since_1975 + TREND_PER_YEAR * yrs_before - 0.66
    ano = ano + rng.normal(0, NOISE, len(dates))
    clim = 14.3 + 1.9 * np.cos(2 * np.pi * (dates.dayofyear - 200) / 365.25)
    status = np.where(np.arange(len(dates)) >= len(dates) - PRELIMINARY_DAYS,
                      "PRELIMINARY", "FINAL")
    df = pd.DataFrame({"date": dates.strftime("%Y-%m-%d"), "2t": (clim + ano).round(3),
                       "clim_91-20": clim.round(3), "ano_91-20": ano.round(3),
                       "status": status})
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write("# Données SYNTHÉTIQUES pour tests\n")
        df.to_csv(f, index=False)


def make_ipcc(path: Path) -> None:
    years = np.arange(1960, 2101)
    mid = 0.3 + np.clip(years - 1970, 0, None) * 0.02
    pd.DataFrame({"year": years, "min_t": (mid - 0.25).round(3),
                  "max_t": (mid + 0.35).round(3)}).to_csv(path, index=False)


if __name__ == "__main__":
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    make_daily(out / "daily.csv")
    make_ipcc(out / "ipcc_sr15.csv")
    print(f"Fixtures écrites dans {out}")

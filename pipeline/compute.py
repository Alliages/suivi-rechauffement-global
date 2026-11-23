"""
Calculs : moyennes mensuelles, anomalies préindustrielles, tendances 30 ans.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from config import (FIRST_TREND_YEAR, LAST_MONTHLY_STEPS, MONTHLY_OFFSETS,
                    TARGET_WARMING, WINDOW_MONTHS)


# --------------------------------------------------------------------------
# Lecture de la série quotidienne Climate Pulse
# --------------------------------------------------------------------------
def read_daily(path) -> pd.DataFrame:
    """Lit le CSV quotidien et renvoie les colonnes normalisées
    date, t2m, anomaly_9120, preliminary."""
    raw = pd.read_csv(path, comment="#")
    cols = {c.lower().strip(): c for c in raw.columns}

    def find(prefix):
        for low, orig in cols.items():
            if low.startswith(prefix):
                return orig
        raise ValueError(f"Colonne « {prefix}* » introuvable : {list(raw.columns)}")

    df = pd.DataFrame({
        "date": pd.to_datetime(raw[find("date")]),
        "t2m": raw[find("2t")].astype(float),
        "anomaly_9120": raw[find("ano")].astype(float),
    })
    status_col = next((o for l, o in cols.items() if l.startswith("status")), None)
    df["preliminary"] = (raw[status_col].astype(str).str.upper() != "FINAL"
                         if status_col else False)
    return df.dropna(subset=["t2m", "anomaly_9120"]).sort_values("date")


# --------------------------------------------------------------------------
# Agrégation mensuelle
# --------------------------------------------------------------------------
def monthly_from_daily(daily: pd.DataFrame) -> pd.DataFrame:
    """Moyennes mensuelles des mois complets uniquement.

    L'anomalie mensuelle (réf. 1991-2020) est la moyenne des anomalies
    quotidiennes ; on y ajoute l'écart mensuel 1991-2020 → 1850-1900.
    """
    d = daily.copy()
    d["month"] = d["date"].dt.to_period("M")
    g = d.groupby("month").agg(
        t2m=("t2m", "mean"),
        anomaly_9120=("anomaly_9120", "mean"),
        n_days=("t2m", "size"),
        preliminary=("preliminary", "any"),
    )
    # On écarte le mois en cours (incomplet)
    g = g[g["n_days"] == g.index.days_in_month]

    offsets = np.array(MONTHLY_OFFSETS)[g.index.month - 1]
    g["anomaly_preindustrial"] = g["anomaly_9120"] + offsets
    g = g.round({"t2m": 3, "anomaly_9120": 3, "anomaly_preindustrial": 3})
    g["status"] = np.where(g["preliminary"], "preliminary", "final")
    out = g.reset_index()[["month", "t2m", "anomaly_9120",
                           "anomaly_preindustrial", "status"]]
    out["month"] = out["month"].astype(str)
    return out


# --------------------------------------------------------------------------
# Tendances sur 30 ans
# --------------------------------------------------------------------------
def trend_for_window(values: np.ndarray) -> tuple[float, float]:
    """Régression linéaire sur l'indice 0..n-1 (comme np.polyfit du notebook).
    Renvoie (pente par mois, ordonnée à l'origine)."""
    m, c = np.polyfit(np.arange(len(values)), values, 1)
    return float(m), float(c)


def compute_trends(monthly: pd.DataFrame) -> pd.DataFrame:
    """Une fenêtre de 361 mois se terminant à chaque mois depuis décembre
    FIRST_TREND_YEAR.

    is_slider_step reproduit les pas du curseur officiel : un pas par année
    (fenêtre finissant en décembre) puis les LAST_MONTHLY_STEPS derniers mois.
    """
    months = pd.PeriodIndex(monthly["month"], freq="M")
    values = monthly["anomaly_preindustrial"].to_numpy()
    first_end = pd.Period(f"{FIRST_TREND_YEAR}-12", freq="M")
    last = months[-1]
    # Dernière année complète : décembre le plus récent disponible
    last_dec_year = last.year if last.month == 12 else last.year - 1

    rows = []
    for i in range(WINDOW_MONTHS - 1, len(months)):
        end = months[i]
        if end < first_end:
            continue
        start = months[i - WINDOW_MONTHS + 1]
        # Fenêtre continue obligatoire (pas de mois manquant)
        if (end - start).n != WINDOW_MONTHS - 1:
            continue
        m, c = trend_for_window(values[i - WINDOW_MONTHS + 1: i + 1])
        n = WINDOW_MONTHS
        # Réchauffement en fin de fenêtre : m*n + c, formule du notebook
        warming_end = m * n + c
        if m > 0:
            # Date d'atteinte : début de fenêtre + int((1,5 - c) / m) mois
            crossing = str(start + int((TARGET_WARMING - c) / m))
        else:
            crossing = ""
        annual = end.month == 12 and end.year <= last_dec_year
        recent = (last - end).n < LAST_MONTHLY_STEPS
        rows.append({
            "window_end": str(end),
            "window_start": str(start),
            "slope_per_decade": round(m * 120, 4),
            "intercept": round(c, 4),
            "warming_at_end": round(warming_end, 3),
            "crossing_1_5": crossing,
            "step_label": str(end.year) if annual and not recent else str(end),
            "is_slider_step": bool(annual or recent),
        })
    return pd.DataFrame(rows)


# --------------------------------------------------------------------------
# Contrôles qualité
# --------------------------------------------------------------------------
def validate(new: pd.DataFrame, old: pd.DataFrame | None,
             bounds: tuple[float, float], max_revision: float) -> list[str]:
    """Renvoie la liste des anomalies détectées (vide = OK)."""
    errors = []
    if new.empty:
        return ["Série mensuelle vide"]
    lo, hi = bounds
    bad = new[(new["anomaly_preindustrial"] < lo) | (new["anomaly_preindustrial"] > hi)]
    if not bad.empty:
        errors.append(f"Valeurs hors bornes : {bad['month'].tolist()[:5]}")
    if old is not None and not old.empty:
        lost = set(old["month"]) - set(new["month"])
        if lost:
            errors.append(f"Mois disparus : {sorted(lost)[:5]}")
        merged = old.merge(new, on="month", suffixes=("_old", "_new"))
        final = merged[merged["status_old"] == "final"]
        diff = (final["anomaly_preindustrial_new"] - final["anomaly_preindustrial_old"]).abs()
        revised = final[diff > max_revision]
        if not revised.empty:
            errors.append(f"Mois finaux révisés de plus de {max_revision} °C : "
                          f"{revised['month'].tolist()[:5]}")
    return errors

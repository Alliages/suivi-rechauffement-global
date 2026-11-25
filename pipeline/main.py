"""
Point d'entrée du pipeline.

    python pipeline/main.py                 # télécharge, calcule, écrit data/
    python pipeline/main.py --site          # + assemble la page dans _site/
    python pipeline/main.py --site --render # + images et GIF dans _site/exports/
    python pipeline/main.py --daily fichier.csv   # utilise un CSV local (hors ligne)
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime, timezone

import pandas as pd

import config as C
from compute import compute_trends, monthly_from_daily, read_daily, validate
import content as Content
from download import download


def ensure_ipcc() -> None:
    """L'enveloppe GIEC est fixe : téléchargée une fois puis versionnée."""
    if not C.IPCC_CSV.exists():
        download(C.IPCC_URL, C.IPCC_CSV)


# --------------------------------------------------------------------------
# Écriture des sorties
# --------------------------------------------------------------------------
def write_outputs(monthly: pd.DataFrame, trends: pd.DataFrame) -> dict:
    C.DATA_DIR.mkdir(exist_ok=True)
    monthly.to_csv(C.MONTHLY_CSV, index=False)
    trends.to_csv(C.TRENDS_CSV, index=False)

    ipcc = pd.read_csv(C.IPCC_CSV)
    ipcc = ipcc[(ipcc["year"] >= C.IPCC_YEARS[0]) & (ipcc["year"] <= C.IPCC_YEARS[1])]

    latest = trends.iloc[-1]
    meta = {
        "last_month": monthly["month"].iloc[-1],
        "last_anomaly": float(monthly["anomaly_preindustrial"].iloc[-1]),
        "last_status": monthly["status"].iloc[-1],
        "latest_warming": float(latest["warming_at_end"]),
        "latest_crossing": latest["crossing_1_5"],
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ"),
        "source": C.DAILY_SERIES_URL,
        "monthly_offsets": C.MONTHLY_OFFSETS,
        "trend_years": C.TREND_YEARS,
    }
    C.META_JSON.write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
    C.CONTENT_JSON.write_text(json.dumps(Content.build(), separators=(",", ":")), encoding="utf-8")

    # Fichier unique pour la page (format colonnes, plus léger)
    series = {
        "meta": meta,
        "config": {
            "x_range": C.PLOT_X_RANGE, "y_range": C.PLOT_Y_RANGE,
            "likely_range": C.IPCC_LIKELY_RANGE, "target": C.TARGET_WARMING,
            "x_view": C.X_VIEW, "grid_step": C.GRID_STEP, "colors": C.PAGE_COLORS,
            "export_size": C.DEFAULT_SIZE_PX, "days_per_month": C.DAYS_PER_MONTH,
        },
        "monthly": monthly.to_dict(orient="list"),
        "trends": trends.to_dict(orient="list"),
        "ipcc": ipcc[["year", "min_t", "max_t"]].to_dict(orient="list"),
    }
    C.SERIES_JSON.write_text(json.dumps(series, separators=(",", ":")), encoding="utf-8")
    return meta


def build_site() -> None:
    """Copie la page et les données dans _site/ (artefact GitHub Pages)."""
    if C.SITE_OUT_DIR.exists():
        shutil.rmtree(C.SITE_OUT_DIR)
    C.SITE_OUT_DIR.mkdir(parents=True)
    for nom in C.SITE_SRC_FILES:
        src = C.ROOT_DIR / nom
        if src.is_dir():
            shutil.copytree(src, C.SITE_OUT_DIR / nom)
        else:
            shutil.copy2(src, C.SITE_OUT_DIR / nom)
    shutil.copytree(C.DATA_DIR, C.SITE_OUT_DIR / "data")
    print(f"Site assemblé : {C.SITE_OUT_DIR}")


# --------------------------------------------------------------------------
def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--daily", help="CSV quotidien local (sinon téléchargé)")
    p.add_argument("--site", action="store_true", help="assembler _site/")
    p.add_argument("--render", action="store_true",
                   help="générer images et GIF par défaut dans _site/exports/")
    p.add_argument("--force", action="store_true",
                   help="publier même si les contrôles qualité échouent")
    a = p.parse_args(argv)

    # 1. Données brutes
    if a.daily:
        daily_path = a.daily
    else:
        daily_path = C.DAILY_CACHE
        download(C.DAILY_SERIES_URL, daily_path)
    ensure_ipcc()

    # 2. Calculs
    monthly = monthly_from_daily(read_daily(daily_path))
    trends = compute_trends(monthly)

    # 3. Contrôles qualité par rapport à la version précédente
    old = pd.read_csv(C.MONTHLY_CSV, dtype={"month": str}) if C.MONTHLY_CSV.exists() else None
    errors = validate(monthly, old, C.ANOMALY_BOUNDS, C.MAX_FINAL_REVISION)
    if errors:
        print("Contrôles qualité en échec :", *errors, sep="\n  - ")
        if not a.force:
            return 1

    # 4. Sorties
    meta = write_outputs(monthly, trends)
    print(f"Dernier mois : {meta['last_month']} ({meta['last_status']}), "
          f"anomalie {meta['last_anomaly']:+.2f} °C, "
          f"tendance 30 ans {meta['latest_warming']:.2f} °C, "
          f"1,5 °C vers {meta['latest_crossing']}")

    if a.site:
        build_site()
    if a.render:
        import render
        render.render_defaults(C.SITE_OUT_DIR / "exports")
    return 0


if __name__ == "__main__":
    sys.exit(main())

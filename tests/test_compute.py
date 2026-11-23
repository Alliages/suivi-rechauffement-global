"""Tests de la méthode (pytest)."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "pipeline"))
from compute import compute_trends, monthly_from_daily, validate  # noqa: E402
from config import MONTHLY_OFFSETS, WINDOW_MONTHS  # noqa: E402


def linear_monthly(a=0.2137, b=0.002, start="1960-01", n=800):
    months = pd.period_range(start, periods=n, freq="M")
    return pd.DataFrame({
        "month": months.astype(str),
        "anomaly_preindustrial": a + b * np.arange(n),
        "status": "final",
    })


def test_trend_exact_on_linear_series():
    df = linear_monthly()
    tr = compute_trends(df)
    row = tr.iloc[-1]
    # Pente exacte : b par mois → b*120 par décennie
    assert abs(row["slope_per_decade"] - 0.002 * 120) < 1e-6
    # Date d'atteinte : début + int((1,5 - c)/b) mois
    start = pd.Period(row["window_start"], freq="M")
    i0 = df.index[df["month"] == row["window_start"]][0]
    c = 0.2137 + 0.002 * i0
    expected = start + int((1.5 - c) / 0.002)
    assert row["crossing_1_5"] == str(expected)
    # Réchauffement en fin de fenêtre : m*n + c
    assert abs(row["warming_at_end"] - (0.002 * WINDOW_MONTHS + c)) < 1e-3


def test_slider_steps_like_official_tool():
    df = linear_monthly(start="1960-01", n=12 * 66 + 7)   # finit en juillet 2026
    tr = compute_trends(df)
    steps = tr[tr["is_slider_step"]]
    labels = steps["step_label"].tolist()
    assert labels[0] == "2000"
    assert "2024" in labels and "2026" not in labels   # 2025-12 tombe dans les 12 derniers mois
    assert labels[-12:] == [str(p) for p in pd.period_range("2025-08", "2026-07", freq="M")]


def test_monthly_from_daily_offsets_and_incomplete_month():
    dates = pd.date_range("2024-01-01", "2024-03-10", freq="D")
    daily = pd.DataFrame({"date": dates, "t2m": 14.0, "anomaly_9120": 0.5,
                          "preliminary": dates >= "2024-02-20"})
    m = monthly_from_daily(daily)
    assert m["month"].tolist() == ["2024-01", "2024-02"]       # mars incomplet
    assert abs(m["anomaly_preindustrial"].iloc[0] - (0.5 + MONTHLY_OFFSETS[0])) < 1e-9
    assert m["status"].tolist() == ["final", "preliminary"]


def test_validate_detects_revision_and_loss():
    old = linear_monthly(n=50)
    new = old.copy()
    new.loc[10, "anomaly_preindustrial"] += 0.2
    assert any("révisés" in e for e in validate(new, old, (-2, 4), 0.05))
    assert any("disparus" in e for e in validate(new.iloc[:-1], old, (-2, 4), 0.05))
    assert validate(old, old, (-2, 4), 0.05) == []

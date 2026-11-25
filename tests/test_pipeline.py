"""Bout en bout sur données synthétiques : main.py (pytest)."""
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "pipeline"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import config as C  # noqa: E402
import main  # noqa: E402
from make_fixture import make_daily, make_ipcc  # noqa: E402


@pytest.fixture(scope="module")
def series(tmp_path_factory):
    """Lance main.py sur un dossier temporaire (data/ du dépôt intact)."""
    tmp = tmp_path_factory.mktemp("pipeline")
    make_daily(tmp / "daily.csv")
    make_ipcc(tmp / "ipcc.csv")
    mp = pytest.MonkeyPatch()
    data = tmp / "data"
    for name, path in {"DATA_DIR": data, "MONTHLY_CSV": data / "m.csv",
                       "TRENDS_CSV": data / "t.csv", "META_JSON": data / "meta.json",
                       "SERIES_JSON": data / "series.json", "CONTENT_JSON": data / "content.json",
                       "IPCC_CSV": tmp / "ipcc.csv"}.items():
        mp.setattr(C, name, path)
    assert main.main(["--daily", str(tmp / "daily.csv")]) == 0
    mp.undo()
    return json.loads((data / "series.json").read_text(encoding="utf-8"))


def test_series_json_carries_page_config(series):
    cfg = series["config"]
    assert cfg["export_size"] == list(C.DEFAULT_SIZE_PX)
    assert cfg["days_per_month"] == C.DAYS_PER_MONTH
    assert series["meta"]["trend_years"] == C.TREND_YEARS
    assert len(series["monthly"]["month"]) == len(series["monthly"]["anomaly_preindustrial"])

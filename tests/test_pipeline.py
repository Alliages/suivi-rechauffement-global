"""Bout en bout sur données synthétiques : main.py puis rendu (pytest)."""
import argparse
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "pipeline"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import config as C  # noqa: E402
import main  # noqa: E402
import render  # noqa: E402
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


def test_select_frames_filters_and_ends_on_last(series):
    sel = render.select_frames(series, "courbe", "2020-01", "2020-12", 5)
    months = [series["monthly"]["month"][i] for i, _ in sel]
    assert months == ["2020-01", "2020-06", "2020-11", "2020-12"]
    sel = render.select_frames(series, "extrapolation", None, None, 1000)
    assert sel[-1][1]["window_end"] == series["trends"]["window_end"][-1]


def test_render_static_and_animation(series, tmp_path):
    png = Path(render.render_static(series, tmp_path, lang="en"))
    assert png.exists() and png.stat().st_size > 10_000
    res = render.render_animation(series, "extrapolation", tmp_path, lang="en",
                                  debut="2025-01", pas=4, size=(320, 180), zip_frames=True)
    assert Path(res["gif"]).name == "extrapolation_en.gif"
    assert Path(res["zip"]).exists()
    res = render.render_animation(series, "courbe", tmp_path, debut="2026-01",
                                  fmt="svg", gif=False, size=(320, 180))
    assert all(f.suffix == ".svg" for f in Path(res["frames"]).iterdir())


@pytest.mark.parametrize("args", [["--debut", "2010-1"], ["--fps", "0"],
                                  ["--largeur", "99999"], ["--pas", "0"]])
def test_cli_rejects_bad_values(args, capsys):
    with pytest.raises(SystemExit):
        render.main(args)


def test_month_arg_accepts_valid():
    assert render.month_arg("2010-01") == "2010-01"
    with pytest.raises(argparse.ArgumentTypeError):
        render.month_arg("2010-13")

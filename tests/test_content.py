"""Tests du contenu des onglets (data/content.json)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "pipeline"))
from config import MONTHLY_OFFSETS  # noqa: E402
from content import build  # noqa: E402


def test_content_structure():
    out = build()
    assert set(out) == {"fr", "en"}
    for lang in ("fr", "en"):
        assert len(out[lang]["faq"]) == 7
        assert len(out[lang]["glossary"]) == 6
        assert out[lang]["source"].startswith("<h2>")


def test_offsets_table_tracks_config():
    out = build()
    block = out["fr"]["faq"][4]["a"]
    assert f"<td>{MONTHLY_OFFSETS[0]:.2f}</td>" in block
    assert "<td>0.88</td>" in block
    assert "{offsets_table}" not in block and "{offsets_table}" not in out["en"]["faq"][4]["a"]
    assert "écart constant de 0,88 °C" in block
    assert "offset of 0.88 °C" in out["en"]["faq"][4]["a"]

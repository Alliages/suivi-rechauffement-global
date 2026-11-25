"""
Textes des onglets FAQ / Glossaire / Code source, publiés dans data/content.json.

Le texte vit dans pipeline/content_src.json. Seuls le tableau des écarts
mensuels ({offsets_table}) et l'écart annuel ({annual_offset}) sont insérés
ici depuis config.py.
"""
from __future__ import annotations

import json

import config as C

_MONTHS = {
    "fr": ["Jan", "Fév", "Mar", "Avr", "Mai", "Juin", "Juil", "Août", "Sep", "Oct", "Nov", "Déc"],
    "en": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
}
_MONTHS_HEADER = {"fr": "Mois", "en": "Month"}
_ANNUAL_HEADER = {"fr": "Année", "en": "Annual Mean"}
_ROW_LABEL = {"fr": "Écart appliqué", "en": "Applied offset"}


def _offsets_table(lang: str) -> str:
    heads = "".join(f"<th>{m}</th>" for m in _MONTHS[lang])
    values = "".join(f"<td>{v:.2f}</td>" for v in C.MONTHLY_OFFSETS)
    return (
        f'<thead><tr><th scope="col">{_MONTHS_HEADER[lang]}</th>{heads}'
        f'<th scope="col">{_ANNUAL_HEADER[lang]}</th></tr></thead>'
        f"<tbody><tr><td>{_ROW_LABEL[lang]}</td>{values}"
        f"<td>{C.ANNUAL_OFFSET:.2f}</td></tr></tbody>"
    )


def build() -> dict:
    """Contenu complet {langue: {faq, glossary, source}} prêt pour le JSON."""
    out = json.loads(C.CONTENT_SRC.read_text(encoding="utf-8"))
    for lang, part in out.items():
        annual = f"{C.ANNUAL_OFFSET:.2f}"
        if lang == "fr":
            annual = annual.replace(".", ",")
        for item in part["faq"]:
            item["a"] = (item["a"].replace("{offsets_table}", _offsets_table(lang))
                         .replace("{annual_offset}", annual))
    return out

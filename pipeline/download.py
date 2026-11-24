"""Téléchargement HTTP partagé par le pipeline (User-Agent identifiable)."""
from __future__ import annotations

import urllib.request


def http_get(url: str, timeout: int = 60) -> bytes:
    """Renvoie le contenu d'une URL (aucune dépendance externe)."""
    req = urllib.request.Request(url, headers={"User-Agent": "suivi-rechauffement-global"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()

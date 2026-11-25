"""Téléchargement HTTP partagé par le pipeline (User-Agent identifiable)."""
from __future__ import annotations

import urllib.request
from pathlib import Path

from config import HTTP_TIMEOUT, USER_AGENT


def http_get(url: str, timeout: int = HTTP_TIMEOUT) -> bytes:
    """Renvoie le contenu d'une URL (aucune dépendance externe)."""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def download(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(http_get(url))
    print(f"Téléchargé : {url}")

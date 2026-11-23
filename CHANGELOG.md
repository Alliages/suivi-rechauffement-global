# CHANGELOG

Versions : dernier chiffre pair = évolution, impair = correction ou mineur. 0.9 : l'outil fonctionne ; 1.0 : première version annoncée et diffusée.

## 0.9.1 — 2026-11-23

- Correction : `index.html` et `vendor/` déplacés de `site/` à la racine du dépôt, pour que la page fonctionne (chemins relatifs `vendor/`, `data/`, `exports/`).
- Pipeline et workflow adaptés (`SITE_SRC_FILES`, déclencheurs `index.html` / `vendor/**`) ; `_site/` reste assemblé de la même façon.

## 0.9.0 — 2026-11-23

Version de référence : l'outil est fonctionnel. Mise en place du suivi de version.

- Pipeline : données quotidiennes ERA5 (Climate Pulse) → moyennes mensuelles, anomalies, tendance sur 30 ans, date d'atteinte de 1,5 °C, contrôles qualité.
- Mise à jour automatique les 4, 8 et 15 de chaque mois (GitHub Actions) et publication sur GitHub Pages.
- Page bilingue FR/EN : graphique Plotly, curseur d'extrapolation, enveloppe GIEC SR15.
- Exports : graphique PNG/SVG, données CSV/JSON, GIF et archives d'images, script `scripts/export.ps1`.
- Ajout de `VERSION`, `CHANGELOG.md` et `ROADMAP.md`.

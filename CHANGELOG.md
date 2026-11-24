# CHANGELOG

Versions : dernier chiffre pair = évolution, impair = correction ou mineur. 0.9 : l'outil fonctionne ; 1.0 : première version annoncée et diffusée.

## 0.9.4 — 2026-11-24

- Graphique : zoom initial de l'axe X réduit à 1950 → 2055 (l'enveloppe GIEC reste complète en interne, seule la vue initiale change ; zoom/pan restent possibles).
- Encarts de dates (mois de départ orange, mois d'atteinte rouge) placés juste sous la ligne 0 °C de l'axe Y, dans le graphique.
- Curseur : le texte « Extrapoler depuis : <mois/année> » est affiché au lancement (légende HTML au-dessus du graphique, mise à jour à chaque déplacement du curseur) et ne nécessite plus un clic sur le slider.
- Correction : le fichier `VERSION` est publié dans `_site/` (ajouté à `SITE_SRC_FILES`), le pied de page peut donc lire la version au lieu d'un 404 sur `/VERSION`.

## 0.9.3 — 2026-11-24

- Pied de page : version de l'application (lue depuis le fichier `VERSION`), liens vers le code source (dépôt GitHub), vers l'application originale C3S et vers Guillaume Meunier, ainsi que la mention C3S/ECMWF officielle.
- Graphique : étiquettes « 1,5 °C » (rouge) et niveau de réchauffement courant (orange) décalées à droite du tracé (`xref: paper`, marge droite élargie) pour ne plus se superposer aux courbes.

## 0.9.2 — 2026-11-24

- `index.html` : rendu aligné sur l'application officielle C3S (Roadmap « Rendu visuel proche de l'application officielle ») :
  - phrase de synthèse en tête du graphique (« Le réchauffement mondial a atteint… X °C en <mois>… 1,5 °C en <mois> ») avec valeurs colorées, mise à jour à chaque pas du curseur ;
  - curseur « Extrapoler depuis : » natif Plotly, graduations par année puis mois récents, comme l'application officielle ;
  - fenêtre de 30 ans surlignée en orange, tendance rouge sombre prolongée jusqu'au point d'atteinte de 1,5 °C (distracteur blanc) ;
  - lignes verticales avec dates sous l'axe : mois de départ (orange) et mois d'atteinte (rouge) ; pointillés horizontaux 1,5 °C (rouge) et niveau courant (orange) avec étiquettes à droite ;
  - enveloppe GIEC en aplat rose clair et losange « estimation probable du GIEC » ; légende sur une ligne en bas ;
  - seule la page `index.html` change : pipeline et données inchangés (schéma `series.json` et `limit_x_position` optionnel gérés).

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

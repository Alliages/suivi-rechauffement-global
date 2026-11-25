# CHANGELOG

Versions : dernier chiffre pair = évolution, impair = correction ou mineur. 0.9 : l'outil fonctionne ; 1.0 : première version annoncée et diffusée.

## 1.2.6 — 2026-11-25

- Contour blanc de 3 px autour du logo du bandeau, épousant la forme hexagonale (fond blanc + clip-path, sans modifier le favicon).

## 1.2.5 — 2026-11-25

- Bandeau rouge foncé pleine largeur en tête de page : logo hexagonal (favicon) à gauche du titre, titre et liens FR/EN en blanc, « Données jusqu'à »/« mise à jour le » relookés pour le fond rouge.

## 1.2.4 — 2026-11-25

- Icônes Tabler inline dans les onglets (graphique, FAQ, glossaire, code), couleur suivie du libellé (accent orange quand l'onglet est actif), sans nouvelle dépendance.

## 1.2.3 — 2026-11-24

- Survol des points d'anomalie au style de l'application officielle : bandeau orange fondé sur la palette de la page, titre « Changement de température observé » (gras), sous-titre « Depuis l'époque préindustrielle (1850-1900) », puis mois et valeur.
## 1.2.2 — 2026-11-24

- Mise à jour programmée simplifiée : une seule exécution mensuelle le 5 (cron `23 5 5 * *`), comme l'application officielle C3S ; FAQ et écran « code source » alignés.
## 1.2.1 — 2026-11-24

- Favicon hexagonal (courbe GIEC + seuil 1,5 °C) : `favicon.svg` à la racine, copié dans `_site/`.
## 1.2.0 — 2026-11-24

- Audit appliqué (16 points) : `pipeline/config.py` désormais unique source des paramètres (chemins, méthode, bornes, palette, libellés des rendus) ; `index.html` reçoit sa palette et ses bornes via `series.json` et son texte via `data/content.json` (page ~33 Ko).
- FAQ 5 : tableau des écarts mensuels généré depuis `config.MONTHLY_OFFSETS` (une seule source de vérité).
- `compute_trends` vectorisé (sommes cumulées au lieu d'un `np.polyfit` par fenêtre) ; sorties vérifiées identiques.
- Helper `pipeline/download.py` partagé par `main.py` et `render.py` ; rendu des images d'animation une seule fois (PNG réutilisé pour le GIF) ; corrections diverses (`timedelta` en tête, comparaison de frames).
- Ancres `#faq`, `#glossaire`, `#code` pour chaque onglet ; `scripts/export.ps1` épinglé au tag `v1.2.0`.
## 1.1.0 — 2026-11-24

- Onglets d'information intégrés à la page, sous le graphique : **Application** (vue actuelle), **FAQ** (7 questions repliées, FR/EN, avec le tableau des écarts mensuels), **Glossaire** (6 termes avec navigation), **Code source** (lien dépôt + application originale + méthode).
- Bilingue via le mécanisme `data-i18n` existant, sans nouvelle dépendance : la page reste à ~58 Ko (Plotly et données restent dans `vendor/` et `data/`).

## 1.0.0 — 2026-11-24

- Dépendances épinglées dans `requirements.txt` : le flux mensuel automatique devient reproductible, sans montée de version subie.
- Actions GitHub épinglées par SHA de commit (checkout, setup-python, upload-pages-artifact, deploy-pages).
- Versions alignées sur `VERSION` : 1.0.0, première version annoncée et diffusée.

## 0.9.9 — 2026-11-24

- Nouvel encart d'introduction entre le graphique et le pied de page : « À quel point sommes-nous proches d'un réchauffement mondial de 1,5 °C ? » et son paragraphe explicatif, traduits de l'application originale C3S (FR/EN).

## 0.9.6 — 2026-11-24

- Mise en page alignée sur la maquette (`outil_suivi.png`) :
  - les trois cartes grises sont remplacées par un bloc de synthèse en phrases avec grandes valeurs colorées : « En octobre 2026… » (titré orange) ; « Le réchauffement d'octobre est de : +1,75 °C » (orange) ; « Le réchauffement mondial a atteint une valeur estimée à : +1,45 °C » (rouge) ; « Si la tendance sur 30 ans se poursuivait, le réchauffement mondial atteindrait 1,5 °C en : oct. 2028 » (rouge) — les deux dernières sont mises à jour à chaque déplacement du curseur ;
  - la phrase de synthèse n'apparaît plus en double dans le graphique (l'annotation d'en-tête Plotly est retirée ; restent les étiquettes 1,5 °C / +1,45 °C à droite et les encarts de dates) ;
  - date de mise à jour déplacée en haut à droite, sous les boutons FR/EN ;
  - légende du graphique centrée sous le tracé ; exports resserrés (≈ un tiers de largeur) ; responsive mobile ajusté (en-tête empilé, valeurs réduites).

## 0.9.8 — 2026-11-24

- Bloc de synthèse conforme à la maquette : le titre « En <mois> … » est placé à l'intérieur d'un encadré au fond pêche (avec les deux phrases à grandes valeurs) ; la phrase mensuelle « Le réchauffement du mois <mois année> est de : » reste en tout petit, posée sous le titre de la page.
- À l'ouverture de la page, le graphique s'affiche directement avec la dernière date sélectionnée (les lignes de tendance et les encarts de dates sont présents dès le premier rendu, sans clic sur le curseur).
- Espaces superflus supprimés : marge basse du graphique et espaces autour du pied de page réduits.

## 0.9.7 — 2026-11-24

- La date en haut à droite est sur deux lignes (« Données jusqu'à … » / « mise à jour le … »), alignée à droite et en plus petit.
- Le titre orange du bloc de synthèse reprend le libellé « En <mois> … » et suit directement le mois sélectionné par le curseur (à la place de « Extrapoler depuis : ») ; la première phrase de synthèse, « Le réchauffement du mois <mois année> est de : » (avec l'année), est écrite elle et sa valeur en tout petit, à taille identique.
- Le bloc d'options est aligné à droite et en plus petit.
- Le pied de page est aligné à gauche ; les blocs Export et Méthode sont déplacés tout en bas, sous le pied de page.
- L'étiquette rouge « 1,5 °C » à droite est relevée avec une petite flèche qui la relie à la ligne 1,5 °C.
- Nettoyage : suppression de marqueurs de conflit `=======` restés dans ce fichier après des fusions.

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

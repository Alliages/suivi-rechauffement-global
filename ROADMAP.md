# ROADMAP

Version en cours : 1.2.2. Seule liste de suivi du projet. Les idées s'ajoutent ici ; rien n'est codé sans « Lance » / « GO ».

## À faire

### Rendu visuel proche de l'application officielle C3S
Référence : capture de l'application Copernicus (Global Temperature Trend Monitor).

- **Phrases de synthèse en tête de page**, centrées, valeurs en couleur :
  - « Le réchauffement mondial a atteint un niveau estimé de X °C en <mois> » (X et mois en orange) ;
  - « Si la tendance sur 30 ans se poursuivait, il atteindrait 1,5 °C en <mois année> » (rouge sombre).
  - Remplacent ou complètent les trois cartes actuelles.
- **Curseur « Extrapoler à partir de : <mois année> »** pleine largeur, au-dessus du graphique, avec graduations par année (2000, 2004, … puis mois récents).
- **Graphique** :
  - observations mensuelles en points orange reliés par un trait fin ; partie hors fenêtre de 30 ans en orange pâle ;
  - droite de tendance rouge sombre, de début de fenêtre jusqu'au point marqué d'atteinte de 1,5 °C ;
  - lignes horizontales en pointillés : 1,5 °C (rouge) et niveau courant (orange), avec étiquette à droite ;
  - deux lignes verticales avec date en bas : mois de départ (orange) et mois d'atteinte (rouge) ;
  - enveloppe GIEC en aplat rose clair, et losange « estimation probable du GIEC » ;
  - axe x 1970 → 2060, axe y environ −0,2 → 2,0 °C, grille horizontale fine tous les 0,5 °C ;
  - légende en bas sur une ligne : tendance, observations, estimation GIEC, projections GIEC.
- Police et palette alignées sur cette référence (orange `--series`, rouge `--accent`) ; rendu identique sur mobile.
- Même mise en forme pour les exports d'images et de GIF (`render.py`), pour cohérence avec la page.

## Fait

- 0.9.0 : outil fonctionnel (pipeline, mise à jour mensuelle, page, exports). Détail dans `CHANGELOG.md`.
- 0.9.2-0.9.9 : liens du pied de page (code source, application originale, Guillaume Meunier) et version affichée, mention Copernicus, favicon, rendu aligné sur la maquette, encart d'introduction. Détail dans `CHANGELOG.md`.
- 1.0.0 : dépendances et actions GitHub épinglées (audit), versions alignées.
- 1.1.0 : onglets d'information (Application, FAQ, Glossaire, Code source), bilingues FR/EN, FAQ repliée par question, tableau des écarts mensuels, sans nouvelle dépendance.
- 1.2.0 : audit appliqué : constantes centralisées dans `pipeline/config.py` (palette page + rendu Python + libellés), `compute_trends` vectorisé, tendances vérifiées identiques à `np.polyfit`, helper `download.py` commun, rendu des images une seule fois par image d'animation, contenus des onglets déplacés dans `data/content.json` (tableau FAQ 5 généré depuis `MONTHLY_OFFSETS`), ancres `#faq`/`#glossaire`/`#code`, tests renforcés (9 tests).
- 1.2.1 : favicon hexagonal SVG (courbe GIEC + seuil 1,5 °C).
- 1.2.2 : mise à jour mensuelle le 5 seulement (au lieu des 4, 8, 15).

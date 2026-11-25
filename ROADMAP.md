# ROADMAP

Version en cours : 1.3.1. Seule liste de suivi du projet. Les idées s'ajoutent ici

## À faire

 - RAS

## Fait

- 0.9.0 : outil fonctionnel (pipeline, mise à jour mensuelle, page, exports). Détail dans `CHANGELOG.md`.
- 0.9.2-0.9.9 : liens du pied de page (code source, application originale, Guillaume Meunier) et version affichée, mention Copernicus, favicon, rendu aligné sur la maquette, encart d'introduction. Détail dans `CHANGELOG.md`.
- 1.0.0 : dépendances et actions GitHub épinglées (audit), versions alignées.
- 1.1.0 : onglets d'information (Application, FAQ, Glossaire, Code source), bilingues FR/EN, FAQ repliée par question, tableau des écarts mensuels, sans nouvelle dépendance.
- 1.2.0 : audit appliqué : constantes centralisées dans `pipeline/config.py` (palette page + rendu Python + libellés), `compute_trends` vectorisé, tendances vérifiées identiques à `np.polyfit`, helper `download.py` commun, rendu des images une seule fois par image d'animation, contenus des onglets déplacés dans `data/content.json` (tableau FAQ 5 généré depuis `MONTHLY_OFFSETS`), ancres `#faq`/`#glossaire`/`#code`, tests renforcés (9 tests).
- 1.2.1 : favicon hexagonal SVG (courbe GIEC + seuil 1,5 °C).
- 1.2.2 : mise à jour mensuelle le 5 seulement (au lieu des 4, 8, 15).
- 1.2.3 : survol des points au style de l'application officielle (bandeau orange, titre, sous-titre, mois et valeur).
- 1.2.4 : petites icônes SVG Tabler inline devant les libellés des onglets.
- 1.2.5 : bandeau d'en-tête rouge foncé pleine largeur avec le favicon en logo.
- 1.2.6 : contour blanc de 3 px autour du logo du bandeau.
- 1.2.7 : proportions de l'hexagone du logo corrigées, date d'après réduite, liens des onglets en rouge foncé.
- 1.3.0 : audit appliqué : planning du 5 effectif, droits CI par job, CSP, `app.js`/`style.css`, validation des paramètres, Dependabot + pip-audit, Pillow 13, animations FR/EN, rendu sans recréer la figure, FAQ dans `content_src.json`, tests bout en bout.
- 1.3.1 : README réorganisé (badges, en-tête centré, liens de navigation) selon le modèle fourni.

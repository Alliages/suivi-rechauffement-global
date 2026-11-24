# ROADMAP

Version en cours : 1.0.0. Seule liste de suivi du projet. Les idées s'ajoutent ici ; rien n'est codé sans « Lance » / « GO ».

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

### Onglets d'information
Barre d'onglets en haut de page, avec icône et soulignement de l'onglet actif, comme la référence :

1. **Application** : la page actuelle (synthèse, curseur, graphique, exports).
2. **FAQ** : questions fréquentes, par exemple :
   - que signifie « atteindre 1,5 °C » ici, et en quoi diffère-t-il de l'Accord de Paris (moyenne sur 20 ans) ?
   - pourquoi une extrapolation n'est-elle pas une prévision ?
   - pourquoi 30 ans de tendance ?
   - d'où viennent les données, à quelle fréquence sont-elles mises à jour ?
   - pourquoi un écart avec l'outil officiel Copernicus ?
   - qu'est-ce qu'un mois « provisoire » ?
   - comment citer et réutiliser les données et images ?
3. **Glossaire** : anomalie, niveau préindustriel (1850-1900), période de référence 1991-2020, ERA5, réanalyse, tendance linéaire, extrapolation, enveloppe GIEC, SR15, mois provisoire / final.
4. **Code source** : explication de la méthode pas à pas (reprend la section « Méthode » actuelle), extraits de `compute.py` et `config.py`, lien vers le dépôt GitHub, licence GPL3.

Contraintes : bilingue FR/EN avec le mécanisme `data-i18n` existant ; sans nouvelle dépendance ; onglets accessibles au clavier (`role="tablist"`) ; adresse par ancre (`#faq`, `#glossaire`, `#code`) pour partager un onglet.

## Fait

- 0.9.0 : outil fonctionnel (pipeline, mise à jour mensuelle, page, exports). Détail dans `CHANGELOG.md`.
- 0.9.2-0.9.9 : liens du pied de page (code source, application originale, Guillaume Meunier) et version affichée, mention Copernicus, favicon, rendu aligné sur la maquette, encart d'introduction. Détail dans `CHANGELOG.md`.
- 1.0.0 : dépendances et actions GitHub épinglées (audit), versions alignées.

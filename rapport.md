# TP NeoProto : compte-rendu

**Nom :** 

**Prénom :** 

**Date :** 

---

## 1. Implémentation et simulation du pendule double

**Q1.1** Quels sont les paramètres de simulation fournis à l'entrée du système à simuler ?
Donner le nom de chaque grandeur physique (avec son unité) et le nom de la variable correspondante dans le code.

**Q1.2** Quel solveur est utilisé pour résoudre l'équation differentielle du mouvement ?

**Q1.3** Quelles seraient les valeurs à fournir au dictionnaire `params` pour initialiser un système avec, pour chacun des pendules, un angle initial de 45 degrés et une vitesse initiale nulle ?

## 2. Analyse de données

> À partir de ce point du TP, il est conseillé de garder les paramètres suivants :
> - `time_s`: `10`
> - `time_step_s`: `0.01`

**Q2.1** Quelles sont les fonctions mathématiques représentées par chacune des méthodes `plot_XXX()` de `Simulator` ?

**Q2.2** Lancer une simulation avec les paramètres de votre choix et enregistrer les graphiques générés par chaque méthode `plot_XXX()` dans un dossier `results/` créé au préalable.
_N'oubliez pas de nommer chaque fichier de façon compréhensible!_

**Q2.3** Que peut-on caractériser avec un portrait de phase ?

**Q2.4** Définir _deux_ assertions par fonction représentée pour s'assurer que leur implémentation est cohérente.

## 3. Aspects chaotiques du système

**Q3.1** Quelle est la définition d'un système chaotique ?

**Q3.2** Trouver **deux** configurations pour les conditions initiales qui font passer le système d'un état stable à un état chaotique et les présenter.

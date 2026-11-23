# Calcul des potions et des recettes

**19 novembre 2026** · **État** Révision approuvée. [Spécification](../specification.md)

- L’énoncé exige la liste des potions réalisables et les recettes d’une potion donnée. L’élaboration propose `--list` et `--recipes` et retient la gestion de l’inventaire comme fonctionnalité supplémentaire.
- Exiger une potion de départ en stock permet de détecter une base manquante et de partir d’une potion intermédiaire déjà possédée.
- Compter le stock pour chaque suite et exclure les cycles évite de proposer des étapes qui dépensent des réactifs sans faire avancer le brassage.
- Normaliser `Awkward` et `Thick` relie les étapes des fichiers fournis. L’effet reste identifiable après un changement de contenant.

[Énoncé](../../../../../enonce-etc.md) · [Brainstorming](../../brainstorm/brainstorm.md)

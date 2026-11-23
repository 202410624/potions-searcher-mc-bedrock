# Brainstorm — Inventaire d’ingrédients de potions

- **Début** 2026-11-19
- **Dernière mise à jour** 2026-11-19
- **Clôture** 2026-11-19
- **Statut** terminé

## Besoin

Le joueur veut suivre dans son terminal les quantités d’ingrédients de potions qu’il possède. Les recettes d’exemple de `bedrock-samples-main/behavior_pack/recipes` fournissent le catalogue. Par exemple, `brew_awkward_ghast_tear.json` déclare `minecraft:ghast_tear` comme réactif. Les quantités personnelles sont conservées dans un fichier JSON local.

## Approche retenue

La saisie par arguments permet d’ajouter plusieurs ingrédients en une commande. La saisie guidée aurait demandé des réponses successives dans le terminal. La personne a choisi la saisie par arguments.

## Décisions consolidées

- `potions --show` et `potions -s` affichent les ingrédients de l’inventaire et leurs quantités.
- `potions --add` et `potions -a` acceptent une ou plusieurs paires nom-quantité. Par exemple, `potions -a blaze_powder 3 ghast_tear 6` ajoute les deux quantités aux valeurs déjà enregistrées. Sans argument, la commande affiche un exemple d’utilisation.
- L’inventaire est un objet JSON dont chaque clé est un nom d’ingrédient. La valeur associée contient le champ `nombre`, par exemple `{"ghast_tear":{"nombre":6}}`.
- La commande valide chaque paire indépendamment. Elle enregistre les ajouts dont le nom figure dans le catalogue et dont la quantité est un entier strictement positif. Chaque paire invalide est ignorée et déclenche un avertissement. Si la commande contient au moins une paire invalide, elle affiche aussi l’aide de `potions --help` (ou `potions -h`).
- Pour un nom inconnu comme `ghost_tear`, le message demandé est `l'ingredient que vous avez cherche n'existe pas`. Par exemple, `potions -a blaze_powder 3 ghost_tear 6` ajoute 3 `blaze_powder`, signale le nom inconnu et affiche l’aide. Une paire incomplète ou une quantité invalide déclenche également un avertissement.

## Questions laissées à la spécification

- Fixer le nom et l’emplacement du fichier d’inventaire ainsi que le comportement à sa première utilisation.
- Préciser les variantes de noms acceptées et la présentation de la liste et de l’aide.

## Hors portée

La synchronisation avec un inventaire en jeu et le calcul de recettes réalisables sont hors de la portée de ce besoin.

## Journal

- [Source de l’inventaire et saisie des ajouts](logs/01-inventaire-et-ajouts.md)

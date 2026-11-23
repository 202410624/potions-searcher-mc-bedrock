# Catalogue et commandes

- **Ouverture et dernière mise à jour** 19 novembre 2026
- **État** Résolu
- **Travail concerné** [Spécification de l’inventaire](../specification.md)

## Point de départ

Le brainstorming retenait les ajouts par arguments, la validation indépendante des paires et l’affichage de l’aide après une erreur. Il laissait à la spécification les variantes de noms et la présentation de la sortie.

## Évolution de la réflexion

- Les recettes fournies comprennent des recettes de mélange et de changement de contenant. Les deux utilisent le champ `reagent` et contribuent au catalogue.
- Les recettes utilisent des identifiants préfixés par `minecraft:` et les exemples approuvés utilisent des noms courts. L’élaboration a retenu les deux formes avec une clé courte commune. Elle a aussi retenu un tri alphabétique à l’affichage et un seul affichage de l’aide après les avertissements d’une commande.
- Le premier brouillon attribuait l’ajout multiple à `--add`. La personne a demandé que `--add` et `-a` acceptent un seul ingrédient et que `--add_multiple` et `-am` prennent en charge les ajouts multiples.

## Décision

La commande d’ajout simple accepte une seule paire. L’élaboration a retenu le rejet complet en présence d’arguments excédentaires pour signaler une erreur de syntaxe sans effectuer d’ajout. La validation indépendante des paires s’applique à l’ajout multiple. La personne a approuvé la spécification mise à jour.

## Source

- [Dossier de brainstorming](../../brainstorm/brainstorm.md)

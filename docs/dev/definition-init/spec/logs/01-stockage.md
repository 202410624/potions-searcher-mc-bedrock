# Stockage de l’inventaire

- **Ouverture et dernière mise à jour** 19 novembre 2026
- **État** Résolu
- **Travail concerné** [Spécification de l’inventaire](../specification.md)

## Point de départ

Le choix d’un inventaire JSON local et du champ `nombre` vient de la personne. Le brainstorming laissait le chemin et le comportement à la première utilisation à la spécification.

## Options examinées

Un fichier relatif au répertoire courant rendrait l’inventaire dépendant de l’endroit où le joueur lance la commande. Un fichier sous le dossier personnel donne au joueur un emplacement stable. La création lors de la consultation aurait impliqué une écriture pour une opération de lecture.

## Décision

L’élaboration a retenu `~/.potions/inventaire.json` et la création au premier ajout valide. Un fichier absent représente un inventaire vide. Si un fichier existant est illisible ou invalide, une erreur signale le problème et le fichier est préservé. La personne a approuvé la spécification qui consigne ces décisions.

## Source

- [Dossier de brainstorming](../../brainstorm/brainstorm.md)

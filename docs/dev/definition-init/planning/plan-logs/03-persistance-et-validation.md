# Sujet de travail — Persistance et validation de la commande

- **Ouvert le** 2026-11-19
- **Dernière mise à jour** 2026-11-19
- **État** Résolu
- **Travail concerné** [Plan d’implantation](../plan.md)

## Point de départ

Préciser le traitement d’une commande partiellement valide et le modèle minimal de fichier pour que la mise en œuvre puisse être testée.

## Options examinées

Écrire chaque paire valide au fur et à mesure expose les lots à un échec après une écriture partielle. Valider tout le lot puis remplacer le fichier depuis un temporaire dans le même dossier donne un seul point d’écriture. Pour les commandes, un parseur personnalisé permettrait de tout contrôler, mais `argparse` gère déjà les alias et l’aide. La CLI peut valider les paires et les quantités après l’analyse des options.

## Décision actuelle

L’agent retient un remplacement atomique par lot et un verrou adjacent ouvert en mode exclusif. Un verrou déjà présent entraîne un échec explicite qui laisse le stock intact. Un arrêt forcé peut laisser un verrou résiduel. Le README expliquera comment le retirer une fois tous les processus arrêtés. Le lecteur conserve le niveau positif présent sur une potion et accepte son omission avec la valeur logique 1. Un premier ajout de potion écrit le niveau 1. La CLI utilise `argparse`, traite les paires de gauche à droite et avertit pour un dernier objet sans quantité. Une commande avec des paires invalides renvoie 2 après avoir appliqué son éventuel sous-ensemble valide. Les erreurs de fichier renvoient 1, et une consultation sans résultat renvoie 0.

## Artefacts liés

- [Spécification approuvée](../../spec/specification.md)

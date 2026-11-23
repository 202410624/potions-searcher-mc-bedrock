# Sujet de travail — Catalogue et parcours

- **Ouvert le** 2026-11-19
- **Dernière mise à jour** 2026-11-19
- **État** Résolu
- **Travail concerné** [Plan d’implantation](../plan.md)

## Point de départ

Déterminer la représentation des états et la frontière entre lecture des données et calcul des suites.

## Faits et contraintes

Les deux fichiers de changement de contenant décrivent des familles génériques, avec `minecraft:potion`, `minecraft:splash_potion` et `minecraft:lingering_potion`. Le contrôle des données livrées a relevé 70 recettes de mélange, deux règles de contenant et aucun JSON mal formé. Les fichiers de mélange identifient des effets concrets. Avec le stock d’exemple, la larme de Ghast permet aussi de transformer l’eau en potion banale. Les suites approuvées distinguent le départ et chaque transformation. Les quantités sont propres à chaque suite.

## Options examinées

Appliquer les règles génériques pendant le parcours obligerait le moteur et la validation des requêtes à connaître les conventions Bedrock. Développer ces règles au chargement donne un ensemble d’états et de transitions que les deux consommateurs peuvent partager. Un suivi des états commun à tout le parcours éliminerait des suites distinctes qui convergent. Suivre les états et les quantités pour chaque branche conserve ces suites.

## Décision actuelle

L’agent retient un catalogue en mémoire indexé par état de départ. Il concrétise les changements de contenant en conservant l’effet. Le moteur parcourt ce graphe en profondeur depuis chaque potion en stock, avec les états visités et les réactifs consommés propres à la branche. Les recettes identiques issues de fichiers redondants partagent une transition. Le champ `niveau` est conservé dans le stock et la distinction entre effets suit les identifiants Bedrock.

## Artefacts liés

- [Spécification approuvée](../../spec/specification.md)

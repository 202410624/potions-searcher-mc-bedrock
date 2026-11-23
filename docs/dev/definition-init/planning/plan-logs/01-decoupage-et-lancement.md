# Sujet de travail — Découpage et lancement

- **Ouvert le** 2026-11-19
- **Dernière mise à jour** 2026-11-23
- **État** Résolu
- **Travail concerné** [Plan d’implantation](../plan.md)

## Point de départ

Définir les unités du premier assistant Python et rendre la commande `potions` accessible depuis un répertoire quelconque.

## Faits et contraintes

Le dossier contient la spécification approuvée et les données Bedrock fournies. La racine ne contient ni code Python ni dépôt Git. L’énoncé exige des tests unitaires, des exemples et un flux que l’élève peut expliquer.

## Options examinées

Un script unique minimise la préparation, mais ferait évoluer ensemble le décodage des fichiers Bedrock, la persistance, la recherche et les arguments. Un paquet avec un point d’entrée installé en mode éditable permet de garder les données fournies à leur emplacement et d’utiliser la commande depuis n’importe quel dossier.

## Décision actuelle

L’agent retient un paquet `assistant_potions` avec quatre modules. Le catalogue décode les données, l’inventaire possède le format et l’écriture, le moteur calcule les suites, et la CLI orchestre les trois. Chaque tâche livre une de ces unités et ses tests. L’installation éditable expose `potions` et lui donne accès aux données du dossier de remise. Le plan est placé sous `docs/dev/definition-init/planning/`, au même niveau que la spécification et le brainstorming. Les points de contrôle Git s’appliquent si le dossier est placé dans un dépôt.

Le plan initial proposait le cadre de tests fourni avec Python. L’élève a choisi `pytest` le 19 novembre 2026 et a demandé de simplifier son intégration le 23 novembre. Les fichiers qui appellent l’API utilisent `import pytest`. La suite se lance avec un interpréteur sur lequel `pytest` est disponible.

## Artefacts liés

- [Spécification approuvée](../../spec/specification.md)

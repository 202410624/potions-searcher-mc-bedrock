---
name: spec-elaboration
description: "À utiliser après brainstorming lorsqu'une approche choisie doit être transformée en spécification de conception approuvée avant planning. Ne sert ni à découvrir le besoin ni à produire le plan d'implantation."
---

# Élaborer une spécification

**Skill compagnon requis :** lire et appliquer [`documenting-work`](../documenting-work/SKILL.md) pour suivre les choix de conception pendant cette étape.

## Étape préiminaire

Une spec est l'étape de réalisation d'un `brainstorming`, à moins que la personne n'établisse une demande claire et cohérente de réalisation et renseigne explicitement toutes les informations requises. Si la demande est ambigue ou imprécise, demander l'établissement d'un livrable de `brainstorming` avant la réalisation de la spec. Ne pas démarrer soi-même ce brainstorming.

## Étape de réalisation

Transformer le dossier de décisions de `brainstorming`, ou la demande précise et complète, en document de
conception suffisamment précis pour que `planning` puisse préparer un plan sans
devoir clarifier de nouveau le besoin.

## Vérifier les entrées

Vérifier que soient connus les mêmes informations qu'un brainstorm renseigne :

- le problème, le public cible, l'intention et la raison;
- les objectifs, non-objectifs et anti-objectifs;
- les contraintes importantes;
- l'approche choisie et les compromis acceptés;
- les principales décisions de comportement ou de réalisation;
- les questions ouvertes laissées à la personne qui construira le plan.

Si une information manque et que sa réponse modifierait le résultat, interrompre
l'élaboration, indiquer ce qui manque et demander à la personne de compléter
l'entrée ou de faire réaliser un `brainstorming`. Ne jamais invoquer
automatiquement l'étape antécédente ni combler silencieusement une décision
importante.

Une décision raisonnable qui ne modifie pas la portée peut être prise ici.
L'identifier comme une décision de conception, la justifier et en conserver le cheminement dans un journal.

## Dimensionner le document

| Ampleur | Forme |
|---|---|
| Petite modification | Spécification courte : une ou deux phrases par section pertinente |
| Projet ou évolution structurante | Spécification complète |

Si le travail contient plusieurs projets indépendants, produire une
spécification distincte pour chacun et convenir de leur ordre.

## Rédiger

Créer le document à partir de
[`assets/spec-template.md`](assets/spec-template.md). Retirer seulement les sections sans objet; ne pas laisser de champs fictifs ni de mentions « à déterminer ».

Distinguer :

- ce que la personne a demandé ou décidé;
- les décisions prises durant l'élaboration, avec leur justification;
- ce qui reste à la discrétion de la personne qui construira.

Décrire le comportement attendu et les contraintes sans écrire le plan d'implantation tâche par tâche.

## Vérifier du point de vue de la construction

Effectuer une passe de conformité et de cohérence de la spec afin de s'assurer qu'elle couvre tous les aspects d'implantation et soit diffusable et compréhensible, sans les détails d'élaboration, aux instances chargées de l'implantation.

Classer chaque constat :

- **Déjà répondu** : intégrer la réponse présente dans la conversation ou le
  projet.
- **Mineur** : trancher raisonnablement et consigner la décision.
- **Réservé à la personne** : poser la question, car sa réponse modifie le
  résultat.

Regrouper les questions réservées dans un seul message, de la plus importante à
la moins importante. Mettre ensuite la spécification à jour. Ne faire qu'une
seule passe de questions issue de cette vérification.

## Faire approuver

Présenter le document et une courte liste des décisions prises durant son
élaboration. Demander explicitement si la spécification décrit bien ce qui doit
être construit.

### Barrière obligatoire

Ne jamais invoquer ni commencer automatiquement une étape antécédente ou
suivante. Ne pas invoquer `planning` et ne rien construire, même après
l'approbation de la spécification, sans une demande explicite de la personne ou
d'un skill d'orchestration. La lecture et l'exploration restent permises.

Si l'approbation demande une modification, mettre le document à jour et obtenir
une nouvelle approbation.

## Livrables attendus

Une spécification de conception approuvée constitue un seul livrable, même si
son élaboration s'étend sur plusieurs échanges. Si le travail contient plusieurs
projets indépendants, chacun produit son propre livrable.

Le livrable comprend :

- le document de spécification consolidé, créé à partir du gabarit;
- les journaux des décisions de conception prises durant l'élaboration, liés
  depuis la spécification;
- les diagrammes, exemples, contrats d'interface ou autres artefacts retenus
  lorsqu'ils sont nécessaires pour comprendre sans ambiguïté ce qui doit être
  construit.

Le livrable est considéré comme final lorsque l'approbation explicite de la
personne est consignée dans la conversation.

Le skill définit l'organisation interne du livrable, mais pas son emplacement
global. Utiliser le répertoire de destination fourni par la personne ou par un
skill d'organisation. Ne pas déduire si le projet est organisé par initiative,
par étape ou selon une autre convention. Si aucune destination n'est fournie,
présenter la spécification dans la conversation et demander où l'enregistrer
avant de créer des fichiers.

Organiser le livrable ainsi :

```text
<destination>/
├── specification.md
├── logs/
├── diagrams/
└── annexes/
```

Créer `logs/` dès qu'une décision de conception demande une réflexion distincte;
appliquer [`documenting-work`](../documenting-work/SKILL.md) pour la tenir à
jour. Ne créer `diagrams/` et `annexes/` que lorsqu'ils contiennent un artefact
retenu. Relier chaque journal et artefact depuis `specification.md`.

Les notes brutes, les variantes rejetées sans valeur explicative, le
plan d'implantation et le code produit ne font pas partie du livrable. Une
question qui modifierait le résultat ne doit pas demeurer ouverte au moment de
l'approbation; seules les libertés de réalisation explicitement déléguées peuvent
être transmises à `planning`.

Après approbation, remettre le chemin de la spécification et, le cas échéant,
de ses artefacts retenus. Indiquer que ce livrable peut alimenter `planning`,
puis s'arrêter. Attendre une demande explicite avant toute étape suivante et ne
pas commencer directement l'implantation.

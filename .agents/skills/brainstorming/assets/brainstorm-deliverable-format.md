# Format du livrable de brainstorming

## Unité du livrable

Un brainstorming complet constitue un seul livrable.

Le skill définit l'organisation interne de ce livrable, mais pas son emplacement
dans le projet. Utiliser le répertoire de destination fourni par la personne ou
par un skill d'organisation. Ne pas déduire si le projet est organisé par
initiative, par étape ou selon une autre convention. Si aucune destination n'est
fournie, présenter le livrable dans la conversation et demander où l'enregistrer
avant de créer des fichiers.

## Organisation

Regrouper le livrable dans un dossier autonome :

```text
<destination>/
├── brainstorm.md
├── logs/
│   ├── 01-public-cible.md
│   └── 02-portee.md
├── diagrammes/
├── prototypes/
└── annexes/
```

Créer `logs/` dès qu'un sujet de réflexion doit être suivi séparément. Ne créer
les autres sous-dossiers que lorsqu'ils contiennent réellement un artefact retenu.

## Fichier principal

Créer le fichier Markdown principal `brainstorm.md` à partir de
[brainstorm-template.md](brainstorm-template.md). Adapter les sections au sujet
sans conserver de rubrique vide qui n'apporte rien.

Garder ce fichier concis et consolidé. Il contient un index compact des sujets de
réflexion, mais pas leur journal détaillé.

## Journaux des sujets de réflexion

Appliquer le skill [`documenting-work`](../../documenting-work/SKILL.md) pour
segmenter les sujets et tenir leurs journaux dans `logs/`. Après une avancée
significative, mettre à jour les sections consolidées et l'index des sujets
dans `brainstorm.md`.

## Artefacts retenus

Conserver avec le fichier principal les artefacts qui appuient une décision ou
facilitent la transmission du brainstorming :

- les diagrammes retenus, avec leur source modifiable et, lorsque pertinent, une
  version directement consultable;
- les prototypes exploratoires utiles, isolés dans leur propre dossier;
- les maquettes, comparaisons, exemples de données ou autres annexes nécessaires.

Chaque prototype conservé comporte une courte note qui indique la question
explorée, ce qui a été essayé, les apprentissages obtenus, la décision qui en
découle et son devenir : jeter, conserver comme référence ou reprendre dans un
travail ultérieur.

Ne pas conserver tous les brouillons ou toutes les variantes. Consigner plutôt
les options rejetées et leur motif dans le fichier principal lorsqu'elles sont
utiles à la compréhension des décisions.

## Clôture

Le livrable terminé doit permettre à `spec-elaboration` d'identifier directement :

- les décisions à respecter;
- l'approche retenue et les compromis acceptés;
- les artefacts à utiliser;
- les questions encore ouvertes;
- les éléments explicitement hors portée.

Avant de déclarer le brainstorming terminé :

1. demander une dernière correction;
2. confirmer la destination du livrable;
3. enregistrer le livrable à cette destination, ou obtenir l'accord explicite
   de la personne pour le conserver uniquement dans la conversation;
4. vérifier que les décisions, les questions ouvertes et les éléments hors
   portée sont consolidés.

Une destination absente est une action à résoudre, pas une raison de déclarer
le brainstorming terminé. Ne pas déduire un emplacement à partir de la structure
du projet.

Le livrable documente la réflexion et ses conclusions; il ne constitue ni une
spécification ni un plan de réalisation. Sa clôture ne démarre pas
automatiquement `spec-elaboration`.

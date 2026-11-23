---
name: brainstorming
description: "Utiliser avant toute évolution dont le besoin, le public cible, l'intention, la finalité, la portée ou l'approche n'est pas suffisamment défini. Clarifier le problème et produire les décisions nécessaires à spec-elaboration; ne pas rédiger ni la spécification ni le plan."
---

# Objectifs

Découvrir l'intention et la couverture d'une modification, d'un ajout ou d'un nouveau développement. Le résultat attendu est une approche choisie et inventaire de décisions utilisable par `spec-elaboration`.

**Skill compagnon requis :** lire et appliquer [`documenting-work`](../documenting-work/SKILL.md) pour tenir les journaux des sujets de réflexion pendant ce brainstorming.

## Déterminer si une conversation est nécessaire

- Ne pas transformer une tâche claire en processus de brainstorm inutile. 
- Si une décision peut émerger directement, faire une proposition concrète et annoncer les hypothèses
importantes.

## Établir le contexte

Dans un projet existant, lire avant de questionner :

- la vision, le public cicle, la finalité et l'intention du projet;
- les fichiers, spécifications et plans désignés;
- le fonctionnement actuel des parties concernées;
- les conventions et contraintes établies;
- l'état du progrès du projet;
- les décisions ultérieures consignées en lien avec l'état de progression actuel.

Ne pas demander une information déjà présente ni rouvrir une décision prise.
Présenter les constatations susceptibles de modifier la demande.

## Conduire la conversation

- S'assurer de la compréhension de la demande en reformulant brièvement son énoncé;
- indiquer, selon ta comréhension, quel est le changement, le public cible, son intention, les parties touchées et les contraintes découvertes;
- inviter la personne à corriger cette compréhension.

S'il manque une information, poser une question ouverte sans proposer de réponses.
Poser une seule question à la fois en informant en quoi elle permet de faire progresser la réflexion.

Amener la personne à décrire avant de lui présenter des options. Utiliser son
vocabulaire et éviter le jargon de processus. Si un terme technique permet d'alléger la discussion ou d'aobrder le problème sous un nouvel angle, introduire la terminologie adéquate sans élaborer les détails théoriques.

### Territoire à couvrir

Utiliser cette liste comme aide-mémoire, jamais comme questionnaire :

- problèmes à rédoudres;
- intentions de la personne;
- visions à long termes;
- raison d'agir maintenant;
- résultat attendu et critères de réussite;
- objectifs, non-objectifs et anti-objectifs;
- état actuel et tentatives antérieures;
- contraintes techniques, pédagogiques ou organisationnelles;
- détails importants et exemples appréciés ou rejetés.

Construire chaque question à partir de la réponse précédente ou d'une
constatation du projet.

## Présenter les approches

Lorsque le besoin est compris par toi et la personne, présenter les approches dans un message distinct.

1. Trouver plusieurs solutions réelles.
2. Écarter celles qui contredisent l'objectif ou les contraintes.
3. Décrire les deux ou trois approches restantes et leurs compromis.
4. Recommander une approche et justifier le choix.
5. Faire choisir la personne, sauf si elle vous a confié cette décision.

Lorsqu'une seule approche est raisonnable, l'indiquer et expliquer pourquoi les
autres ne conviennent pas.

## Utiliser un support visuel

Garder les exigences, la portée et les compromis conceptuels dans le texte.
Utiliser un support visuel comme une esquisse, une maquette ou un diagramme lorsqu'ils facilient la compréhension et permettent d'appuyer les propos du texte.

## Prototype exploratoire

Proposer un prototype jetable peu couteux sans l'implanter directement. Un prototype approuvé :

- répond à une question précise;
- comporte peu ou pas de tests;
- n'est pas du code de production;
- ne remplace ni la spécification ni le plan;
- apporte un exemple tangible de réalisation potentielle; 
- rapporte ses apprentissages dans la conversation.

Conserver ou développer ce prototype constitue une nouvelle décision de la personne.

## Reformuler progressivement

Dès qu'une partie est comprise, la reformuler puis demander ce qui est incorrect
ou manquant. Distinguer les décisions de la personne, vos propositions
justifiées et les questions encore ouvertes.

Documenter la progression du brainstorming et les décisions prises tout le long du processus.

## Critères de fin

Le brainstorming est terminé lorsque la personne décide de clore le brainstorming ou sinon sont suffisamment définis :

- le problème, le public cible et l'intention;
- les objectifs, non-objectifs et anti-objectifs;
- les contraintes importantes;
- l'approche choisie et les compromis acceptés;
- les principales décisions de comportement ou de réalisation;
- les questions ouvertes laissées à la personne qui réalisera la spécification.

Avant de déclarer le brainstorming terminé, vérifier aussi que la destination du
livrable est connue. Si elle ne l'est pas, demander où l'enregistrer.

Ne pas rédiger la spécification dans ce skill.

### Contrôle de clôture

Ne clore le brainstorming qu'après avoir vérifié les éléments suivants :

- les décisions sont consolidées;
- une dernière correction a été demandée;
- la destination est confirmée;
- le livrable est enregistré, ou sa conservation uniquement dans la conversation actuelle est explicitement acceptée;
- aucune étape suivante n'est démarrée automatiquement.

## Limite entre les étapes

Ne jamais invoquer ni commencer automatiquement une autre étape ou un autre
skill. Lorsque le brainstorming est terminé, présenter le livrable, indiquer
qu'il peut alimenter `spec-elaboration`, puis s'arrêter. Attendre une demande
explicite de la personne ou d'un skill d'orchestration avant de poursuivre.

## Livrables attendus

Un brainstorming constitue un seul livrable.

Pour documenter ou clore un brainstorming, lire
[references/brainstorm-deliverable-format.md](assets/brainstorm-deliverable-format.md), puis présenter le
dossier de décisions et demander une dernière correction.

Avant ce passage, ne pas écrire de code produit, créer de structure de projet ni
installer de dépendances. La lecture, l'exploration et un prototype explicitement
approuvé restent permis.

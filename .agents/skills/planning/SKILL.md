---
name: planning
description: À utiliser lorsqu'une spécification ou des exigences décrivent une tâche en plusieurs étapes, avant de modifier le code
---

# Planifier

**Skill compagnon requis :** lire et appliquer [`documenting-work`](../documenting-work/SKILL.md) pour suivre les décisions de planification au fil du travail.

## Vue d'ensemble

Rédiger des plans de mise en œuvre d'une sécification.

- Présumer la rédaction de code idiomatique dans le langage du projet. 
- Décider sur les questions ouvertes. Documenter ces décisions. 
- Fournir le plan complet sous forme de tâches ciblées. 
- Renforcer DRY, YAGNI et le développement piloté par les tests (TDD).

## Vérification de la portée

Si la spécification englobe plusieurs sous-systèmes indépendants ou plusieurs fonctionnalités distinctes, recommander de la décomposer en plans distincts, chacun étant consacré à un sous-système ou à une fonctionnalité. Chaque plan doit aboutir à un composant fonctionnel, autonome et testable indépendamment des autres.

Décomposer tout plan dont la mise en oeuvre produirait un ensemble de changements trop vaste ou complexe pour être compris, observé et vérifié efficacement par un humain en une seule révision. Chaque sous-plan doit produire un résultat cohérent et vérifiable.

## Décomposition en unités

Avant de définir les tâches, identifier et préciser: 

- les unités à créer ou à modifier;
- leur responsabilité;
- leur interfaces. 

C'est à cette étape que les décisions de décomposition sont arrêtées.

- Chaque unité doit avoir une responsabilité unique, des frontières claires et des contrats explicites.
- Privilégier des unités de taille adéquate pour être comprises, modifiées et vérifiées indépendamment.
- Regrouper les éléments qui évoluent et opèrent ensemble. Décomposer selon les responsabilités plutôt que selon les couches techniques.
- Dans un projet existant, respecter les conventions et la structure établies.
- Ne prévoir une restructuration que lorsqu'elle est nécessaire à l'implantation ou améliore sensiblement la maintenabilité.

Cette décomposition détermine l'organisation des fichiers et guide la définition des tâches. Chaque tâche doit produire un changement cohérent, observable et vérifiable indépendamment.

## Journaux de planification

Pour un plan enregistré dans `<destination>/<nom-fichier>.md`, placer les
journaux dans `<destination>/<nom-fichier>-logs/`. Ouvrir un journal dès qu'un
choix de décomposition, d'interface, d'ordre des tâches ou de vérification exige
une réflexion distincte. La décomposition initiale doit laisser une trace de
ses choix importants; une simple liste finale de décisions dans le plan ne
remplace pas ce cheminement.

Suivre le format et la mise à jour des journaux définis dans
[`documenting-work`](../documenting-work/SKILL.md). Lier chaque journal au
résumé de la décision active dans l'en-tête du plan. Les décisions déjà fixées
par la spécification sont des contraintes à reprendre, non des décisions
nouvelles à attribuer à la planification.
Si aucune décision nouvelle n'a été nécessaire, inscrire « Aucune décision
nouvelle » dans cette section du plan et ne pas créer de journal vide.

## Dimensionnement des tâches

Une tâche est la plus petite unité qui possède son propre cycle de tests et qui mérite une étape de révision distincte. Pour déterminer les frontières des tâches, intégrer la préparation, la configuration, la mise en place de la structure et la documentation à la tâche dont le livrable en dépend. Ne séparer des tâches que lorsqu'une personne chargée de la révision pourrait raisonnablement refuser l'une tout en approuvant l'autre. Chaque tâche se termine par un livrable testable de façon indépendante.

## Granularité des étapes

**Chaque étape correspond à une action dont le résultat peut être vérifié :**

- « Écrire le test qui échoue » : une étape.
- « Exécuter le test pour confirmer qu'il échoue » : une étape.
- « Écrire le minimum de code nécessaire pour faire réussir le test » : une étape.
- « Exécuter les tests pour confirmer qu'ils réussissent » : une étape.
- « Créer un commit » : une étape.

## En-tête du document de planification

Chaque plan DOIT commencer avec le contenu de [`assets/plan-header-template.md`](assets/plan-header-template.md). Copier ce modèle d'en-tête dans le nouveau document, puis remplacer tous les champs entre crochets par les valeurs tirées de la spécification. Conserver les sections « Contraintes globales » et « Points d'attention pour la révision », même lorsqu'elles sont vides après vérification.

## Structure d'une tâche

Chaque tâche DOIT suivre le contenu de [`assets/task-template.md`](assets/task-template.md). Copier ce modèle pour chaque tâche, puis remplacer tous les champs entre crochets et les exemples par les fichiers, interfaces, tests, commandes et résultats attendus propres à cette tâche.

## Contenu d'une étape

Une étape est terminée lorsque la personne chargée de la mise en œuvre peut en tirer exactement une réalisation raisonnable. C'est l'unique exigence : l'étape doit être sans ambiguïté, mais elle n'a pas à être exhaustive. Chaque type d'étape contient uniquement les renseignements nécessaires pour éliminer l'ambiguïté :

### Étapes

Les étapes suivantes:

- **Test :** le nom du test et ses assertions, sous forme de code, avec les valeurs exactes de la spécification.
- **Code :** la signature exacte (nom, paramètres, type de retour), le fichier où elle se trouve et les valeurs précises imposées par la spécification. La personne chargée de la mise en œuvre écrit le corps. Le corps n'est fourni que pour un algorithme que la signature et les tests ne permettent pas de déduire, ou pour un texte exact imposé par la spécification.
- **Vérification :** la commande à exécuter et le résultat qui confirme la réussite.
- **Une référence à une autre tâche :** le bloc « Interfaces » de cette autre tâche précise ce qu'il faut utiliser; le plan ne répète pas son code.

### Qualité du plan

- **Décisions** : Le plan doit expliciter les décisions qui ne peuvent être laissées à la personne chargée de l'implantation.
- **Concision** : Le plan doit guider l'implantation sans décrire le code à écrire.
- **Complétude** : Éviter les décisions reportées, les directives vagues et les éléments non définis.
- **Autoévaluation** : Détecter les détails excessifs et les décisions manquantes.

## Autoévaluation

Après avoir rédigé le plan complet, relire la spécification avec un regard neuf et vérifier le plan en fonction de celle-ci. Cette liste sert à votre propre vérification; elle ne demande pas de déléguer la révision à un sous-agent.

**1. Couverture de la spécification :** Parcourir chaque section ou exigence de la spécification. Peut-on désigner une tâche qui la met en œuvre? Énumérer les lacunes.

**2. Examen des étapes :** Chaque étape doit permettre à la personne chargée de la mise en œuvre de produire exactement une réalisation raisonnable, sans en contenir davantage. Une ligne qui ne prend aucune décision est une lacune; le corps d'une fonction déjà déterminé par la signature et les tests est une transcription. Corriger les deux.

**3. Cohérence des types :** Les types, les signatures de méthodes et les noms de propriétés utilisés dans les tâches ultérieures correspondent-ils à ceux définis dans les tâches précédentes? Une fonction nommée `clearLayers()` dans la tâche 3, mais `clearFullLayers()` dans la tâche 7, constitue une erreur.

**4. Points d'attention pour la révision :** Pour chaque catégorie d'entrées ou mode de défaillance suggéré par la spécification, existe-t-il une tâche dont les tests le couvrent? Les cinq cas non couverts les plus susceptibles de nuire à une personne doivent figurer dans la section « Points d'attention pour la révision », et le test correspondant à chaque élément doit être ajouté à la tâche qui possède le code concerné. Une section vide signifie que la vérification a été faite et qu'aucun cas n'a été trouvé, et non que la vérification a été omise.

**5. Proportion :** Comparer la longueur du plan à celle de la spécification. Un plan plusieurs fois plus long que la spécification qu'il met en œuvre est une transcription du programme, et non un plan. Si les blocs de code occupent la majeure partie du document, remplacer les corps par des signatures, des noms de tests et des assertions, puis vérifier que chaque étape demeure sans ambiguïté.

Si des problèmes sont découverts, les corriger directement. Il n'est pas nécessaire de refaire l'autoévaluation : corriger, puis poursuivre. Si une exigence de la spécification n'est associée à aucune tâche, ajouter la tâche manquante.

## Passage à l'exécution

Après avoir enregistré et autoévalué le plan, fournir à votre partenaire humain un lien lui permettant de le lire. Si cette personne a déjà indiqué explicitement une méthode d'exécution, lui demander de réviser le plan et de confirmer qu'il correspond à ses attentes. Attendre sa révision avant de commencer la mise en œuvre, puis utiliser la méthode retenue. Sinon, lui demander de réviser le plan et de choisir une méthode d'exécution avant de commencer la mise en œuvre.

**« Plan terminé et enregistré dans `<destination>/<nom-fichier>.md`. Veuillez le réviser. Correspond-il à vos attentes? »**


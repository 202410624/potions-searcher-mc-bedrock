---
name: executing-plans
description: "Mettre en œuvre un plan de développement Python, une fonctionnalité à la fois, avec tests exécutés et résultats vérifiables. À utiliser lorsqu'un plan est prêt à être réalisé."
---

# Exécuter un plan

Lire le plan, la spécification ou les critères d'acceptation, les consignes du projet et le code concerné. Respecter les modifications déjà présentes. Appliquer [`programming-standards`](../programming-standards/SKILL.md) au code créé ou révisé et utiliser [`documenting-work`](../documenting-work/SKILL.md) pour conserver les décisions importantes prises pendant l'exécution.

## Avancer par fonctionnalité

Pour chaque tâche du plan :

1. Repérer le comportement attendu, les fichiers concernés et la vérification prévue. Relever toute contradiction avec les exigences avant de coder.
2. Écrire ou adapter un petit ensemble de tests qui vérifie le comportement observable. Couvrir les cas normaux, limites et invalides pertinents. Exécuter au moins un nouveau test et vérifier qu'il échoue pour la raison attendue.
3. Implémenter la fonctionnalité sans élargir la portée. Garder visibles la validation des entrées, les erreurs, les invariants et les événements à journaliser lorsque le sujet les exige.
4. Exécuter les tests ciblés, puis la suite du projet. Pour les projets de l'atelier, la commande de référence est `python -m pytest -q`.
5. Lire les résultats et examiner les changements. Corriger un échec avant de déclarer la tâche terminée; vérifier qu'un test ne reproduit pas seulement l'implémentation. Mettre à jour le suivi du plan et consigner les commandes réellement exécutées avec leurs résultats dans le journal du projet.

Passer à la tâche suivante lorsque son comportement est vérifié. Un test qui réussit sans avoir mis en évidence le défaut attendu doit être réexaminé.

## Traiter un écart

Si le plan contredit les exigences ou le code existant, déterminer le changement minimal qui respecte le résultat demandé. Consigner le constat, les options et le choix dans un journal selon `documenting-work`; relier ce journal au suivi du plan. Placer ces journaux à côté du plan, dans `<nom-du-plan>-execution-logs/`. Demander une précision lorsque l'écart modifierait le comportement attendu ou qu'aucune interprétation raisonnable ne permet de poursuivre.

Ne pas présenter une vérification non exécutée comme réussie. Signaler les blocages et les limites observés sans inventer de résultat.

## Vérifier l'ensemble

Après la dernière modification :

- comparer le résultat aux critères d'acceptation et aux tâches du plan;
- examiner les changements hors portée, les cas limites manquants, les assertions employées à la place d'une validation et les journaux trop silencieux ou trop bavards;
- exécuter à nouveau la suite complète et lire son résultat;
- résumer les fonctionnalités réalisées, les tests exécutés et leurs résultats, les décisions prises et les limites restantes, avec des liens vers les journaux utiles.

Le travail est terminé lorsque le résultat demandé est observable et que son état de vérification est rapporté fidèlement.

# Standards de programmation pour les projets Python

Le code attendu doit pouvoir être lu, expliqué, débogué et modifié par une personne qui reprend le projet. Ces critères s'appliquent au code nouveau ou directement touché par une demande.

## Noms et mise en forme

- Nommer les éléments selon leur rôle dans le domaine, plutôt qu'avec des noms génériques comme `data`, `item` ou `manager` lorsque leur rôle est connu.
- Employer `snake_case` pour les modules, fonctions et variables, `PascalCase` pour les classes et `UPPER_SNAKE_CASE` pour les constantes. Garder un même terme pour un même concept dans tout le projet.
- Utiliser quatre espaces par niveau d'indentation. Répartir les collections, appels et conditions sur plusieurs lignes lorsque cela facilite la lecture.
- Éviter les abréviations obscures et les noms à une lettre, sauf pour un indice local évident.
- Respecter les conventions cohérentes déjà présentes dans le projet. Ne pas ajouter de formateur, de linter ou de dépendance pour appliquer ce document.

## Flux de contrôle et fonctions

Une clause de garde rend une entrée invalide ou une sortie anticipée visible avant le traitement principal :

```python
def calculate_total(prices, discount_rate):
    if not 0 <= discount_rate <= 1:
        raise ValueError("discount_rate must be between 0 and 1")

    subtotal = sum(prices)
    discount = subtotal * discount_rate
    return subtotal - discount
```

Préférer une boucle explicite lorsque le traitement comporte plusieurs décisions, des sorties anticipées ou des effets de bord. Une compréhension reste appropriée pour une transformation courte et claire.

Extraire une fonction si son nom révèle une règle du domaine, si une décision doit être testée isolément ou si une répétition est significative. Ne pas découper le code uniquement pour raccourcir un fichier. Une classe ou une abstraction générique doit répondre à une responsabilité réelle du projet.

## Entrées, exceptions et assertions

- Valider les données externes avec une condition et une exception adaptée. Les assertions Python peuvent être désactivées; elles ne conviennent donc pas à la validation des entrées.
- Utiliser une assertion pour un état qui devrait être impossible si le programme est correct, par exemple une capacité restante négative après une affectation déjà validée.
- Capturer une exception seulement si le code peut la traiter, la traduire, l'enrichir ou effectuer un nettoyage nécessaire. Conserver l'erreur initiale lors d'une traduction utile au diagnostic :

```python
try:
    records = load_records(path)
except OSError as error:
    raise RuntimeError(f"Cannot load records from {path}") from error
```

Ne pas intercepter toutes les erreurs pour retourner silencieusement une valeur par défaut. La gestion d'une ligne invalide d'un fichier peut toutefois être locale si le cahier des charges demande de poursuivre le traitement.

## Journalisation et commentaires

Journaliser les événements nécessaires pour comprendre les opérations et les refus prévus par le sujet. Éviter de répéter dans le journal chaque ligne de code exécutée ou de copier des données sensibles sans nécessité.

Un commentaire en français explique une raison, une contrainte ou un choix difficile à déduire du code. Il ne traduit pas une instruction Python évidente. Supprimer ou corriger un commentaire qui ne correspond plus au comportement.

## Révision d'un changement

Avant de conclure, vérifier que :

- le chemin principal se lit dans un ordre compréhensible;
- les noms, sorties anticipées, erreurs et effets de bord sont explicites;
- les validations externes et les invariants internes ont chacun le bon mécanisme;
- les nouvelles abstractions résolvent un besoin observable;
- les tests pertinents ont été exécutés et leurs résultats sont rapportés tels qu'observés;
- les modifications de style restent liées à la tâche.

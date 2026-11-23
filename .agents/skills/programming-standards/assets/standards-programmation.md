# Standards de programmation pédagogiques

Ce document décrit le résultat attendu. Le code doit rester professionnel, tout en étant assez explicite pour qu'un étudiant puisse en suivre le déroulement, le déboguer et le modifier.

## Principes directeurs

Le code attendu est :

- lisible lors d'une première lecture;
- explicable étape par étape;
- centré sur le vocabulaire du domaine;
- testable sans dépendances cachées;
- assez simple pour exposer le mécanisme enseigné;
- assez rigoureux pour servir de modèle de pratique professionnelle.

Quand tu présentes ou modifies du code, privilégie un formatage aéré et lisible. Évite les one-liners qui compriment des objets ou une déstructuration d'objet sur une seule ligne si une version multilignes est plus facile à lire pour un humain.

La simplicité ne signifie pas supprimer les validations, la gestion des erreurs ou les frontières architecturales. Elle consiste à rendre ces éléments visibles sans ajouter d'abstraction qui ne résout pas encore un besoin réel.

## Nomenclature

Les identifiants du code sont en anglais. Les explications pédagogiques, les commentaires et la documentation destinée aux étudiants sont en français.

- Nommer les données avec des noms : `customer`, `exchangeRequest`, `savedRecord`.
- Nommer les opérations avec des verbes : `findCustomer`, `validateRequest`, `saveExchange`.
- Nommer les booléens comme des prédicats : `isAuthenticated`, `hasPermission`, `canRetry`.
- Employer les termes du domaine plutôt que des noms génériques comme `data`, `item`, `thing` ou `manager` lorsque le rôle est connu.
- Éviter les abréviations non usuelles et les noms à une lettre, sauf pour un indice local évident.
- Utiliser la même expression pour le même concept dans toutes les couches concernées.

## Mise en forme JavaScript

- Indentation de quatre espaces.
- Point-virgule à la fin des instructions.
- Apostrophes simples pour les chaînes, sauf si la chaîne elle-même devient moins lisible.
- Une déclaration par étape conceptuelle.
- Objets, tableaux, appels et déstructurations sur plusieurs lignes lorsque leur lecture horizontale devient difficile.
- Imports regroupés dans l'ordre suivant : modules de Node.js, dépendances externes, modules locaux. Séparer les groupes par une ligne vide lorsqu'il y en a plusieurs.
- Montage des routes chaîné.

La lisibilité détermine le retour à la ligne; aucune longueur maximale arbitraire n'est imposée.

```js
const {
    customerId,
    requestedFormat,
    destination,
} = request.body;

const exchangeRequest = {
    customerId,
    requestedFormat,
    destination,
};
```

Une expression courte peut rester sur une ligne lorsqu'elle demeure immédiatement compréhensible.

## Flux de contrôle

Préférer les clauses de garde afin de rendre les conditions d'arrêt visibles et de réduire l'imbrication.

```js
function calculateTotal(cart) {
    if (cart.items.length === 0) {
        return 0;
    }

    const subtotal = calculateSubtotal(cart.items);
    return applyDiscount(subtotal, cart.discount);
}
```

Éviter :

- les ternaires imbriqués;
- les conditions longues qui mélangent plusieurs décisions du domaine;
- les chaînes de transformations dont chaque étape modifie implicitement l'état;
- les boucles détournées pour produire des effets de bord difficiles à repérer.

Une méthode de tableau convient à une transformation courte et connue. Une boucle explicite convient mieux lorsque plusieurs étapes, sorties anticipées ou effets de bord doivent être observés.

## Fonctions et abstractions

Une fonction doit avoir une intention principale que son nom permet d'anticiper. Sa taille n'est pas limitée par un nombre arbitraire de lignes.

Extraire une fonction lorsqu'au moins une de ces conditions est satisfaite :

- le nom de la fonction explique une règle ou une étape importante;
- le traitement est réutilisé de manière significative;
- l'extraction permet de tester une décision isolément;
- le niveau d'abstraction du code appelant devient plus cohérent.

Ne pas extraire uniquement pour raccourcir un fichier. Préférer une fonction ou un objet simple à une classe, une fabrique générique ou un patron de conception lorsque ces derniers n'apportent pas encore de responsabilité distincte.

Lorsque plusieurs paramètres forment un même concept, un objet nommé rend l'appel plus explicite :

```js
const exchange = createExchange({
    source,
    destination,
    format,
});
```

## Asynchronisme et erreurs

- Attendre ou retourner chaque promesse intentionnelle.
- Utiliser `async` et `await` pour exposer l'ordre des opérations.
- Ne pas ajouter un `try` et `catch` qui ne fait que cacher l'erreur.
- Traduire une erreur technique en erreur du domaine à la frontière appropriée.
- Effectuer le nettoyage dans un bloc `finally` lorsqu'il doit avoir lieu dans tous les cas.
- Conserver la cause d'une erreur enrichie : `new Error(message, { cause: error })` lorsque cette forme est disponible.

```js
try {
    return await exchangeDao.save(exchange);
} catch (error) {
    throw new Error('Unable to save the exchange', {
        cause: error,
    });
}
```

## Commentaires pédagogiques

Un commentaire explique pourquoi le code existe, quelle contrainte il respecte ou quelle observation l'étudiant doit faire. Il ne paraphrase pas une instruction évidente.

```js
// Le service reçoit le DAO afin que le test puisse remplacer la persistance.
const exchangeService = createExchangeService(exchangeDao);
```

Dans les commentaires français, les identifiants sont placés entre guillemets droits : `"exchangeDao"`.

Un `TODO` pédagogique nomme le résultat attendu et les contraintes importantes, sans dicter toutes les étapes :

```js
// TODO : Retourner une erreur du domaine lorsque le client est introuvable.
```

Le code réutilisant un objectif pédagogique antérieur ne doit pas systématiquement être commenté,
à moins qu'un réinvestissement n'introduise de nouveau concepts.

## Écart entre code existant et standard

Appliquer ces standards au code nouveau et aux lignes directement modifiées. Une divergence voisine peut être corrigée lorsqu'elle est petite et réduit une incohérence immédiate. Une normalisation étendue doit faire l'objet d'une demande distincte afin de garder les changements faciles à réviser.

Lorsqu'une convention locale contredit un objectif pédagogique important, expliquer l'écart et proposer la modification minimale. Ne pas introduire automatiquement un formateur, un linter ou une nouvelle dépendance.

## Grille de révision

Avant de considérer le code terminé, vérifier :

- les noms expriment-ils le domaine et l'intention?
- le chemin principal se lit-il de haut en bas?
- les sorties anticipées et les erreurs sont-elles visibles?
- les effets de bord et les dépendances sont-ils explicites?
- chaque abstraction résout-elle un besoin observable?
- les commentaires ajoutent-ils une explication utile?
- le code utilise-t-il uniquement la complexité nécessaire au problème?
- les changements de style restent-ils dans la portée de la tâche?

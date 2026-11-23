---
name: programming-standards
description: "Appliquer les conventions de lisibilité et de robustesse aux projets Python du cours lors de la rédaction ou de la révision du code."
---

# Standards de programmation

Utiliser ce skill pour écrire ou réviser le code Python d'un projet. Lire les consignes du projet et les fichiers voisins avant de modifier le code. Si une consigne du projet précise un choix différent, la respecter.

## Écrire un code facile à expliquer et à modifier

- Garder les étapes importantes et les décisions du domaine visibles; nommer une étape intermédiaire lorsqu'elle clarifie le traitement.
- Choisir des noms précis en anglais. Utiliser les conventions Python : `snake_case` pour les modules, fonctions et variables, `PascalCase` pour les classes et `UPPER_SNAKE_CASE` pour les constantes.
- Donner une intention principale à chaque fonction. Extraire une fonction lorsqu'elle nomme une règle, isole une décision testable ou élimine une répétition significative.
- Préférer une clause de garde à une imbrication profonde. Éviter les expressions compactes difficiles à suivre, les effets de bord cachés et les abstractions sans besoin concret.
- Pour les applications locales du cours, garder un déroulement synchrone, sauf exigence explicite du projet.

## Rendre les erreurs et les effets observables

- Valider les données reçues et lever une exception appropriée pour une entrée invalide. Réserver `assert` aux invariants internes; une assertion ne remplace pas la validation d'une entrée.
- Utiliser `try` et `except` lorsqu'une erreur peut être traitée, traduite ou enrichie. Lors d'une traduction, conserver la cause avec `raise ... from error` si elle aide au diagnostic. Ne pas masquer une erreur sans traitement.
- Journaliser les événements utiles au diagnostic selon les exigences du projet, sans recopier chaque étape ni exposer inutilement les données traitées.
- Écrire des commentaires informatifs en français pour expliquer une raison ou une contrainte, sans paraphraser le code. Retirer ceux qui sont devenus faux.

## Limiter et vérifier la révision

- Appliquer ces conventions au code créé ou directement modifié. Éviter un reformatage général sans lien avec la demande.
- Vérifier les branches, les erreurs et les effets de bord concernés par la modification. Exécuter les tests pertinents et rapporter leur résultat réel.
- Consulter [les standards détaillés](references/standards-programmation.md) pour des critères et des exemples de révision en Python.

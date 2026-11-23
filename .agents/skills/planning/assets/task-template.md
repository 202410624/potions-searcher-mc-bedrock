### Tâche N : [Nom du composant]

**Fichiers :**

- Créer : `chemin/exact/vers/fichier.py`
- Modifier : `chemin/exact/vers/fichier_existant.py:123-145`
- Tester : `tests/chemin/exact/vers/test.py`

**Interfaces :**

- Consomme : [Ce que cette tâche utilise des tâches précédentes — signatures exactes]
- Produit : [Ce dont les tâches suivantes dépendent — noms exacts des fonctions,
  paramètres et types de retour. La personne qui réalise une tâche ne voit que
  celle-ci; ce bloc lui indique les noms et les types utilisés par les tâches voisines.]

- [ ] **Étape 1 : Écrire le test qui échoue**

```python
def test_comportement_precis():
    resultat = fonction(entree)
    assert resultat == valeur_attendue
```

- [ ] **Étape 2 : Exécuter le test pour confirmer qu'il échoue**

Exécuter : `pytest tests/chemin/test.py::nom_du_test -v`
Résultat attendu : ÉCHEC avec « function not defined »

- [ ] **Étape 3 : Implémenter `fonction(entree: TypeEntree) -> TypeResultat` dans `chemin/exact/vers/fichier.py`**

Ajouter une phrase sur l'approche lorsque la signature et le test laissent un
choix à faire (appel de bibliothèque, structure de données); inclure un bloc de
code uniquement pour un algorithme qu'ils ne permettent pas de déduire.

- [ ] **Étape 4 : Exécuter le test pour confirmer qu'il réussit**

Exécuter : `pytest tests/chemin/test.py::nom_du_test -v`
Résultat attendu : RÉUSSITE

- [ ] **Étape 5 : Créer un commit**

```bash
git add tests/chemin/test.py src/chemin/fichier.py
git commit -m "feat: ajouter une fonctionnalité précise"
```

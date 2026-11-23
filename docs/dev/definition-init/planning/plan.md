# Plan de mise en œuvre de l’assistant de brassage de potions Bedrock

**Objectif** Livrer la commande `potions` pour consulter les brassages réalisables et gérer un inventaire local.

**Architecture** Le catalogue transforme les données Bedrock en transitions entre potions. L’inventaire charge et enregistre les quantités. Le moteur calcule les suites réalisables à partir de ces deux entrées, puis la CLI valide les arguments et présente les résultats.

**Pile technologique** Python 3.10 ou ultérieur, bibliothèque standard à l’exécution, `pytest` pour les tests et Setuptools pour l’installation éditable.

**Spécification** [Spécification approuvée](../spec/specification.md). Lire ce document et la spécification avant l’implantation.

**Suivi d’exécution** [Commandes, résultats et décisions](plan-execution-logs/01-verifications.md).

## Décisions de planification

- Livrer quatre unités testables séparément et installer le point d’entrée en mode éditable pour garder les données à leur emplacement dans la remise. [Découpage et lancement](plan-logs/01-decoupage-et-lancement.md)
- Utiliser `pytest` dans les tests, avec `import pytest` lorsque le fichier appelle son API. [Découpage et lancement](plan-logs/01-decoupage-et-lancement.md)
- Concrétiser les règles de contenant dans le catalogue et suivre les réactifs et états visités pour chaque branche du parcours. [Catalogue et parcours](plan-logs/02-catalogue-et-parcours.md)
- Appliquer chaque lot en une écriture atomique, conserver le niveau des potions et fixer les codes de sortie de la CLI. [Persistance et validation](plan-logs/03-persistance-et-validation.md)

## Contraintes globales

- Lire les recettes dans `bedrock-samples-main/behavior_pack/recipes`.
- Créer `~/.potions/inventaire.json` au premier ajout valide.
- La saisie respecte la casse. Stocker et afficher les noms courts.
- Une suite part d’une potion en stock et comporte au moins une étape, sans repasser par le même état. La consultation ne modifie pas le stock.
- Fournir le code Python, les données, les tests unitaires et des exemples d’exécution. Remettre les prompts, skills, instructions, documents et journaux.
- Lancer les commandes `python -m pytest` depuis la racine avec un interpréteur sur lequel `pytest` est disponible.
- Chaque étape de commit suppose un dépôt Git existant. La racine actuelle est un dossier sans Git.

## Points d’attention pour la révision

- Un lot avec une quantité négative, un objet inconnu ou une paire incomplète doit traiter aussi les paires valides et afficher l’aide une fois. Voir tâche 4.
- Un inventaire corrompu doit être signalé et rester intact, même lors d’un ajout valide. Voir tâches 2 et 4.
- Un catalogue absent doit bloquer les commandes qui en dépendent. L’aide et l’affichage de l’inventaire doivent rester accessibles. Voir tâches 1 et 4.
- Une suite qui consomme deux fois le même réactif doit exiger deux unités. Une autre suite peut utiliser séparément le même stock. Voir tâche 3.
- Un échec de remplacement du fichier d’inventaire doit laisser en place le fichier d’origine. Voir tâche 2.

---

### Tâche 1 — Charger le catalogue Bedrock

**Fichiers**

- Créer `assistant_potions/__init__.py` et `assistant_potions/catalogue.py`.
- Tester dans `tests/test_catalogue.py`.

**Interfaces**

- Produit `Transition(depart: str, reactif: str, arrivee: str)`, une dataclass immuable et hachable.
- Produit `Catalogue(potions: frozenset[str], reactifs: frozenset[str], par_depart: dict[str, tuple[Transition, ...]])`, une dataclass dont les champs servent à la consultation.
- Produit `nom_court(nom: str) -> str`, qui retire le préfixe exact `minecraft:` lorsqu’il est présent, et `charger_catalogue(dossier: Path) -> Catalogue`, qui lève `ErreurCatalogue` si les données sont indisponibles ou invalides.

- [x] **Étape 1 — Écrire les tests.** Utiliser le dossier fourni pour `test_catalogue_bedrock` et la fixture `tmp_path` pour `test_catalogue_indisponible`.

```python
# test_catalogue_bedrock
assert "potion_type:thick" in catalogue.potions
assert "potion_type:water" in catalogue.potions
assert "ghast_tear" in catalogue.reactifs
assert Transition("potion_type:water", "nether_wart", "potion_type:awkward") in (
    catalogue.par_depart["potion_type:water"]
)
assert Transition("potion_type:regeneration", "gunpowder", "splash_potion:regeneration") in (
    catalogue.par_depart["potion_type:regeneration"]
)
assert Transition("splash_potion:regeneration", "dragon_breath", "lingering_potion:regeneration") in (
    catalogue.par_depart["splash_potion:regeneration"]
)
assert nom_court("minecraft:Ghast_Tear") == "Ghast_Tear"

# test_catalogue_indisponible — paramétrer un chemin absent, un dossier vide
# et un JSON mal formé dans tmp_path
with pytest.raises(ErreurCatalogue):
    charger_catalogue(dossier)
```

- [x] **Étape 2 — Vérifier l’échec.** Exécuter `python -m pytest -v tests/test_catalogue.py`. Attendre une erreur de collecte liée à l’import du module à créer.
- [x] **Étape 3 — Implémenter les interfaces dans `catalogue.py`.** Lire les JSON UTF-8 du dossier et sélectionner les deux clés de brassage de la spécification. Exiger trois champs textuels non vides pour chaque recette de brassage et traiter un dossier sans recette comme indisponible. Normaliser les effets `Awkward` et `Thick` lors de la lecture des données. Recueillir les états concrets des mélanges, puis produire les transitions génériques pour chaque effet disponible dans le contenant source, dans l’ordre potion, splash, lingering. Les clés génériques `potion`, `splash_potion` et `lingering_potion` correspondent aux familles d’états portant un effet. Dédupliquer les triplets et trier les transitions d’un départ par réactif, puis par arrivée.
- [x] **Étape 4 — Vérifier la réussite.** Relancer `python -m pytest -v tests/test_catalogue.py`. Attendre le succès de tous les tests du fichier.
- **Étape 5 — Créer le commit si Git est disponible.** Sans objet ici. `git rev-parse --show-toplevel` confirme l’absence de dépôt.

---

### Tâche 2 — Lire et mettre à jour l’inventaire JSON

**Fichiers**

- Créer `assistant_potions/inventaire.py`.
- Tester dans `tests/test_inventaire.py`.

**Interfaces**

- Produit `EntreeInventaire(nombre: int, niveau: int | None = None)`, une dataclass immuable.
- Produit `lire_inventaire(chemin: Path) -> dict[str, EntreeInventaire]` et `ajouter_au_stock(chemin: Path, ajouts: Mapping[str, int]) -> None`. Les deux lèvent `ErreurInventaire` pour un fichier invalide ou une erreur d’accès. Le contrat de l’ajout exige des noms courts et des quantités déjà validés.

- [x] **Étape 1 — Écrire les tests** avec la fixture `tmp_path`. Employer `chemin = tmp_path / ".potions" / "inventaire.json"` et `json.loads` pour lire le résultat sur disque.

```python
# test_premier_ajout_et_cumul
assert lire_inventaire(chemin) == {}
assert not chemin.parent.exists()
ajouter_au_stock(chemin, {})
assert not chemin.parent.exists()
ajouter_au_stock(chemin, {"potion_type:water": 1, "nether_wart": 1})
ajouter_au_stock(chemin, {"nether_wart": 2})
assert json.loads(chemin.read_text(encoding="utf-8")) == {
    "potion_type:water": {"nombre": 1, "niveau": 1},
    "nether_wart": {"nombre": 3},
}

# test_inventaire_invalide — paramétrer b"{" et un nombre JSON true
with pytest.raises(ErreurInventaire):
    ajouter_au_stock(chemin, {"ghast_tear": 1})
assert chemin.read_bytes() == contenu_initial

# test_compatibilite_et_echec_ecriture — dossier prérempli avec une potion de niveau 2
# et une potion sans niveau, puis remplacement simulé avec monkeypatch
assert lire_inventaire(chemin)["potion_type:speed"].niveau == 2
assert lire_inventaire(chemin)["potion_type:water"].niveau == 1
with monkeypatch.context() as correctif:
    correctif.setattr("assistant_potions.inventaire.os.replace", echec_remplacement)
    with pytest.raises(ErreurInventaire):
        ajouter_au_stock(chemin, {"potion_type:speed": 1})
assert chemin.read_bytes() == contenu_initial
assert list(chemin.parent.iterdir()) == [chemin]
ajouter_au_stock(chemin, {"potion_type:speed": 1})
assert lire_inventaire(chemin)["potion_type:speed"] == EntreeInventaire(2, 2)
```

Pour la simulation, définir `echec_remplacement(source, destination)` de façon à lever `OSError`. Dans `test_verrou_existant`, précréer le marqueur avec les octets `b"occupe"` à côté d’un stock valide, vérifier que `ajouter_au_stock(chemin, {"ghast_tear": 1})` lève `ErreurInventaire` et comparer les octets des deux fichiers à leur contenu initial.

- [x] **Étape 2 — Vérifier l’échec.** Exécuter `python -m pytest -v tests/test_inventaire.py`. Attendre une erreur de collecte liée à l’import du module à créer.
- [x] **Étape 3 — Implémenter les interfaces dans `inventaire.py`.** Exiger un objet JSON dont les clés sont des noms courts, sous la forme d’un réactif ou de l’un des trois identifiants de potion avec un effet. Exiger un `nombre` entier positif ou nul et, s’il figure sur une potion, un `niveau` entier strictement positif. Rejeter les booléens et les champs hors schéma. Une potion sans niveau a le niveau logique 1. Pour un lot non vide, créer au besoin le dossier et prendre un verrou exclusif via la création de `inventaire.json.lock` avec le mode `x`. En cas de verrou présent, signaler l’échec. Relire sous verrou, fusionner les quantités, écrire le JSON UTF-8 dans un fichier temporaire du même dossier, fermer ce fichier et appeler `os.replace`. Nettoyer le temporaire et le verrou de l’appelant à la sortie.
- [x] **Étape 4 — Vérifier la réussite.** Relancer `python -m pytest -v tests/test_inventaire.py`. Attendre le succès de tous les tests du fichier.
- **Étape 5 — Créer le commit si Git est disponible.** Sans objet ici. `git rev-parse --show-toplevel` confirme l’absence de dépôt.

---

### Tâche 3 — Calculer toutes les suites réalisables

**Fichiers**

- Créer `assistant_potions/brassage.py`.
- Tester dans `tests/test_brassage.py`.

**Interfaces**

- Consomme `Catalogue` et `Transition` de la tâche 1.
- Produit `Suite(depart: str, etapes: tuple[Transition, ...], total_reactifs: dict[str, int])` et `calculer_suites(catalogue: Catalogue, quantites: Mapping[str, int]) -> dict[str, list[Suite]]`. Le résultat indexe les suites par potion d’arrivée.

- [x] **Étape 1 — Écrire les tests.** Pour `test_regeneration`, charger le catalogue fourni. Pour `test_quantites_et_cycles`, utiliser quatre états `potion_type:a`, `potion_type:b`, `potion_type:c` et `potion_type:d` et les transitions `a → b`, `b → c`, `a → d`, `d → c`, `b → a`, chacune avec `nether_wart`. Donner une unité de `a` en stock et tester une, puis deux unités de ce réactif. Dans `test_departs_distincts`, ajouter une unité de `b` au même stock et chercher `c`.

```python
# test_regeneration
assert [
    (s.depart, [t.arrivee for t in s.etapes], s.total_reactifs)
    for s in suites["potion_type:regeneration"]
] == [
    ("potion_type:water", ["potion_type:awkward", "potion_type:regeneration"],
     {"nether_wart": 1, "ghast_tear": 1})
]
assert calculer_suites(catalogue, {"ghast_tear": 1}) == {}

# test_quantites_et_cycles
assert "potion_type:c" not in avec_un
assert "potion_type:a" not in avec_deux
assert [s.etapes[0].arrivee for s in avec_deux["potion_type:c"]] == [
    "potion_type:b", "potion_type:d"
]
assert all(s.total_reactifs == {"nether_wart": 2} for s in avec_deux["potion_type:c"])
assert stock == {"potion_type:a": 1, "nether_wart": 2}

# test_departs_distincts
assert {s.depart for s in avec_deux_departs["potion_type:c"]} == {
    "potion_type:a", "potion_type:b"
}
```

- [x] **Étape 2 — Vérifier l’échec.** Exécuter `python -m pytest -v tests/test_brassage.py`. Attendre une erreur de collecte liée à l’import du module à créer.
- [x] **Étape 3 — Implémenter les interfaces dans `brassage.py`.** Visiter les potions possédées en ordre alphabétique. Pour chaque départ de quantité positive, suivre les transitions en profondeur dans l’ordre du catalogue. Une branche conserve ses étapes, ses états visités, départ compris, et ses totaux par réactif. Chaque transition possible produit une suite, puis le parcours continue avec les compteurs de cette suite. Une arrivée déjà visitée dans la branche ou une consommation qui dépasserait la quantité du stock arrête cette transition. Dans `test_regeneration`, employer le stock JSON d’exemple de la spécification.
- [x] **Étape 4 — Vérifier la réussite.** Relancer `python -m pytest -v tests/test_brassage.py`. Attendre le succès de tous les tests du fichier.
- **Étape 5 — Créer le commit si Git est disponible.** Sans objet ici. `git rev-parse --show-toplevel` confirme l’absence de dépôt.

---

### Tâche 4 — Livrer la commande et les exemples de remise

**Fichiers**

- Créer `assistant_potions/cli.py`, `pyproject.toml` et `README.md`.
- Tester dans `tests/test_cli.py`.

**Interfaces**

- Consomme `nom_court`, `charger_catalogue` et `ErreurCatalogue` de la tâche 1, `lire_inventaire`, `ajouter_au_stock` et `ErreurInventaire` de la tâche 2, et `calculer_suites` de la tâche 3.
- Produit `main(argv: Sequence[str] | None = None, *, chemin_inventaire: Path | None = None, dossier_recettes: Path | None = None) -> int`. Le point d’entrée `potions` l’appelle sans paramètres. Les tests injectent les chemins avec `tmp_path` et capturent les flux standard avec `capsys`.

- [x] **Étape 1 — Écrire les tests.** Créer une fonction de test par scénario du tableau et utiliser `pytest.mark.parametrize` pour les variantes indépendantes d’alias et d’arguments. Pour les recettes réalisables, utiliser une eau, une verrue du Nether, une larme de Ghast et une potion de vitesse. Pour les ajouts, relire le JSON après l’appel.

| Test | Appel et assertions |
| --- | --- |
| `test_aide_et_stock` | `--help` et `-h` renvoient 0 et présentent les six options, leurs alias, syntaxes et exemples. `--show` et `-s` renvoient 0, donnent exactement `L’inventaire est vide.\n` pour un chemin absent, puis `ghast_tear : 1\nnether_wart : 2\n` pour ces deux entrées stockées en ordre inverse. |
| `test_ajouts_valides` | `--add minecraft:ghast_tear 6` puis `-a ghast_tear 1` donnent 7 larmes. `--add_multiple blaze_powder 3 ghast_tear 6 ghast_tear 2` puis `-am blaze_powder 1` donnent 4 poudres et 15 larmes. Les quatre appels renvoient 0. |
| `test_ajouts_invalides` | `-a` et `-am` affichent respectivement `potions -a ghast_tear 6` et `potions -am blaze_powder 3 ghast_tear 6` et renvoient 2. `-a ghast_tear 6 blaze_powder 3` et `-a ghast_tear 6 surplus` renvoient 2 et laissent le fichier absent. |
| `test_lots_partiels` | `-am ghast_tear 2 Ghast_Tear 1 blaze_powder -1 nether_wart 0 sugar 1.5 ghast_tear 3 redstone` renvoie 2, stocke uniquement cinq larmes et donne cinq avertissements, dont `l'ingredient que vous avez cherche n'existe pas`, suivis d’une seule ligne commençant par `usage:`. Un lot `-am sugar x poudre 2` renvoie 2 et conserve les octets du stock. |
| `test_liste_et_recettes` | `--list` et `-l` renvoient 0 et affichent les lignes triées `potion_type:awkward`, `potion_type:mundane` et `potion_type:regeneration`, une fois chacune. `--recipes minecraft:potion_type:regeneration` et `-r potion_type:regeneration` renvoient 0. Vérifier les lignes de la recette données à l’étape 3 et l’identité des octets sur disque avant et après les quatre consultations. |
| `test_recettes_sans_resultat_ou_invalides` | Avec un stock vide, `-l` et `-r potion_type:regeneration` renvoient 0 et signalent l’absence de résultat. `-r`, `-r potion_type:inconnue` et `-r potion_type:water potion_type:speed` renvoient 2 avec une erreur et une seule aide. |
| `test_erreurs_de_fichiers` | Avec un catalogue absent, `-l`, `-r potion_type:water` et `-a ghast_tear 1` renvoient 1, `-h` et `-s` renvoient 0, et le stock reste absent. Avec un inventaire contenant seulement `{`, `-s` et un ajout valide renvoient 1 et le fichier garde ses octets. Simuler aussi un échec de remplacement avec `monkeypatch` et vérifier le code 1 et les octets du stock valide. |

- [x] **Étape 2 — Vérifier l’échec.** Exécuter `python -m pytest -v tests/test_cli.py`. Attendre une erreur de collecte liée à l’import du module à créer.
- [x] **Étape 3 — Implémenter `main` dans `cli.py`.** Utiliser `argparse` pour déclarer les options et leurs alias, générer l’aide et analyser l’option initiale exacte. Valider les arguments restants selon la commande, par groupes successifs de deux pour les lots, afin que les valeurs négatives ou invalides restent des données à valider. Accepter une quantité formée de chiffres ASCII et convertible en un entier strictement positif. Pour une paire complète, valider d’abord le nom dans le catalogue, puis la quantité. Émettre un avertissement par paire rejetée, cumuler les ajouts valides et appeler le stockage une fois. L’aide en cas d’erreur suit les avertissements sur stderr. Les résultats et les deux exemples d’ajout sans argument vont sur stdout. Renvoi 2 pour une erreur de syntaxe ou un lot partiellement invalide, 1 pour une erreur de données ou d’accès, 0 pour une commande réussie, résultat vide inclus. Sans commande, présenter l’aide et renvoyer 0. Un argument excédentaire après `--list`, `--show` ou `--help` produit une erreur de syntaxe.

  Calculer les chemins par défaut à l’appel avec `Path.home() / ".potions" / "inventaire.json"` et le dossier `bedrock-samples-main/behavior_pack/recipes` relatif à la racine du paquet source. Charger le catalogue uniquement pour les recherches et la validation d’objets. Afficher une potion par ligne pour `--list` et les entrées du stock au format spécifié. Afficher les recettes sous forme de blocs séparés par une ligne vide, avec les totaux par réactif en ordre alphabétique. L’exemple attendu est le suivant.

  ```text
  Départ : potion_type:water
    nether_wart → potion_type:awkward
    ghast_tear → potion_type:regeneration
  Réactifs :
    ghast_tear : 1
    nether_wart : 1
  ```

  Employer `Aucune potion réalisable.` et `Aucune recette réalisable pour {potion}.` pour les recherches vides. Déclarer `setuptools>=64` comme dépendance de construction, `requires-python = ">=3.10"` et `potions = "assistant_potions.cli:main"` dans `[project.scripts]` et déclarer explicitement le paquet `assistant_potions` dans la configuration Setuptools.

- [x] **Étape 4 — Vérifier la réussite et la remise.** Depuis la racine, exécuter `python -m pip install --editable .` dans l’environnement virtuel de démonstration, puis `python -m pytest -v` et attendre le succès de toute la suite. Exécuter `potions --help` et `potions --list` depuis un autre dossier avec un dossier personnel de test. Depuis ce dossier, exécuter `potions -am potion_type:water 1 nether_wart 1 ghast_tear 1`, `potions -s`, `potions -l`, puis `potions -r potion_type:regeneration`. Vérifier les trois entrées triées, la présence de la régénération et les deux étapes attendues. Rédiger le README avec les commandes d’installation et de tests, la démonstration, le flux des données et un index des données, prompts, instructions, skills, documents et journaux de la remise. Préciser comment identifier et retirer un fichier verrou résiduel après avoir arrêté tous les processus `potions`.
- **Étape 5 — Créer le commit si Git est disponible.** Sans objet ici. `git rev-parse --show-toplevel` confirme l’absence de dépôt.

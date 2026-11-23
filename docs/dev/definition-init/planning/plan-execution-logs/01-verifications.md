# Exécution du plan de brassage

- **Ouvert le** 2026-11-23
- **Travail concerné** [Plan d’implantation](../plan.md)

## Point de départ

Exécuter les quatre tâches du plan dans l’ordre et vérifier les comportements dans PyCharm. Le Python disponible est la version 3.13.0 avec pytest 9.1.1. `git rev-parse --show-toplevel` confirme l’absence de dépôt Git dans le dossier et ses parents.

## Résultats

- Catalogue, avant implantation. `python -m pytest -v tests/test_catalogue.py` renvoie 1 avec l’erreur de collecte attendue sur le paquet absent.
- Catalogue, après implantation. `python -m pytest -v tests/test_catalogue.py` et `python -m pytest -q` réussissent avec 5 tests chacune.
- Inventaire, avant implantation. `python -m pytest -v tests/test_inventaire.py` renvoie 1 à la collecte, car le module est absent.
- Inventaire, après implantation. La même commande réussit avec 9 tests, puis `python -m pytest -q` réussit avec 14 tests.
- Brassage, avant implantation. `python -m pytest -v tests/test_brassage.py` renvoie 1 à la collecte, car le module est absent.
- Brassage, après implantation. La même commande réussit avec 3 tests, puis `python -m pytest -q` réussit avec 17 tests.
- CLI, avant implantation. `python -m pytest -v tests/test_cli.py` renvoie 1 à la collecte, car le module est absent.
- CLI, première vérification. La même commande réussit avec 24 tests, puis `python -m pytest -q` réussit avec 41 tests.
- CLI, vérification des options exactes. `python -m pytest -q tests/test_cli.py -k syntaxes_invalides` relève deux échecs. `argparse` accepte `-ll` et `-aa` en regroupant les options courtes. L’agent ajoute une vérification du nom exact de l’option initiale. La suite ciblée passe ensuite avec 26 tests et la suite complète avec 43 tests.
- Démonstration, premier essai. `python -m pip install --editable .` échoue pendant l’installation des dépendances de construction, car le chemin configuré du fichier de certificats TLS de PostgreSQL est absent.
- Démonstration, reprise. Dans le seul processus de test, l’agent retire la référence invalide dans `CURL_CA_BUNDLE`. La validation TLS reste active. `python -m pip install --editable .` réussit dans un environnement virtuel temporaire, puis `python -m pytest -v` réussit avec 43 tests.
- Point d’entrée installé. Depuis un autre dossier avec un profil Windows temporaire, `potions --help` présente les options et `potions --list` annonce un résultat vide sans créer de stock. Après `potions -am potion_type:water 1 nether_wart 1 ghast_tear 1`, `potions -s` affiche trois entrées triées et `potions -l` affiche les potions étrange, banale et de régénération. `potions -r potion_type:regeneration` affiche les deux étapes et les totaux attendus. Une seconde consultation donne la même empreinte SHA-256 de l’inventaire avant et après.

- Vérification finale. `python -m pytest -q` réussit avec 43 tests après le retrait des métadonnées de construction générées dans le dossier de remise.

## Artefacts liés

- [Prompts de l’initiative](02-prompt.md)
- [Guide d’utilisation](../../../../../README.md)

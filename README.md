# Assistant de brassage de potions Bedrock

La commande `potions` utilise ton inventaire local pour lister les potions réalisables et afficher toutes les suites qui mènent à une potion donnée.

## Installation et tests

Depuis le dossier de remise, avec Python 3.10 ou ultérieur, exécute ces commandes dans PowerShell.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --editable .
.\.venv\Scripts\python.exe -m pip install pytest
.\.venv\Scripts\python.exe -m pytest -q
```

L’exécutable se trouve dans `.venv\Scripts\potions.exe`. Après activation de l’environnement virtuel, tu peux l’appeler par son nom depuis n’importe quel dossier. Tu peux aussi appeler l’exécutable par son chemin complet.

Pour utiliser `potions` dans les nouveaux terminaux PowerShell sans activer l’environnement, exécute une fois cette commande depuis le dossier du projet.

```powershell
.\.venv\Scripts\potions.exe --install
```

L’option enregistre l’alias dans le profil de ton compte pour les versions de PowerShell trouvées. Ouvre un nouveau terminal et tape `potions --help`. Si tu déplaces le projet, relance l’option depuis le nouvel exécutable pour mettre à jour le chemin. Pour retirer l’alias, supprime la ligne marquée `# assistant-potions: alias potions` dans les profils indiqués par la commande.

## Démonstration

Au premier ajout valide, la commande crée `~/.potions/inventaire.json`. Cette démonstration suppose un stock vide. Les ajouts se cumulent si tu relances les commandes.

```text
potions --help
potions -am potion_type:water 1 nether_wart 1 ghast_tear 1
potions -s
potions -l
potions -r potion_type:regeneration
```

`potions -s` affiche les trois entrées en ordre alphabétique. `potions -l` affiche `potion_type:awkward`, `potion_type:mundane` et `potion_type:regeneration`. La dernière commande affiche cette suite.

```text
Départ : potion_type:water
  nether_wart → potion_type:awkward
  ghast_tear → potion_type:regeneration
Réactifs :
  ghast_tear : 1
  nether_wart : 1
```

Pour brasser, lance `potions --brew potion_type:regeneration` ou `potions -b potion_type:regeneration`, puis saisis le nombre de potions à créer. La commande utilise la recette la plus courte qui couvre tout le lot. Elle retire les potions de départ et les réactifs, puis enregistre les potions obtenues dans la même mise à jour. Si le stock est insuffisant, elle refuse le lot.

Pour retrouver le nom d’un ingrédient de brassage dans le catalogue, utilise `potions --search ghast` ou `potions -sch ghast`. La recherche accepte un nom complet ou partiel, ignore la casse et affiche les résultats en ordre alphabétique. Par exemple, `ghast` donne `ghast_tear`.

Les noms utilisés pour les ajouts et les recettes respectent la casse. Tu peux les saisir avec le préfixe `minecraft:` ou sous leur forme courte. Un lot applique les paires valides ensemble et signale chaque paire rejetée. Les codes de sortie sont `0` pour une commande réussie, `1` pour une erreur de données ou d’accès et `2` pour une erreur de saisie, y compris un lot partiellement appliqué.

Si un arrêt forcé laisse le fichier `~/.potions/inventaire.json.lock` et que les ajouts signalent que le verrou existe, assure-toi que tous les processus `potions` sont arrêtés. Supprime alors uniquement `inventaire.json.lock`, puis relance la commande.

## Flux des données

1. [catalogue.py](assistant_potions/catalogue.py) lit les JSON de brassage et construit les transitions. Les changements de contenant conservent l’effet de la potion.
2. [inventaire.py](assistant_potions/inventaire.py) lit les quantités. Lors d’un ajout, il relit le stock sous verrou et remplace le fichier en une seule opération.
3. [brassage.py](assistant_potions/brassage.py) parcourt les transitions depuis chaque potion en stock. Chaque branche suit ses états visités et ses quantités de réactifs.
4. [cli.py](assistant_potions/cli.py) valide la commande et affiche le stock, les potions réalisables ou le détail des recettes.

## Index de la remise

- [Énoncé et instructions de remise](enonce-etc.md)
- [Données Bedrock fournies](bedrock-samples-main/behavior_pack/recipes/)
- [Tests pytest](tests/)
- [Skills du projet](.agents/skills/)
- [Prompt d’implantation](docs/dev/definition-init/planning/plan-execution-logs/02-prompt.md)
- [Brainstorming et journal](docs/dev/definition-init/brainstorm/brainstorm.md)
- [Spécification et journaux](docs/dev/definition-init/spec/specification.md)
- [Plan et journaux de planification](docs/dev/definition-init/planning/plan.md)
- [Journal d’exécution et résultats](docs/dev/definition-init/planning/plan-execution-logs/01-verifications.md)

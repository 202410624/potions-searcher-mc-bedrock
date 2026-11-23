# Assistant de brassage de potions Bedrock

**Statut** Révision approuvée le 19 novembre 2026. [Énoncé](../../../../enonce-etc.md) · [Brainstorming](../brainstorm/brainstorm.md)

Le joueur utilise une commande Python pour trouver les potions qu’il peut brasser et consulter leurs recettes. La gestion d’un inventaire JSON local constitue la fonctionnalité supplémentaire.

## Commandes

| Option de `potions` | Comportement |
| --- | --- |
| `--list`, `-l` | Liste les potions réalisables par ordre alphabétique, sans doublons. |
| `--recipes POTION`, `-r POTION` | Affiche toutes les suites réalisables pour une potion, avec le départ, les étapes dans l’ordre et le total par réactif. |
| `--show`, `-s` | Affiche le stock par ordre alphabétique au format `nom : quantité`. Si le stock est vide, affiche `L’inventaire est vide.` |
| `--add OBJET QUANTITÉ`, `-a` | Ajoute exactement une paire. |
| `--add_multiple OBJET QUANTITÉ ...`, `-am` | Cumule les quantités de toutes les paires valides, y compris celles d’un même objet. |
| `--help`, `-h` | Présente les options, leurs alias, la syntaxe et des exemples. |

## Recettes et stock

- Lire `input`, `reagent` et `output` des recettes `minecraft:recipe_brewing_mix` et `minecraft:recipe_brewing_container` dans `bedrock-samples-main/behavior_pack/recipes`. Normaliser `Awkward` et `Thick` en minuscules à la lecture.
- Identifier les potions par `potion_type:<effet>`, `splash_potion:<effet>` ou `lingering_potion:<effet>`. Un changement de contenant conserve l’effet.
- Accepter les réactifs et potions du catalogue, eau comprise, avec ou sans le préfixe `minecraft:`. La saisie respecte la casse. Stocker et afficher les noms courts.
- Créer `~/.potions/inventaire.json` au premier ajout valide. Un fichier absent vaut un inventaire vide. Exemple de contenu JSON.

```json
{
  "potion_type:water":{
    "nombre":1,
    "niveau":1
  },
  "nether_wart":{
    "nombre":1
  },
  "ghast_tear": {
    "nombre":1
  },
    "potion_type:speed":{
    "nombre":1,
    "niveau":1
  }
}
```

## Brassages réalisables

Une suite part d’une potion en stock et comporte au moins une étape, sans repasser par le même état. Chaque étape transforme la potion courante et exige une unité de son réactif. Les quantités se cumulent dans une suite. Chaque suite est évaluée séparément et la consultation ne modifie pas le stock.

Deux suites sont distinctes si le départ ou une transformation diffère. Avec le stock d’exemple, `potions -r potion_type:regeneration` affiche le passage de l’eau à la potion étrange avec `nether_wart`, puis à la régénération avec `ghast_tear`. Une larme de Ghast seule ne suffit pas.

## Validation

- Sans argument, afficher l’exemple de la commande utilisée (`potions -a ghast_tear 6` ou `potions -am blaze_powder 3 ghast_tear 6`). Une paire complète exige une quantité entière décimale strictement positive.
- Avertir pour chaque paire invalide, puis afficher l’aide une fois. Pour un objet inconnu dans une paire complète, afficher `l'ingredient que vous avez cherche n'existe pas`.
- Rejeter tout ajout simple qui reçoit plus d’une paire ou des arguments excédentaires. Un ajout multiple sans paire valide laisse le fichier intact.
- Signaler l’absence de résultat pour `--list` et `--recipes`. Pour `--recipes`, afficher une erreur et l’aide si la potion est inconnue ou si le nombre d’arguments diffère de un.
- Signaler un inventaire illisible ou invalide, un catalogue indisponible pour une commande qui en dépend, ou un échec d’écriture. Préserver l’inventaire existant.

## Remise

Fournir le code Python, les données, les tests unitaires et des exemples d’exécution. Remettre les prompts, skills, instructions, documents et journaux. L’élève doit pouvoir expliquer le code et le flux des données, puis en faire la démonstration sur demande.

**Hors portée** Synchronisation avec Minecraft.  
**Choix libres** Parseur, structure du code, recherche des suites, écriture JSON, présentation des recettes et texte des autres avertissements.

[Journaux du stockage](logs/01-stockage.md) · [Catalogue et commandes](logs/02-catalogue-et-commandes.md) · [Calcul des recettes](logs/03-calcul-des-potions-et-des-recettes.md)

"""Transforme les recettes JSON de brassage Bedrock en transitions indexées par potion de
départ.
"""

import json
from dataclasses import dataclass
from pathlib import Path


MIX_KEY = "minecraft:recipe_brewing_mix"
CONTAINER_KEY = "minecraft:recipe_brewing_container"
CONTAINERS = ("potion", "splash_potion", "lingering_potion")
POTION_PREFIXES = dict(zip(CONTAINERS, ("potion_type", "splash_potion", "lingering_potion")))
EFFECT_NAMES = {"Awkward": "awkward", "Thick": "thick"}


class ErreurCatalogue(ValueError):
    """Signale un catalogue de brassage illisible, invalide ou sans recette de mélange."""


@dataclass(frozen=True)
class Transition:
    """Décrit une étape reliant une potion ou un contenant de départ à son résultat au moyen
    d’un réactif.
    """
    depart: str
    reactif: str
    arrivee: str


@dataclass(frozen=True)
class Catalogue:
    """Regroupe les identifiants de potions, les réactifs et les transitions rangées par
    potion de départ.
    """
    potions: frozenset[str]
    reactifs: frozenset[str]
    par_depart: dict[str, tuple[Transition, ...]]


def nom_court(nom: str) -> str:
    """Retire le préfixe `minecraft:` s’il est présent et conserve la casse du nom."""
    return nom.removeprefix("minecraft:")


def normalize_potion(name: str) -> str:
    """Valide la forme contenant-effet et normalise les variantes de casse connues. Une forme
    invalide lève ErreurCatalogue.
    """
    container, separator, effect = name.partition(":")
    if container not in POTION_PREFIXES.values() or not separator or not effect or ":" in effect:
        raise ErreurCatalogue(f"Identifiant de potion invalide dans le catalogue ({name}).")
    return f"{container}:{EFFECT_NAMES.get(effect, effect)}"


def read_transition(recipe: object, path: Path) -> Transition:
    """Extrait les noms courts des champs `input`, `reagent` et `output`. Lève ErreurCatalogue
    en identifiant le fichier si la recette ou un champ est invalide.
    """
    if not isinstance(recipe, dict):
        raise ErreurCatalogue(f"Recette de brassage invalide dans {path.name}.")

    fields = []
    for key in ("input", "reagent", "output"):
        value = recipe.get(key)
        if not isinstance(value, str) or not nom_court(value).strip():
            raise ErreurCatalogue(f"Champ {key} invalide dans {path.name}.")
        fields.append(nom_court(value))
    return Transition(*fields)


def charger_catalogue(dossier: Path) -> Catalogue:
    """Lit les fichiers JSON, déduplique les transitions et applique les changements de
    contenant en conservant les effets. Retourne le catalogue indexé ou lève ErreurCatalogue
    si les données sont illisibles, invalides ou sans mélange.
    """
    mixes = set()
    container_rules = set()
    try:
        for path in sorted(dossier.iterdir()):
            if path.suffix != ".json" or path.is_dir():
                continue
            document = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(document, dict):
                raise ErreurCatalogue(f"Document de recette invalide dans {path.name}.")
            if MIX_KEY in document:
                recipe = read_transition(document[MIX_KEY], path)
                mixes.add(Transition(
                    normalize_potion(recipe.depart), recipe.reactif, normalize_potion(recipe.arrivee)
                ))
            if CONTAINER_KEY in document:
                recipe = read_transition(document[CONTAINER_KEY], path)
                if recipe.depart not in CONTAINERS or recipe.arrivee not in CONTAINERS:
                    raise ErreurCatalogue(f"Contenant générique invalide dans {path.name}.")
                container_rules.add(recipe)
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ErreurCatalogue(f"Impossible de lire le catalogue dans {dossier} ({error}).") from error

    if not mixes:
        raise ErreurCatalogue(f"Aucune recette de mélange dans {dossier}.")

    potions = {state for mix in mixes for state in (mix.depart, mix.arrivee)}
    transitions = set(mixes)
    # Les règles du contenant suivant utilisent les états créés au contenant précédent.
    for container in CONTAINERS:
        prefix = POTION_PREFIXES[container] + ":"
        for rule in (rule for rule in container_rules if rule.depart == container):
            target = POTION_PREFIXES[rule.arrivee]
            sources = [potion for potion in potions if potion.startswith(prefix)]
            for source in sources:
                arrival = f"{target}:{source.removeprefix(prefix)}"
                transitions.add(Transition(source, rule.reactif, arrival))
                potions.add(arrival)

    indexed = {}
    for transition in sorted(transitions, key=lambda t: (t.depart, t.reactif, t.arrivee)):
        indexed.setdefault(transition.depart, []).append(transition)
    return Catalogue(
        frozenset(potions),
        frozenset(transition.reactif for transition in transitions),
        {source: tuple(steps) for source, steps in indexed.items()},
    )

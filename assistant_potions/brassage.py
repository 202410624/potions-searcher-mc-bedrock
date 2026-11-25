"""Recherche les recettes réalisables et calcule les prélèvements pour brasser un lot."""

from collections.abc import Mapping, Sequence
from dataclasses import dataclass

from .catalogue import WATER_BOTTLE_ALIASES, Catalogue, Transition


@dataclass(frozen=True)
class Suite:
    """Décrit une potion de départ, les transitions successives et le nombre d’unités de
    chaque réactif requis.
    """
    depart: str
    etapes: tuple[Transition, ...]
    total_reactifs: dict[str, int]


def calculer_suites(
    catalogue: Catalogue, quantites: Mapping[str, int]
) -> dict[str, list[Suite]]:
    """Explore les transitions du catalogue depuis chaque potion disponible. Retourne les
    suites non vides regroupées par potion obtenue selon les quantités en stock.
    """
    recipes: dict[str, list[Suite]] = {}

    def visit(current: str, visited: frozenset[str], recipe: Suite) -> None:
        """Explore la branche depuis la potion courante sans revisiter un état ni dépasser le
        stock de réactifs. Ajoute chaque prolongement admissible aux résultats avant de
        poursuivre.
        """
        for step in catalogue.par_depart.get(current, ()):
            if step.arrivee in visited:
                continue
            used = recipe.total_reactifs.get(step.reactif, 0) + 1
            if used > quantites.get(step.reactif, 0):
                continue

            # Chaque branche possède ses propres totaux et ses propres états visités.
            totals = recipe.total_reactifs.copy()
            totals[step.reactif] = used
            next_recipe = Suite(recipe.depart, (*recipe.etapes, step), totals)
            recipes.setdefault(step.arrivee, []).append(next_recipe)
            visit(step.arrivee, visited | {step.arrivee}, next_recipe)

    available = {
        WATER_BOTTLE_ALIASES.get(name, name)
        for name, quantity in quantites.items()
        if quantity > 0
    }
    for start in sorted(catalogue.potions.intersection(available)):
        visit(start, frozenset({start}), Suite(start, (), {}))
    return recipes


def retraits_brassage(
    recipes: Sequence[Suite], stock: Mapping[str, int], quantity: int
) -> dict[str, int] | None:
    """Calcule les quantités à retirer pour la suite la plus courte qui couvre tout le lot.
    Répartit au besoin le prélèvement d’eau entre ses noms en stock et retourne `None`
    si aucune suite ne convient.
    """
    for recipe in sorted(recipes, key=lambda suite: len(suite.etapes)):
        withdrawals = {name: total * quantity for name, total in recipe.total_reactifs.items()}
        if any(stock.get(name, 0) < total for name, total in withdrawals.items()):
            continue

        # Un ancien inventaire peut répartir l’eau entre le nom canonique et ses alias.
        sources = (recipe.depart, *(
            alias for alias, potion in WATER_BOTTLE_ALIASES.items() if potion == recipe.depart
        ))
        remaining = quantity
        for name in sources:
            already_used = withdrawals.get(name, 0)
            taken = min(remaining, stock.get(name, 0) - already_used)
            if taken:
                withdrawals[name] = already_used + taken
                remaining -= taken
            if remaining == 0:
                return withdrawals

    return None

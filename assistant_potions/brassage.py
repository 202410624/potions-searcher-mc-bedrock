"""Calcule les suites de brassage réalisables avec les potions et les réactifs en stock."""

from collections.abc import Mapping
from dataclasses import dataclass

from .catalogue import Catalogue, Transition


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

    for start in sorted(catalogue.potions.intersection(quantites)):
        if quantites[start] > 0:
            visit(start, frozenset({start}), Suite(start, (), {}))
    return recipes

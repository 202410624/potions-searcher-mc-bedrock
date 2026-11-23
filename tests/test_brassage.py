"""Vérifie la recherche des suites de brassage selon le stock et les chemins du catalogue."""

from pathlib import Path

import pytest

from assistant_potions.brassage import calculer_suites
from assistant_potions.catalogue import Catalogue, Transition, charger_catalogue


RECIPES = Path(__file__).resolve().parents[1] / "bedrock-samples-main/behavior_pack/recipes"
START = "potion_type:a"
VIA_B = "potion_type:b"
END = "potion_type:c"
VIA_D = "potion_type:d"
REAGENT = "nether_wart"


@pytest.fixture
def cyclic_catalogue():
    """Fournit un petit catalogue où deux branches rejoignent la même potion et où l’une peut
    revenir au départ.
    """
    return Catalogue(
        frozenset({START, VIA_B, END, VIA_D}),
        frozenset({REAGENT}),
        {
            START: (Transition(START, REAGENT, VIA_B), Transition(START, REAGENT, VIA_D)),
            VIA_B: (Transition(VIA_B, REAGENT, START), Transition(VIA_B, REAGENT, END)),
            VIA_D: (Transition(VIA_D, REAGENT, END),),
        },
    )


def test_regeneration():
    """Charge le catalogue Bedrock et vérifie que le stock préparé produit la suite attendue
    vers la régénération avec les bons réactifs. Vérifie aussi qu’un réactif seul ne permet
    aucun brassage.
    """
    catalogue = charger_catalogue(RECIPES)
    stock = {"potion_type:water": 1, "nether_wart": 1, "ghast_tear": 1, "potion_type:speed": 1}
    recipes = calculer_suites(catalogue, stock)["potion_type:regeneration"]

    assert [(recipe.depart, [step.arrivee for step in recipe.etapes], recipe.total_reactifs)
            for recipe in recipes] == [
        ("potion_type:water", ["potion_type:awkward", "potion_type:regeneration"],
         {"nether_wart": 1, "ghast_tear": 1})
    ]
    assert calculer_suites(catalogue, {"ghast_tear": 1}) == {}


def test_quantites_et_cycles(cyclic_catalogue):
    """Compare deux stocks sur le catalogue cyclique et vérifie la limite de réactifs,
    l’exclusion du retour au départ et les totaux des deux branches. Vérifie aussi que le
    stock reste intact et qu’une potion à zéro exemplaire ne sert pas de départ.
    """
    stock = {START: 1, REAGENT: 2}
    limited_recipes = calculer_suites(cyclic_catalogue, {START: 1, REAGENT: 1})
    recipes = calculer_suites(cyclic_catalogue, stock)

    assert END not in limited_recipes
    assert START not in recipes
    assert [recipe.etapes[0].arrivee for recipe in recipes[END]] == [VIA_B, VIA_D]
    assert all(recipe.total_reactifs == {REAGENT: 2} for recipe in recipes[END])
    assert stock == {START: 1, REAGENT: 2}
    assert calculer_suites(cyclic_catalogue, {START: 0, REAGENT: 2}) == {}


def test_departs_distincts(cyclic_catalogue):
    """Place deux potions de départ en stock et vérifie que les suites vers la même cible
    conservent leurs départs dans l’ordre attendu.
    """
    recipes = calculer_suites(cyclic_catalogue, {VIA_B: 1, START: 1, REAGENT: 2})
    assert [recipe.depart for recipe in recipes[END]] == [START, START, VIA_B]

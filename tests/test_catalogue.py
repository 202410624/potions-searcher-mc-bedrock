"""Vérifie la lecture des recettes Bedrock, leur normalisation et le rejet des catalogues
invalides.
"""

from pathlib import Path

import pytest

from assistant_potions.catalogue import ErreurCatalogue, Transition, charger_catalogue, nom_court


RECIPES = Path(__file__).resolve().parents[1] / "bedrock-samples-main/behavior_pack/recipes"


def test_catalogue_bedrock():
    """Charge les recettes fournies et vérifie des exemples de potions, de réactifs et de
    transitions de mélange et de contenant. Vérifie aussi que le retrait du préfixe préserve
    la casse.
    """
    catalogue = charger_catalogue(RECIPES)
    assert {"potion_type:water", "potion_type:thick"} <= catalogue.potions
    assert "ghast_tear" in catalogue.reactifs
    for start, reagent, end in [
        ("potion_type:water", "nether_wart", "potion_type:awkward"),
        ("potion_type:regeneration", "gunpowder", "splash_potion:regeneration"),
        ("splash_potion:regeneration", "dragon_breath", "lingering_potion:regeneration"),
    ]:
        assert Transition(start, reagent, end) in catalogue.par_depart[start]
    assert nom_court("minecraft:Ghast_Tear") == "Ghast_Tear"


@pytest.mark.parametrize("state", ["missing", "empty", "json", "schema"])
def test_catalogue_indisponible(tmp_path, state):
    """Prépare un dossier absent, vide ou contenant une recette illisible ou incomplète.
    Vérifie que le chargement lève ErreurCatalogue dans chaque cas.
    """
    directory = tmp_path / "recipes"
    if state != "missing":
        directory.mkdir()
    if state == "json":
        (directory / "bad.json").write_text("{", encoding="utf-8")
    if state == "schema":
        (directory / "bad.json").write_text(
            '{"minecraft:recipe_brewing_mix": {"input": ""}}', encoding="utf-8"
        )
    with pytest.raises(ErreurCatalogue):
        charger_catalogue(directory)

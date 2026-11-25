"""Vérifie les options, les sorties et les effets de bord de la commande `potions`."""

import json
from pathlib import Path

import pytest

from assistant_potions.cli import main
from assistant_potions.powershell import ALIAS_MARKER


RECIPES = Path(__file__).resolve().parents[1] / "bedrock-samples-main/behavior_pack/recipes"
WATER = "potion_type:water"
REGENERATION = "potion_type:regeneration"
UNKNOWN_INGREDIENT = "l'ingredient que vous avez cherche n'existe pas"


@pytest.fixture
def inventory(tmp_path):
    """Fournit le chemin d’un inventaire dans le dossier temporaire du test."""
    return tmp_path / ".potions" / "inventaire.json"


@pytest.fixture
def run(inventory):
    """Fournit un appel à la commande qui utilise l’inventaire temporaire du test et accepte
    un catalogue de remplacement.
    """
    def invoke(*args, recipes=RECIPES):
        """Transmet les arguments et les chemins injectés à `main`, puis retourne son code de
        sortie.
        """
        return main(args, chemin_inventaire=inventory, dossier_recettes=recipes)
    return invoke


def write_stock(path, records):
    """Prépare un inventaire de test en créant son dossier et en écrivant les entrées JSON
    fournies.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(records), encoding="utf-8")


@pytest.mark.parametrize("option", ["-h", "--help"])
def test_aide_et_stock(option, run, capsys):
    """Appelle les deux variantes de l’aide et vérifie le succès ainsi que la présence des
    options, des arguments et des exemples.
    """
    assert run(option) == 0
    output = capsys.readouterr().out
    for flag in ("--help", "-h", "--list", "-l", "--show", "-s", "--recipes", "-r",
                 "--search", "-sch", "--add", "-a", "--add_multiple", "-am", "--install",
                 "--clear", "-c", "--delete", "-d"):
        assert flag in output
    assert "POTION" in output and "OBJET QUANTITÉ" in output
    assert "potions -a ghast_tear 6" in output
    assert "potions -am blaze_powder 3 ghast_tear 6" in output


@pytest.mark.parametrize("option", ["-s", "--show"])
def test_affichage_stock(option, run, capsys, inventory):
    """Affiche d’abord un inventaire absent et vérifie qu’il reste absent. Écrit ensuite deux
    entrées et vérifie leur affichage trié avec les deux variantes de la commande.
    """
    assert run(option) == 0
    assert capsys.readouterr().out == "L’inventaire est vide.\n"
    assert not inventory.exists()
    write_stock(inventory, {"nether_wart": {"nombre": 2}, "ghast_tear": {"nombre": 1}})
    assert run(option) == 0
    assert capsys.readouterr().out == "ghast_tear : 1\nnether_wart : 2\n"


@pytest.mark.parametrize("option", ["-c", "--clear"])
def test_vider_inventaire(option, run, inventory, tmp_path):
    """Vide un stock sans catalogue et vérifie qu’une deuxième commande réussit aussi."""
    write_stock(inventory, {WATER: {"nombre": 2}, "ghast_tear": {"nombre": 1}})
    for _ in range(2):
        assert run(option, recipes=tmp_path / "absent") == 0
        assert json.loads(inventory.read_text(encoding="utf-8")) == {}


@pytest.mark.parametrize("option", ["-d", "--delete"])
def test_retirer_du_stock(option, run, inventory, tmp_path):
    """Vérifie qu’un retrait partiel conserve le niveau et qu’un retrait total efface l’entrée."""
    remaining = {"ghast_tear": {"nombre": 1}}
    write_stock(inventory, {**remaining, WATER: {"nombre": 3, "niveau": 2}})
    assert run(option, f"minecraft:{WATER}", "2", recipes=tmp_path / "absent") == 0
    assert json.loads(inventory.read_text(encoding="utf-8")) == {
        **remaining, WATER: {"nombre": 1, "niveau": 2},
    }
    assert run(option, WATER, "1", recipes=tmp_path / "absent") == 0
    assert json.loads(inventory.read_text(encoding="utf-8")) == remaining


@pytest.mark.parametrize(("args", "code"), [
    (("-c", "extra"), 2),
    (("-d", "ghast_tear"), 2),
    (("-d", "ghast_tear", "0"), 2),
    (("-d", "ghast_tear", "-1"), 2),
    (("-d", "ghast_tear", "2"), 1),
    (("-d", "nether_wart", "1"), 1),
])
def test_suppression_refusee(args, code, run, inventory):
    """Vérifie que les refus de saisie ou de stock laissent le fichier intact."""
    write_stock(inventory, {"ghast_tear": {"nombre": 1}})
    original = inventory.read_bytes()
    assert run(*args) == code
    assert inventory.read_bytes() == original


def test_ajouts_valides(run, inventory):
    """Ajoute des réactifs seuls et par lots avec les alias longs et courts. Vérifie la
    normalisation du préfixe et le cumul des quantités dans le JSON.
    """
    assert run("--add", "minecraft:ghast_tear", "6") == 0
    assert run("-a", "ghast_tear", "1") == 0
    assert json.loads(inventory.read_text(encoding="utf-8")) == {"ghast_tear": {"nombre": 7}}
    assert run("--add_multiple", "blaze_powder", "3", "ghast_tear", "6", "ghast_tear", "2") == 0
    assert run("-am", "blaze_powder", "1") == 0
    assert json.loads(inventory.read_text(encoding="utf-8")) == {
        "blaze_powder": {"nombre": 4}, "ghast_tear": {"nombre": 15}
    }


def test_recherche_ingredients(run, capsys, inventory):
    """Recherche par fragment ou identifiant complet dans le catalogue avec un inventaire absent.
    Vérifie qu’afficher les correspondances ou leur absence ne crée pas l’inventaire.
    """
    assert run("--search", "GHAST") == 0
    assert capsys.readouterr().out == "ghast_tear\n"
    assert run("-sch", "minecraft:ghast_tear") == 0
    assert capsys.readouterr().out == "ghast_tear\n"
    assert run("-sch", "potion_type:regeneration") == 0
    assert REGENERATION in capsys.readouterr().out.splitlines()
    assert run("-sch", "water_bottle") == 0
    assert capsys.readouterr().out.splitlines() == ["water_bottle", "water_bottles"]
    assert run("-sch", "ingredient_inconnu") == 0
    assert "Aucun ingrédient trouvé" in capsys.readouterr().out
    assert not inventory.exists()


@pytest.mark.parametrize(("option", "example"), [
    ("-a", "potions -a ghast_tear 6"), ("-am", "potions -am blaze_powder 3 ghast_tear 6"),
])
def test_exemples_ajouts(option, example, run, capsys, inventory):
    """Lance chaque option d’ajout sans argument et vérifie le code 2, l’exemple affiché,
    l’aide unique et l’absence de fichier créé.
    """
    assert run(option) == 2
    output = capsys.readouterr()
    assert output.out.strip() == example
    assert output.err.count("usage:") == 1
    assert not inventory.exists()


@pytest.mark.parametrize("args", [
    ("-a", "ghast_tear", "6", "blaze_powder", "3"),
    ("-a", "ghast_tear", "6", "surplus"),
    ("-a", "ghast_tear", "１２"),
    ("-l", "surplus"), ("-s", "surplus"), ("-h", "surplus"),
    ("--lis",), ("--",), ("-ll",), ("-aa", "ghast_tear", "1"),
    ("--search",), ("-sch", "minecraft:"), ("-sch", "ghast", "tear"),
])
def test_ajouts_et_syntaxes_invalides(args, run, capsys, inventory):
    """Soumet des arguments ou des options invalides et vérifie le code 2, l’affichage unique
    de l’aide et l’absence de fichier créé.
    """
    assert run(*args) == 2
    assert capsys.readouterr().err.count("usage:") == 1
    assert not inventory.exists()


def test_lots_partiels(run, capsys, inventory):
    """Soumet un lot mixte et vérifie le code 2, le cumul des paires valides et les
    avertissements suivis de l’aide. Vérifie ensuite qu’un lot entièrement invalide laisse le
    fichier intact.
    """
    assert run("-am", "ghast_tear", "2", "Ghast_Tear", "1", "blaze_powder", "-1",
               "nether_wart", "0", "sugar", "1.5", "ghast_tear", "3", "redstone") == 2
    assert json.loads(inventory.read_text(encoding="utf-8")) == {"ghast_tear": {"nombre": 5}}
    lines = capsys.readouterr().err.splitlines()
    assert len([line for line in lines[:5] if line.startswith("Avertissement")]) == 5
    assert UNKNOWN_INGREDIENT in lines[0]
    assert [index for index, line in enumerate(lines) if line.startswith("usage:")] == [5]

    original = inventory.read_bytes()
    assert run("-am", "sugar", "x", "poudre", "2") == 2
    assert inventory.read_bytes() == original


def test_liste_et_recettes(run, capsys, inventory):
    """Prépare un stock permettant le brassage de régénération, puis vérifie la liste triée et
    chaque ligne de la recette avec les deux variantes des options. Vérifie aussi que les
    consultations préservent le stock.
    """
    assert run("-a", "minecraft:water_bottle", "1") == 0
    assert run("-am", "water_bottles", "1", "nether_wart", "1", "ghast_tear", "1") == 0
    assert json.loads(inventory.read_text(encoding="utf-8"))[WATER]["nombre"] == 2
    original = inventory.read_bytes()
    for option in ("--list", "-l"):
        assert run(option) == 0
        assert capsys.readouterr().out.splitlines() == [
            "potion_type:awkward", "potion_type:mundane", REGENERATION,
        ]
    for option, potion in (("--recipes", f"minecraft:{REGENERATION}"), ("-r", REGENERATION)):
        assert run(option, potion) == 0
        assert capsys.readouterr().out.splitlines() == [
            f"Départ : {WATER}", "  nether_wart → potion_type:awkward",
            f"  ghast_tear → {REGENERATION}", "Réactifs :", "  ghast_tear : 1", "  nether_wart : 1",
        ]
    assert inventory.read_bytes() == original

    assert run("-a", "potion_type:awkward", "1") == 0
    assert run("-r", REGENERATION) == 0
    assert "Départ : potion_type:awkward" in capsys.readouterr().out.splitlines()


def test_recettes_sans_resultat(run, capsys):
    """Consulte les brassages avec un stock vide et vérifie le succès et les messages
    d’absence de résultat pour la liste et la potion ciblée.
    """
    assert run("-l") == 0
    assert capsys.readouterr().out.strip() == "Aucune potion réalisable."
    assert run("-r", REGENERATION) == 0
    assert capsys.readouterr().out.strip() == f"Aucune recette réalisable pour {REGENERATION}."


@pytest.mark.parametrize("option", ["-b", "--brew"])
def test_brassage_du_lot(option, run, inventory, monkeypatch, capsys):
    """Brasse deux potions avec de l’eau stockée sous deux noms et une seule potion intermédiaire.
    Vérifie le retrait de l’eau et des réactifs, le cumul sans changement de niveau et la
    conservation de la potion intermédiaire.
    """
    awkward = "potion_type:awkward"
    write_stock(inventory, {
        WATER: {"nombre": 1}, "water_bottles": {"nombre": 1},
        awkward: {"nombre": 1}, REGENERATION: {"nombre": 1, "niveau": 2},
        "nether_wart": {"nombre": 3}, "ghast_tear": {"nombre": 2},
    })
    monkeypatch.setattr("builtins.input", lambda prompt: "2")

    assert run(option, f"minecraft:{REGENERATION}") == 0
    assert f"2 × {REGENERATION}" in capsys.readouterr().out
    assert json.loads(inventory.read_text(encoding="utf-8")) == {
        WATER: {"nombre": 0, "niveau": 1}, "water_bottles": {"nombre": 0},
        awkward: {"nombre": 1, "niveau": 1}, REGENERATION: {"nombre": 3, "niveau": 2},
        "nether_wart": {"nombre": 1}, "ghast_tear": {"nombre": 0},
    }


@pytest.mark.parametrize(("quantity", "expected_code"), [("2", 1), ("0", 2), ("abc", 2)])
def test_brassage_refuse_sans_modifier_le_stock(quantity, expected_code, run, inventory, monkeypatch):
    """Prépare de quoi brasser une potion, puis soumet un lot trop grand ou une quantité invalide.
    Vérifie le code de refus et la conservation du JSON à l’identique.
    """
    write_stock(inventory, {WATER: {"nombre": 2}, "nether_wart": {"nombre": 2},
                            "ghast_tear": {"nombre": 1}})
    original = inventory.read_bytes()
    monkeypatch.setattr("builtins.input", lambda prompt: quantity)

    assert run("-b", REGENERATION) == expected_code
    assert inventory.read_bytes() == original


@pytest.mark.parametrize("args", [
    ("-r",), ("-r", "potion_type:inconnue"), ("-r", WATER, "potion_type:speed"),
])
def test_recettes_invalides(args, run, capsys):
    """Demande une recette sans cible, avec une cible inconnue ou avec deux cibles. Vérifie le
    code 2, le message d’erreur et l’affichage unique de l’aide.
    """
    assert run(*args) == 2
    errors = capsys.readouterr().err
    assert "Erreur" in errors
    assert errors.count("usage:") == 1


def test_catalogue_absent(run, tmp_path, inventory, capsys):
    """Injecte un dossier absent et vérifie que les commandes qui exigent un catalogue
    échouent avec un diagnostic. Vérifie que l’aide et la consultation du stock réussissent
    sans créer d’inventaire.
    """
    directory = tmp_path / "absent"
    for args in (("-l",), ("-r", WATER), ("-a", "ghast_tear", "1"), ("-sch", "ghast")):
        assert run(*args, recipes=directory) == 1
        assert "catalogue" in capsys.readouterr().err
    assert run("-h", recipes=directory) == 0
    assert run(recipes=directory) == 0
    assert run("-s", recipes=directory) == 0
    assert not inventory.exists()


def test_inventaire_corrompu(run, inventory, capsys):
    """Écrit du JSON incomplet, puis vérifie que la lecture et l’ajout signalent une erreur
    d’inventaire et que le fichier conserve son contenu.
    """
    inventory.parent.mkdir()
    inventory.write_bytes(b"{")
    assert run("-s") == 1
    assert "inventaire" in capsys.readouterr().err
    assert run("-a", "ghast_tear", "1") == 1
    assert "inventaire" in capsys.readouterr().err
    assert inventory.read_bytes() == b"{"


def test_echec_de_remplacement(run, inventory, monkeypatch, capsys):
    """Simule un échec de remplacement pendant un ajout. Vérifie le code 1, le diagnostic
    d’inventaire et la conservation du fichier initial.
    """
    write_stock(inventory, {"ghast_tear": {"nombre": 1}})
    original = inventory.read_bytes()

    def fail_replace(source, destination):
        """Lève OSError à la place du remplacement de fichier pour simuler un échec de
        sauvegarde.
        """
        raise OSError("Échec simulé")

    monkeypatch.setattr("assistant_potions.inventaire.os.replace", fail_replace)
    assert run("-a", "ghast_tear", "1") == 1
    assert "inventaire" in capsys.readouterr().err
    assert inventory.read_bytes() == original


def test_install_command_updates_powershell_profiles(run, tmp_path, monkeypatch, capsys):
    """Simule Windows, un profil temporaire et un lanceur. Vérifie que l’installation préserve
    le contenu existant, qu’une répétition est sans effet et qu’un déplacement du lanceur met
    à jour l’unique alias en échappant l’apostrophe.
    """
    profile = tmp_path / "Documents" / "PowerShell" / "profile.ps1"
    profile.parent.mkdir(parents=True)
    original = b"# Commentaire existant\r\nSet-Alias gs Get-ChildItem"
    profile.write_bytes(original)
    launcher = tmp_path / "Old" / "potions.exe"
    monkeypatch.setattr("assistant_potions.powershell.sys.platform", "win32")
    monkeypatch.setattr("assistant_potions.powershell.find_profiles", lambda: [profile])
    monkeypatch.setattr("assistant_potions.powershell.find_launcher", lambda: launcher)

    assert run("--install", recipes=tmp_path / "absent") == 0
    assert str(profile) in capsys.readouterr().out
    first_installation = profile.read_bytes()
    assert first_installation.decode("utf-8-sig").startswith(original.decode() + "\r\n")
    assert str(launcher) in first_installation.decode("utf-8-sig")
    assert run("--install") == 0
    assert profile.read_bytes() == first_installation

    old_launcher = launcher
    launcher = tmp_path / "Dossier d'examen" / "potions.exe"
    assert run("--install") == 0
    updated = profile.read_text(encoding="utf-8-sig")
    escaped_target = str(launcher).replace("'", "''")
    assert f"Set-Alias -Name potions -Value '{escaped_target}'" in updated
    assert updated.count(ALIAS_MARKER) == 1
    assert "Set-Alias gs Get-ChildItem" in updated
    assert str(old_launcher) not in updated


def test_install_command_rejects_extra_arguments(run, monkeypatch, capsys):
    """Remplace l’installateur par un garde, puis soumet un argument superflu. Vérifie le code
    2 et le diagnostic, et échoue si l’installateur est appelé.
    """
    def unexpected_install():
        """Fait échouer le test si la commande invalide atteint l’installateur."""
        pytest.fail("Une commande invalide ne doit pas accéder au profil.")

    monkeypatch.setattr("assistant_potions.cli.install_command", unexpected_install)
    assert run("--install", "surplus") == 2
    assert "--install ne prend aucun argument." in capsys.readouterr().err

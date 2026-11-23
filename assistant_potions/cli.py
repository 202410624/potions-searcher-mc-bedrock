"""Interprète les commandes de l’assistant et affiche leurs résultats dans le terminal."""

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from .brassage import Suite, calculer_suites
from .catalogue import Catalogue, ErreurCatalogue, charger_catalogue, nom_court
from .inventaire import ErreurInventaire, ajouter_au_stock, lire_inventaire
from .powershell import CommandInstallationError, install_command


ADD_EXAMPLE = "potions -a ghast_tear 6"
BATCH_EXAMPLE = "potions -am blaze_powder 3 ghast_tear 6"
UNKNOWN_INGREDIENT = "l'ingredient que vous avez cherche n'existe pas"
COMMANDS = (
    ("--help", "-h", "help", "Afficher l’aide."),
    ("--list", "-l", "list", "Lister les potions réalisables."),
    ("--recipes", "-r", "recipes", "POTION : afficher toutes ses recettes réalisables."),
    ("--show", "-s", "show", "Afficher l’inventaire."),
    ("--search", "-sch", "search", "INGRÉDIENT : chercher par nom dans le catalogue."),
    ("--add", "-a", "add", "OBJET QUANTITÉ : ajouter un objet au stock."),
    ("--add_multiple", "-am", "batch", "OBJET QUANTITÉ ... : ajouter plusieurs paires."),
    ("--install-command", None, "install", "Enregistrer la commande potions dans PowerShell."),
)


class CommandError(ValueError):
    """Signale une option inconnue ou des arguments incompatibles avec la commande."""


def make_parser() -> argparse.ArgumentParser:
    """Construit le parseur et son aide à partir des options et alias déclarés dans COMMANDS.
    """
    parser = argparse.ArgumentParser(
        prog="potions",
        description="Consulter les brassages réalisables et gérer l’inventaire local.",
        epilog=(
            "Exemples :\n"
            "  potions -h\n"
            "  potions -s\n"
            "  potions -l\n"
            "  potions -r potion_type:regeneration\n"
            "  potions -sch ghast\n"
            f"  {ADD_EXAMPLE}\n"
            f"  {BATCH_EXAMPLE}"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        allow_abbrev=False,
        add_help=False,
    )
    commands = parser.add_mutually_exclusive_group()
    for flag, alias, command, description in COMMANDS:
        options = (flag, alias) if alias else (flag,)
        commands.add_argument(
            *options, dest="command", action="store_const", const=command, help=description
        )
    return parser


def parse_quantity(raw: str) -> int:
    """Convertit une suite de chiffres ASCII en entier strictement positif. Une saisie
    invalide lève ValueError.
    """
    if raw.isascii() and raw.isdecimal():
        quantity = int(raw)
        if quantity > 0:
            return quantity
    raise ValueError("Quantité invalide")


def validate_additions(
    args: Sequence[str], catalogue: Catalogue
) -> tuple[dict[str, int], list[str]]:
    """Valide les paires nom-quantité à l’aide du catalogue. Cumule les ajouts valides par nom
    court et retourne les avertissements dans l’ordre de saisie.
    """
    additions: dict[str, int] = {}
    warnings = []
    for index in range(0, len(args), 2):
        name = nom_court(args[index])
        if index + 1 == len(args):
            warnings.append(f"Quantité manquante pour {name}.")
            continue
        if name not in catalogue.reactifs and name not in catalogue.potions:
            warnings.append(f"{UNKNOWN_INGREDIENT} ({name}).")
            continue
        try:
            quantity = parse_quantity(args[index + 1])
        except ValueError:
            warnings.append(f"Quantité invalide pour {name}. Entrez un entier positif.")
            continue
        additions[name] = additions.get(name, 0) + quantity
    return additions, warnings


def print_recipe(recipe: Suite) -> None:
    """Affiche la potion de départ, les étapes dans leur ordre de brassage et les totaux de
    réactifs triés par nom.
    """
    print(f"Départ : {recipe.depart}")
    for step in recipe.etapes:
        print(f"  {step.reactif} → {step.arrivee}")
    print("Réactifs :")
    for reagent, total in sorted(recipe.total_reactifs.items()):
        print(f"  {reagent} : {total}")


def main(
    argv: Sequence[str] | None = None,
    *,
    chemin_inventaire: Path | None = None,
    dossier_recettes: Path | None = None,
) -> int:
    """Exécute la commande à partir de `argv` ou des arguments du terminal, avec des chemins
    de données facultatifs. Retourne 0 en cas de succès, 1 pour une erreur de données ou
    d’accès et 2 pour une saisie invalide, même si une partie du lot a été enregistrée.
    """
    args = sys.argv[1:] if argv is None else argv
    parser = make_parser()
    if not args:
        parser.print_help()
        return 0

    try:
        if not any(args[0] in (flag, alias) for flag, alias, _, _ in COMMANDS):
            raise CommandError(f"Commande inconnue ({args[0]}).")
        # Seule l’option initiale est analysée par argparse. Le reste forme les données.
        command = parser.parse_args(args[:1]).command
        values = args[1:]
        if command in {"help", "list", "show", "install"} and values:
            raise CommandError(f"{args[0]} ne prend aucun argument.")
        if command == "help":
            parser.print_help()
            return 0
        if command == "install":
            for profile in install_command():
                print(f"Alias potions enregistré dans {profile}")
            print("Ouvre un nouveau terminal PowerShell, puis tape potions --help.")
            return 0
        if command in {"add", "batch"} and not values:
            print(ADD_EXAMPLE if command == "add" else BATCH_EXAMPLE)
            parser.print_help(file=sys.stderr)
            return 2
        if command == "add" and len(values) != 2:
            raise CommandError("--add exige exactement une paire OBJET QUANTITÉ.")
        if command == "recipes" and len(values) != 1:
            raise CommandError("--recipes exige exactement un nom de potion.")
        if command == "search":
            if len(values) != 1:
                raise CommandError("--search exige exactement un nom ou un fragment de nom.")
            query = nom_court(values[0].strip().casefold())
            if not query:
                raise CommandError("--search exige un nom ou un fragment de nom non vide.")

        inventory_path = chemin_inventaire
        if inventory_path is None:
            try:
                inventory_path = Path.home() / ".potions" / "inventaire.json"
            except RuntimeError as error:
                raise ErreurInventaire("Impossible de localiser le dossier personnel.") from error
        if command == "show":
            inventory = lire_inventaire(inventory_path)
            if not inventory:
                print("L’inventaire est vide.")
            for name, entry in sorted(inventory.items()):
                print(f"{name} : {entry.nombre}")
            return 0

        recipes_path = dossier_recettes
        if recipes_path is None:
            recipes_path = Path(__file__).resolve().parents[1] / "bedrock-samples-main/behavior_pack/recipes"
        catalogue = charger_catalogue(recipes_path)

        if command == "search":
            matching = sorted(name for name in catalogue.reactifs if query in name.casefold())
            if matching:
                print("\n".join(matching))
            else:
                print(f"Aucun ingrédient trouvé pour « {values[0]} ».")
            return 0

        if command in {"add", "batch"}:
            additions, warnings = validate_additions(values, catalogue)
            for warning in warnings:
                print(f"Avertissement : {warning}", file=sys.stderr)
            if warnings:
                parser.print_help(file=sys.stderr)
            if additions:
                ajouter_au_stock(inventory_path, additions)
            return 2 if warnings else 0

        target = None
        if command == "recipes":
            target = nom_court(values[0])
            if target not in catalogue.potions:
                raise CommandError(f"Potion inconnue ({target}).")

        stock = {name: entry.nombre for name, entry in lire_inventaire(inventory_path).items()}
        recipes = calculer_suites(catalogue, stock)
        if target is None:
            if recipes:
                print("\n".join(sorted(recipes)))
            else:
                print("Aucune potion réalisable.")
        else:
            matching = recipes.get(target, [])
            if not matching:
                print(f"Aucune recette réalisable pour {target}.")
            for index, recipe in enumerate(matching):
                if index:
                    print()
                print_recipe(recipe)
        return 0
    except CommandError as error:
        print(f"Erreur : {error}", file=sys.stderr)
        parser.print_help(file=sys.stderr)
        return 2
    except (ErreurCatalogue, ErreurInventaire, CommandInstallationError) as error:
        print(f"Erreur : {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())

"""Valide et conserve l’inventaire local dans un fichier JSON mis à jour sous verrou."""

import json
import os
import re
from collections.abc import Iterator, Mapping
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from tempfile import NamedTemporaryFile

from .catalogue import POTION_PREFIXES


SHORT_NAME = re.compile(r"[a-zA-Z0-9_./-]+")


class ErreurInventaire(ValueError):
    """Signale un inventaire invalide ou un échec d’accès ou de sauvegarde."""


@dataclass(frozen=True)
class EntreeInventaire:
    """Stocke la quantité d’un objet et, pour une potion, son niveau."""
    nombre: int
    niveau: int | None = None


def is_potion(name: str) -> bool:
    """Détermine si le nom utilise un préfixe de potion reconnu et un effet de forme valide.
    """
    container, _, effect = name.partition(":")
    return container in POTION_PREFIXES.values() and SHORT_NAME.fullmatch(effect) is not None


def read_entry(name: str, record: object) -> EntreeInventaire:
    """Valide le nom court et les champs d’une entrée JSON, puis attribue le niveau 1 par
    défaut aux potions. Lève ErreurInventaire si l’entrée est invalide.
    """
    potion = is_potion(name)
    if not potion and not SHORT_NAME.fullmatch(name):
        raise ErreurInventaire(f"Nom court invalide dans l’inventaire ({name}).")

    allowed_fields = {"nombre", "niveau"} if potion else {"nombre"}
    if not isinstance(record, dict) or record.keys() - allowed_fields:
        raise ErreurInventaire(f"Entrée invalide pour {name}.")
    quantity = record.get("nombre")
    if type(quantity) is not int or quantity < 0:
        raise ErreurInventaire(f"Nombre invalide pour {name}.")

    level = None
    if potion:
        level = record.get("niveau", 1)
        if type(level) is not int or level < 1:
            raise ErreurInventaire(f"Niveau invalide pour {name}.")
    return EntreeInventaire(quantity, level)


def lire_inventaire(chemin: Path) -> dict[str, EntreeInventaire]:
    """Lit le fichier JSON et valide ses entrées. Retourne un dictionnaire vide si le fichier
    est absent et lève ErreurInventaire si le contenu est illisible ou invalide.
    """
    try:
        content = chemin.read_text(encoding="utf-8")
    except FileNotFoundError:
        return {}
    except (OSError, UnicodeError) as error:
        raise ErreurInventaire(f"Impossible de lire l’inventaire ({chemin}).") from error

    try:
        records = json.loads(content)
    except (ValueError, RecursionError) as error:
        raise ErreurInventaire(f"JSON invalide dans l’inventaire ({chemin}).") from error
    if not isinstance(records, dict):
        raise ErreurInventaire("L’inventaire doit contenir un objet JSON.")
    return {name: read_entry(name, record) for name, record in records.items()}


def write_inventory(path: Path, inventory: Mapping[str, EntreeInventaire]) -> None:
    """Sérialise l’inventaire dans un fichier temporaire, puis remplace le fichier cible.
    Supprime le temporaire en cas d’échec et laisse remonter l’erreur.
    """
    records = {}
    for name, entry in inventory.items():
        record = {"nombre": entry.nombre}
        if entry.niveau is not None:
            record["niveau"] = entry.niveau
        records[name] = record

    temporary_path = None
    try:
        # Le remplacement atomique exige un fichier fermé, sur le même volume.
        with NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=path.parent, suffix=".tmp", delete=False
        ) as temporary:
            temporary_path = Path(temporary.name)
            json.dump(records, temporary, ensure_ascii=False, indent=2, sort_keys=True)
            temporary.write("\n")
        os.replace(temporary_path, path)
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)


def ajouter_au_stock(chemin: Path, ajouts: Mapping[str, int]) -> None:
    """Ajoute un lot validé à l’inventaire en préservant les niveaux existants."""
    mettre_a_jour_stock(chemin, ajouts, retraits={})


@contextmanager
def verrouiller_inventaire(chemin: Path) -> Iterator[None]:
    """Réserve l’écriture de l’inventaire et libère le verrou même en cas d’échec."""
    lock = chemin.with_name(chemin.name + ".lock")
    try:
        chemin.parent.mkdir(parents=True, exist_ok=True)
        lock_file = lock.open("x", encoding="utf-8")
        try:
            lock_file.close()
            yield
        finally:
            lock.unlink()
    except OSError as error:
        raise ErreurInventaire(f"Impossible de mettre à jour l’inventaire ({error}).") from error
    except ValueError as error:
        if isinstance(error, ErreurInventaire):
            raise
        raise ErreurInventaire(f"Impossible d’encoder l’inventaire ({error}).") from error


def vider_inventaire(chemin: Path) -> None:
    """Remplace le stock par un inventaire vide sous verrou, s’il existe déjà."""
    with verrouiller_inventaire(chemin):
        try:
            chemin.stat()
        except FileNotFoundError:
            return
        write_inventory(chemin, {})


def mettre_a_jour_stock(
    chemin: Path,
    ajouts: Mapping[str, int],
    *,
    retraits: Mapping[str, int],
    supprimer_epuise: bool = False,
) -> None:
    """Applique les mouvements sous verrou et retire les entrées épuisées si demandé.
    Lève `ErreurInventaire` si un retrait dépasse le stock courant ou si la mise à jour échoue.
    """
    if not ajouts and not retraits:
        return

    with verrouiller_inventaire(chemin):
        inventory = lire_inventaire(chemin)
        for name, quantity in retraits.items():
            entry = inventory.get(name)
            if entry is None or entry.nombre < quantity:
                raise ErreurInventaire(f"Stock insuffisant pour {name}.")
            remaining = entry.nombre - quantity
            if supprimer_epuise and remaining == 0 and name not in ajouts:
                del inventory[name]
            else:
                inventory[name] = EntreeInventaire(remaining, entry.niveau)
        for name, quantity in ajouts.items():
            entry = inventory.get(name)
            if entry is None:
                entry = EntreeInventaire(0, 1 if is_potion(name) else None)
            inventory[name] = EntreeInventaire(entry.nombre + quantity, entry.niveau)
        write_inventory(chemin, inventory)

"""Vérifie la persistance, la validation et la protection de l’inventaire JSON."""

import json

import pytest

from assistant_potions.inventaire import (
    EntreeInventaire,
    ErreurInventaire,
    ajouter_au_stock,
    lire_inventaire,
)


def test_premier_ajout_et_cumul(tmp_path):
    """Part d’un inventaire absent et vérifie qu’un lot vide ne crée pas de dossier. Ajoute
    ensuite une potion et un réactif, puis vérifie le niveau par défaut et le cumul écrit dans
    le JSON.
    """
    path = tmp_path / ".potions" / "inventaire.json"
    assert lire_inventaire(path) == {}
    ajouter_au_stock(path, {})
    assert not path.parent.exists()
    ajouter_au_stock(path, {"potion_type:water": 1, "nether_wart": 1})
    ajouter_au_stock(path, {"nether_wart": 2})
    assert json.loads(path.read_text(encoding="utf-8")) == {
        "potion_type:water": {"nombre": 1, "niveau": 1},
        "nether_wart": {"nombre": 3},
    }


@pytest.mark.parametrize("content", [
    b"{",
    b'{"ghast_tear":{"nombre":true}}',
    b'{"ghast_tear":{"nombre":1,"niveau":1}}',
    b'{"potion_type:":{"nombre":1}}',
    b'{"minecraft:ghast_tear":{"nombre":1}}',
    b'{"potion_type:water":{"nombre":1,"niveau":0}}',
])
def test_inventaire_invalide(tmp_path, content):
    """Écrit une entrée ou un document JSON invalide et tente un ajout. Vérifie que l’erreur
    laisse le fichier intact et ne laisse aucun fichier auxiliaire.
    """
    path = tmp_path / "inventaire.json"
    path.write_bytes(content)
    with pytest.raises(ErreurInventaire):
        ajouter_au_stock(path, {"ghast_tear": 1})
    assert path.read_bytes() == content
    assert list(tmp_path.iterdir()) == [path]


def test_compatibilite_et_echec_ecriture(tmp_path, monkeypatch):
    """Prépare des potions avec et sans niveau enregistré, puis simule un échec de sauvegarde.
    Vérifie les niveaux lus, la conservation du fichier, le nettoyage et le maintien du niveau
    explicite au nouvel essai.
    """
    path = tmp_path / "inventaire.json"
    content = b'{"potion_type:speed":{"nombre":1,"niveau":2},"potion_type:water":{"nombre":1}}'
    path.write_bytes(content)
    inventory = lire_inventaire(path)
    assert inventory["potion_type:speed"].niveau == 2
    assert inventory["potion_type:water"].niveau == 1

    def fail_replace(source, destination):
        """Lève OSError à la place du remplacement de fichier pour tester le nettoyage après
        l’échec.
        """
        raise OSError("Échec simulé")

    with monkeypatch.context() as patch:
        patch.setattr("assistant_potions.inventaire.os.replace", fail_replace)
        with pytest.raises(ErreurInventaire):
            ajouter_au_stock(path, {"potion_type:speed": 1})
    assert path.read_bytes() == content
    assert list(tmp_path.iterdir()) == [path]
    ajouter_au_stock(path, {"potion_type:speed": 1})
    assert lire_inventaire(path)["potion_type:speed"] == EntreeInventaire(2, 2)


def test_verrou_existant(tmp_path):
    """Prépare un inventaire et un verrou déjà présents, puis tente un ajout. Vérifie le refus
    et la conservation des deux fichiers.
    """
    path = tmp_path / "inventaire.json"
    content = b'{"ghast_tear":{"nombre":1}}'
    path.write_bytes(content)
    lock = tmp_path / "inventaire.json.lock"
    lock.write_bytes(b"occupe")

    with pytest.raises(ErreurInventaire):
        ajouter_au_stock(path, {"ghast_tear": 1})
    assert path.read_bytes() == content
    assert lock.read_bytes() == b"occupe"

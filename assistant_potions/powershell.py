"""Installe l’alias `potions` dans les profils PowerShell de l’utilisateur sous Windows."""

import codecs
import re
import shutil
import subprocess
import sys
import sysconfig
from pathlib import Path
from tempfile import NamedTemporaryFile


ALIAS_MARKER = "# assistant-potions: alias potions"
ALIAS_PREFIX = "Set-Alias -Name potions -Value "
PROFILE_QUERY = "[Console]::OutputEncoding = [Text.Encoding]::UTF8; $PROFILE.CurrentUserAllHosts"


class CommandInstallationError(RuntimeError):
    """Signale un obstacle à l’installation de l’alias dans un profil PowerShell."""


def find_launcher() -> Path:
    """Cherche `potions.exe` à côté du programme lancé, puis dans le dossier des scripts
    Python. Lève CommandInstallationError si aucun fichier ne correspond.
    """
    candidates = (
        Path(sys.argv[0]).absolute().with_name("potions.exe"),
        Path(sysconfig.get_path("scripts")) / "potions.exe",
    )
    for launcher in candidates:
        if launcher.is_file():
            return launcher
    raise CommandInstallationError(
        "potions.exe est introuvable. Installe le projet dans cet environnement Python."
    )


def find_profiles() -> list[Path]:
    """Interroge les versions de PowerShell disponibles pour obtenir les chemins distincts des
    profils de l’utilisateur communs à tous les hôtes. Lève CommandInstallationError si aucun
    shell n’est disponible ou si une requête échoue ou renvoie un chemin non absolu.
    """
    profiles = []
    for name in ("powershell.exe", "pwsh.exe"):
        shell = shutil.which(name)
        if shell is None:
            continue
        try:
            result = subprocess.run(
                [shell, "-NoProfile", "-NonInteractive", "-Command", PROFILE_QUERY],
                check=True, capture_output=True, encoding="utf-8", timeout=15,
            )
        except (OSError, subprocess.SubprocessError, UnicodeError) as error:
            raise CommandInstallationError(
                f"Impossible de localiser le profil de {name}."
            ) from error
        profile = Path(result.stdout.strip().lstrip("\ufeff"))
        if not profile.is_absolute():
            raise CommandInstallationError(f"Chemin du profil de {name} invalide.")
        if profile not in profiles:
            profiles.append(profile)
    if not profiles:
        raise CommandInstallationError("PowerShell est introuvable.")
    return profiles


def update_profile(profile: Path, launcher: Path) -> None:
    """Ajoute ou actualise l’alias marqué dans un profil non signé, en échappant le chemin et
    en reprenant ses fins de ligne. Remplace le fichier en cas de changement et lève
    CommandInstallationError si le profil est signé.
    """
    try:
        original = profile.read_bytes()
    except FileNotFoundError:
        original = b""

    if original.startswith((codecs.BOM_UTF16_LE, codecs.BOM_UTF16_BE)):
        encoding = "utf-16"
    elif original.startswith(codecs.BOM_UTF8) or not original:
        encoding = "utf-8-sig"
    else:
        encoding = "utf-8"

    content = original.decode(encoding)
    if "# SIG # Begin signature block" in content:
        raise CommandInstallationError(f"Le profil est signé : {profile}")

    line_break = re.search(r"\r\n|\n|\r", content)
    newline = line_break.group() if line_break else "\r\n"
    # Les apostrophes typographiques sont aussi des délimiteurs pour PowerShell.
    target = re.sub("['‘’]", lambda match: match.group() * 2, str(launcher))
    alias = f"{ALIAS_PREFIX}'{target}' {ALIAS_MARKER}{newline}"

    lines = []
    installed = False
    for line in content.splitlines(keepends=True):
        if line.startswith(ALIAS_PREFIX) and line.rstrip().endswith(ALIAS_MARKER):
            if not installed:
                lines.append(alias)
                installed = True
        else:
            lines.append(line)
    if not installed:
        if content and not content.endswith(("\n", "\r")):
            lines.append(newline)
        lines.append(alias)

    updated = "".join(lines)
    if updated == content:
        return

    # Windows PowerShell reconnaît l’UTF-8 avec BOM lorsque le profil contient des accents.
    if encoding == "utf-8" and not alias.isascii():
        encoding = "utf-8-sig"
    profile.parent.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile(dir=profile.parent, delete=False) as temporary:
        temporary_path = Path(temporary.name)
        try:
            temporary.write(updated.encode(encoding))
            temporary.close()
            temporary_path.replace(profile)
        finally:
            temporary.close()
            temporary_path.unlink(missing_ok=True)


def install_command() -> list[Path]:
    """Sous Windows, détecte le lanceur et les profils, installe l’alias dans chacun et
    retourne les chemins traités. Signale les échecs d’installation avec
    CommandInstallationError.
    """
    if sys.platform != "win32":
        raise CommandInstallationError("Cette option est prévue pour PowerShell sous Windows.")
    launcher = find_launcher()
    profiles = find_profiles()
    for profile in profiles:
        try:
            update_profile(profile, launcher)
        except (OSError, UnicodeError) as error:
            raise CommandInstallationError(
                f"Impossible de modifier le profil PowerShell {profile} : {error}"
            ) from error
    return profiles

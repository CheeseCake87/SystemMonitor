from pathlib import Path
from json import loads


def walk_find_logo() -> Path | None:
    cwd = Path(__file__).parent

    logo = cwd / "logo.gif"

    if logo.exists():
        return logo

    for r in range(3):
        cwd = cwd.parent
        logo = cwd / "logo.gif"
        if logo.exists():
            return logo

    dev_check = Path(__file__).parent / "dist" / "logo.gif"
    if dev_check.exists():
        return dev_check

    return None


def walk_find_config():
    cwd = Path(__file__).parent

    config = cwd / "config.json"

    if config.exists():
        return loads(config.read_text())

    for r in range(3):
        cwd = cwd.parent
        config = cwd / "config.json"
        if config.exists():
            return loads(config.read_text())

    dev_check = Path(__file__).parent / "dist" / "config.json"
    if dev_check.exists():
        return loads(dev_check.read_text())

    raise FileNotFoundError("config.json not found")


def walk_find_config_file():
    cwd = Path(__file__).parent

    config = cwd / "config.json"

    if config.exists():
        return loads(config.read_text())

    for r in range(3):
        cwd = cwd.parent
        config = cwd / "config.json"
        if config.exists():
            return config

    dev_check = Path(__file__).parent / "dist" / "config.json"
    if dev_check.exists():
        return config

    raise FileNotFoundError("config.json not found")

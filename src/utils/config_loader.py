"""
config_loader.py

Loads application configuration files.

Supported files:
    - config/settings.yaml
    - config/keywords.yaml
"""

from pathlib import Path
import yaml

from src.utils.logger import get_logger

logger = get_logger(__name__)


# --------------------------------------------------
# PATHS
# --------------------------------------------------

CONFIG_DIR = Path("config")

SETTINGS_FILE = CONFIG_DIR / "settings.yaml"
KEYWORDS_FILE = CONFIG_DIR / "keywords.yaml"


# --------------------------------------------------
# YAML LOADER
# --------------------------------------------------

def load_yaml(file_path: Path) -> dict:
    """
    Load a YAML file and return a dictionary.

    Args:
        file_path (Path)

    Returns:
        dict
    """

    try:

        if not file_path.exists():

            raise FileNotFoundError(
                f"File not found: {file_path}"
            )

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            data = yaml.safe_load(file)

            if data is None:
                return {}

            return data

    except Exception as error:

        logger.error(
            f"Failed to load {file_path}: {error}"
        )

        raise


# --------------------------------------------------
# SETTINGS
# --------------------------------------------------

def load_settings() -> dict:
    """
    Load settings.yaml
    """

    settings = load_yaml(
        SETTINGS_FILE
    )

    logger.info(
        "settings.yaml loaded successfully"
    )

    return settings


# --------------------------------------------------
# KEYWORDS
# --------------------------------------------------

def load_keywords() -> dict:
    """
    Load keywords.yaml
    """

    keywords = load_yaml(
        KEYWORDS_FILE
    )

    logger.info(
        "keywords.yaml loaded successfully"
    )

    return keywords


# --------------------------------------------------
# COMBINED CONFIG
# --------------------------------------------------

def load_all_configs() -> tuple:
    """
    Returns:
        (settings, keywords)
    """

    settings = load_settings()

    keywords = load_keywords()

    return settings, keywords


# --------------------------------------------------
# TEST
# --------------------------------------------------

if __name__ == "__main__":

    print("\nLoading settings...\n")

    settings = load_settings()

    print(settings)

    print("\nLoading keywords...\n")

    keywords = load_keywords()

    print(keywords)

    print("\nConfiguration loaded successfully.\n")

import yaml
from pathlib import Path
from typing import Dict, Any


def load_config(config_path: str = "config/config.yaml") -> Dict[str, Any]:
    """
    Load configuration from a YAML file.
    :param config_path: Path to the YAML configuration file.
    :return: Dictionary containing the configuration.
    """
    config_file = Path(config_path)
    if not config_file.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    with open(config_file, 'r', encoding='utf-8') as f:
        config: Dict[str, Any] = yaml.safe_load(f)

    return config




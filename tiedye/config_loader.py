"""
tiedye/core/config-loader.py

This module is responsible for loading and parsing the application's
config file (config.yaml).
"""

import yaml
from pathlib import Path

def load_config():

    """
    Finds, loads, and parses the config.yaml file.

    This function locates the configuration file relative to its own location, 
    ensuring that it works regardless of where the script is executed from.

    returns:
        dict: a dictionary containing the parsed config

    raises:
        FileNotFoundError: if the config.yaml file cannot be found
    """

    config_path = Path(__file__).parent / "config.yaml"

    if not config_path.exists():
        raise FileNotFoundError(
            f"Configuration file not found at: {config_path}. "
            "Please ensure 'config.yaml' exists in the 'tiedye' directory."
        )

    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    return config
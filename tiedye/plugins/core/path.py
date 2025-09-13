"""
tiedye/plugins/core/path.py

This module contains the core logic for managing path shortcuts.
"""

import typer
import yaml
from pathlib import Path
from typing import Dict, Any

from tiedye.config_loader import load_config

def _get_project_root() -> Path:
    """
    Finds the root directory of the TieDye-CLI project itself.
    """
    return Path(__file__).parent.parent.parent.parent

def _update_paths(
        op: str,
        name: str,
        path_str: str = None
):
    """
    A helper function to add or remove a path from the config.
    """
    config = load_config()
    paths = config.setdefault('paths', {})

    if op == "save":
        path = Path(path_str).expanduser().resolve()
        if not path.is_dir():
            typer.secho(f"Error: Path '{path}' is not a valid directory.", fg = typer.colors.RED)
            return
        paths[name] = str(path)
        typer.secho(f"✅ Saved shortcut '{name}' -> '{paths[name]}'", fg = typer.colors.GREEN)
    
    elif op == "remove" and name in paths:
        del paths[name]
        typer.echo(f"Removed shortcut '{name}'.")
    
    config_path = _get_project_root() / "tiedye" / "config.yaml"
    with open(config_path, 'w') as f:
        yaml.dump(config, f, indent = 2, sort_keys = False)

def save_path(
        name: str,
        path_str: str
):
    """
    Saves a new path shortcut
    """
    _update_paths("save", name, path_str)

def remove_path(
        name: str
):
    """
    Removes an existing path shortcut.
    """
    _update_paths("remove", name)

def list_paths(
        config: Dict[str, Any]
):
    """
    Lists all saved path shortcuts.
    """
    paths = config.get('paths', {})

    typer.secho("Saved Path Shortcuts:", bold = True)
    paths['home'] = str(_get_project_root())

    if not paths:
        typer.echo("No shortcuts have been saved yet.")
        return
    
    for name, path in sorted(paths.items()):
        typer.echo(f"  - {name}: {path}")

def get_path(
        config: Dict[str, Any],
        name: str
):
    """
    Prints a saved path to the console for shell processing.
    """
    # handle the special 'home' case to get the project root.
    if name == 'home':
        print(_get_project_root())
        return
    
    paths = config.get('paths', {})
    path_to_print = paths.get(name)

    if path_to_print:
        print(path_to_print)
    else:
        # Printing to stderr is important so the shell doesnt capture the error message as a valid path.
        typer.secho(f"Error: Shortcut '{name}' not found.", fg = typer.colors.RED, err = True)
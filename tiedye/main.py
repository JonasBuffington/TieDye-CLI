"""
tiedye/main.py

This module is the main entry point for the TieDye CLI app.
It uses Typer to create a clean command-line interface.
"""

import typer
from pathlib import Path
from .core.config_loader import load_config
from .core.sorter import sort_files

app = typer.Typer(
    help = "TieDye CLI: A tool for file sorting, project scaffolding, and workflow automation.",
    no_args_is_help = True
)

@app.command("sort")
def sort(
    source: str = typer.Argument(
        ..., # makes the argument required
        help="The path to the directory we want to sort."
    )
):
    """
    Sorts files in a directory based on the rules in config.yaml
    """
    print("Initializing sorter...")
    try:
        # --- 1. Load Configuration ---
        config = load_config()

        # --- 2. Call the Core Logic ---
        sort_files(config, source)

        print("\nSorting Complete!")

    except FileNotFoundError as e:
        typer.secho(f"ERROR: {e}", fg = typer.colors.RED)
    except Exception as e:
        typer.secho(f"An unexpected error occured: {e}", fg = typer.colors.RED)

@app.command("scaffold")
def scaffold():
    pass

if __name__ == "__main__":
    app()
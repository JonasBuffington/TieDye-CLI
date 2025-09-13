"""
tiedye/main.py

This module is the main entry point for the TieDye CLI app.
It uses Typer to create a clean command-line interface.
"""

import typer
import os
from pathlib import Path
from .config_loader import load_config
from .plugins.core.sorter import sort_files
from .plugins.core.scaffolder import save_template, create_project, list_templates, favorite_template, unfavorite_template

app = typer.Typer(
    help = "TieDye CLI: A tool for file sorting, project scaffolding, and workflow automation.",
    no_args_is_help = True
)

# --- Sort Command ---
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

    if source == ".":
        source = os.getcwd()

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

# --- Scaffolder Command Group ---
scaffold_app = typer.Typer(
    help = "Save and create new projects from templates."
)

app.add_typer(scaffold_app, name = "scaffold")

@scaffold_app.command("save")
def scaffold_save(
    source: str = typer.Argument(
        ...,
        help = "The path to the source directory to save as a template."
    ),
    name: str = typer.Argument(
        ...,
        help = "The name to save the template as."
    )
):
    """
    Saves a directory structure as a reusable template.
    """

    if source == ".":
        source = os.getcwd()

    try:
        config = load_config()
        save_template(config, name, source)
    except Exception as e:
        typer.secho(f"An unexpected error occurred: {e}", fg = typer.colors.RED)

@scaffold_app.command("new")
def scaffold_new(
    template: str = typer.Argument(
        ...,
        help = "The name of the template to use."
    ),
    name: str = typer.Argument(
        ...,
        help = "The name of the new project directory to create."
    )
):
    """
    Creates a new project from a saved template.
    """
    try:
        config = load_config()
        create_project(config,  template, name)
    except Exception as e:
        typer.secho(f"An unexpected error occurred: {e}", fg = typer.colors.RED)

@scaffold_app.command("list")
def scaffold_list():
    """
    Lists all avaliable project templates.
    """
    try:
        config = load_config()
        list_templates(config)
    except Exception as e:
        typer.secho(f"An unexpected error occurred: {e}", fg = typer.colors.RED)

@scaffold_app.command("favorite")
def scaffold_favorite(
    name: str = typer.Argument(
        ...,
        help = "The name of the template to mark as favorite."
    )
):
    """
    Marks a template as a favorite.
    """
    favorite_template(name)

@scaffold_app.command("unfavorite")
def scaffold_unfavorite(
    name: str = typer.Argument(
        ...,
        help = "The name of the template to unmark as favorite."
    )
):
    """
    Removes a template from the favorites list.
    """
    unfavorite_template(name)
    

if __name__ == "__main__":
    app()
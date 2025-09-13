"""
tiedye/core/scaffolder.py

This module contains the core logic for the project scaffolding feature.
"""

import shutil
import yaml
import typer

from pathlib import Path
from typing import Dict, Any
from tiedye.config_loader import load_config
from tiedye.logging import log_event

def save_template(
        config: Dict[str, Any],
        template_name: str,
        source_path_str: str
):
    """
    Saves a directory structure as a new template
    """
    scaffolder_config = config.get('scaffolder', {})
    templates_dir_str = scaffolder_config.get('templates_dir')

    if not templates_dir_str:
        print("Error: 'scaffolder.templates_dir' is not defined in config.yaml")
        return
    
    # --- Path Setup and Validation ---
    source_path = Path(source_path_str).expanduser()
    templates_dir = Path(templates_dir_str).expanduser()
    template_dest_path = templates_dir / template_name

    if not source_path.is_dir():
        print(f"Error: Source path '{source_path}' is not a valid directory.")
        return
    
    # we do not allow overwriting an existing template
    if template_dest_path.exists():
        print(f"Error: Template '{template_name}' already exists.")
        return
    
    # --- Template Creation ---
    try:
        # Ensure the main templates directory exists
        templates_dir.mkdir(parents = True, exist_ok = True)
        # shutil.copytree recursively copies an entire directory tree.
        shutil.copytree(source_path, template_dest_path)
        typer.secho(
            f"✅ Successfully saved template '{template_name}'.",
            fg = typer.colors.GREEN
        )
        typer.echo(f"   -> Location: {template_dest_path}")

        log_event(
            "template_saved",
            {
                "template_name": template_name,
                "source_path": str(source_path)
            }
        )
    except Exception as e:
        typer.secho(f"An error occured while saving the template: {e}", fg = typer.colors.RED)

def create_project(
    config: Dict[str, Any],
    template_name: str,
    project_name: str
):
    """
    Creates a new project directory from a saved template
    """
    scaffolder_config = config.get('scaffolder', {})
    templates_dir_str = scaffolder_config.get('templates_dir')
    dest_dir_str = scaffolder_config.get('default_project_destination', ".")

    if not templates_dir_str:
        typer.secho("Error: 'scaffolder.templates_dir' is not defined in config.yaml.", fg = typer.colors.RED)
        return
    
    # --- Path Setup and Validation ---
    templates_dir = Path(templates_dir_str).expanduser()
    template_source_path = templates_dir / template_name

    dest_dir = Path(dest_dir_str).expanduser()
    project_dest_path = dest_dir / project_name

    if not template_source_path.is_dir():
        typer.secho(f"Error: Template '{template_name}' not found.", fg = typer.colors.RED)
        return

    if project_dest_path.exists():
        typer.secho(f"Error: Directory '{project_name}' already exists at that location.", fg = typer.colors.RED)
        return
    
    # --- Project Creation ---
    try:
        # ensure the base destination directory exists before copying.
        dest_dir.mkdir(parents = True, exist_ok = True)
        shutil.copytree(template_source_path, project_dest_path)
        typer.secho(
            f"✅ Successfully created project '{project_name}' from template '{template_name}'.",
            fg = typer.colors.GREEN
        )
        typer.echo(f"   -> Location: {project_dest_path}")

        log_event(
            "project_created",
            {
                "project_name": project_name,
                "template_name": template_name,
                "destination_path": str(project_dest_path)
            }
        )
    except Exception as e:
        typer.secho(f"An error occured while creating the project: {e}", fg = typer.colors.RED)

def list_templates(
        config: Dict[str, Any]
):
    """
    Lists all currently saved project templates.
    """
    scaffolder_config = config.get('scaffolder', {})
    templates_dir_str = scaffolder_config.get('templates_dir')
    favorites = scaffolder_config.get('favorites', [])

    if not templates_dir_str:
        typer.secho("Error: 'scaffolder.templates_dir' is not defined in config.yaml.", fg = typer.colors.RED)
        return
    
    templates_dir = Path(templates_dir_str).expanduser()

    if not templates_dir.is_dir():
        typer.echo("Template directory not found. Save a template first!")
        return
    
    templates = [item.name for item in templates_dir.iterdir() if item.is_dir()]

    if not templates:
        typer.echo("No templates discovered in template directory.")

    fav_templates = sorted([t for t in templates if t in favorites])
    other_templates = sorted([t for t in templates if t not in favorites])

    if fav_templates:
        typer.secho("⭐ Favorite Templates:", bold = True, fg = typer.colors.YELLOW)
        for template_name in fav_templates:
            typer.secho(f"  - {template_name}", fg = typer.colors.YELLOW)

    if other_templates:
        typer.secho("Avaliable Templates:", bold = True)
        for template_name in other_templates:
            typer.echo(f"  - {template_name}")

def _update_favorites(
        op: str,
        template_name: str
):
    """
    A helper function to add or remove a favorite from the config.
    """
    config = load_config()
    scaffolder_config = config.setdefault('scaffolder', {})
    favorites = scaffolder_config.setdefault('favorites', [])

    if op == "add" and template_name not in favorites:
        favorites.append(template_name)
    elif op == "remove" and template_name in favorites:
        favorites.remove(template_name)
    
    config_path = Path(__file__).parent.parent.parent / "config.yaml"
    with open(config_path, 'w') as f:
        yaml.dump(config, f, indent = 2, sort_keys = False)

def favorite_template(
        template_name: str
):
    """
    Adds a template to the favorites list.
    """
    _update_favorites("add", template_name)
    typer.secho(f"⭐ Marked '{template_name}' as a favorite.", fg = typer.colors.YELLOW)

def unfavorite_template(
        template_name: str
):
    """
    Removes a template from the favorites list.
    """
    _update_favorites("remove", template_name)
    typer.echo(f"Unmarked '{template_name}' as a favorite.")
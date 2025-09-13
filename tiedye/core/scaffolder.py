"""
tiedye/core/scaffolder.py

This module contains the core logic for the project scaffolding feature.
"""

import shutil
from pathlib import Path
from typing import Dict, Any
import typer

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

    if not templates_dir_str:
        typer.secho("Error: 'scaffolder.templates_dir' is not defined in config.yaml.", fg = typer.colors.RED)
        return
    
    templates_dir = Path(templates_dir_str).expanduser()

    if not templates_dir.is_dir():
        typer.echo("Template directory not found. Save a template first!")
        return
    
    templates = [item.name for item in templates_dir.iterdir() if item.is_dir()]

    if not templates:
        typer.echo("No templates have been saved yet.")
        return
    
    typer.secho("Avaliable Templates:", bold = True)
    for template_name in sorted(templates):
        typer.echo(f"  - {template_name}")
"""
tiedye/core/scaffolder.py

This module contains the core logic for the project scaffolding feature.
"""

import shutil
from pathlib import Path
from typing import Dict, Any

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
        print(f"Successfully saved template '{template_name}'.")
    except Exception as e:
        print(f"An error occured while saving the template: {e}")

def create_project(
        config: Dict[str, Any],
        template_name: str,
        project_name: str
):
    """
    Creates a new project directory from a saved template.
    """
    scaffolder_config =  config.get('scaffolder', {})
    templates_dir_str = scaffolder_config.get('templates_dir')

    if not templates_dir_str:
        print("Error: 'scaffolder.templates_dir' is not defined in config.yaml.")
        return
    
    # --- Path Setup and Validation ---
    templates_dir = Path(templates_dir_str).expanduser()
    template_source_path = templates_dir / template_name
    project_dest_path = Path(project_name) # (creates path in current dir)

    if not template_source_path.is_dir():
        print(f"Error: Template '{template_name}' not found.")
        return
    
    if project_dest_path.exists():
        print(f"Error: Directory '{project_name}' already exists in this location.")
        return
    
    # --- Project Creation ---
    try:
        shutil.copytree(template_source_path, project_dest_path)
        print(f"Successfully created project '{project_name}' from template '{template_name}'.")
    except Exception as e:
        print(f"An error occured while creating the project: {e}")
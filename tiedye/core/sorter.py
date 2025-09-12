"""
tiedye/core/sorter.py

This module contains the core logic for the file sorting feature.
"""

import os
import shutil
from pathlib import Path
from typing import Dict, Any

# --[ MODIFICATION START]
# This is the fully refactored function using the two-pass approach
# to prevent the renaming bug, formatted to your specifications.
def sort_files(
  config: Dict[str, Any],
  source_dir_str: str
):
  """
  Scans a source directory and sorts files into target folders based on
  rules defined in the configuration.

  Args:
      config: The loaded configuration dictionary for the application.
      source_dir_str: The string path of the directory to scan.
  """

  # --- 1. Configuration and Path Setup ---
  sorter_config = config.get('sorter', {}) # (fall back to empty dictionary)
  if not sorter_config:
    print("Error: 'sorter' configuration is missing from config.yaml.")
    return
  
  source_dir = Path(source_dir_str).expanduser() # (convert '~' to home dir)

  if not source_dir.is_dir():
    print(f"Error: Source directory not found at '{source_dir}'")
    return
  
  rules = sorter_config.get('rules', [])
  collision_policy = sorter_config.get('collision_policy', 'skip')
  recursive = sorter_config.get('recursive_scan', True)
  ignore_patterns = sorter_config.get('ignore_patterns', [])

  print(f"Scanning '{source_dir}'...")

  # --- 2. Phase 1: Scan and Collect Files ---
  # First, we gather a list of all files to move. This prevents issues where
  # we modify the directory tree while we are still iterating over it.
  files_to_move = []
  
  # Path.glob('*') gets everything in the top-level directory.
  # Path.rglob('*') gets everything in the directory and all subdirectories.
  file_iterator = source_dir.rglob('*') if recursive else source_dir.glob('*')

  for item_path in file_iterator:
    if item_path.name in ignore_patterns:
      continue
    
    if item_path.is_file():
      files_to_move.append(item_path)

  # --- 3. Phase 2: Process and Move Files ---
  # Now, we iterate over our static list of files to perform the move operations.
  for item_path in files_to_move:
    matched_rule = None
    for rule in rules:
      if item_path.suffix.lower() in rule.get('extensions', []):
        matched_rule = rule
        break # (found a matching rule, no need to check others)
    
    if matched_rule:
      target_folder_str = matched_rule['target_folder']
      target_folder = Path(target_folder_str).expanduser()
      target_folder.mkdir(parents=True, exist_ok=True)

      destination_path = target_folder / item_path.name

      # Prevent trying to move a file that is already in its destination folder.
      if item_path.parent == target_folder:
        continue

      # --- Collision Handling ---
      if destination_path.exists():
        if collision_policy == 'skip':
          print(f"Skipping '{item_path.name}', destination exists.")
          continue
        elif collision_policy == 'overwrite':
          print(f"Overwriting '{destination_path}'.")
        elif collision_policy == 'rename':
          count = 1
          while destination_path.exists():
            new_name = f"{item_path.stem}({count}){item_path.suffix}"
            destination_path = target_folder / new_name
            count += 1
          print(f"Renaming to '{destination_path.name}'.")

      # --- The Move Operation ---
      try:
        shutil.move(item_path, destination_path)
        print(f"Moved: '{item_path.name}' -> '{target_folder}'")
      except PermissionError:
        print(f"Error: Permission denied to move '{item_path.name}'.")
      except Exception as e:
        print(f"An unexpected error occurred while moving '{item_path.name}': {e}")

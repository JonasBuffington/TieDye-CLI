"""
tiedye/plugins/git_workflows/git_plugin.py

This module contains the core logic for Git workflow automation.
"""

import subprocess
import typer
import shutil
from typing import List

def _run_command(command: List[str]):
    """
    A helper function to run a shell command and handle its output.

    This function is the heart of our interaction with external tools.
    It's designed to be safe and provide clear feedback.
    """
    typer.secho(f"🏃 Running: {' '.join(command)}", fg = typer.colors.YELLOW)

    # check = true: if the command returns a non-zero exit code, it will raise
    # a CallProcessError exception which will stop the script.
    try:
        result = subprocess.run(
            command,
            check = True,
            capture_output = True,
            text = True
        )
        if result.stdout:
            typer.echo(result.stdout)
        return True
    except FileNotFoundError:
        typer.secho(f"Error: Command '{command[0]}' not found. Is Git installed and in your PATH?", fg = typer.colors.RED)
        return False
    except subprocess.CalledProcessError as e:
        typer.secho(f"❌ Command failed with exit code {e.returncode}", fg = typer.colors.RED)
        typer.secho(e.stderr, fg = typer.colors.RED)
        return False
    
def start_feature(branch_name: str):
    """
    Automates the process of starting a new feature branch from an
    up-to-date main branch.
    """
    typer.secho(f"🚀 Starting new feature branch '{branch_name}'...", bold = True)

    commands = [
        ["git", "checkout", "main"],
        ["git", "pull", "origin", "main"],
        ["git", "checkout", "-b", branch_name],
        ["git", "push", "-u", "origin", branch_name]
    ]

    # Execute every command in sequence. If any command fails, the loop will
    # be broken because _run_command will return False.
    for cmd in commands:
        if not _run_command(cmd):
            typer.secho("\n🛑 Aborting feature start due to an error.", fg = typer.colors.RED)
            return
    
    typer.secho(f"\n✅ Successfully created and pushed feature branch '{branch_name}'.", fg = typer.colors.GREEN)
    typer.echo("You are now on the new branch and ready to start coding.")

def sync_work(commit_message: str):
    """
    Automates adding, committing, and pushing changes in the current branch.
    """
    typer.secho("🔃 Syncing work with remote repository...", bold = True)

    commands = [
        ["git", "add", "."],
        ["git", "commit", "-m", commit_message],
        ["git", "push"]
    ]
    
    for cmd in commands:
        if not _run_command(cmd):
            typer.secho("\n🛑 Aborting sync due to an error.", fg = typer.colors.RED)
            return
    
    typer.secho("\n✅ Successfully synced your changes.", fg = typer.colors.GREEN)

def finish_feature():
    """
    Opens a web browser to create a pull request for the current branch.
    Requires the GitHub CLI ('gh') to be installed.
    """
    typer.secho("🏁 Finishing feature and creating pull request...", bold = True)

    if not shutil.which('gh'):
        typer.secho("Error: GitHub CLI ('gh') not found.", fg = typer.colors.RED)
        typer.echo("Please install it to use this feature. See: https://cli.github.com/")
        return
    
    command = ["gh", "pr", "create", "--fill", "--web"]

    if not _run_command(command):
        typer.secho("\n🛑 Could not create pull request.", fg = typer.colors.RED)
        return
    
    typer.secho("\n✅ Your browser has been opened to create the pull request.", fg = typer.colors.GREEN)
from pipes import Template
import subprocess
from rich import print
import typer
import yaml
from astrodown.cli.install import PackageManager
import os
from pathlib import Path


def run_shell(cmd: str, verbose: bool = True, **kwargs):
    if verbose:
        prompt_success(cmd)
    try:
        _completed_process = subprocess.run(cmd, shell=True, check=True, **kwargs)
    except Exception as e:
        prompt_error(f"command `{cmd}` failed with reason: {e}")
        raise typer.Exit(1)


def colored_text(text: str, color: str = "green", bold: bool = True):
    begin_tag = f"[bold {color}]" if bold else f"[{color}]"
    end_tag = f"[/bold {color}]" if bold else f"[/{color}]"
    return f"{begin_tag}{text}{end_tag}"


def prompt_error(*text: any, bold: bool = True):
    print(colored_text("\[astrodown]:", color="red", bold=bold), *text)


def prompt_success(*text: any, bold: bool = True):
    print(colored_text("\[astrodown]:", color="green", bold=bold), *text)


def config_exists(config_file: str = "_astrodown.yml") -> bool:
    return os.path.exists(config_file)


def get_astrodown_config(config_file: str = "_astrodown.yml", verbose: bool = True):
    if not config_exists(config_file):
        if verbose:
            prompt_error(f"config file {config_file} not found")
        return None

    with open(config_file, "r") as f:
        try:
            return yaml.safe_load(f)
        except Exception as e:
            if verbose:
                prompt_error(
                    f"""config file {config_file} is not valid: {e}
                    using defaults instead"""
                )
            return None


def get_package_manager(
    config_file: str = "_astrodown.yml", verbose: bool = True
) -> PackageManager:
    config = get_astrodown_config(config_file, verbose=verbose)
    if config is not None:
        return config["node"]["package_manager"]
    else:
        if verbose:
            prompt_success(
                "using default package manager",
            )
        return PackageManager.npm

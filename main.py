import click
import pyperclip
import json
import os
import sys
import subprocess
from typing import Union


CONFIG_PATH = "C:\\alial\\asmcli\\config.json"
CONFIG_TEMPLATE = {
    "entries_files_paths": [
        ".\\entries.json"
    ],
    "entries_constants": {
        "%CWD%": "C:\\alial\\asmcli",
        "%BROWSER%": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
    },
}


@click.command()
@click.option("--entry_name", default=None, help="Name of entry in file 'entries.json'")
def main(entry_name: str) -> None:
    """Run alial server's entry by name"""
    # Get or create application config
    config = get_or_create_config()

    # Use default app directory
    # TODO: need to rewrite concept of CWD
    # TODO: maybe need installer program?
    cwd = config["entries_constants"]["%CWD%"]
    os.chdir(cwd)

    # Get server entry by name
    try:
        target_entry = get_entry_by_name(config["entries_files_paths"], entry_name)
    except KeyError as error:
        print(f"Error: {error}")
        sys.exit()

    # Copy text to clipboard
    pyperclip.copy(target_entry["c2c"])
    pyperclip.paste()

    # Change work directory
    os.chdir(target_entry["cwd"])

    # Start subtarget processes
    for subtarget in target_entry["subtargets"]:
        subcommand = replace_constants(subtarget, config["entries_constants"])
        start_target_process(subcommand)

    # Start target process
    command = replace_constants(target_entry["target"], config["entries_constants"])
    start_target_process(command)


def get_or_create_config():
    """Get application config, or create from template if it not exists"""
    is_config_exists = os.path.exists(CONFIG_PATH)
    if not is_config_exists:
        with open(CONFIG_PATH, "w", encoding="utf-8") as new_config_file:
            json.dump(CONFIG_TEMPLATE, new_config_file, ensure_ascii=True, indent=4)
        return CONFIG_TEMPLATE

    config_file_text = open(CONFIG_PATH, "r", encoding="utf-8").read()
    return json.loads(config_file_text)


def get_entry_by_name(
    entries_files_paths: list[str], entry_name: str,
) -> dict[str, Union[str, list[str]]]:
    """Get server's entry from file 'entries.json' by name"""
    target_entry = None
    for entry_file_path in entries_files_paths:
        entries_file_text = open(entry_file_path, "r", encoding="utf-8").read()
        entries = json.loads(entries_file_text)
        for entry in entries:
            if entry["name"] != entry_name:
                continue
            else:
                target_entry = entry

        if target_entry != None:
            return target_entry

    raise KeyError(
        f"Entry with name '{entry_name}' does not exists. Check 'config.json' file"
    )


def replace_constants(template: str, constants: dict[str, str]) -> str:
    """Replace defined constants from 'config.json'"""
    for constant_name in constants.keys():
        if constant_name in template:
            template = template.replace(constant_name, constants[constant_name])
    return template


def start_target_process(command: str) -> None:
    """Start target process by command with no wait for complete"""
    subprocess.Popen(
        command,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        shell=True,
        creationflags=subprocess.CREATE_NEW_CONSOLE,
    )


if __name__ == "__main__":
    main()

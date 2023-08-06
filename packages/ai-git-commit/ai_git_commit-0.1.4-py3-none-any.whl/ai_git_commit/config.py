import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import ini


def file_exists(path: str) -> bool:
    """Check is file exists or not"""
    return Path(path).is_file()


class KnownError(Exception):
    pass


def parse_assert(name: str, condition: bool, message: str):
    if not condition:
        raise KnownError(f"Invalid config property {name}: {message}")


def openai_key(key: Optional[str]) -> str:
    if not key:
        raise KnownError(
            "Please set your OpenAI API key via `ai_git_commit config set OPENAI_KEY=<your token>"
        )
    parse_assert("OPENAI_KEY", key.startswith("sk-"), 'Must start with "sk-"')
    return key


def locale(locale: Optional[str]) -> str:
    if not locale:
        return "en"
    parse_assert(
        "locale",
        bool(re.match("^[a-z-]+$", locale)),
        "Must be a valid locale (letters and dashes/underscores). You can consult the list of codes in: https://wikipedia.org/wiki/List_of_ISO_639-1_codes",
    )
    return locale


config_parsers = {"OPENAI_KEY": openai_key, "locale": locale}

ConfigKeys = Tuple[str, ...]


class RawConfig(Dict[str, Optional[str]]):
    pass


class ValidConfig(Dict[str, str]):
    pass


def read_config_file() -> RawConfig:
    config_path = (
        os.path.join(os.path.expanduser("~"), ".ai-git-commit")
        if not file_exists(".env")
        else os.path.join(os.getcwd(), ".env")
    )
    if not file_exists(config_path):
        return RawConfig()
    with open(config_path, "r") as f:
        raw_config = ini.parse(f.read())
        return RawConfig(raw_config)


def set_configs(key_values: Tuple[Tuple[str, str], ...]):
    config = read_config_file()
    for key, value in key_values:
        if key not in config_parsers:
            raise KnownError(f"Invalid config property: {key}")
        parsed = config_parsers[key](value)
        config[key] = parsed
    config_path = os.path.join(os.path.expanduser("~"), ".ai-git-commit")
    with open(config_path, "w") as f:
        f.write(ini.stringify(config))


def get_config(cli_config: Optional[RawConfig] = None) -> ValidConfig:
    config = read_config_file()
    parsed_config = {}
    for key, parser in config_parsers.items():
        value = (
            cli_config.get(key) if cli_config and key in cli_config else config.get(key)
        )
        parsed_config[key] = parser(value)
    return ValidConfig(parsed_config)


class ICommitMessage(Dict):
    id: int
    subject: str
    body: List[str | None]

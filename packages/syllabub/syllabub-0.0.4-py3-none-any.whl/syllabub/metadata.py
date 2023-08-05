# SPDX-License-Identifier: AGPL-3.0-or-later
# SPDX-FileCopyrightText: Copyright 2022 David Seaward and contributors

import logging
import os
import shutil
import sys
from importlib import resources

import chevron
import tomli

LOOKUP = {
    "DCO-1.1-git-signoff": {
        "text": "DCO 1.1 with a signed-off-by line",
        "command": "git commit --signoff",
    },
    "DCO-1.1-git-gpg-sign": {
        "text": "DCO 1.1 with a GPG signature",
        "command": "git commit --gpg-sign",
    },
    "contributor-covenant-2.1": "Contributor Covenant 2.1",
    "ubuntu-2.0": "Ubuntu Code of Conduct 2.0",
}


def bad_key_returns_default(value, default):
    """Decorated function will avoid KeyErrors and instead return a default value."""

    def decorator(function):
        def wrapper(*args, **kwargs):
            try:
                return function(*args, **kwargs)
            except KeyError:
                logging.error(f"{value} not found, using {default}")
                return default

        return wrapper

    return decorator


def tidy_file_text(text: str):
    while "\n\n\n" in text:
        text = text.replace("\n\n\n", "\n\n")
    return text.strip() + "\n"


def validate_environment():
    missing = []

    for executable in ["python3", "pdm", "git"]:
        if shutil.which(executable) is None:
            missing.append(executable)

    if not os.path.exists("pyproject.toml"):
        missing.append("pyproject.toml")

    if len(missing) != 0:
        missing_text = ", ".join(missing)
        sys.exit(f"Missing {missing_text}")


class Project:
    _pyproject = {}

    def load(self):
        with open("pyproject.toml", "rb") as f:
            self._pyproject = tomli.load(f)

    @staticmethod
    def clean():
        for path in ["COPYING", "LICENSE"]:
            try:
                os.remove(path)
            except OSError:
                pass  # skip missing files

    @property
    @bad_key_returns_default("Project name", "new-project")
    def short_name(self):
        return self._pyproject["project"]["name"]

    @property
    def full_title(self):
        try:
            return self._pyproject["tool"]["syllabub"]["project"]["title"]
        except KeyError:
            return self.short_name

    @property
    @bad_key_returns_default("Conduct", "contributor-covenant-2.1")
    def conduct_shortcode(self):
        return self._pyproject["tool"]["syllabub"]["project"]["conduct"]

    @property
    def conduct(self):
        try:
            return LOOKUP[self.conduct_shortcode]
        except KeyError:
            logging.error(f"Conduct '{self.conduct_shortcode}' not recognised.")
            return ""

    @property
    @bad_key_returns_default("Origin", "DCO-1.1-git-signoff")
    def origin_shortcode(self):
        return self._pyproject["tool"]["syllabub"]["project"]["origin"]

    @property
    def origin(self):
        try:
            return LOOKUP[self.origin_shortcode]["text"]
        except KeyError:
            logging.error(f"Origin '{self.conduct_shortcode}' not recognised.")
            return ""

    @property
    def origin_command(self):
        try:
            return LOOKUP[self.origin_shortcode]["command"]
        except KeyError:
            logging.error(f"Origin '{self.conduct_shortcode}' not recognised.")
            return ""

    @property
    @bad_key_returns_default("Copyright", "MISSING")
    def copyright(self):
        return self._pyproject["tool"]["syllabub"]["project"]["copyright"]

    @property
    @bad_key_returns_default("Bill of materials", "reuse sbom")
    def sbom_command(self):
        return self._pyproject["tool"]["syllabub"]["project"]["sbom"]

    @property
    @bad_key_returns_default("URL", "https://example.com")
    def url(self):
        return self._pyproject["tool"]["syllabub"]["project"]["url"]

    @property
    @bad_key_returns_default("License", "MISSING")
    def spdx_identifier(self):
        return self._pyproject["project"]["license"]["text"]

    @property
    @bad_key_returns_default("Description", "MISSING")
    def description(self):
        return self._pyproject["project"]["description"]

    def _populate_template(self, name):
        filename = name + ".mustache"
        with resources.open_text("syllabub.builtin", filename) as template:
            return tidy_file_text(chevron.render(template, self))

    def write_template(self, name, path=None):
        text = self._populate_template(name)

        if path is None:
            path = name
        else:
            path = os.path.join(path, name)

        with open(path, "w") as t:
            t.writelines(text)

    @staticmethod
    def copy_text(source, target):
        text = resources.read_text("syllabub.builtin", source)
        with open(target, "w") as t:
            t.write(text)

    @staticmethod
    def copy_binary(source, target):
        binary = resources.read_binary("syllabub.builtin", source)
        with open(target, "wb") as t:
            t.write(binary)

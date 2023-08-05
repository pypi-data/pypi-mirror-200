# SPDX-License-Identifier: AGPL-3.0-or-later
# SPDX-FileCopyrightText: Copyright 2022 David Seaward and contributors

import logging
import os.path
import shutil

from syllabub.metadata import Project, validate_environment


def version():
    return "0.0.2"


def invoke():
    # retrieve available data from pyproject.toml
    validate_environment()
    project = Project()
    project.load()
    project.clean()

    # write straightforward templates
    project.write_template("pyproject.toml")
    project.write_template("README.md")
    project.write_template(".gitignore")
    project.write_template("Makefile")
    project.write_template("pdm.lock.license")

    # create generic logo (if missing)
    if not os.path.exists("logo.png"):
        project.copy_binary("logo.png", "logo.png")
        project.copy_text("logo.png.license", "logo.png.license")

    # create minimal source folder (if missing)
    src_parent = f"src/{project.short_name}"
    init_file = f"{src_parent}/__init__.py"
    if not os.path.exists(init_file):
        os.makedirs(src_parent, exist_ok=True)
        with open(init_file, "w"):
            pass  # create empty file
        project.write_template("cli.py", src_parent)

    # create minimal test folder (if missing)
    tests_parent = "tests"
    if not os.path.exists(tests_parent):
        os.makedirs(tests_parent, exist_ok=True)
        project.write_template("test_cli.py", tests_parent)

    # populate CONDUCT file
    if project.conduct_shortcode == "contributor-covenant-2.1":
        project.copy_text("CONDUCT.COVENANT", "CONDUCT")
        project.copy_text("CONDUCT.COVENANT.license", "CONDUCT.license")
    elif project.conduct_shortcode == "ubuntu-2.0":
        project.copy_text("CONDUCT.UBUNTU", "CONDUCT")
        project.copy_text("CONDUCT.UBUNTU.license", "CONDUCT.license")
    else:
        logging.error("Conduct shortcode not recognised.")

    # populate COPYING file (if possible)
    license_path = f"LICENSES/{project.spdx_identifier}.txt"
    if os.path.exists(license_path):
        shutil.copyfile(license_path, "COPYING")
    else:
        logging.error(f"License {license_path} not found.")

    # write CONTRIBUTING files (actually the Developer Certificate of Origin)
    project.copy_text("CONTRIBUTING.DCO", "CONTRIBUTING")
    project.copy_text("CONTRIBUTING.DCO.license", "CONTRIBUTING.license")

    # write bespoke license for Developer Certificate of Origin
    os.makedirs("LICENSES", exist_ok=True)
    project.copy_text(
        "LicenseRef-DCO-1.1-license.txt", "LICENSES/LicenseRef-DCO-1.1-license.txt"
    )

    print("Conventional files generated. Please review diff before committing.")


if __name__ == "__main__":
    invoke()

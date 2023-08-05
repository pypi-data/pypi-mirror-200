# SPDX-License-Identifier: AGPL-3.0-or-later
# SPDX-FileCopyrightText: Copyright 2022 David Seaward and contributors

from syllabub.metadata import Project


def test_empty_project():
    p = Project()
    assert p._pyproject == {}

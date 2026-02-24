#!/usr/bin/env python3
"""
Setup script for theo_opt: Interactive figures for Lectures in Theoretical Optics

This setup.py reads configuration from pyproject.toml and passes it to setuptools.
"""

import tomllib
from pathlib import Path
from setuptools import setup

# Read pyproject.toml
pyproject_path = Path(__file__).parent / "pyproject.toml"
with open(pyproject_path, "rb") as f:
    pyproject_data = tomllib.load(f)

# Extract project metadata from pyproject.toml
project_config = pyproject_data.get("project", {})

# Prepare setup() arguments from pyproject.toml
setup_kwargs = {
    "packages": [],
}

# Install everything into bin (non-standard, but matches requested layout)
root_dir = Path(__file__).parent

script_paths = sorted(p for p in root_dir.glob("*.py") if p.name != "setup.py")
empy_paths = sorted(p for p in (root_dir / "EMpy").rglob("*.py"))
stuff_paths = sorted(p for p in (root_dir / "stuff").rglob("*.py"))

data_files = []
if script_paths:
    data_files.append(("bin", [str(p) for p in script_paths]))
if empy_paths:
    data_files.append(("bin/EMpy", [str(p) for p in empy_paths if p.parent.name == "EMpy"]))
    data_files.append(("bin/EMpy/modesolvers", [str(p) for p in empy_paths if p.parent.name == "modesolvers"]))
if stuff_paths:
    data_files.append(("bin/stuff", [str(p) for p in stuff_paths]))

if data_files:
    setup_kwargs["data_files"] = data_files

# Extract and format author information
authors = project_config.get("authors", [])
if authors:
    # Get first author as primary author
    primary_author = authors[0]
    setup_kwargs["author"] = primary_author.get("name")
    if primary_author.get("email"):
        setup_kwargs["author_email"] = primary_author.get("email")
    # Add secondary authors
    if len(authors) > 1:
        secondary_authors = authors[1:]
        setup_kwargs["author"] += ", " + ", ".join(a.get("name") for a in secondary_authors)
        if any(a.get("email") for a in secondary_authors):
            setup_kwargs["author_email"] += ", " + ", ".join(a.get("email") for a in secondary_authors if a.get("email"))

# Extract and format maintainer information
maintainers = project_config.get("maintainers", [])
if maintainers:
    # Get first maintainer as primary maintainer
    primary_maintainer = maintainers[0]
    setup_kwargs["maintainer"] = primary_maintainer.get("name")
    if primary_maintainer.get("email"):
        setup_kwargs["maintainer_email"] = primary_maintainer.get("email")
    # Add secondary maintainers
    if len(maintainers) > 1:
        secondary_maintainers = maintainers[1:]
        setup_kwargs["maintainer"] += ", " + ", ".join(m.get("name") for m in secondary_maintainers)
        if any(m.get("email") for m in secondary_maintainers):
            setup_kwargs["maintainer_email"] += ", " + ", ".join(m.get("email") for m in secondary_maintainers if m.get("email"))

# Extract URL (use Homepage if available)
urls = project_config.get("urls", {})
if urls.get("Homepage"):
    setup_kwargs["url"] = urls["Homepage"]

setup(**setup_kwargs)

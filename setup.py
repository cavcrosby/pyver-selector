"""The package installation file for the setuptools system."""
# Standard Library Imports

# Third Party Imports
from setuptools import setup

# Local Application Imports

# MONITOR(cavcrosby): these deps can be migrated back to pyproject.toml once
# Renovate supports a Python manager for pyproject.toml that can interpret said
# file according to PEP 621. This includes no longer needing to install
# setuptools. For reference on the GitHub issue tracking this:
# https://github.com/renovatebot/renovate/issues/10187
setup(
    install_requires=[
        "poetry ==1.2.2",
    ],
    extras_require={
        "dev": [
            "black ==22.10.0",
            "flake8 ==6.0.0",
            "flake8-docstrings ==1.6.0",
            "yamllint ==1.28.0",
        ],
    },
)

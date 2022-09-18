#!/usr/bin/env python3
"""Determines the greatest Python version to use for a project."""
# Standard Library Imports
import argparse
import logging
import logging.config
import pathlib
import subprocess
import sys

# Third Party Imports
from poetry.core.semver.version import Version
from poetry.core.version.exceptions import InvalidVersion
from poetry.factory import Factory

# Local Application Imports

# constants
_arg_parser = argparse.ArgumentParser(
    description=__doc__,
    allow_abbrev=False,
)

# option labels
VERBOSE_SHORT_OPTION = "v"
VERBOSE_LONG_OPTION = "verbose"

logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "console": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"  # noqa: E501
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "console",
            },
        },
        "loggers": {
            "": {"level": "INFO", "handlers": ["console"]},
        },
    }
)
_logger = logging.getLogger(__name__)


def retrieve_cmd_args():
    """Retrieve command arguments from the command line.

    Returns
    -------
    Namespace
        An object that holds attributes pulled from the command line.

    Raises
    ------
    SystemExit
        If user input is not considered valid when parsing arguments.

    """
    _arg_parser.add_argument(
        f"-{VERBOSE_SHORT_OPTION}",
        f"--{VERBOSE_LONG_OPTION}",
        action="store_true",
        help="increase verbosity",
    )

    args = vars(_arg_parser.parse_args())
    return args


def pyver_selector(args):
    """Start the main program execution."""
    python_vers = subprocess.run(
        ("pyenv", "install", "--list"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        check=True,
    )
    if args[VERBOSE_LONG_OPTION]:
        _logger.setLevel(logging.DEBUG)

    # I should never, ever, use this hypothetical Python 1
    greatest_python_ver = Version.parse("1")
    project_pkg = Factory().create_poetry(pathlib.Path(".")).package
    for python_ver in python_vers.stdout.split():
        try:
            parsed_python_ver = Version.parse(python_ver.strip())
            _logger.debug(f"{str(parsed_python_ver)}")
            _logger.debug(
                "parsed_python_ver.is_no_suffix_release(): "
                f"{parsed_python_ver.is_no_suffix_release()}"
            )
            _logger.debug(
                "project_pkg.python_constraint.allows(parsed_python_ver): "
                f"{project_pkg.python_constraint.allows(parsed_python_ver)}"
            )
            _logger.debug(
                "greatest_python_ver < parsed_python_ver: "
                f"{greatest_python_ver < parsed_python_ver}"
            )
            if (
                parsed_python_ver.is_no_suffix_release()
                and project_pkg.python_constraint.allows(parsed_python_ver)
                and greatest_python_ver < parsed_python_ver
            ):
                greatest_python_ver = parsed_python_ver
        except InvalidVersion:
            # will trip up on other variants of Python (e.g anaconda-1.7.0)
            continue

    return greatest_python_ver


def main():
    """Entry point to start the main program execution."""
    args = retrieve_cmd_args()
    print(pyver_selector(args))
    sys.exit(0)


if __name__ == "__main__":
    main()

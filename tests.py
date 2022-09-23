"""Tests most Makefile targets."""
# Standard Library Imports
import os
import sys
import unittest

# Third Party Imports
from poetry.core.semver.exceptions import ParseConstraintError

# Local Application Imports
from pyver_selector import pyver_selector

# constants and other program configurations
RUNNING_WORKINGDIR = os.getcwd()


class TestReturnExactVersion(unittest.TestCase):
    """Run test to return exact version."""

    def setUp(self):
        """Set up environment before running test method(s)."""
        os.chdir("./tests/return-exact-version")

    def tearDown(self):
        """Tear down environment after running test method(s)."""
        os.chdir(RUNNING_WORKINGDIR)

    def test_return_exact_version(self):
        """Run test to return exact version."""
        self.assertEqual(str(pyver_selector({"verbose": False})), "3.9.14")


class TestReturnExactVersionMakefile(unittest.TestCase):
    """Run test to return exact version based on Makefile constraint."""

    def setUp(self):
        """Set up environment before running test method(s)."""
        os.chdir("./tests/return-exact-version-makefile")

    def tearDown(self):
        """Tear down environment after running test method(s)."""
        os.chdir(RUNNING_WORKINGDIR)

    def test_return_exact_version_makefile(self):
        """Run test to return exact version based on Makefile constraint."""
        self.assertEqual(str(pyver_selector({"verbose": False})), "3.10.7")


class TestInvalidConstraint(unittest.TestCase):
    """Run test to throw exception for invalid python constraint."""

    def setUp(self):
        """Set up environment before running test method(s)."""
        os.chdir("./tests/invalid-constraint")

    def tearDown(self):
        """Tear down environment after running test method(s)."""
        os.chdir(RUNNING_WORKINGDIR)

    def test_invalid_constraint(self):
        """Run test to throw exception for invalid python constraint."""
        try:
            pyver_selector({"verbose": False})
        except Exception as e:
            self.assertIsInstance(e, ParseConstraintError)


if __name__ == "__main__":
    unittest.main()
    sys.exit(0)

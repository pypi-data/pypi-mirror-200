#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Test script.

This script executes the unit tests for the package.

"""

from contextlib import contextmanager
from json import load, dumps
from pathlib import Path
from shutil import copytree
from subprocess import CalledProcessError, run
from sys import stderr
from tempfile import TemporaryDirectory, TemporaryFile
from unittest import main, TestCase

from pashword.core import pash, sets, book


dir_tests = Path(__file__).parent
dir_material = dir_tests/'material'

with open(dir_tests/'references.json', 'r', encoding='utf-8') as ref_file:
    ref = load(ref_file)


def runcheck(command):
    """Run a command and check the exit code.

    If the exit code of the executed command is different from 0, a
    RuntimeError containing the output of the command is raised.

    Parameters
    ----------
    command : str
        Command to be runned.

    Raises
    ------
    RuntimeError
        If the command exited with an error code.

    """
    with TemporaryFile() as file:
        try:
            run(command, shell=True, check=True, stdout=file, stderr=file)
        except CalledProcessError as error:
            file.seek(0)
            raise RuntimeError(file.read().decode()) from error


@contextmanager
def temporary(directory='.'):
    """Return a temporary clone of the target test directory.

    Parameters
    ----------
    directory : str
        Name of the directory to clone from material.

    Returns
    -------
    str
        Path to the cloned target directory.

    """
    temp_dir = TemporaryDirectory()
    path = Path(temp_dir.name)
    copytree(dir_material/directory, path, dirs_exist_ok=True)
    try:
        yield path
    finally:
        temp_dir.cleanup()


def display(data):
    """Print data in JSON format.

    Parameters
    ----------
    data : dict or list
        Data to be displayed.

    """
    print("\n"+dumps(data, indent=4), file=stderr)


class TestCore(TestCase):
    """Class for testing core subpackage."""

    def test_metacharacters(self):
        """Test metacharacter set retrieval."""
        for metacharacter, charaters in ref['sets'].items():
            self.assertEqual(charaters, sets.get(metacharacter))

    def test_combinations(self):
        """Test combination number."""
        for form, number in ref['combinations'].items():
            self.assertEqual(number, sets.combinations(form))

    def test_hexdigest(self):
        """Test hash value."""
        for key, salt, value in ref['hexdigest']:
            self.assertEqual(value, pash.hexdigest(key, salt))

    def test_password(self):
        """Test pashword."""
        for key, salt, form, value in ref['password']:
            self.assertEqual(value, pash.password(key, salt, form))

    def test_same(self):
        """Test key match."""
        with temporary('logins') as material:
            key = 'key'
            path = material/'validate.json'
            pash.save(key, path)
            self.assertTrue(pash.same(key, path))

    def test_load(self):
        """Test password book loading."""
        with temporary('logins') as material:
            data = book.load(material/'user.conf')
        self.assertTrue(ref['loading'], data)

    def test_matching(self):
        """Test name matching."""
        data = book.matching(ref['matching']['input'], '*1')
        self.assertEqual(ref['matching']['output'], data)

    def test_decode(self):
        """Test decoding."""
        with temporary('logins') as material:
            data = book.load(material/'user.conf')
            decoded = book.decode(data, ref['decoding']['key'])
            self.assertEqual(ref['decoding']['output'], decoded)


class TestCommandLineInterface(TestCase):
    """Class for testing the CLI."""

    def test_help(self):
        """Test help option."""
        runcheck("pashword --help")
        runcheck("pashword read --help")
        runcheck("pashword sort --help")

    def test_features(self):
        """Test all features."""
        with temporary('logins') as material:
            conf = material/'user.conf'
            json = material/'user.json'
            prompt = dir_material/'inputs'/'read.txt'
            runcheck(f"pashword read {conf} < {prompt}")
            runcheck(f"pashword read {conf} --hash {json} < {prompt}")
            runcheck(f"pashword read {conf} --hash {json} < {prompt}")
            runcheck(f"pashword sort {conf} < {prompt}")
            runcheck(f"pashword read {conf} < {prompt}")


if __name__ == '__main__':
    main(buffer=True)

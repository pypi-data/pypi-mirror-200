#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Test script.

This script executes the unit tests for the package.

"""

from contextlib import contextmanager
from pathlib import Path
from shutil import copytree
from subprocess import DEVNULL, run
from tempfile import TemporaryDirectory
from unittest import main, TestCase

from pashword.core import sets, hash, book
from pashword.main import sort


dir_tests = Path(__file__).parent
dir_target = dir_tests/'target'
dir_inputs = dir_tests/'inputs'


def runcheck(command):
    """Run a command and check the exit code.

    Parameters
    ----------
    command : str
        Command to be runned.

    Raises
    ------
    CalledProcessError
        If the command exited with an error code.

    """
    run(command, shell=True, check=True, stdout=DEVNULL)


@contextmanager
def temporary_target():
    """Return a temporary clone of the target test directory.

    Returns
    -------
    str
        Path to the cloned target directory.

    """
    temp_dir = TemporaryDirectory()
    path = Path(temp_dir.name)
    copytree(dir_target, path, dirs_exist_ok=True)
    try:
        yield path
    finally:
        temp_dir.cleanup()


class TestCore(TestCase):

    def test_metacharacters(self):
        stored = 'ABCDEFGHJKLMNPRSTUVWXYZ'
        self.assertEqual(stored, sets.get('u'))
        stored = 'ABCDEFGHJKLMNPRSTUVWXYZ23456789abcdefghijkmnopqrstuvwxyz'
        self.assertEqual(stored, sets.get('*'))
        self.assertEqual('-', sets.get('-'))

    def test_combinations(self):
        self.assertEqual(1, sets.combinations('a'))
        self.assertEqual(1, sets.combinations('ab'))
        self.assertEqual(8, sets.combinations('d'))
        self.assertEqual(8**2, sets.combinations('dd'))

    def test_hexdigest(self):
        stored = '8342d2719fa5821c254d6484cfc0716fc1e01b8e290ea575187762fc428d14bd293db60510a7d17e09a714d8aec70c6f5e430a966c499e3d1ad3dede7feb2e32'
        self.assertEqual(stored, hash.hexdigest('key', 'salt'))

    def test_password(self):
        stored = '5YhNDd77dZ8us6du'
        self.assertEqual(stored, hash.password('key', 'salt', '*'*16))

    def test_same(self):
        with temporary_target() as target:
            key = 'key'
            path = target/'validate.json'
            hash.save(key, path)
            self.assertTrue(hash.same(key, path))

    def test_load(self):
        with temporary_target() as target:
            data = book.load(target/'user.conf')

    def test_filter(self):
        data = {'n1': {'form': '1'}, 'n2': {'form': '2'}}
        stored = {'n1': {'form': '1'}}
        self.assertEqual(stored, book.matching(data, '*1'))

    def test_decode(self):
        with temporary_target() as target:
            data = book.load(target/'user.conf')
            decoded = book.decode(data, "secret key")
            stored = 'B2nG-hLAe-5Pom'
            self.assertEqual(stored, decoded['entity-one.org']['password'])


class TestMain(TestCase):

    def test_sort(self):
        with temporary_target() as target:
            sort.main(target/'user.conf')


class TestCommandLineInterface(TestCase):

    def test_help(self):
        runcheck("pashword --help")
        runcheck("pashword read --help")
        runcheck("pashword sort --help")

    def test_features(self):
        with temporary_target() as target:
            book = target/'user.conf'
            hash = target/'user.json'
            runcheck(f"pashword read {book} < {dir_inputs/'read.txt'}")
            runcheck(f"pashword read {book} --hash {hash} < {dir_inputs/'read.txt'}")
            runcheck(f"pashword read {book} --hash {hash} < {dir_inputs/'read.txt'}")
            runcheck(f"pashword sort {book} < {dir_inputs/'read.txt'}")
            runcheck(f"pashword read {book} < {dir_inputs/'read.txt'}")


if __name__ == '__main__':
    main(buffer=True)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Test script.

This script executes the unit tests for the package.

"""

from contextlib import contextmanager, redirect_stdout
from json import load, dumps
from pathlib import Path
from shutil import copytree, rmtree
from subprocess import CalledProcessError, run
from sys import stderr
from tempfile import TemporaryDirectory, TemporaryFile
from unittest import main, TestCase

from treecker.core import comparison, naming, snapshot, tree
from treecker.main import commit, init, issues, status


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

    def test_file_hash(self):
        """Test file hash value."""
        data = tree.file_hash(dir_material/'tracked'/'file.txt')
        self.assertEqual(ref['file_hash'], data)

    def test_file_size(self):
        """Test file size retrieval."""
        size = tree.file_size(dir_material/'tracked'/'file.txt')
        self.assertEqual(ref['file_size'], size)

    def test_node_no_hash(self):
        """Test tree without hash."""
        node = tree.tree_node(dir_material/'tracked', [], False)
        self.assertDictEqual(ref['test_node_no_hash'], node)

    def test_node_hash(self):
        """Test tree without hash."""
        node = tree.tree_node(dir_material/'tracked', ['file*'], True)
        self.assertDictEqual(ref['test_node_hash'], node)

    def test_items(self):
        """Test tree flattening."""
        node = tree.tree_node(dir_material/'tracked', [], False)
        items = tree.tree_items(node)
        self.assertListEqual(ref['flattened'], items)

    def test_snapshot_serialization(self):
        """Test serialization."""
        for hashing in (True, False):
            with self.subTest(hash=hashing):
                with temporary('tracked') as tracked:
                    snap1 = snapshot.take(tracked, hashing)
                    snapshot.save(tracked, snap1)
                    snap2 = snapshot.load(tracked)
                    self.assertDictEqual(snap1, snap2)

    def test_naming_issues(self):
        """Test naming issues."""
        for node, length in ref['issues']:
            data = naming.get_issues(node)
            self.assertEqual(len(data), length)

    def test_differences(self):
        """Test identification of differences."""
        for node1, node2, hashing, length in ref['differences']:
            data = comparison.get_differences(node1, node2, hashing)
            self.assertEqual(length, len(data))


class TestMain(TestCase):
    """Class for testing main subpackage."""

    def test_init(self):
        """Test init feature."""
        for hashing in (True, False):
            with self.subTest(hashing=hashing):
                with temporary('tracked') as tracked:
                    with redirect_stdout(None):
                        init.main(dir=tracked, hash=hashing)
                        self.assertRaises(
                            Exception,
                            init.main,
                            dir=tracked,
                            hash=hashing
                        )

    def test_status(self):
        """Test status feature."""
        with temporary('tracked') as tracked:
            with redirect_stdout(None):
                init.main(dir=tracked, hash=True)
                for hashing in (True, False):
                    with self.subTest(hashing=hashing):
                        status.main(dir=tracked, hash=hashing)

    def test_commit(self):
        """Test commit feature."""
        with temporary('tracked') as tracked:
            with redirect_stdout(None):
                init.main(dir=tracked, hash=False)
                commit.main(dir=tracked, hash=False)

    def test_issues(self):
        """Test issues feature."""
        with temporary('tracked') as tracked:
            with redirect_stdout(None):
                issues.main(dir=tracked)


class TestCommandLineInterface(TestCase):
    """Class for testing the CLI."""

    def test_help(self):
        """Test help option."""
        runcheck("treecker --help")
        runcheck("treecker init --help")
        runcheck("treecker status --help")
        runcheck("treecker commit --help")
        runcheck("treecker issues --help")

    def test_features(self):
        """Test all features."""
        with temporary('tracked') as tracked:
            runcheck(f"treecker init --hash --dir {tracked}")
            runcheck(f"treecker status --hash --dir {tracked}")
            rmtree(tracked/'subdir')
            prompt = dir_material/'inputs'/'commit-n.txt'
            runcheck(f"treecker commit --dir {tracked} < {prompt}")
            runcheck(f"treecker commit --dir {tracked} < {prompt}")
            runcheck(f"treecker issues --dir {tracked}")


if __name__ == '__main__':
    main()

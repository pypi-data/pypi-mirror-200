#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Test script.

This script executes the unit tests for the package.

"""

from contextlib import contextmanager, redirect_stdout
from pathlib import Path
from shutil import copytree, rmtree
from subprocess import DEVNULL, run
from tempfile import TemporaryDirectory
from unittest import main, TestCase

from treecker.core import comparison, naming, snapshot, tree
from treecker.main import commit, init, issues, status


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

    def test_file_hash(self):
        with temporary_target() as target:
            hash = tree.file_hash(target/'file.txt')
            self.assertEqual('6c636eca9b4df0f8244ed6e9ad37517c', hash)

    def test_file_size(self):
        with temporary_target() as target:
            size = tree.file_size(target/'file.txt')
            self.assertEqual(52, size)

    def test_node_no_hash(self):
        with temporary_target() as target:
            node = tree.tree_node(target, [], False)
            stored = {
                'file.txt': [52],
                'subdir': {
                    'setup.sh': [49],
                },
            }
            self.assertDictEqual(stored, node)

    def test_node_hash(self):
        with temporary_target() as target:
            node = tree.tree_node(target, ['file*'], True)
            stored = {
                'subdir': {
                    'setup.sh': [49, '6f8693e997b0a35a91962bac1ad0eb72'],
                },
            }
            self.assertDictEqual(stored, node)

    def test_items(self):
        with temporary_target() as target:
            node = tree.tree_node(target, [], False)
            items = tree.tree_items(node)
            stored = [(['file.txt'], [52]), (['subdir', 'setup.sh'], [49])]
            self.assertListEqual(stored, items)

    def test_snapshot_serialization(self):
        for hash in (True, False):
            with self.subTest(hash=hash):
                with temporary_target() as target:
                    snap1 = snapshot.take(target, hash)
                    snapshot.save(target, snap1)
                    snap2 = snapshot.load(target)
                    self.assertDictEqual(snap1, snap2)

    def test_naming_issues(self):
        issues = naming.get_issues({'UP': [10]})
        self.assertEqual(len(issues), 1)
        issues = naming.get_issues({'spa ce': [2]})
        self.assertEqual(len(issues), 1)
        issues = naming.get_issues({'a.tar.gz': [2]})
        self.assertEqual(len(issues), 0)

    def test_differences(self):
        node1 = {'a': {'b': [2, 'h1']}, 'c': {'d': [2, 'h2']}}
        node2 = {'a': {'b': [2, 'h1']}, 'c': {'d': [2, 'h2']}}
        node3 = {'a': {'b': [2, 'h1']}}
        for hash in (True, False):
            with self.subTest(hash=hash):
                diffs = comparison.get_differences(node1, node2, hash)
                self.assertEqual(0, len(diffs))
                diffs = comparison.get_differences(node1, node3, hash)
                self.assertEqual(1, len(diffs))


class TestMain(TestCase):

    def test_init(self):
        for hash in (True, False):
            with self.subTest(hash=hash):
                with temporary_target() as target:
                    with redirect_stdout(None):
                        init.main(dir=target, hash=hash)
                        self.assertRaises(Exception, init.main, dir=target, hash=hash)

    def test_status(self):
        with temporary_target() as target:
            with redirect_stdout(None):
                init.main(dir=target, hash=True)
                for hash in (True, False):
                    with self.subTest(hash=hash):
                            status.main(dir=target, hash=hash)

    def test_commit(self):
        with temporary_target() as target:
            with redirect_stdout(None):
                init.main(dir=target, hash=False)
                commit.main(dir=target, hash=False)

    def test_issues(self):
        with temporary_target() as target:
            with redirect_stdout(None):
                issues.main(dir=target)


class TestCommandLineInterface(TestCase):

    def test_help(self):
        runcheck("treecker --help")
        runcheck("treecker init --help")
        runcheck("treecker status --help")
        runcheck("treecker commit --help")
        runcheck("treecker issues --help")

    def test_features(self):
        with temporary_target() as target:
            runcheck(f"treecker init --hash --dir {target}")
            runcheck(f"treecker status --hash --dir {target}")
            rmtree(target/'subdir')
            runcheck(f"treecker commit --dir {target} < {dir_inputs/'commit-n.txt'}")
            runcheck(f"treecker commit --dir {target} < {dir_inputs/'commit-y.txt'}")
            runcheck(f"treecker issues --dir {target}")


if __name__ == '__main__':
    main()

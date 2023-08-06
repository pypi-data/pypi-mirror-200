# -*- coding: utf-8 -*-

"""Snapshot module.

This module implements the functionalities related to the snapshots.

"""

from datetime import datetime, timezone
from json import dumps as serialize, load as deserialize
from logging import getLogger
from pathlib import Path

from treecker import config
from treecker._version import __version_tuple__
from treecker.core.tree import tree_node


logger = getLogger(__name__)


def take(directory, hashing):
    """Return a snapshot of the directory.

    Parameters
    ----------
    directory : str
        Path to the tracked directory.
    hashing : bool
        Add hash value to file signatures.

    Returns
    -------
    dict
        Directory snapshot data.

    """
    logger.debug("taking snapshot of %s", directory)
    file = config.get(__name__, 'snap_file')
    ignore = config.get(__name__, 'ignore_patterns').split()
    ignore.append(file)
    date = datetime.now(timezone.utc).isoformat(timespec="seconds")
    node = tree_node(directory, ignore, hashing)
    snapshot = {
        'version': list(__version_tuple__),
        'date': date,
        'hash': hashing,
        'tree': node,
    }
    return snapshot


def save(directory, snapshot):
    """Save the snapshot in the directory.

    Parameters
    ----------
    directory : str
        Path to the tracked directory.
    snapshot : dict
        Directory snapshot to be saved.

    """
    logger.debug("saving snapshot of %s", directory)
    path = Path(directory) / config.get(__name__, 'snap_file')
    with open(path, "w", encoding='utf-8') as file:
        file.write(serialize(snapshot))


def load(directory):
    """Load the last snapshot of the directory.

    Parameters
    ----------
    directory : str
        Path to the tracked directory.

    Returns
    -------
    dict
        Last snapshot of the directory.

    """
    logger.debug("loading snapshot of %s", directory)
    path = Path(directory) / config.get(__name__, 'snap_file')
    with open(path, "r", encoding='utf-8') as file:
        snapshot = deserialize(file)
    return snapshot


def initialized(directory):
    """Check if the directory is tracked.

    Parameters
    ----------
    directory : str
        Path to the directory.

    Returns
    -------
    bool
        True if the directory is tracked.

    """
    path = Path(directory) / config.get(__name__, 'snap_file')
    return path.is_file()

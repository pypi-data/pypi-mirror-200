# -*- coding: utf-8 -*-

"""Comparison module.

This module implements the comparison between two trees.

"""

from logging import getLogger
from pathlib import Path

from treecker import config
from treecker.core.colors import colorize


logger = getLogger(__name__)


def get_differences(old, new, hashing, path=None):
    """Return a list of the differences between two tree objects.

    Parameters
    ----------
    old : dict
        Old directory node.
    new : dict
        New directory node.
    hashing : bool
        Compare file hash values.
    path : list
        Initial path.

    Returns
    -------
    list
        Differences betwen the two nodes.

    """
    logger.debug("getting differences at %s", path)
    if path is None:
        path = []
    listing = []
    if isinstance(old, dict) and isinstance(new, dict):
        for node in old:
            if node in new:
                listing += get_differences(
                    old[node],
                    new[node],
                    hashing,
                    path+[node],
                )
            else:
                listing.append({'type': 'removed', 'path': path+[node]})
        for node in new:
            if node not in old:
                listing.append({'type': 'added', 'path': path+[node]})
    elif isinstance(old, dict) or isinstance(new, dict):
        listing.append({'type': 'removed', 'path': path})
        listing.append({'type': 'added', 'path': path})
    elif (old[0] != new[0]) or hashing and (old[1] != new[1]):
        listing.append({'type': 'edited', 'path': path})
    return listing


def differences_log(differences):
    """Return a printable log of the differences.

    Parameters
    ----------
    differences : list
        List of differences.

    Returns
    -------
    str
        Differences log.

    """
    logger.debug("creating difference log")
    color, symbol = {}, {}
    for name, value in config[__name__].items():
        if name.startswith('color_'):
            color[name[6:]] = value
        elif name.startswith('symbol_'):
            symbol[name[7:]] = value
    lines = []
    for diff in differences:
        path = Path(*diff['path'])
        line = colorize(f"{symbol[diff['type']]} {path}", color[diff['type']])
        lines.append(line)
    if len(differences) == 0:
        lines.append("no change found")
    log = "\n".join(lines)
    return log

# -*- coding: utf-8 -*-

"""Naming module.

This module implements the naming check.

"""

from fnmatch import fnmatch
from logging import getLogger
from pathlib import Path
from re import fullmatch

from treecker import config
from treecker.core.colors import colorize


logger = getLogger(__name__)


def get_issues(tree, path=None):
    """Return a list of the naming issues.

    Parameters
    ----------
    tree : dict
        Directory node.
    path : list
        Initial path.

    Returns
    -------
    list
        Issues.

    """
    logger.debug("getting issues at %s", path)
    if path is None:
        path = []
    listing = []
    pattern = config.get(__name__, 'match_pattern')
    ignore = config.get(__name__, 'ignore_patterns').split()
    if isinstance(tree, dict):
        for name, child in tree.items():
            if fullmatch(pattern, name) is None:
                if not any(fnmatch(name, pattern) for pattern in ignore):
                    text = f"{name} does not match {pattern}"
                    listing.append({'text': text, 'path': path+[name]})
            listing += get_issues(child, path+[name])
    return listing


def issues_log(issues):
    """Return a printable log of the naming issues.

    Parameters
    ----------
    issues : list
        Issues.

    Returns
    -------
    str
        Issues log.

    """
    logger.debug("creating issue log")
    lines = []
    color = config.get(__name__, 'color_issue')
    for issue in issues:
        path = Path(*issue['path'])
        text = issue['text']
        line = f'{path} {colorize(text, color)}'
        lines.append(line)
    if len(issues) == 0:
        lines.append("no issue found")
    log = "\n".join(lines)
    return log

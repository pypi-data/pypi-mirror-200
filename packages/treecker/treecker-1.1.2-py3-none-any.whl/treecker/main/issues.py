# -*- coding: utf-8 -*-

"""Issues feature.

This module implements the feature that allows to check the file and
directory names.

"""

from logging import getLogger
from os.path import join

from treecker import config
from treecker.core.naming import get_issues, issues_log
from treecker.core.snapshot import take


logger = getLogger(__name__)


def setup(parser):
    """Configure the parser for the module.

    Parameters
    ----------
    parser : ArgumentParser
        Parser dedicated to the module.

    """
    logger.debug("defining command-line arguments")
    parser.set_defaults(
        func=main,
    )
    parser.add_argument(
        '--dir',
        help="path to the tracked directory",
        type=str,
    )


def main(**kwargs):
    """Display incorrectly named files and directories.

    Keyword Arguments
    -----------------
    dir : str
        Path to the tracked directory.

    """
    logger.debug("retrieving parameters")
    kwargs.setdefault('dir', config.get(__name__, 'dir'))

    logger.debug("loading tree structure")
    config.read(join(kwargs['dir'], config.get('DEFAULT', 'conf_file')))
    snap = take(kwargs['dir'], False)
    tree = snap['tree']

    logger.debug("displaying recommendations")
    listing = get_issues(tree)
    log = issues_log(listing)
    print(log)

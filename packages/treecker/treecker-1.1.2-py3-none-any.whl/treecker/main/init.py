# -*- coding: utf-8 -*-

"""Init feature.

This module implements the feature that allows to initialize a tree
tracker in a directory.

"""

from logging import getLogger
from os.path import join

from treecker import config
from treecker.core.snapshot import initialized, save, take


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
    parser.add_argument(
        '--hash',
        action='store_true',
        help="add hash value to file signatures",
    )


def main(**kwargs):
    """Create the first snapshot of a directory.

    Keyword Arguments
    -----------------
    dir : str
        Path to the tracked directory.
    hash : bool
        Add hash value to file signatures.

    """
    logger.debug("retrieving parameters")
    kwargs.setdefault('dir', config.get(__name__, 'dir'))
    kwargs.setdefault('hash', config.getboolean(__name__, 'hash'))

    logger.debug("initializing the tracker in the directory")
    if initialized(kwargs['dir']):
        raise FileExistsError(f"{kwargs['dir']} treecker already initialized")
    config.read(join(kwargs['dir'], config.get('DEFAULT', 'conf_file')))
    snap = take(kwargs['dir'], kwargs['hash'])
    save(kwargs['dir'], snap)
    print(f"treecker initialized in {kwargs['dir']}")

# -*- coding: utf-8 -*-

"""Status feature.

This module implements the feature that allows to display the changes
that have occurred in the tracked directory.

"""

from datetime import datetime, timezone
from logging import getLogger
from os.path import join

from treecker import config
from treecker.core.comparison import get_differences, differences_log
from treecker.core.snapshot import initialized, load, take


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
        help="compare file hash values",
    )


def main(**kwargs):
    """Display the changes since last snapshot.

    Keyword Arguments
    -----------------
    dir : str
        Path to the tracked directory.
    hash : bool
        Compare file hash values.

    """
    logger.debug("retrieving parameters")
    kwargs.setdefault('dir', config.get(__name__, 'dir'))
    kwargs.setdefault('hash', config.getboolean(__name__, 'hash'))

    logger.debug("loading latest snapshot")
    config.read(join(kwargs['dir'], config.get('DEFAULT', 'conf_file')))
    if not initialized(kwargs['dir']):
        raise FileNotFoundError(f"{kwargs['dir']} treecker not initialized")
    snap1 = load(kwargs['dir'])

    logger.debug("informing user")
    date = datetime.fromisoformat(snap1['date'])
    zone = datetime.now(timezone.utc).astimezone().tzinfo
    date = date.astimezone(zone).isoformat(timespec="seconds")
    print(f"comparing with snapshot from {date} ({zone})")

    logger.debug("taking snapshot")
    hash1 = snap1['hash']
    if kwargs['hash'] and not hash1:
        raise RuntimeError("previous hash values not known")
    hash2 = kwargs['hash']
    if not hash2:
        print("comparison of files based on their size only")
    snap2 = take(kwargs['dir'], hash2)

    logger.debug("displaying differences")
    listing = get_differences(snap1['tree'], snap2['tree'], hash2)
    log = differences_log(listing)
    print(log)

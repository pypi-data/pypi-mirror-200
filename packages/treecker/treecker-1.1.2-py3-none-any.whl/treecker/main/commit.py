# -*- coding: utf-8 -*-

"""Commit feature.

This module implements the feature that allows to save in a new
snapshot the changes that have occurred in the directory.

"""

from datetime import datetime, timezone
from logging import getLogger
from os.path import join

from treecker import config
from treecker.core.comparison import get_differences, differences_log
from treecker.core.snapshot import initialized, load, save, take


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
    """Save the changes in a new snapshot.

    Keyword Arguments
    -----------------
    dir : str
        Path to the tracked directory.

    """
    logger.debug("retrieving parameters")
    kwargs.setdefault('dir', config.get(__name__, 'dir'))

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
    hash2 = hash1
    if not hash2:
        print("comparison of files based on their size only")

    logger.debug("displaying differences")
    snap2 = take(kwargs['dir'], hash2)
    listing = get_differences(snap1['tree'], snap2['tree'], hash2)
    log = differences_log(listing)
    print(log)

    logger.debug("saving new snapshot")
    if len(listing) > 0:
        if input("save modifications? (y|n) ") == "y":
            save(kwargs['dir'], snap2)
            print(f"changes commited in {kwargs['dir']}")

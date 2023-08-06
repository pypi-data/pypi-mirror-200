# -*- coding: utf-8 -*-

"""Password book sorting feature.

This module implements the functionality that allows to sort a
password configuration file.

"""

from logging import getLogger

from pashword.core.book import load, save


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
        'book',
        help="path to the password book file",
        type=str,
        metavar='path',
    )


def main(book):
    """Sort a password book.

    Parameters
    ----------
    book : str
        Path to the password book file.

    """
    logger.debug("loading password book '%s'", book)
    data = load(book)

    logger.debug("sorting password book '%s'", book)
    ordered = {}
    for name in sorted(data.keys()):
        ordered[name] = data[name]

    logger.debug("saving password book '%s'", book)
    save(book, ordered)

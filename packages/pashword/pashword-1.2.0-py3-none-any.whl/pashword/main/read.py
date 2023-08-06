# -*- coding: utf-8 -*-

"""Password reading feature.

This module implements the functionality that allows to search and
decode a password.

"""

from getpass import getpass
from logging import getLogger
from os.path import isfile
from pathlib import Path
from platform import system

from pashword import config
from pashword.core.book import decode, matching, load
from pashword.core.colors import colorize
from pashword.core.pash import same, save
from pashword.core.sets import combinations

if system() == 'Linux':
    import readline
    _ = readline


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
    parser.add_argument(
        '--hash',
        help="path to the hash of the key",
        type=str,
        metavar='path',
    )
    exclusive = parser.add_mutually_exclusive_group()
    exclusive.add_argument(
        '--hide',
        action='store_true',
        help="to hide passwords",
    )
    exclusive.add_argument(
        '--show',
        dest='hide',
        action='store_false',
        help="to show passwords",
    )


def main(book, **kwargs):
    """Decode and display the passwords contained in the book.

    Parameters
    ----------
    book : str
        Path to the password book file.

    Keyword Arguments
    -----------------
    hash : str
        Path to the hash of the key.
    hide : bool
        To hide passwords.

    """
    logger.debug("retrieving parameters")
    kwargs.setdefault('hash', config.get(__name__, 'hash'))
    kwargs.setdefault('hide', config.getboolean(__name__, 'hide'))
    colors = {}
    colors['name'] = config.get(__name__, 'color_name')
    colors['show'] = config.get(__name__, 'color_show')
    colors['hide'] = config.get(__name__, 'color_hide')
    colors['warn'] = config.get(__name__, 'color_warn')
    colors['pash'] = colors['hide'] if kwargs['hide'] else colors['show']

    logger.debug("loading password book '%s'", book)
    data = load(book)
    file = colorize(Path(book).name, colors['warn'])
    print(f"reading {file} ({len(data)} sections)")

    logger.debug("filtering sections")
    pattern = input("matching pattern: ")
    filtered = matching(data, pattern)
    print(f"\n{len(filtered)} matching section(s) found")
    if len(filtered) == 0:
        raise SystemExit()
    for name in filtered:
        print(f"- {colorize(name, colors['name'])}")

    logger.debug("decoding passwords")
    key = get_key(kwargs, colors)
    decoded = decode(filtered, key)
    for name, entries in decoded.items():
        logger.debug("displaying section '%s'", name)
        print(f"\n[{colorize(name, colors['name'])}]")
        for field, value in entries.items():
            if field not in ('password', 'form'):
                print(f"{field} = {value}")
        number = combinations(entries['form'])
        pash = f"{colorize(entries['password'], colors['pash'])}"
        print(f"pash = {pash} ({number:1.0e})")
    print()


def get_key(kwargs, colors):
    """Return the secret key entered by the user.

    Parameters
    ----------
    kwargs : dict
        Keyword arguments of the main function.
    colors : dict
        Color codes.

    Returns
    -------
    str
        The secret key.

    """
    logger.debug("retrieving secret key")
    while True:
        if kwargs['hide']:
            key = getpass("secret key: ")
        else:
            key = input("secret key: ")
        if len(key) == 0:
            raise SystemExit()
        if kwargs['hash'] == '':
            return key
        if isfile(kwargs['hash']):
            if same(key, kwargs['hash']):
                return key
            print(colorize("incorrect secret key", colors['warn']))
            logger.debug("incorrect secret key")
        else:
            logger.info("saving key hash value in '%s'", kwargs['hash'])
            save(key, kwargs['hash'])
            print(f"key hash saved in {kwargs['hash']}")
            return key

# -*- coding: utf-8 -*-

"""Password book handling.

This module implements functionalities to manipulate password books.

"""

from configparser import ConfigParser
from fnmatch import fnmatch
from logging import getLogger

from pashword.core.pash import password


logger = getLogger(__name__)


def load(path):
    """Return the data contained in the file.

    Parameters
    ----------
    path : str
        Path to the password book.

    Returns
    -------
    dict
        Password book data.

    """
    config = ConfigParser()
    logger.debug("loading book '%s'", path)
    with open(path, 'r', encoding='utf-8') as file:
        config.read_file(file)
    book = {}
    for name in config.sections():
        book[name] = dict(config[name])
    return book


def save(path, book):
    """Save the book into a file.

    Parameters
    ----------
    path : str
        Path of the password book to be saved.
    book : dict
        Password book data to be saved.

    """
    config = ConfigParser()
    config.read_dict(book)
    logger.debug("saving book in '%s'", path)
    with open(path, 'w', encoding='utf-8') as file:
        config.write(file)


def matching(book, pattern):
    """Return the accounts whose name matches the pattern.

    Parameters
    ----------
    book : dict
        Password book.
    pattern : str
        Filtering pattern.

    Returns
    -------
    dict
        Filtered password book.

    """
    logger.debug("filtering with '%s' pattern", pattern)
    filtered = {}
    for name, account in book.items():
        if fnmatch(name, pattern):
            filtered[name] = account
    return filtered


def decode(book, key):
    """Return the book augmented with passwords.

    Parameters
    ----------
    book : dict
        Password book.
    key : str
        Secret key.

    Returns
    -------
    dict
        Decoded password book.

    """
    decoded = {}
    for name, account in book.items():
        logger.debug("decoding section '%s'", name)
        data = account.copy()
        form = data.pop('form')
        salt = ''.join(sorted(data.values())) + name
        word = password(key, salt, form)
        data = {**account, 'password': word}
        decoded[name] = data
    return decoded

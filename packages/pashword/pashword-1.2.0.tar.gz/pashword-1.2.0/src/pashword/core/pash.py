# -*- coding: utf-8 -*-

"""Hashing and passwords.

This module provides the hash features for password creation and
secret key validation.

"""

from hashlib import new
from json import dump, load
from logging import getLogger
from uuid import uuid4

from pashword import config
from pashword.core.sets import get


logger = getLogger(__name__)


def digest(key, salt):
    """Return the hash value in binary.

    Parameters
    ----------
    key : str
        Secret key.
    salt : str
        Hash salt.

    Returns
    -------
    bytes
        Digest value.

    """
    algo = config.get(__name__, 'hash_algo')
    logger.debug("hashing with '%s'", algo)
    hashing = new(algo, usedforsecurity=True)
    hashing.update(key.encode('utf-8'))
    hashing.update(salt.encode('utf-8'))
    return hashing.digest()


def hexdigest(key, salt):
    """Return the hash value in hexadecimal.

    Parameters
    ----------
    key : str
        Secret key.
    salt : str
        Hash salt.

    Returns
    -------
    str
        Hexadecimal digest value.

    """
    return digest(key, salt).hex()


def password(key, salt, form):
    """Return the account password.

    Parameters
    ----------
    key : str
        Secret key.
    salt : str
        Hash salt.
    form : str
        Password format.

    Returns
    -------
    str
        Password value.

    """
    logger.debug("getting integer hash value")
    series = digest(key, salt)
    index = int.from_bytes(series, byteorder='big', signed=False)
    logger.debug("getting resulting string")
    word = []
    for metacharacter in form:
        characters = get(metacharacter)
        size = len(characters)
        word.append(characters[index % size])
        index //= size
    word = ''.join(word)
    return word


def save(key, path):
    """Save a hash of the key in a file.

    Parameters
    ----------
    key : str
        Secret key.
    path : str
        Path of the file containing the hash.

    """
    salt = str(uuid4())
    data = {
        'salt': salt,
        'hash': hexdigest(key, salt),
    }
    logger.debug("saving hash value in '%s'", path)
    with open(path, 'w', encoding='utf-8') as file:
        dump(data, file)


def same(key, path):
    """Return wether the key is the same as the one from the file.

    Parameters
    ----------
    key : str
        Secret key.
    path : str
        Path of the file containing the hash.

    """
    logger.debug("loading hash value from '%s'", path)
    with open(path, 'r', encoding='utf-8') as file:
        data = load(file)
    return data['hash'] == hexdigest(key, data['salt'])

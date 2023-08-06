# -*- coding: utf-8 -*-

"""Character sets.

This module provides the character sets used for the construction of
passwords.

"""

from logging import getLogger

from pashword import config


logger = getLogger(__name__)


def get(metacharacter):
    """Return the set of characters associated to the metacharacter.

    Parameters
    ----------
    metacharacter : str
        Character associated with a set of characters.

    Returns
    -------
    str
        The set of characters associated to the metacharacter.

    """
    logger.debug("retrieving '%s' character set", metacharacter)
    return config.get(__name__, metacharacter, fallback=metacharacter)


def combinations(form):
    """Return the number of possible combinations for the given format.

    Parameters
    ----------
    form : str
        Metacharacters defining the password format.

    Returns
    -------
    int
        The number of possible combinations for the given format.

    """
    logger.debug("computing combinations for '%s'", form)
    number = 1
    for metacharacter in form:
        number *= len(get(metacharacter))
    return number

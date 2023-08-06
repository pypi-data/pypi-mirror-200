# -*- coding: utf-8 -*-

"""Pashword package.

This Python package allows you to easily and securely manage your
passwords.

"""

__author__ = 'Dunstan Becht'

from configparser import ConfigParser
from logging import basicConfig
from pkgutil import get_data


config = ConfigParser()
config.read_string(get_data(__package__, 'default.conf').decode())

basicConfig(level=config.get(__name__, 'log'))

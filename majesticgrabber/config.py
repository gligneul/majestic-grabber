# SPDX-License-Identifier: GPL-3.0-only
# Copyright (c) 2020, Gabriel Ligneul

import collections
import configparser
import logging
import pathlib
import sys

_Youtube = collections.namedtuple('_Youtube', 'key')
_Library = collections.namedtuple('_Library', 'path album_prefix')

def load():
    global youtube
    global library

    parser = configparser.ConfigParser()
    parser.read(pathlib.Path.home() / '.majesticgrabber.conf')
    try:
        library = _Library(parser['library']['path'],
                parser['library']['album_prefix'])
        youtube = _Youtube(parser['youtube']['key'])
        logging.info(library)
        logging.info(youtube)
    except KeyError as e:
        print("Error: unable to find key '" + e.args[0] + "' in config file")
        sys.exit(1)


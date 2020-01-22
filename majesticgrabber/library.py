# SPDX-License-Identifier: GPL-3.0-only
# Copyright (c) 2020, Gabriel Ligneul

import collections
import logging
import re
from majesticgrabber import config

Tags = collections.namedtuple('Tags', 'position artist track album '
        'album_artist year')
Music = collections.namedtuple('Music', 'id path tags')

ALBUM_ARTIST = 'Majestic Casual'

def _group_albums(videos):
    '''group music in albums by year and month'''
    albums = {}
    for video in videos:
        album_name = video.date[:7]
        if album_name not in albums:
            albums[album_name] = []
        albums[album_name].append(video)
    return albums

_title_re = re.compile(r'^([^-]*)\s*[–-]\s*(?:([^|]*)|(?:([^|]*)\s\|.*))$')
def _parse_title(title):
    m = _title_re.match(title)
    if m:
        return m.group(0), m.group(1) or m.group(2)

def _to_music(video, pos):
    album_name = config.library.album_prefix + ' ' + video.date[:7]
    parse_result = _parse_title(video.title)
    if not parse_result:
        logging.info('ignoring "' + video.title + '"')
        return None, pos
    artist, track = parse_result
    # path = config.library.path + '/' + album_name + '/'
    tags = Tags(pos, artist, track, album_name, ALBUM_ARTIST, video.date[:4])
    return Music(video.id, '', tags), pos + 1

def insert(videos):
    missing = []
    for album in _group_albums(videos).values():
        album.sort(key=lambda video: video.date)
        pos = 1
        for video in album:
            music, pos = _to_music(video, pos)
            if music: # e se arquivo nao exite
                missing.append(music)
    
    logging.info('missing ' + str(len(missing)) + ' music files')
    return missing

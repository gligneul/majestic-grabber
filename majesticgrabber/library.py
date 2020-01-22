# SPDX-License-Identifier: GPL-3.0-only
# Copyright (c) 2020, Gabriel Ligneul

import collections
import logging
import re
import pathlib
from majesticgrabber import config

Tags = collections.namedtuple('Tags', 'position artist track album '
        'album_artist year')
Music = collections.namedtuple('Music', 'id path tags thumbnail')

ALBUM_ARTIST = 'Majestic Casual'

def _album_name(video):
    '''group music in albums by year and month'''
    return config.library.album_prefix + ' ' + video.date[:7]

def _group_albums(videos):
    albums = {}
    for video in videos:
        album_name = _album_name(video)
        if album_name not in albums:
            albums[album_name] = []
        albums[album_name].append(video)
    return albums

_title_re = re.compile(r'^([^-]*)\s[–-]\s(?:([^|]*)|(?:([^|]*)\s\|.*))$')
def _parse_title(title):
    m = _title_re.match(title)
    if m:
        return m.group(1), m.group(2) or m.group(3)

def _to_music(video, pos):
    parse_result = _parse_title(video.title)
    if not parse_result:
        logging.info('ignoring "' + video.title + '"')
        return None, pos
    artist, track = parse_result
    album_name = _album_name(video)
    track_name = '{:02d} {} - {}.mp3'.format(pos, artist, track)
    path = pathlib.Path(config.library.path) / album_name / track_name
    tags = Tags(pos, artist, track, album_name, ALBUM_ARTIST, video.date[:4])
    return Music(video.id, path, tags, video.thumbnail), pos + 1

def insert(videos):
    missing = []
    for album in _group_albums(videos).values():
        album.sort(key=lambda video: video.date)
        pos = 1
        for video in album:
            music, pos = _to_music(video, pos)
            if music and not music.path.exists():
                missing.append(music)
    logging.info('missing ' + str(len(missing)) + ' music files')
    return missing

# SPDX-License-Identifier: GPL-3.0-only
# Copyright (c) 2020, Gabriel Ligneul

import collections
import logging
import re
import pathlib
from majesticgrabber import config

Tags = collections.namedtuple('Tags', 'position artist track album '
        'album_artist year')
Music = collections.namedtuple('Music', 'id path tags')
Cover = collections.namedtuple('Cover', 'path url')
Missing = collections.namedtuple('Missing', 'dirs musics covers')

ALBUM_ARTIST = 'Majestic Casual'

def _base_path():
    return pathlib.Path(config.library.path)

def _album_name(video):
    '''names the album "<prefix> <year>-<month>"'''
    return config.library.album_prefix + ' ' + video.date[:7]

def _group_albums(videos):
    '''group music in albums by year and month'''
    albums = {}
    for video in videos:
        album_name = _album_name(video)
        if album_name not in albums:
            albums[album_name] = []
        albums[album_name].append(video)
    for album in albums.values():
        album.sort(key=lambda video: video.date)
    return albums

_title_re = re.compile(r'^([^-]*)\s[–-]\s(?:([^|]*)|(?:([^|]*)\s\|.*))$')
def _parse_title(title):
    '''extract the artist and track in "<artist> - <track> (| ...)?"'''
    m = _title_re.match(title)
    if m:
        return m.group(1), m.group(2) or m.group(3)

def _missing_dirs(albums):
    missing = []
    base_path = _base_path()
    if not base_path.exists():
        missing.append(base_path)
    for name in albums:
        album_path = base_path / name
        if not album_path.exists():
            missing.append(album_path)
    logging.info('missing ' + str(len(missing)) + ' dirs')
    return missing

def _missing_musics(albums):
    missing = []
    for album_name, album in albums.items():
        pos = 1
        for video in album:
            parse_result = _parse_title(video.title)
            if not parse_result:
                logging.info('ignoring video "' + video.title + '"')
                continue
            artist, track = parse_result
            track_name = '{:02d} {} - {}.mp3'.format(pos, artist, track)
            path = _base_path() / album_name / track_name
            if not path.exists():
                tags = Tags(pos, artist, track, album_name, ALBUM_ARTIST,
                    video.date[:4])
                missing.append(Music(video.id, path, tags))
            pos += 1
    logging.info('missing ' + str(len(missing)) + ' music files')
    return missing
    
def _missing_covers(albums):
    missing = []
    for album_name, album in albums.items():
        path = _base_path() / album_name / 'cover.jpg'
        if path.exists():
            continue
        for video in album:
            if video.thumbnail:
                missing.append(Cover(path, video.thumbnail['url']))
                break
        else:
            logging.warn('no cover for album ' + album_name)
    logging.info('missing ' + str(len(missing)) + ' cover files')
    return missing

def get_missing(videos):
    albums = _group_albums(videos)
    return Missing(
        _missing_dirs(albums),
        _missing_musics(albums),
        _missing_covers(albums)
    )

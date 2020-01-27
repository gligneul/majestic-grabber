# SPDX-License-Identifier: GPL-3.0-only
# Copyright (c) 2020, Gabriel Ligneul

import collections
import logging
import re
import pathlib
from majesticgrabber import config, cover, mp3dl, tagger

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

def _create_dir_if_absent(dir):
    if not dir.exists():
        logging.info('creating dir ' + str(dir))
        dir.mkdir()

def _create_dirs(albums):
    base_path = _base_path()
    _create_dir_if_absent(base_path)
    for name in albums:
        album_path = base_path / name
        if not album_path.exists():
            _create_dir_if_absent(album_path)

def _get_mp3(video, album_name, pos, artist, track):
    track_name = '{:02d} {} - {}.mp3'.format(pos, artist, track)
    path = _base_path() / album_name / track_name
    if path.exists():
        return
    logging.info('getting music ' + str(path))
    mp3dl.download(video.id, path.basename())
    thumbnail_path = path.with_suffix('.jpg')
    thumbnail = cover.get_and_resize(thumbnail_path, video.thumbnail)
    tagger.set_tags(path, pos, artist, track, album_name, ALBUM_ARTIST,
                    video.date[:4], video.id, thumbnail_path)
    thumbnail_path.unlink()

def _download_music(albums):
    for album_name, album in albums.items():
        pos = 1
        for video in album:
            parse_result = _parse_title(video.title)
            if not parse_result:
                logging.info('ignoring video "' + video.title + '"')
                continue
            _get_mp3(video, album_name, pos, *parse_result)
            pos += 1

def _download_covers(albums):
    for album_name, album in albums.items():
        path = _base_path() / album_name / 'cover.jpg'
        if path.exists():
            cover.get_and_resize(path, album[0].thumbnail)

def get_missing(videos):
    albums = _group_albums(videos)
    _create_dirs(albums)
    _download_music(albums)
    _download_covers(albums)

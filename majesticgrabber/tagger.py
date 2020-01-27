# SPDX-License-Identifier: GPL-3.0-only
# Copyright (c) 2020, Gabriel Ligneul

import eyed3

def set_tags(path, pos, artist, title, album, album_artist, year, id, cover):
    audio = eyed3.load(path)
    if not audio.tag:
        audiofile.initTag()
    tag = audio.tag
    tag.track_num = pos
    tag.artist = artist
    tag.title = title
    tag.album = album
    tag.album_artist = album_artist
    tag.comments.set(id)
    with open(cover, 'rb') as cover_file:
        tag.images.set(3, cover_file.read(), 'image/jpeg')
    tag.save()

# SPDX-License-Identifier: GPL-3.0-only
# Copyright (c) 2020, Gabriel Ligneul

import logging
from youtube_dl.YoutubeDL import YoutubeDL

YOUTUBE_WATCH = "https://www.youtube.com/watch?v="

def download(id, path):
    postprocessors = [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '0',
        'nopostoverwrites': False
    }]
    ydl_opts = {
        'postprocessors': postprocessors,
        'outtmpl': path
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([YOUTUBE_WATCH + id])


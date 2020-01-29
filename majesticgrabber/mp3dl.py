# SPDX-License-Identifier: GPL-3.0-only
# Copyright (c) 2020, Gabriel Ligneul

import os
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
    without_suffix = os.path.splitext(path)[0]
    ydl_opts = {
        'ratelimit': 1048576,
        'postprocessors': postprocessors,
        'outtmpl': without_suffix + '.%(ext)s',
        'format': 'bestaudio/best',
        'quiet': True
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([YOUTUBE_WATCH + id])


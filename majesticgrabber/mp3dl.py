# SPDX-License-Identifier: GPL-3.0-only
# Copyright (c) 2020, Gabriel Ligneul

import logging
from youtube_dl.YoutubeDL import YoutubeDL

YOUTUBE_WATCH = "https://www.youtube.com/watch?v="

def download(id, path):
    print(id, path)

#        logging.info("downloading video " + id + " as " + path)
#        cmd = [self.ytdl, YOUTUBE_WATCH + id, "-x", "--audio-format", "mp3",
#                "--audio-quality", "0", "-o", path]


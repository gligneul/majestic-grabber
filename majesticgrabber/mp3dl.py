# SPDX-License-Identifier: GPL-3.0-only
# Copyright (c) 2020, Gabriel Ligneul

import logging
import os
import requests
import subprocess
import tempfile

YOUTUBE_DL_URL = "https://youtube-dl.org/downloads/latest/youtube-dl"
YOUTUBE_WATCH = "https://www.youtube.com/watch?v="

def get_youtube_dl():
        fd, path = tempfile.mkstemp()
        logging.info("youtube-dl downloading")
        r = requests.get(YOUTUBE_DL_URL)
        with os.fdopen(fd, 'wb') as f:
            f.write(r.content)
        os.chmod(path, 0o755)
        logging.info("youtube-dl available at " + path)
        return path

class Mp3Dl:
    def __init__(self):
        self.ytdl = get_youtube_dl()

    def __del__(self):
        os.remove(self.ytdl)

    def download(self, id, path):
        logging.info("downloading video " + id + " as " + path)
        cmd = [self.ytdl, YOUTUBE_WATCH + id, "-x", "--audio-format", "mp3",
                "--audio-quality", "0", "-o", path]
        subprocess.check_call
        proc = subprocess.Popen(cmd, stdout = subprocess.PIPE,
                stderr = subprocess.PIPE)
        stdout, stderr = proc.communicate()
        if proc.returncode == 0:
            logging.debug(stdout.decode('ascii'))
        else:
            logging.error(stdout.decode('ascii'))
            logging.error(stderr.decode('ascii'))

#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
# Copyright (c) 2020, Gabriel Ligneul

import logging
from majesticgrabber import channel, config, library

logging.basicConfig(level = logging.INFO)
config.load()
videos = channel.get_videos('majesticcasual')
library.get_missing(videos)

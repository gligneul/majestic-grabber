# SPDX-License-Identifier: GPL-3.0-only
# Copyright (c) 2020, Gabriel Ligneul

import requests
import PIL.Image

def get_and_resize(path, url):
    r = requests.get(url)
    with open(path, 'wb') as file:
        file.write(r.content)
    image = PIL.Image.open(path)
    w, h = image.size
    boarder = (w - h) / 2
    box = (boarder, 0, h + boarder, h)
    new_image = image.crop(box)
    new_image.save(path)

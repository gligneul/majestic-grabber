# SPDX-License-Identifier: GPL-3.0-only
# Copyright (c) 2020, Gabriel Ligneul

import logging
import collections
import googleapiclient.discovery
from majesticgrabber import config

logging.getLogger('googleapiclient.discovery').disabled = True

Video = collections.namedtuple('Video', 'id title date thumbnail')

def get_videos(channel_name):
    logging.info('creating youtube client')
    youtube = googleapiclient.discovery.build('youtube', 'v3',
            cache_discovery = False, developerKey = config.youtube.key)
    
    logging.info('fetching youtube channel playlist')
    channels_response = youtube.channels().list(
        part = 'contentDetails',
        forUsername = channel_name
    ).execute()
    channel = channels_response['items'][0]
    if not channel:
        logging.error('channel not found')
        return None
    playlist_id = channel['contentDetails']['relatedPlaylists']['uploads']

    logging.info('fetching playlist videos')
    videos = []
    playlistitems_request = youtube.playlistItems().list(
        part = 'snippet',
        playlistId = playlist_id,
        maxResults = 50
    )
    while playlistitems_request:
        playlistitems_response = playlistitems_request.execute()
        for playlist_item in playlistitems_response['items']:
            item = playlist_item['snippet']
            video = Video(
                item['resourceId']['videoId'],
                item['title'],
                item['publishedAt'],
                item['thumbnails'].get('maxres', None)
            )
            videos.append(video)
        playlistitems_request = youtube.playlistItems().list_next(
            playlistitems_request, playlistitems_response)
        playlistitems_request = None # TODO remove this line

    logging.info('fetched ' + str(len(videos)) + ' videos from youtube')
    return videos


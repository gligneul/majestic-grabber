# SPDX-License-Identifier: GPL-3.0-only
# Copyright (c) 2020, Gabriel Ligneul

import logging
import collections
import googleapiclient.discovery
from majesticgrabber import config

logging.getLogger('googleapiclient.discovery').disabled = True

Video = collections.namedtuple('Video', 'id title date thumbnail')

def create_client():
    logging.info('creating youtube client')
    return googleapiclient.discovery.build('youtube', 'v3',
            cache_discovery = False, developerKey = config.youtube.key)

def fetch_uploads(youtube, channel_name):
    logging.info('fetching upload playlist id')
    channels_response = youtube.channels().list(
        part = 'contentDetails',
        forUsername = channel_name
    ).execute()
    channel = channels_response['items'][0]
    if not channel:
        logging.error('channel not found')
        return None
    return channel['contentDetails']['relatedPlaylists']['uploads']

def get_best_thumbnail(item):
    thumbnails = [t for t in item['thumbnails'].values()]
    thumbnails.sort(key=lambda t: t['width'], reverse=True)
    return thumbnails[0]['url']

def fetch_videos(youtube, playlist_id):
    logging.info('fetching videos')
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
                get_best_thumbnail(item)
            )
            videos.append(video)
        playlistitems_request = youtube.playlistItems().list_next(
            playlistitems_request, playlistitems_response)
    return videos

def get_videos(channel_name):
    youtube = create_client()
    uploads = fetch_uploads(youtube, channel_name)
    if not uploads:
        return None
    videos = fetch_videos(youtube, uploads)
    logging.info('fetched ' + str(len(videos)) + ' videos from youtube')
    return videos


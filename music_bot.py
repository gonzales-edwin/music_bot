import json
import os
import random
import time

import praw
import requests

''' 
    TODO: remove functions to only use slack and deprecate file creation
'''
REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
REDDIT_USER_AGENT = os.getenv('REDDIT_USER_AGENT')
SLACK_JSON_HEADER = {'Content-type': 'application/json'}
SLACK_POST_WEBHOOK = os.getenv('SLACK_POST_WEBHOOK')
SLACK_MUSIC_CHANNEL_ID = os.getenv('SLACK_MUSIC_CHANNEL_ID')

video_url_list = 'download.txt'
reddit = praw.Reddit(client_id=REDDIT_CLIENT_ID,
                     client_secret=REDDIT_CLIENT_SECRET,
                     user_agent=REDDIT_USER_AGENT)
print(f'Reddit API is callable: [ {reddit.read_only} ]')


def slack_post_message(message):
    json_data = json.dumps({'text': message})
    post = requests.post(SLACK_POST_WEBHOOK, headers=SLACK_JSON_HEADER, data=json_data)
    return post

subreddit = reddit.subreddit('listentothis')


def get_random_post():
    random_post = subreddit.random()
    post = reddit.submission(id=random_post)
    song_title = post.title
    song_url = post.url
    slack_post_message(song_title)
    slack_post_message(song_url)
    print(f'{song_title} - {song_url}')
    genre = song_title[song_title.index('[') + 1: song_title.index(']')].split()
    return random.choice(genre)


def search_post(search_keyword):
    random_post = subreddit.search(search_keyword, limit=None, sort=None)
    for result in random_post:
        if 'youtu' in result.url:
            print(f'{result.title} - {result.url}')
            with open(video_url_list, 'r+') as text_file:
                lines = text_file.readlines()
                if f'{result.url}\n' in lines:
                    print(f'{result.title} already in file')
                    continue
                line = result.url
                text_file.write(line + '\n')
        else:
            continue

while True:
    new_post = get_random_post()
    time.sleep(5)
    search_post(new_post)
    time.sleep(180)

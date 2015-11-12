import os
import json
import fnmatch
from collections import namedtuple
from os.path import basename

from vk_api import VkApi, AuthorizationError
import requests


Song = namedtuple('Song', ['id', 'title', 'source', 'duration'])


class OnlineSource:

    def __init__(self):
        self.songs = []
        self.connection = None
        if os.path.isfile('vk_config.json'):
            with open('vk_config.json', 'r') as conf:
                data = json.loads(conf.read())
                if data:
                    username = data.keys()[0]
                    if self.login(username, username):
                        self.songs = self.get_audios()

    def get_audios(self, owner_id=None):
        response = self.connection.method('audio.get', {'owner_id': owner_id} if owner_id else None)
        return [Song(item['id'], u"{} - {}".format(item['artist'], item['title']), item['url'], item['duration']) for item in response['items']]

    def login(self, login, password):
        if login and password:
            self.connection = VkApi(login, password)
            try:
                self.connection.authorization()
                print('autorization')
            except requests.exceptions.ConnectionError:
                print('has not connection')
            except AuthorizationError as error_msg:
                print(error_msg)
            except TypeError as fkng_msg:
                print(fkng_msg)
            else:
                return True
        return False


class OfflineSource:
    def __init__(self, directory):
        self.songs = []
        self.get_files(directory)

    def get_files(self, path):
        for f in os.listdir(path):
            f = os.path.join(path, f)
            if os.path.isdir(f):
                self.get_files(f)  # recurse
            if fnmatch.fnmatch(f, '*.mp3'):
                self.songs.append(Song(basename(f), f))



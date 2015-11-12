import pygame
import urllib

class Player:
    def __init__(self, songs):
        pygame.init()
        pygame.mixer.init()
        self.set_songs(songs)

    def set_songs(self, songs):
        self.current_song_index = 0
        self.songs = songs
        self.paused = True
        if self.songs:
            self.play(0)

    def _get_next_song(self, index):
        next_index = self.current_song_index + index
        if next_index >= len(self.songs):
            next_index = 0
        elif next_index < 0:
            next_index = len(self.songs) - 1
        self.current_song_index = next_index
        return self.songs[next_index] if len(self.songs) > next_index >= 0 else None

    def _on_song_ends(self):
        self.play(1)

    @staticmethod
    def _load_source(source):
        if source.startswith('http'):
            song_file = urllib.urlopen(source)
            pygame.mixer.music.load(song_file)
        else:
            pygame.mixer.music.load(source)

    def on_song_change(self, **kwargs):
        pass

    def play_pause(self):
        if self.paused:
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()
        self.paused = not self.paused

    def play(self, index=0):
        self.paused = False
        song = self._get_next_song(index)
        if song:
            self._load_source(song.source)
            pygame.mixer.music.play()
            self.on_song_change(song=song)

    def play_by_index(self, index):
        self.paused = False
        self.current_song_index = index
        song = self.songs[index]
        self._load_source(song.source)
        pygame.mixer.music.play()
        self.on_song_change(song=song)

    def set_volume(self, volume):
        pygame.mixer.music.set_volume(volume)

    def update(self):
        if not self.paused and not pygame.mixer.music.get_busy():
            self._on_song_ends()

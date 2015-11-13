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

    def _get_current_song(self):
        return self.songs[self.current_song_index]

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

    def _play(self, loop=0, start=0.0):
        self.start_offset = start
        pygame.mixer.music.play(loop, start)

    def on_song_change(self, **kwargs):
        pass

    def on_play_progress(self, sec):
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
            self._play()
            self.on_song_change(song=song)

    def play_by_index(self, index):
        self.paused = False
        self.current_song_index = index
        song = self.songs[index]
        self._load_source(song.source)
        self._play()
        self.on_song_change(song=song)

    def set_volume(self, volume):
        pygame.mixer.music.set_volume(volume)

    def _get_current_progress(self):
        return self.start_offset + pygame.mixer.music.get_pos() / 1000

    def set_progress(self, sec):
        self._play(0, float(sec))

    # def inc_progress(self, inc):
    #     curr_progress = self._get_current_progress()
    #     if inc > 0:
    #         end_range = self._get_current_song().duration - curr_progress
    #     else:
    #         end_range = 0 - curr_progress
    #     return curr_progress + end_range/2

    def update(self):
        if not self.paused:
            if not pygame.mixer.music.get_busy():
                self._on_song_ends()
            else:
                self.on_play_progress(self._get_current_progress())

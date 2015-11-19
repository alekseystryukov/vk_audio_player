import vlc


class Player:
    def __init__(self, songs):
        self.player = vlc.MediaPlayer()
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

    def _load_source(self, source):
        self.player.set_media(vlc.Media(source))

    def _play(self, loop=0, start=0.0):
        self.start_offset = start
        self.player.play()

    def on_song_change(self, **kwargs):
        pass

    def on_play_progress(self, sec):
        pass

    def play_pause(self):
        self.player.set_pause(int(not self.paused))
        self.paused = not self.paused

    def play(self, index=0):
        song = self._get_next_song(index)
        if song:
            self._load_source(song.source)
            self._play()
            self.paused = False
            self.on_song_change(song=song)


    def play_by_index(self, index):
        self.paused = False
        self.current_song_index = index
        song = self.songs[index]
        self._load_source(song.source)
        self._play()
        self.on_song_change(song=song)

    def stop(self):
        self.paused = True
        self.player.stop()

    def set_volume(self, volume):
        self.player.audio_set_volume(int(volume))

    def _get_current_progress(self):
        return self.player.get_position()

    def set_progress(self, percent):
        self.player.set_position(percent)

    def update(self):
        if not self.paused:
            if not self.player.is_playing():
                self._on_song_ends()
            else:
                self.on_play_progress(self._get_current_progress())

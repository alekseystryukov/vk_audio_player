

from musicplayer import Player
from song_sources import OnlineSource, OfflineSource
from gui import Interface


gui = Interface()
vk_music = OnlineSource()

player = Player(vk_music.songs)
        #or OfflineSource(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')).songs
if vk_music.songs:
    gui.show_player(vk_music.songs, player)
    print('after show player')
else:
    gui.show_login()

    def on_credentials_entered(login, password):
        if vk_music.login(login, password):
            songs_list = vk_music.get_audios()
            player.set_songs(player)
            gui.show_player(songs_list, player)
            return True
        return False

    gui.on_credentials_entered = on_credentials_entered

import time

start_time = 0
while True:
    gui.update()
    cur_time = time.time()
    if cur_time - start_time > 1:
        start_time = cur_time
        player.update()
#window.mainloop()
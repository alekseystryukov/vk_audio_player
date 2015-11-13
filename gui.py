from Tkinter import *
import tkMessageBox


class Interface:
    def __init__(self):
        self.window = Tk()
        self.window.title("Music Player")

    def show_player(self, songs, player):

        def cmd_play_pause(*args):
            player.play_pause()

        def cmd_next(*args):
            player.play(1)

        def cmd_prev(*args):
            player.play(-1)

        def cmd_volume(vol):
            player.set_volume(float(vol)/100)

        def cmd_list(event):
            index = Lb.nearest(event.y)
            if index > -1:
                player.play_by_index(index)

        def on_song_change(song):
            # title
            song_label.set(song.title)
            curr = Lb.curselection()
            if curr:
                Lb.select_clear(curr[0])

            # song list
            index = songs.index(song)
            Lb.select_set(index)
            Lb.see(index)
            Lb.activate(index)

            # song progress
            progress.configure(to=song.duration)
            print('set song duration: {}'.format(song.duration))

        self.disable_progress_update = False

        def cmd_progress(e):
            sec = progress.get()
            print('set progress: {}'.format(sec))
            player.set_progress(sec)
            self.disable_progress_update = False

        def cmd_progress_click(e):
            # disable auto update
            self.disable_progress_update = True

            # fix default increment
            # this cause crash program
            # direct = progress.identify(e.x, e.y)
            # if direct == 'trough1':
            #     inc = -1
            # elif direct == 'trough2':
            #     inc = 1
            # else:
            #     inc = 0
            # if inc:
            #     sec = player.inc_progress(inc)
            #     progress.set(sec)

        def on_play_progress(sec):
            if not self.disable_progress_update:
                progress.set(sec)
                #print('progress: {}'.format(sec))

        player.on_song_change = on_song_change
        player.on_play_progress = on_play_progress

        self.clear_frame(self.window)
        menu = Frame(self.window, relief=RAISED, pady=6, padx=6)
        song_label = StringVar()
        Label(menu, textvariable=song_label, pady=4).pack()
        Button(menu, text="Play/Pause", command=cmd_play_pause).pack(side=LEFT)
        Button(menu, text="Prev", command=cmd_prev).pack(side=LEFT)
        Button(menu, text="Next", command=cmd_next).pack(side=LEFT)
        volume = Scale(menu, from_=0, to=100, orient=HORIZONTAL, showvalue=0,
                             length=150, sliderlength=20, command=cmd_volume)

        volume.pack(side=RIGHT)
        volume.set(100)

        progress = Scale(menu, from_=0, to=100, orient=HORIZONTAL, showvalue=0,
                         length=300, sliderlength=20)

        progress.bind("<Button-1>", cmd_progress_click)
        progress.bind("<ButtonRelease-1>", cmd_progress)

        progress.pack(side=BOTTOM, fill=X, expand=1)

        menu.pack(fill=X, side=TOP)

        frame = Frame(self.window, relief=RAISED, borderwidth=1, height=50)

        Lb = Listbox(frame)
        scrollbar = Scrollbar(frame, command=Lb.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        Lb.configure(yscrollcommand=scrollbar.set)

        for song in songs:
            Lb.insert(END, song.title)

        Lb.bind("<Button-1>", cmd_list)
        Lb.pack(fill=BOTH, expand=1)

        frame.pack(fill=BOTH, side=BOTTOM, expand=1)

        if not player.paused:
            on_song_change(songs[player.current_song_index])

    def show_login(self):
        self.clear_frame(self.window)
        login_frame = Frame(self.window, pady=10, padx=10)

        Label(login_frame, text="Username").grid(row=0, sticky=E)
        Label(login_frame, text="Password").grid(row=1, sticky=E)

        login_input = Entry(login_frame)
        pass_input = Entry(login_frame, show="*")

        login_input.grid(row=0, column=1)
        pass_input.grid(row=1, column=1)

        def _login_btn_clicked():
            username = login_input.get().strip()
            password = pass_input.get().strip()

            if username and password:
                if self.on_credentials_entered(username, password):
                    tkMessageBox.showinfo("Login info", "Success!")
                else:
                    tkMessageBox.showerror("Login error", "Incorrect login or password entered!")
            else:
                tkMessageBox.showerror("Login error", "Login and password both required!")

        Button(login_frame, text="Login", command=_login_btn_clicked).grid(columnspan=2)
        login_frame.pack()

    @staticmethod
    def clear_frame(frame):
        for widget in frame.winfo_children():
            Interface.clear_frame(widget)
            widget.destroy()

    def on_credentials_entered(self, login, password):
        pass

    def update(self):
        self.window.update_idletasks()
        self.window.update()

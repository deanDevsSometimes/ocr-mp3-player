import tkinter as tk
from tkinter import ttk
from tkinter import *

import youtube_to_mp3
import playlist_management
import settings


class MyApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.geometry('360x640')
        self.resizable(False, False)
        self.title("OCR MP3 Player")
        self.configure(bg=settings.colours["primary"])

        style = ttk.Style(self)
        style.theme_create("dummy", parent="alt", settings={
            "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0]}},
            "TNotebook.Tab": {
                "configure": {"padding": [5, 1], "background": settings.colours["secondary"]},
                "map": {"background": [("selected", settings.colours["secondary"])],
                        "expand": [("selected", [1, 1, 1, 0])]}}})

        style.theme_use('dummy')
        style.configure('TNotebook.Tab', background=settings.colours["primary"], foreground='white')
        style.map("TNotebook", background=[("selected", settings.colours["secondary"])])

        tabControl = ttk.Notebook(self)
        tab1 = Frame(tabControl, background=settings.colours["primary"])
        tab2 = Frame(tabControl, background=settings.colours["primary"])
        tab3 = Frame(tabControl, background=settings.colours["primary"])
        tabControl.add(tab1, text='YouTube MP3 Player')
        tabControl.add(tab2, text='My Playlists')
        tabControl.add(tab3, text='Settings')
        tabControl.pack(expand=True, fill=BOTH)

        # Tab 1 - YouTube MP3 Downloader

        youtubeMp3DownloaderEntry = tk.Entry(tab1, width=30)
        youtubeMp3DownloaderEntry.place(x=90, y=35)

        def download_button_function():
            data = youtubeMp3DownloaderEntry.get()
            title = youtube_to_mp3.get_title(data)
            if title != None:
                global temporary_label
                temporary_label = tk.Label(tab1, text= youtube_to_mp3.get_title(data), font=("Comic Sans", 10))
                temporary_label.place(x=0, y=100)
                global temporary_button
                temporary_button = tk.Button(tab1, text="Confirm", font=("Comic Sans", 8),
                                             background=settings.colours["secondary"], command=confirm)
                temporary_button.place(x=10, y=130)

        def confirm():
            data = youtubeMp3DownloaderEntry.get()
            youtube_to_mp3.download_youtube_mp3(data)
            temporary_label.destroy()
            temporary_button.destroy()

            global success_label
            success_label = tk.Label(tab1, text='Success', fg='light green', bg = settings.colours["primary"])
            success_label.place(x=0, y=160)

            self.after(5000, cleanup)

        def cleanup():

            success_label.destroy()

        youtube_label = tk.Label(tab1, text="Youtube MP3 Downloader", font=("Comic Sans", 13),
                                 background=settings.colours["secondary"])
        youtube_label.place(x=80, y=10)
        youtube_button = tk.Button(tab1, text="Download Now", font=("Comic Sans", 8),
                                   background=settings.colours["secondary"], command=download_button_function)
        youtube_button.place(x=140, y=60)

        # Tab 2 - Playlist System

        scrollbar = tk.Scrollbar(tab2, orient='vertical')
        scrollbar.pack(side='right', fill='y')

        text = tk.Text(tab2, yscrollcommand=scrollbar.set, height=0, width=0)
        text.place(x=0, y=0)

        def input_playlist_name():
            # Create a new Tkinter window for the user to input a name
            global input_window
            input_window = tk.Tk()
            input_window.title("Input Playlist Name")
            input_window.geometry("200x100")

            # Create a Tkinter Entry widget
            entry = tk.Entry(input_window)
            entry.pack()

            # Create a Tkinter Button widget to submit the name
            submit_button = tk.Button(input_window, text='Submit', command=lambda: submit(entry.get()))
            submit_button.pack()

            # Run the Tkinter event loop for the input window
            input_window.mainloop()

        def submit(name):
            # Close the input window
            if playlist_management.create_playlist(name):
                input_window.destroy()

                # Create a directory based on the input name
                button = tk.Button(tab2, text=name, bg=settings.colours["secondary"], width=60,
                                   command=lambda p=name: display_content(p, button))
                button.pack()

        def delete_downloaded_file(listbox):
            selected = listbox.curselection()
            if selected:
                file = listbox.get(selected[0])
                if playlist_management.remove_audio_file_from_downloaded(file):
                    listbox.delete(selected[0])

        def delete_playlist(playlist, p_button, win):

            if playlist_management.delete_playlist(playlist):
                win.destroy()

                p_button.pack_forget()

                for widget in p_button.winfo_children():
                    widget.pack()

                p_button.destroy()

        scrollbar.config(command=text.yview)


        def delete_selected_file(listbox, playlist):
            selected = listbox.curselection()
            if selected:
                file = listbox.get(selected[0])
                if playlist_management.remove_audio_file_from_playlist(file, playlist):
                    listbox.delete(selected[0])

        def display_downloads():
            playlist_window = tk.Tk()
            playlist_window.title(playlist)
            playlist_window.geometry("200x450")

            scrollbar = tk.Scrollbar(playlist_window)
            scrollbar.pack(side='right', fill='y')

            listbox = tk.Listbox(playlist_window, yscrollcommand=scrollbar.set)
            listbox.pack(fill=BOTH)

            files = playlist_management.display_downloaded_audio()

            for file in files:
                listbox.insert('end', file)

            button = tk.Button(playlist_window, text='Delete Audio', command=lambda: delete_downloaded_file(listbox))
            button.pack()

            scrollbar.configure(command=listbox.yview)
            playlist_window.mainloop()

        createNewPlaylistButton = tk.Button(tab2, text="Create New Playlist", font = ("Comic Sans", 15),
                                      background=settings.colours["secondary"], width=33, command=input_playlist_name)
        createNewPlaylistButton.pack()

        downloadedAudioButton = tk.Button(tab2, text = "Downloaded Audio", font = ("Comic Sans", 15),
                                          background = settings.colours["secondary"], width = 33, command=display_downloads)
        downloadedAudioButton.pack()

        for playlist in playlist_management.display_playlists():
            playlist_button = tk.Button(tab2, text=playlist, bg=settings.colours["secondary"], width=60,
                               command=lambda p=playlist: display_content(p, playlist_button))
            playlist_button.pack()

        def display_content(playlist, b):
            playlist_window = tk.Tk()
            playlist_window.title(playlist)
            playlist_window.geometry("200x450")

            scrollbar = tk.Scrollbar(playlist_window)
            scrollbar.pack(side='right', fill='y')

            listbox = tk.Listbox(playlist_window, yscrollcommand=scrollbar.set)
            listbox.pack(fill=BOTH)

            files = playlist_management.display_audio_in_playlist(playlist)

            for file in files:
                listbox.insert('end', file)

            delete_audio_button = tk.Button(playlist_window, text = 'Delete Audio', command= lambda: delete_selected_file(listbox, playlist))
            delete_audio_button.pack()

            delete_playlist_button = tk.Button(playlist_window, text = 'Delete Playlist', command = lambda:
                                               delete_playlist(playlist, b, playlist_window))
            delete_playlist_button.pack()


            scrollbar.configure(command=listbox.yview)
            playlist_window.mainloop()

        # Tab 3 - Settings System

        primaryEntry = tk.Entry(tab3, width=15)
        primaryEntry.place(x=130, y=60)

        secondaryEntry = tk.Entry(tab3, width=15)
        secondaryEntry.place(x=130, y=90)

        def change_primary_colour():
            data = primaryEntry.get().replace(' ', '')
            settings.change_primary(data)
            if settings.is_colour_valid(data):
                style.configure('TNotebook.Tab', background=settings.colours["primary"])

                tab1.configure(background=settings.colours["primary"])
                tab2.configure(background=settings.colours["primary"])
                tab3.configure(background=settings.colours["primary"])
                confirm_primary.configure(background=settings.colours["primary"])

        def change_secondary_colour():
            data = secondaryEntry.get().replace(' ', '')
            settings.change_secondary(data)
            if settings.is_colour_valid(data):
                style.map("TNotebook", background=[("selected", settings.colours["secondary"])])
                youtube_label.configure(background=settings.colours["secondary"])
                youtube_button.configure(background=settings.colours["secondary"])
                settings_label.configure(background=settings.colours["secondary"])
                primary_label.configure(background=settings.colours["secondary"])
                secondary_label.configure(background=settings.colours["secondary"])
                confirm_secondary.configure(background=settings.colours["secondary"])

        settings_label = tk.Label(tab3, text="Settings", font=("Comic Sans", 13),
                                  background=settings.colours["secondary"])
        settings_label.place(x=150, y=10)
        primary_label = tk.Label(tab3, text="Primary Colour", font=("Comic Sans", 8),
                                 background=settings.colours["secondary"])
        primary_label.place(x=50, y=60)
        secondary_label = tk.Label(tab3, text="Secondary Colour", font=("Comic Sans", 8),
                                   background=settings.colours["secondary"])
        secondary_label.place(x=33, y=90)

        confirm_primary = tk.Button(tab3, text="Confirm", font=("Comic Sans", 8),
                                    background=settings.colours["primary"], command=change_primary_colour)
        confirm_primary.place(x=230, y=55)
        confirm_secondary = tk.Button(tab3, text="Confirm", font=("Comic Sans", 8),
                                      background=settings.colours["secondary"], command=change_secondary_colour)
        confirm_secondary.place(x=230, y=90)


if __name__ == '__main__':
    app = MyApp()
    app.mainloop()

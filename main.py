import tkinter
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import *
import vlc
from queue_system import queue
import youtube_to_mp3
import playlist_management
import settings
import threading


class MyApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        # Set the size of the window
        self.geometry('360x640')

        # Disable resizing of the window
        self.resizable(False, False)

        # Set the title of the window
        self.title("OCR MP3 Player")

        # Set the background color of the window
        self.configure(bg=settings.colours["primary"])

        # Set the initial value of the `dragging` flag
        self.dragging = False

        # Create a music queue
        self.music_queue = queue()

        # Create a ttk style for the notebook
        style = ttk.Style(self)

        # Create a new theme for the style with the "dummy" name, using the "alt" theme as the parent
        style.theme_create("dummy", parent="alt", settings={
            "TNotebook": {
                "configure": {
                    "margins": [2, 5, 2, 0]
                }
            },
            "TNotebook.Tab": {
                "configure": {
                    "padding": [5, 1],
                    "background": settings.colours["secondary"]
                },
                "map": {
                    "background": [("selected", settings.colours["secondary"])],
                    "expand": [("selected", [1, 1, 1, 0])]
                }
            }
        })

        # Use the new theme for the style
        style.theme_use('dummy')

        # Configure the background and foreground colors of the notebook tabs
        style.configure('TNotebook.Tab', background=settings.colours["primary"], foreground='white')
        style.map("TNotebook", background=[("selected", settings.colours["secondary"])])

        # Create a ttk notebook widget
        tabControl = ttk.Notebook(self)

        # Create three frames for the tabs
        self.tab1 = Frame(tabControl, background=settings.colours["primary"])
        self.tab2 = Frame(tabControl, background=settings.colours["primary"])
        self.tab3 = Frame(tabControl, background=settings.colours["primary"])

        # Add the tabs to the notebook widget
        tabControl.add(self.tab1, text='YouTube MP3 Player')
        tabControl.add(self.tab2, text='My Playlists')
        tabControl.add(self.tab3, text='Settings')

        # Pack the notebook widget to make it visible
        tabControl.pack(expand=True, fill=BOTH)

        # Tab 1 - YouTube MP3 Downloader

        youtubeMp3DownloaderEntry = tk.Entry(self.tab1, width=30) # Setting the Entry width to 30
        youtubeMp3DownloaderEntry.place(x=90, y=35) # Setting the position of the Entry widget

        def download_button_function(temporary_label=None, temporary_button=None):
            # Get the data from the Entry widget
            data = youtubeMp3DownloaderEntry.get().strip()

            # Check if the data is not an empty string
            if data:
                title = youtube_to_mp3.get_title(data)

                # Check if the title is not None
                if title is not None:
                    # Remove any previously created labels and buttons
                    try:
                        temporary_label.destroy()
                        temporary_button.destroy()
                    except AttributeError:
                        pass

                    def confirm_button():
                        confirm(data, temporary_button, temporary_label, temporary_button)

                    # Create a label to display the title
                    temporary_label = tk.Label(self.tab1, text=title, font=("Comic Sans", 10))
                    temporary_label.place(x=0, y=100)

                    # Create a button to confirm the download
                    temporary_button = tk.Button(self.tab1, text="Confirm", font=("Comic Sans", 8),
                                                 background=settings.colours["secondary"], command=confirm_button)
                    temporary_button.place(x=10, y=130)

        def confirm(data, confirm_button, temporary_label=None, temporary_button=None):
            # Disable the confirm button
            confirm_button.configure(state='disabled')

            progress_label = tk.Label(self.tab1, text='Downloading', font = (18), fg='black', bg=settings.colours["primary"])
            progress_label.pack(side='bottom')

            def update_progress_label():
                result = youtube_to_mp3.download_youtube_mp3(data)
                if result:
                    progress_label.configure(text='Success!', fg='light green', font=('Arial', 18))
                else:
                    progress_label.configure(text='Failure :(', fg='red', font=('Arial', 18))
                temporary_label.destroy()
                temporary_button.destroy()
                self.after(5000, progress_label.destroy)

            # Start a separate thread to run the download_youtube_mp3 function
            thread = threading.Thread(target=update_progress_label)
            thread.start()

        youtube_label = tk.Label(self.tab1, text="Youtube MP3 Downloader", font=("Comic Sans", 13),
                                 background=settings.colours["secondary"])
        youtube_label.place(x=80, y=10)
        youtube_button = tk.Button(self.tab1, text="Download Now", font=("Comic Sans", 8),
                                   background=settings.colours["secondary"], command=download_button_function)
        youtube_button.place(x=140, y=60)

        # Tab 2 - Playlist System

        scrollbar = tk.Scrollbar(self.tab2, orient='vertical')
        scrollbar.pack(side='right', fill='y')

        text = tk.Text(self.tab2, yscrollcommand=scrollbar.set, height=0, width=0)
        text.place(x=0, y=0)

        scrollbar.config(command=text.yview)

        def input_playlist_name():
            # Create a Tkinter Entry widget
            input_window = tk.Tk()
            input_window.title("Input Playlist Name")
            entry = tk.Entry(input_window)
            entry.pack()

            # Create a Tkinter Button widget to submit the name
            submit_button = tk.Button(input_window, text='Submit', command=lambda: submit(entry.get(), input_window))
            submit_button.pack()

            # Set the geometry of the input window
            input_window.geometry("200x100")

            # Run the Tkinter event loop for the input window
            input_window.mainloop()

        def submit(name, gui):
            # Check if the playlist creation was successful
            if playlist_management.create_playlist(name):
                gui.destroy()
                create_playlist_button(name)

        def create_playlist_button(name):
            button = tk.Button(self.tab2, text=name, bg=settings.colours["secondary"], width=60,
                               command=lambda p=name: display_content(p, button))
            button.pack()

        def on_play_playlist(playlist_to_display, win):
            """
            Callback function for playing a playlist.

            Args:
                playlist_to_display (list): List of songs in the playlist.
                win (Tk): Tkinter window to be destroyed.

            """
            # Destroy the window
            win.destroy()

            # Pause the player
            self.player.pause()

            # Set the playlist to the music queue
            self.music_queue.set_playlist_to_queue(playlist_to_display)

            # Start a new thread to play the first song in the queue
            thread = threading.Thread(target=self.play,
                                      args=(self.music_queue.display_queue()[self.music_queue.index],))
            thread.start()

        def display_content(playlist_arg, b):
            # Create the playlist window and set its title to the name of the playlist

            playlist_window = tk.Tk()
            playlist_window.title(playlist_arg)
            playlist_window.geometry("200x450")

            # Create a scrollbar for the window
            scrollbar_for_gui = tk.Scrollbar(playlist_window)
            scrollbar_for_gui.pack(side='right', fill='y')

            # Create a listbox to display the audio files in the playlist
            listbox = tk.Listbox(playlist_window, yscrollcommand=scrollbar_for_gui.set)
            listbox.pack(fill=BOTH)

            # Get the audio files in the playlist
            files = playlist_management.display_audio_in_playlist(playlist_arg)

            # Insert the audio files into the listbox
            for file in files:
                listbox.insert('end', file)

            # Create a button to delete the selected audio file
            delete_audio_button = tk.Button(playlist_window, text='Delete Audio',
                                            command=lambda: delete_selected_file(listbox, playlist_arg))
            delete_audio_button.pack()

            # Create a button to delete the entire playlist
            delete_playlist_button = tk.Button(playlist_window, text='Delete Playlist',
                                               command=lambda: delete_playlist(playlist_arg, b, playlist_window))
            delete_playlist_button.pack()

            # Create a button to move the selected audio file to another playlist
            move_audio_button = tk.Button(playlist_window, text='Move Audio To..',
                                          command=lambda: move_audio_gui(get_selected_file(listbox), playlist_arg,
                                                                         listbox))
            move_audio_button.pack()

            # Create a button to play the entire playlist
            play_playlist_button = tk.Button(playlist_window, text='Play Playlist',
                                             command=lambda: on_play_playlist(playlist_arg, playlist_window))
            play_playlist_button.pack()

            # Connect the scrollbar to the listbox
            scrollbar_for_gui.configure(command=listbox.yview)
            playlist_window.mainloop()


        def delete_selected_file(listbox, playlist_arg):
            """
            Delete the selected audio file from the playlist.

            :param listbox: The tkinter Listbox widget that displays the audio files.
            :param playlist_arg: The playlist to delete the audio file from.
            """
            # Get the index of the selected item in the listbox.
            selected = listbox.curselection()

            # If there is a selected item, delete it from the playlist.
            if selected:
                file = listbox.get(selected[0])
                if playlist_management.remove_audio_file_from_playlist(file, playlist_arg):
                    listbox.delete(selected[0])

        def delete_playlist(playlist_arg, p_button, win):
            """
            Delete a playlist.

            :param playlist_arg: The playlist to delete.
            :param p_button: The tkinter button that represents the playlist in the GUI.
            :param win: The tkinter Toplevel widget that displays the playlist.
            """
            # Delete the playlist.
            success = playlist_management.delete_playlist(playlist_arg)

            # If the playlist was successfully deleted, remove the GUI elements
            # that represent it.
            if success:
                win.destroy()
                p_button.pack_forget()
                p_button.destroy()
            else:
                # If the playlist could not be deleted, display an error message.
                error_message = "Could not delete playlist."
                Tk.messagebox.showerror("Error", error_message)

        def move_audio_gui(file, original_playlist, original_listbox):
            """
            Display a GUI that allows the user to move an audio file from one playlist to another.

            :param file: The audio file to move.
            :param original_playlist: The playlist to move the audio file from.
            :param original_listbox: The tkinter Listbox widget that displays the original audio files.
            """
            # Create the GUI.
            playlist_display = tk.Tk()
            playlist_display.title("Playlists")
            playlist_display.geometry("300x500")
            scrollbar_for_gui = tk.Scrollbar(playlist_display)
            scrollbar_for_gui.pack(side='right', fill='y')

            listbox = tk.Listbox(playlist_display, yscrollcommand=scrollbar_for_gui.set)
            listbox.pack(fill=BOTH)

            # Display the playlists in the GUI.
            playlists = playlist_management.display_playlists()
            for playlist in playlists:
                listbox.insert('end', playlist)

            # Create a button that allows the user to move the audio file.
            move_button = tk.Button(playlist_display, text='Move Audio',
                                    command=lambda: move_audio(file, original_playlist, get_playlist(listbox),
                                                               playlist_display,
                                                               original_listbox))
            move_button.pack()

            # Set up the scrollbar for the GUI.
            scrollbar_for_gui.configure(command=listbox.yview)

            # Start the GUI event loop.
            playlist_display.mainloop()

        def get_selected_file(listbox):
            """
            Get the selected audio file from the listbox.

            :param listbox: The tkinter Listbox widget that displays the audio files.
            :return: The selected audio file, or None if no file is selected.
            """
            # Get the index of the selected item in the listbox.
            selected = listbox.curselection()

            # If there is a selected item, return its value.
            if selected:
                file = listbox.get(selected[0])
                return file
            else:
                return None

        def get_playlist(listbox):
            """
            Get the selected playlist from the listbox.

            :param listbox: The tkinter Listbox widget that displays the playlists.
            :return: The selected playlist, or None if no playlist is selected.
            """
            # Get the index of the selected item in the listbox.
            selected = listbox.curselection()

            # If there is a selected item, return its value.
            if selected:
                playlist = listbox.get(selected[0])
                return playlist
            else:
                return None

        def move_audio(file, original_playlist, new_playlist, gui, listbox):
            """
            Move an audio file from one playlist to another.

            :param file: The audio file to move.
            :param original_playlist: The original playlist that the audio file is in.
            :param new_playlist: The new playlist to move the audio file to.
            :param gui: The tkinter Toplevel widget that displays the playlist management GUI.
            :param listbox: The tkinter Listbox widget that displays the audio files in the original playlist.
            """
            # Move the audio file from the original playlist to the new playlist.
            success = playlist_management.move_audio_file_from_playlist(file, original_playlist, new_playlist)

            # If the audio file was successfully moved, close the playlist management GUI
            # and remove the file from the original playlist in the listbox.
            if success:
                gui.destroy()
                index = listbox.get(0, tk.END).index(file)
                listbox.delete(index)
            else:
                # If the audio file could not be moved, display an error message.
                error_message = "Could not move audio file."
                messagebox.showerror("Error", error_message)

        def move_downloaded_audio(file, new_playlist, gui, listbox):
            """
            Move an audio file from the "downloaded audio" playlist to another playlist.

            :param file: The audio file to move.
            :param new_playlist: The playlist to move the audio file to.
            :param gui: The tkinter Tk object representing the GUI.
            :param listbox: The tkinter Listbox widget that displays the audio files.
            """
            # Validate the inputs.
            if not isinstance(file, str):
                raise TypeError("'file' must be a string.")

            if not isinstance(new_playlist, str):
                raise TypeError("'new_playlist' must be a string.")

            if not isinstance(gui, tk.Tk):
                raise TypeError("'gui' must be a tkinter Tk object.")

            if not isinstance(listbox, tk.Listbox):
                raise TypeError("'listbox' must be a tkinter Listbox object.")

            # Move the audio file.
            playlist_management.move_audio_file_from_downloaded_audio(file, new_playlist)

            # Close the GUI.
            gui.destroy()

            # Remove the audio file from the listbox.
            index = listbox.get(0, tk.END).index(file)
            listbox.delete(index)

        def move_downloaded_audio_gui(f, original_listbox):
            """
            Display a GUI that allows the user to choose a playlist to move a downloaded audio file to.

            :param f: The audio file to move.
            :param original_listbox: The tkinter Listbox widget that displays the audio files in the original playlist.
            """
            # Create a Tk object to represent the GUI.
            playlist_display = tk.Tk()
            playlist_display.title("Playlists")
            playlist_display.geometry("300x500")

            # Create a Frame widget to hold the Listbox widget and the Button widget.
            frame = tk.Frame(playlist_display)
            frame.pack(fill='both', expand=True)

            # Create a Scrollbar widget for the GUI.
            scrollbar_for_gui = tk.Scrollbar(frame, orient='vertical')
            scrollbar_for_gui.pack(side='right', fill='y')

            # Create a Listbox widget to display the available playlists.
            listbox = tk.Listbox(frame, yscrollcommand=scrollbar_for_gui.set)
            listbox.pack(fill='both', expand=True)

            # Populate the Listbox widget with the available playlists.
            files = playlist_management.display_playlists()
            for file in files:
                listbox.insert('end', file)

            # Create a Button widget to initiate the move operation.
            button = tk.Button(playlist_display, text='Move Audio',
                               command=lambda: move_downloaded_audio(
                                   f,
                                   get_playlist(listbox),
                                   playlist_display, original_listbox))
            button.pack(pady=10)

            # Configure the Scrollbar widget.
            scrollbar_for_gui.configure(command=listbox.yview)

            # Start the GUI event loop.
            playlist_display.mainloop()

        def delete_downloaded_file(listbox):
            """
            Deletes the selected audio file from the specified playlist's downloaded audio files.
            :param listbox: The listbox containing the downloaded audio files.
            """
            # Get the selected item in the listbox
            selected = listbox.curselection()

            # Check if an item is selected
            if selected:
                # Get the file name of the selected item
                file = listbox.get(selected[0])

                # Delete the file from the playlist's downloaded audio files
                if playlist_management.remove_audio_file_from_downloaded(file):
                    # If the file was successfully deleted, remove it from the listbox
                    listbox.delete(selected[0])

        def display_downloads():
            """
            Displays a GUI window containing the downloaded audio files in the specified playlist.
            """
            # Create the playlist window and set its properties
            playlist_window = tk.Tk()
            playlist_window.title("Downloaded Audio")
            playlist_window.geometry("200x450")

            # Create the scrollbar for the GUI
            scrollbar_for_gui = tk.Scrollbar(playlist_window)
            scrollbar_for_gui.pack(side='right', fill='y')

            # Create the listbox to display the downloaded audio files
            listbox = tk.Listbox(playlist_window, yscrollcommand=scrollbar_for_gui.set)
            listbox.pack(fill=BOTH)

            # Get the downloaded audio files for the playlist
            files = playlist_management.display_downloaded_audio()

            # Insert the files into the listbox
            for file in files:
                listbox.insert('end', file)

            # Create the "Delete Audio" button
            button = tk.Button(playlist_window, text='Delete Audio',
                               command=lambda: delete_downloaded_file(listbox))
            button.pack()

            # Create the "Move Audio To.." button
            move_audio_button = tk.Button(playlist_window, text='Move Audio To..',
                                          command=lambda: move_downloaded_audio_gui(get_selected_file(listbox),
                                                                                    listbox))
            move_audio_button.pack()

            # Configure the scrollbar
            scrollbar_for_gui.configure(command=listbox.yview)

            # Start the GUI event loop
            playlist_window.mainloop()

        createNewPlaylistButton = tk.Button(self.tab2, text="Create New Playlist", font=("Comic Sans", 15),
                                            background=settings.colours["secondary"], width=33,
                                            command=input_playlist_name)
        createNewPlaylistButton.pack()

        downloadedAudioButton = tk.Button(self.tab2, text="Downloaded Audio", font=("Comic Sans", 15),
                                          background=settings.colours["secondary"], width=33,
                                          command = display_downloads)
        downloadedAudioButton.pack()

        # Create buttons for each playlist
        for playlist in playlist_management.display_playlists():
            # Create a button for the playlist
            playlist_button = tk.Button(self.tab2, text=playlist, bg=settings.colours["secondary"], width=60)

            # Bind the button to the display_content function
            playlist_button.bind("<Button-1>", lambda event, p=playlist: display_content(p, playlist_button))

            # Pack the button to display it
            playlist_button.pack()

        # Tab 2 Continued - MP3 Player

        self.player = vlc.MediaPlayer()

        # Create a Frame to hold the progress bar
        self.buttonFrame = Frame(self.tab2, background=settings.colours['primary'])
        # Pack the frame to the bottom of the tab with a padding of 10 pixels
        self.buttonFrame.pack(side="bottom", fill="none", pady=10)

        # Create a horizontal Scale widget for the progress bar
        self.progress_bar = tk.Scale(self.tab2, from_=0, to=100, orient="horizontal", sliderlength=20, length=200,
                                     bg=settings.colours["primary"], troughcolor=settings.colours["secondary"],
                                     highlightthickness=0, command=self.on_scale_drag)
        # Pack the progress bar to the bottom of the tab and fill it horizontally
        self.progress_bar.pack(side="bottom", fill="x")

        # Bind the start, motion, and end events of a left mouse button press to the progress bar
        self.progress_bar.bind("<ButtonPress-1>", self.on_scale_drag_start)
        self.progress_bar.bind("<B1-Motion>", self.on_scale_drag)
        self.progress_bar.bind("<ButtonRelease-1>", self.on_scale_drag_end)

        # Create a frame for the volume control
        self.volume_frame = Frame(self.tab2, background=settings.colours["primary"])
        # Pack the frame to the bottom of the tab2 widget and fill the horizontal space while not expanding it
        self.volume_frame.pack(side=tk.BOTTOM, fill=tk.X, expand=False)

        # Create a label for the volume control
        self.volume_label = tk.Label(self.volume_frame, text='Volume', background=settings.colours["secondary"])
        # Pack the label to the top of the volume_frame widget
        self.volume_label.pack(side=tk.TOP)

        # Create a scale widget for the volume control
        self.volume_slider = tk.Scale(self.volume_frame, from_=0.0, to=1.0, orient=tk.HORIZONTAL,
                                      bg=settings.colours["primary"], troughcolor=settings.colours["secondary"],
                                      highlightthickness=0, command=self.set_volume)

        # Set the resolution of the volume slider to 0.01 for more precise control
        self.volume_slider.set(1.0)  # Set the initial value to 100
        self.volume_slider.configure(resolution=0.01, sliderlength=20,
                                     length=200)  # Set resolution, slider length, and total length
        self.volume_slider.pack(side=tk.BOTTOM)


        # Create a string variable to store the name of the song
        self.song_name = tk.StringVar()

        # Create a label to display the name of the song
        self.song_label = tk.Label(self.volume_frame, bg=settings.colours["primary"], textvariable=self.song_name)

        # Pack the label at the bottom of the `volume_frame`
        self.song_label.pack(side=tk.BOTTOM)

        # Create the play button
        self.play_button = tk.Button(self.buttonFrame, text='Play', background=settings.colours['secondary'],
                                     command=lambda: self.play(0))

        # Create the pause button
        self.pause_button = tk.Button(self.buttonFrame, text='Pause', background=settings.colours['secondary'],
                                      command=self.pause)

        # Create the backward button
        self.backward_button = tk.Button(self.buttonFrame, text='<<', background=settings.colours['secondary'],
                                         command=self.backward)

        # Create the forward button
        self.forward_button = tk.Button(self.buttonFrame, text='>>', background=settings.colours['secondary'],
                                        command=self.forward)

        # Create the next track button
        self.next_track_button = tk.Button(self.buttonFrame, text='>|', background=settings.colours['secondary'],
                                           command=self.skip_forward)

        # Create the last track button
        self.last_track_button = tk.Button(self.buttonFrame, text='|<', background=settings.colours['secondary'],
                                           command=self.skip_backward)

        # Pack the last track button on the left side with 5 pixels of horizontal padding
        self.last_track_button.pack(side='left', padx=5)

        # Pack the backward button on the left side with 5 pixels of horizontal padding
        self.backward_button.pack(side='left', padx=5)

        # Pack the play button on the left side with 5 pixels of horizontal padding
        self.play_button.pack(side='left', padx=5)

        # Pack the pause button on the left side with 5 pixels of horizontal padding
        self.pause_button.pack(side='left', padx=5)

        # Pack the forward button on the left side with 5 pixels of horizontal padding
        self.forward_button.pack(side='left', padx=5)

        # Pack the next track button on the left side with 5 pixels of horizontal padding
        self.next_track_button.pack(side='left', padx=5)

        # Tab 3 - Settings

        primaryEntry = tk.Entry(self.tab3, width=15)
        primaryEntry.place(x=130, y=60)

        secondaryEntry = tk.Entry(self.tab3, width=15)
        secondaryEntry.place(x=130, y=90)

        def change_primary_colour():
            # Get the entered data and remove any whitespace AND Hashtags
            data = primaryEntry.get().strip().replace('#', '')


            # Get the colour of the current primary colour
            old_colour = settings.colours["primary"]

            # Change the primary color in the settings
            settings.change_primary(data)

            # Check if the entered color is valid
            if settings.is_colour_valid(data):

                # Update the background color of the tabs
                style.configure('TNotebook.Tab', background=settings.colours["primary"])

                # Update the background color of the selected tab
                style.map("TNotebook", background=[("selected", settings.colours["primary"])])

                # A list of tuples containing the tab name and tab object
                tabs = [
                    ('tab1', self.tab1),
                    ('tab2', self.tab2),
                    ('tab3', self.tab3),
                ]

                # Loop through the tabs and update the background color of all widgets within each tab
                for tab in tabs:
                    tab[1].configure(background=settings.colours["primary"])
                    tab_name, tab_obj = tab
                    # Iterate through all child widgets of the tab
                    for child in tab_obj.winfo_children():
                        # Check if the current background color of the child widget matches old_colour
                        if child.cget("background") == old_colour:
                            # Update the background color of the child widget
                            child.configure(background=settings.colours["primary"])

                frames = [
                    self.volume_frame,
                    self.buttonFrame
                ]

                # Change the background color of all widgets in the specified frames
                for frame in frames:
                    for widget in frame.winfo_children():
                        if widget.cget("background") == old_colour:
                            widget.configure(background=settings.colours["primary"])


        def change_secondary_colour():
            data = secondaryEntry.get().strip().replace('#', '')

            if not settings.is_colour_valid(data):
                return

            old_colour = settings.colours["secondary"]
            settings.change_secondary(data)

            style.map("TNotebook.Tab",
                      background=[("selected", settings.colours["secondary"]), ("", settings.colours["primary"])])
            style.configure("TNotebook.Tab", background=settings.colours["primary"])

            tabs = [
                ('tab1', self.tab1),
                ('tab2', self.tab2),
                ('tab3', self.tab3),
            ]

            for tab in tabs:
                tab_name, tab_obj = tab
                # Iterate through all child widgets of the tab
                for child in tab_obj.winfo_children():
                    # Check if the current background color of the child widget matches old_colour
                    if child.cget("background") == old_colour:
                        # Update the background color of the child widget
                        child.configure(background=settings.colours["secondary"])

            frames = [
                self.volume_frame,
                self.buttonFrame
            ]

            # Change the background color of all widgets in the specified frames
            for frame in frames:
                for widget in frame.winfo_children():
                    if widget.cget("background") == old_colour:
                        widget.configure(background=settings.colours["secondary"])

                    if "troughcolor" in widget.keys() and widget.cget("troughcolor") == old_colour:
                        widget.configure(troughcolor=settings.colours["secondary"])

            self.progress_bar.configure(troughcolor=settings.colours["secondary"])

        settings_label = tk.Label(self.tab3, text="Settings", font=("Comic Sans", 13),
                                  background=settings.colours["secondary"])
        settings_label.place(x=150, y=10)
        primary_label = tk.Label(self.tab3, text="Primary Colour", font=("Comic Sans", 8),
                                 background=settings.colours["secondary"])
        primary_label.place(x=50, y=60)
        secondary_label = tk.Label(self.tab3, text="Secondary Colour", font=("Comic Sans", 8),
                                   background=settings.colours["secondary"])
        secondary_label.place(x=33, y=90)

        confirm_primary = tk.Button(self.tab3, text="Confirm", font=("Comic Sans", 8),
                                    background=settings.colours["primary"], command=change_primary_colour)
        confirm_primary.place(x=230, y=55)
        confirm_secondary = tk.Button(self.tab3, text="Confirm", font=("Comic Sans", 8),
                                      background=settings.colours["secondary"], command=change_secondary_colour)
        confirm_secondary.place(x=230, y=90)

    def play(self, file):
        """
        Plays the music file specified in the argument, or resumes playing the current file if no argument is provided.
        :param file: path to the music file to be played
        """
        # If a file is specified in the argument, change the current media
        if file != 0:
            # Create a new media instance from the specified file
            media = vlc.Media(file)
            # Set the player's media to the new instance
            self.player.set_media(media)
        # Play the current media
        self.player.play()
        # Get the name of the current song
        song_name = self.music_queue.get_current_song_name()[:-3]
        # Truncate the name if it's too long
        if len(song_name) > 60:
            song_name = song_name[:57] + "..."
        # Set the song name label
        self.song_name.set(song_name)
        self.update_progress()


    def skip_forward(self):
        """
        Skips to the next track in the queue.
        """
        # Pause the current track
        self.pause()
        # Move to the next track in the queue
        self.music_queue.next_item()
        # Play the next track
        self.play(self.music_queue.display_playing_track())

    def skip_backward(self):
        """
        Skips to the previous track in the queue.
        """
        # Pause the current track
        self.pause()
        # Move to the previous track in the queue
        self.music_queue.last_item()
        # Play the previous track
        self.play(self.music_queue.display_playing_track())

    def pause(self):
        """
        Pauses playback of the current track.
        """
        # Pause the player instance
        self.player.pause()

    def backward(self, step=5000):
        """
        Goes backward in the current track by a specified number of milliseconds.
        """
        current_time = self.player.get_time()
        # Ensure that the new time is not negative
        new_time = max(0, current_time - step)
        self.player.set_time(new_time)

    def forward(self, step=5000):
        """
        Goes forward in the current track by a specified number of milliseconds.
        """
        current_time = self.player.get_time()
        # Ensure that the new time does not exceed the duration of the track
        track_duration = self.player.get_duration()
        new_time = min(track_duration, current_time + step)
        self.player.set_time(new_time)

    def update_progress(self):
        # Get the current position of the music
        current_position = self.player.get_position()

        # If the user is not actively dragging the scale, update it
        if not self.dragging:
            self.progress_bar.set(current_position * 100)

        # Call the update_progress function again after 100 milliseconds
        self.after(100, self.update_progress)

    def on_scale_drag_start(self, event):
        """
        Handle the start of a scale drag event.

        This method sets the `dragging` flag to `True`, indicating that the scale
        drag event has started.
        """
        self.dragging = True

    def on_scale_drag(self, event):
        """
        Handle the progress of a scale drag event.

        This method updates the player's position based on the current position of
        the progress bar, and starts playing the player if it was not already playing.
        """
        if self.dragging:
            # Get the new position based on the current position of the progress bar
            new_position = self.progress_bar.get() / 100
            self.player.set_position(new_position)
            self.player.play()

    def on_scale_drag_end(self, event):
        """
        Handle the end of a scale drag event.

        This method sets the `dragging` flag to `False`, indicating that the scale
        drag event has ended, and updates the player's position based on the final
        position of the progress bar.
        """
        if self.dragging:
            self.dragging = False
            new_position = self.progress_bar.get() / 100
            self.player.set_position(new_position)

    def set_volume(self, volume):
        """
        Set the volume of the player.

        :param volume: The volume to set, as a float in the range [0, 1].
        """
        # Ensure that the volume is within the valid range
        volume = max(0.0, min(1.0, float(volume)))

        # Convert the volume to an integer value in the range [0, 100]
        volume = int(volume * 100)

        # Set the volume of the player
        self.player.audio_set_volume(volume)  # Set the volume as an integer in the range [0, 100]


if __name__ == '__main__':
    app = MyApp()
    app.mainloop()

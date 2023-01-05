class queue():

    def __init__(self):

        self.queue = []
        self.index = 0

    def set_playlist_to_queue(self, playlist):
        from playlist_management import display_audio_in_playlist, playlist_folder
        self.queue = [(playlist_folder + "/" + playlist + "/" + i) for i in display_audio_in_playlist(playlist)]

        if queue:
            return queue

    def display_queue(self):

        return self.queue

    def display_index(self):

        return self.index

    def display_playing_track(self):

        return (self.queue[self.index])

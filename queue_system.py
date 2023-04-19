class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next

class queue():
    def __init__(self):
        self.head = None
        self.tail = None
        self.index = 0
        self.queue = []
        self.playlist = None

    def set_playlist_to_queue(self, playlist):
        from playlist_management import display_audio_in_playlist, playlist_folder
        self.queue = [(playlist_folder + "/" + playlist + "/" + i) for i in display_audio_in_playlist(playlist)]
        self.playlist = playlist

        for track in self.queue:
            node = Node(track)
            if self.tail is None:
                self.head = node
                self.tail = node
            else:
                self.tail.next = node
                self.tail = node

        if self.queue:
            return self.queue

    def is_empty(self):
        return self.head is None

    def enqueue(self, data):
        node = Node(data)
        if self.tail is None:
            self.head = self.tail = node
        else:
            self.tail.next = node
            self.tail = node

    def dequeue(self):
        if self.is_empty():
            return None
        else:
            node = self.head
            self.head = node.next
            if self.head is None:
                self.tail = None
            return node.data

    def display_queue(self):
        return self.queue

    def display_index(self):
        return self.index

    def display_playing_track(self):
        node = self.head
        for i in range(self.index):
            node = node.next
        return node.value

    def next_item(self):
        if self.index + 1 < len(self.queue):
            self.index += 1
        else:
            self.index = 0
        return self.queue[self.index]

    def last_item(self):
        if self.index - 1 < 0:
            self.index = len(self.queue) - 1
        else:
            self.index -= 1
        return self.queue[self.index]

    def get_current_song_name(self):

        from playlist_management import display_audio_in_playlist
        return display_audio_in_playlist(self.playlist)[self.index]

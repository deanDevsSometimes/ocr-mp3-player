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

    def set_playlist_to_queue(self, playlist):
        from playlist_management import display_audio_in_playlist, playlist_folder
        self.queue = [(playlist_folder + "/" + playlist + "/" + i) for i in display_audio_in_playlist(playlist)]

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

import os
import shutil

playlist_folder = "Playlists"


def does_playlist_folder_exist():
    return os.path.isdir(playlist_folder)


def playlist_exists(name):
    for folder in os.listdir(playlist_folder):
        if os.path.isdir(os.path.join(playlist_folder, folder)):
            if folder == name:
                return True

    return False


def display_playlists():
    playlists = []
    playlist_count = 0

    for folder in os.listdir(playlist_folder):
        if os.path.isdir(os.path.join(playlist_folder, folder)):
            playlists.append(folder)
            playlist_count += 1

    return playlists


def create_playlist(name):
    print(f"\nCreating Playlist {name}\n")  #
    try:
        os.mkdir(os.path.join(playlist_folder, name))
        print("Playlist Successfully Created!\n")
    finally:
        print("Sorry, an error has occurred..\n")


def delete_playlist(name):
    print(f"\nDeleting Playlist {name}\n")  #
    try:
        os.rmdir(os.path.join(playlist_folder, name))
        print("Playlist Successfully Deleted\n")
    finally:
        print("Sorry, an error has occurred..\n")

def display_audio_in_playlist(name):
    if playlist_exists(name):
        return os.listdir(playlist_folder + "/" + name)

def display_downloaded_audio():
    downloaded_audio = []
    downloaded_audio_count = 0

    for file in os.listdir("downloaded_audio"):
        if not os.path.isdir(os.path.join("Downloaded Audio", file)):
            downloaded_audio.append(file)
            downloaded_audio_count += 1

    return (downloaded_audio)


def move_audio_file_from_downloaded_audio(file, playlist):
    for indexed_file in os.listdir("Downloaded Audio"):
        if file in indexed_file:
            print(indexed_file)
            is_file = input("Is this your file? (y/n)\n")

            if "y" in is_file:
                shutil.move("Downloaded Audio/" + str(indexed_file),
                            "Playlists/" + str(playlist))


def move_audio_file_from_playlist(file, playlist1, playlist2):
    for indexed_file in os.listdir("Playlists/" + str(playlist1)):
        if file in indexed_file:
            print(indexed_file)
            is_file = input("Is this your file? (y/n)\n")

            if "y" in is_file:
                shutil.move("Playlists/" + str(playlist1) + "/" + indexed_file,
                            "Playlists/" + str(playlist2))

def remove_audio_file_from_playlist(file, playlist):
    for indexed_file in os.listdir("Playlists/" + str(playlist)):
        if file in indexed_file:
            print(indexed_file)
            is_file = input("Is this your file? (y/n)\n")

            if "y" in is_file:
                os.remove("Playlists/" + str(playlist) + "/" + indexed_file)
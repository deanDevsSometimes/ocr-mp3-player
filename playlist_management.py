import os
import shutil

playlist_folder = "Playlists"
downloaded_folder = "downloaded_audio"


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
    try:
        os.mkdir(os.path.join(playlist_folder, name))
        return True
    except:
        return False


def delete_playlist(name):
    try:
        os.rmdir(os.path.join(playlist_folder, name))
        return True
    except:
        return False

def display_audio_in_playlist(name):
    if playlist_exists(name):
        return os.listdir(playlist_folder + "/" + name)

def display_downloaded_audio():
    downloaded_audio = []
    downloaded_audio_count = 0

    for file in os.listdir(downloaded_folder):
        if not os.path.isdir(os.path.join(downloaded_folder, file)):
            downloaded_audio.append(file)
            downloaded_audio_count += 1

    return (downloaded_audio)


def move_audio_file_from_downloaded_audio(file, playlist):
    for indexed_file in os.listdir(downloaded_folder):
        if file in indexed_file:
            shutil.move(downloaded_folder + "/" + str(indexed_file),
                        playlist_folder + "/" + str(playlist))
            return


def move_audio_file_from_playlist(file, playlist1, playlist2):
    for indexed_file in os.listdir(playlist_folder + "/" + str(playlist1)):
        if file in indexed_file:
            shutil.move(playlist_folder + "/" + str(playlist1) + "/" + indexed_file,
                            playlist_folder + "/" + str(playlist2))
            return

def remove_audio_file_from_playlist(file, playlist):
    for indexed_file in os.listdir(playlist_folder + "/" + str(playlist)):
        if file in indexed_file:
            os.remove(playlist_folder + "/" + str(playlist) + "/" + indexed_file)
            return True

    return False

def remove_audio_file_from_downloaded(file):
    for indexed_file in os.listdir(downloaded_folder):
        if file in indexed_file:
            os.remove(downloaded_folder + "/" + indexed_file)
            return True

    return False

import pytube  # Needed to download YouTube videos (For Audio).
import os  # Needed to save downloaded audio files in the Downloaded Audio Section
from pydub import AudioSegment

def get_title(url):
    yt = pytube.YouTube(url)

    return yt.title

def download_youtube_mp3(link, save_dir="downloaded_audio"):
    # Try to create a YouTube object using the link
    try:
        yt = pytube.YouTube(link)
    except pytube.exceptions.RegexMatchError:
        # If the link is not valid, throw an error
        print("Error: Invalid YouTube link")
        return

    if get_title(link) is None:
        # If the video is not available, throw an error
        print("Error: YouTube video is not available")
        return

    # Get the first audio stream available
    audio_stream = yt.streams.filter(only_audio=True).first()
    # Check if the file already exists in the save directory
    if audio_stream.default_filename[:-4]+".mp3" in os.listdir(save_dir):
        # If the file already exists, throw an error
        print("Error: File already exists in the save directory")
        return

    # Download the audio stream to the save directory
    download_path = audio_stream.download(save_dir)

    # Load the downloaded file
    audio = AudioSegment.from_file(download_path, format=audio_stream.subtype)

    # Save the file as an mp3
    mp3_path = download_path.replace(audio_stream.subtype, 'mp3')
    audio.export(mp3_path, format='mp3')

    # Delete the original file
    os.remove(download_path)

    print("Success: YouTube mp3 downloaded to the save directory")


#download_youtube_mp3("https://youtu.be/uPgQez_1b1s?list=RDuPgQez_1b1s", "downloaded_audio")  # Tested Audio


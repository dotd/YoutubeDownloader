import os
import yt_dlp
import pandas as pd
from YoutubeDownloader.definitions import PROJECT_ROOT_DIR

"""
This is a simple single script to download Youtube movie. 
"""


format_options = {
    "best": "bestvideo+bestaudio/best",
    "worst": "worstvideo+worstaudio/worst",
    "mp4": "best[ext=mp4]/best",
    "webm": "best[ext=webm]/best",
    "360p": "best[height<=360]/best",
    "720p": "best[height<=720]/best",
    "1080p": "best[height<=1080]/best",
    "audio_only": "bestaudio[ext=m4a]/bestaudio",
    "audio_mp3": "bestaudio[ext=mp3]/bestaudio",
}


def process_formats(formats):
    # extract from formats the format_id, ext, height, width, filesize, format_note
    # return a list of dictionaries
    formats = [
        {
            "format_id": format.get("format_id", None),
            "format": format.get("format", None),
            "video_ext": format.get("video_ext", None),
            "audio_ext": format.get("audio_ext", None),
            "height": format.get("height", None),
            "width": format.get("width", None),
            "filesize": format.get("filesize", None),
            "filesize_approx": format.get("filesize_approx", None),
            "resolution": format.get("resolution", None),
        }
        for format in formats
    ]
    df = pd.DataFrame(formats)
    return df


def list_yt_dlp_formats(url):
    """
    Lists all available yt-dlp formats for a given URL.

    Args:
        url (str): The URL of the video or playlist.

    Returns:
        list: A list of dictionaries, where each dictionary represents a format
              and contains information like 'format_id', 'ext', 'height', 'width', 'filesize', etc.
              Returns None if an error occurs.
    """
    ydl_opts = {
        "listformats": True,  # This option is useful for command-line output, but info['formats'] is key for programmatic access
        "quiet": True,  # Suppress console output during info extraction
        "noplaylist": True,  # Only list formats for a single video if URL is a playlist
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            if "formats" in info:
                return info["formats"]
            else:
                print(f"No format information found for {url}")
                return None
    except yt_dlp.utils.DownloadError as e:
        print(f"Error extracting information for {url}: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


def download_youtube_video(video_url, save_path, format):
    """
    Downloads a YouTube video in the best available video and audio quality.

    Args:
        video_url (str): URL of the YouTube video.
        save_path (str): Directory to save the downloaded video.
    """
    try:
        # Options for yt-dlp
        ydl_opts = {
            "format": format,  # Download best video and audio and merge
            "outtmpl": f"{save_path}/%(title)s.%(ext)s",  # Save file format
            "merge_output_format": "mp4",  # Merge video and audio into MP4 format
        }

        # Downloading the video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        print(f"Video downloaded successfully and saved in: {save_path}")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    # Input YouTube video URL
    video_url = "https://www.youtube.com/watch?v=ozv8ugNm0P0"

    # Input save directory (default is 'downloads')
    save_path = f"{PROJECT_ROOT_DIR}/downloads001/"

    # create the folder if it does not exist
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    # list the formats
    formats = list_yt_dlp_formats(video_url)
    formats_df = process_formats(formats)
    print(f"formats:\n{formats_df}")

    # Call the function to download the video
    download_youtube_video(video_url, save_path, format=f"best[height<=360]/best")

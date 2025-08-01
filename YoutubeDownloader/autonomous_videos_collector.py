from YoutubeDownloader.definitions import PROJECT_ROOT_DIR
import os
import yaml
import argparse
import sys
import yt_dlp
from urllib.parse import urlparse, parse_qs
from colorama import init, Fore, Style


MAIN_FOLDER = "ZDataVideos"
MAIN_YAML_FILE = "main.yaml"

FORMAT_OPTIONS = {
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

EXAMPLE_FILE = """test:
- https://www.youtube.com/watch?v=09839DpTctU
- https://www.youtube.com/watch?v=d27gTrPPAyk
- https://www.youtube.com/watch?v=ozv8ugNm0P0

channel:
- https://www.youtube.com/@BORGAutomotiveReman
- https://www.youtube.com/@TERREPOWER-llc
"""


def get_channel_urls(channel_url, max_videos=None):
    try:
        # Configure yt-dlp options for channel extraction
        ydl_opts = {
            "quiet": True,
            "extract_flat": True,  # Don't download, just extract info
            "ignoreerrors": True,
            "no_warnings": True,
        }

        if max_videos:
            ydl_opts["playlistend"] = max_videos

        urls = []
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extract channel info
            info = ydl.extract_info(channel_url, download=False)

            if not info:
                print(
                    f"{Fore.RED}Error: Could not extract channel information{Style.RESET_ALL}"
                )
                return None

            # Get channel title
            channel_title = info.get("title", "Unknown Channel")
            print(f"{Fore.GREEN}Channel: {channel_title}{Style.RESET_ALL}")

            # Extract video URLs from entries
            entries = info.get("entries", [])
            if not entries:
                print(f"{Fore.YELLOW}No videos found in channel{Style.RESET_ALL}")
                return []

            print(f"{Fore.CYAN}Found {len(entries)} videos{Style.RESET_ALL}")

            for i, entry in enumerate(entries, 1):
                if entry and "url" in entry:
                    video_url = entry["url"]
                    video_title = entry.get("title", "Unknown Title")
                    urls.append(video_url)
                    print(f"{Fore.GREEN}[{i}] {video_title}{Style.RESET_ALL}")
                    print(f"    URL: {video_url}")

                    if max_videos and i >= max_videos:
                        break
        return urls

    except Exception as e:
        print(f"{Fore.RED}✗ Error extracting channel URLs: {e}{Style.RESET_ALL}")
        return []


def prepare_main_folder(main_path=f"{PROJECT_ROOT_DIR}/{MAIN_FOLDER}"):
    # create main folder with subfolder configs
    folder = f"{main_path}/configs"
    if not os.path.exists(folder):
        # create all path if not exists
        os.makedirs(folder, exist_ok=True)

    # create main file under configs folder
    file = f"{folder}/{MAIN_YAML_FILE}"
    if not os.path.exists(file):
        print(f"Creating example file: {file}")
        # write the example file
        with open(file, "w") as f:
            f.write(EXAMPLE_FILE)


def get_default_yaml_file():
    return f"{PROJECT_ROOT_DIR}/{MAIN_FOLDER}/configs/{MAIN_YAML_FILE}"


def process_channel_name(channel_url):
    if channel_url.startswith("https://www.youtube.com/@"):
        return channel_url.split("/")[-1][1:]
    return channel_url.split("/")[-1]


def read_yaml_into_dict(file=get_default_yaml_file(), max_videos=None):
    with open(file, "r") as f:
        data = yaml.safe_load(f)
        if data is None:
            return {}

        channels, data = get_videos_and_channels_from_dict(data)
        for channel in channels:
            print(f"channel: {channel}")
            videos = get_channel_urls(channel, max_videos)
            data[process_channel_name(channel)] = videos
        # Pretty print the data
        print(yaml.dump(data, indent=4))

        return data


def get_videos_and_channels_from_dict(data):
    # get the videos and channels from the data
    channels = data.get("channel", [])
    # erase key channels from data
    data.pop("channel", None)
    return channels, data


def add_topic_url(topic_url):
    # read yaml file
    yaml_dict = read_yaml_into_dict()

    # add url to the yaml file
    vars = topic_url.split("|")

    yaml_dict[vars[0]].append(vars[1])

    # write yaml file
    with open(get_default_yaml_file(), "w") as f:
        yaml.dump(yaml_dict, f)


def download_video(video_url, save_path, format):
    """
    Downloads a YouTube video in the best available video and audio quality.

    Args:
        video_url (str): URL of the YouTube video.
        save_path (str): Directory to save the downloaded video.
    """

    if type(video_url) is list:
        for url in video_url:
            download_video(url, save_path, format)
        return

    if type(video_url) is not str:
        raise ValueError("video_url must be a string or list of strings")

    try:
        random_string = get_url_random_string(video_url)

        # Options for yt-dlp
        ydl_opts = {
            "format": format,  # Download best video and audio and merge
            "outtmpl": f"{save_path}/%(title)s_%(height)s_{random_string}.%(ext)s",  # Save file format
            "merge_output_format": "mp4",  # Merge video and audio into MP4 format
        }

        # Downloading the video
        print("Downloading...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        print(f"Video downloaded successfully and saved in: {save_path}")

    except Exception as e:
        print(f"An error occurred: {e}")


def get_file_random_string(file_name):
    return file_name.rsplit(".", 1)[0].split("_")[-1]


def get_url_random_string(url):
    return parse_qs(urlparse(url).query).get("v", [""])[0]


def download_missing_videos():
    """
    The file format of a video is FreeString_RandomString.Format
    """

    # read yaml file
    yaml_dict = read_yaml_into_dict(max_videos=None)

    # for each topic, check if the video is in the folder
    for topic, urls in yaml_dict.items():

        # if topic folder do not exists, create it
        topic_folder = f"{PROJECT_ROOT_DIR}/{MAIN_FOLDER}/{topic}"
        print(f"topic_folder: {topic_folder}")
        # if topic folder does not exist, create it
        if not os.path.exists(topic_folder):
            os.makedirs(topic_folder, exist_ok=True)
        # Sometimes we have garbage
        clean_up_garbage_files(topic_folder)

        # read the files in the folder
        files = os.listdir(topic_folder)
        # filter from files all the files that are not videos of any file format (mp4, mkv, etc.)
        videos = [
            file
            for file in files
            if file.endswith((".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm"))
        ]
        # get the random string from the file name: throw the extension, split by underscore, and take the last part.
        files_random_strings = [get_file_random_string(file) for file in videos]
        urls_random_strings = {get_url_random_string(url): url for url in urls}

        # get the urls that are not in the random strings
        urls_to_download = [
            url
            for url_random_string, url in urls_random_strings.items()
            if url_random_string not in files_random_strings
        ]
        # download the urls

        # download the video
        download_video(urls_to_download, topic_folder, format=FORMAT_OPTIONS["360p"])

        # clean up garbage files
        clean_up_garbage_files(topic_folder)


def clean_up_garbage_files(topic_folder):
    # read the files in the folder
    files = os.listdir(topic_folder)
    # filter from files all the files that are not videos of any file format (mp4, mkv, etc.)
    files_to_delete = [
        file
        for file in files
        if not file.endswith((".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm"))
    ]
    print(f"Deleting {len(files_to_delete)} files")
    print(files_to_delete)

    # delete the files
    for file in files_to_delete:
        os.remove(f"{topic_folder}/{file}")


def main(verbose=True):
    # There are 2 main functions:
    # 1. prepare_main_folder: create the main folder and the configs folder
    # 2. update_missing_videos: download the videos that are not in the folder
    prepare_main_folder()
    download_missing_videos()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    if len(sys.argv) == 1:
        # If there are no args, run the main function
        main()
        sys.exit(0)

    # If there are args, parse them
    parser.add_argument("--add_topic_url", type=str, help="Add a url to the yaml file")
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging for debugging downloads",
    )
    args = parser.parse_args()

    # if flag add_url, add url to the yaml file
    if args.add_topic_url:
        add_topic_url(args.add_topic_url)
    else:
        # Run main with verbose flag if specified
        main(verbose=args.verbose)

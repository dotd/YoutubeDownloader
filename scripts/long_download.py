from YoutubeDownloader.definitions import PROJECT_ROOT_DIR
from YoutubeDownloader import youtube_utils 
from YoutubeDownloader import youtube_downloader

if __name__ == "__main__":
    urls = youtube_utils.parse_file(f"{PROJECT_ROOT_DIR}/scripts/long_list.txt")
    print(f"Total urls: {len(urls)}")
    youtube_downloader.download_urls(urls)

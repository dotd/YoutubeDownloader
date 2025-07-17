from YoutubeDownloader import channel_extractor 
from YoutubeDownloader import youtube_downloader
from YoutubeDownloader.definitions import PROJECT_ROOT_DIR
import os
import sys

def get_channel_urls(
        channel, 
        output_list_file,
        downloads_folder,
        limit_urls=10000, 
        ):
    # Begin with channel list of youtubes
    # If output_list_file exists, read it and get the urls from it.
    if os.path.exists(output_list_file):
        with open(output_list_file, "r") as f:
            urls = f.read().splitlines()
    else:
        urls, _ = channel_extractor.get_channel_urls([channel], max_videos=limit_urls) 
    
    urls = urls[:limit_urls]
    # for debug purposes show the urls in a nice format
    print(f"Total videos extracted: {len(urls)}")
    urls_str = "\n".join([f"{i}.\t{url}" for i, url in enumerate(urls)])  
    print(f"urls:\n{urls_str}")

    # save the urls to a file. If folder does not exist of output_list_file does not exist, create it.
    # get folder from output_list_file
    folder = os.path.dirname(output_list_file)
    if not os.path.exists(folder):
        os.makedirs(folder)
    with open(output_list_file, "w") as f:
        f.write("\n".join(urls))

    # Download the urls
    youtube_downloader.download_urls(
        urls=urls, 
        output_dir=downloads_folder,
        format_preference="best")
    

if __name__ == "__main__":
    get_channel_urls(
        channel="https://www.youtube.com/@satisfactoryprocess", 
        output_list_file=f"{PROJECT_ROOT_DIR}/DataIndustrialVideos/satisfactoryprocess/output_list_file.txt", 
        downloads_folder=f"{PROJECT_ROOT_DIR}/DataIndustrialVideos/satisfactoryprocess/"
    ) 
